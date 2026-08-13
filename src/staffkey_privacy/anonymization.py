# SPDX-License-Identifier: Apache-2.0
"""Anonymization layer — the OPEN, auditable module (Apache-2.0).

Intentionally free of proprietary dependencies (no DB, no aggregation service, no network). It
is the auditable seam: anyone can read it and verify that only derived, anonymized points cross
the private -> pool boundary, and that no cell below the k-anonymity floor is ever published.

Responsibilities:
  1. Reduce a private row to a poolable point (drop identity, keep derived scalars).
  2. Pseudonymize the contributor (stable key, not reversible to a user id).
  3. Enforce per-contributor caps (anti-gaming).
  4. Enforce a k-anonymity floor before any cell is emitted.
"""

from __future__ import annotations

import hashlib
import hmac
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

_CENT = Decimal("0.01")

# Minimum distinct contributors per published cell. No cell below this is ever emitted.
K_ANONYMITY_FLOOR = 5
# Max points one contributor may add to a single cell (robustness / anti-gaming).
MAX_POINTS_PER_CONTRIBUTOR_PER_CELL = 3


@dataclass(frozen=True)
class PrivateRow:
    """A single user's private, identified observation (never leaves the user's store as-is)."""

    user_id: str
    period: str  # YYYY-MM
    role: str | None
    seniority: str | None
    stack: str | None
    city: str | None
    client_sector: str | None
    day_rate: Decimal  # PLN, exact to grosz
    days_to_pay: int | None
    verified: bool  # bank-confirmed


@dataclass(frozen=True)
class PoolablePoint:
    """What is allowed into the pool. Carries a pseudonymous key, never the user id."""

    contributor_key: str
    period: str
    role: str | None
    seniority: str | None
    stack: str | None
    city: str | None
    client_sector: str | None
    day_rate: Decimal  # PLN, exact to grosz
    days_to_pay: int | None
    verified: bool


def contributor_key(user_id: str, *, salt: str) -> str:
    """Stable, non-reversible pseudonym for per-contributor accounting.

    HMAC with a server-held salt: lets us cap/count a contributor without storing or exposing
    the user id in the pool. Rotating the salt unlinks future contributions.
    """
    return hmac.new(salt.encode(), user_id.encode(), hashlib.sha256).hexdigest()[:32]


def to_poolable(row: PrivateRow, *, salt: str) -> PoolablePoint:
    """Strip identity, keep only derived scalars + dimensions."""
    return PoolablePoint(
        contributor_key=contributor_key(row.user_id, salt=salt),
        period=row.period,
        role=row.role,
        seniority=row.seniority,
        stack=row.stack,
        city=row.city,
        client_sector=row.client_sector,
        day_rate=row.day_rate.quantize(_CENT, rounding=ROUND_HALF_UP),
        days_to_pay=row.days_to_pay,
        verified=row.verified,
    )


def cap_per_contributor(
    points: Iterable[PoolablePoint],
    *,
    limit: int = MAX_POINTS_PER_CONTRIBUTOR_PER_CELL,
) -> list[PoolablePoint]:
    """Keep at most ``limit`` points per contributor (assumes points share one cell)."""
    seen: dict[str, int] = {}
    kept: list[PoolablePoint] = []
    for p in points:
        n = seen.get(p.contributor_key, 0)
        if n < limit:
            kept.append(p)
            seen[p.contributor_key] = n + 1
    return kept


def meets_k_anonymity(
    points: Sequence[PoolablePoint], *, floor: int = K_ANONYMITY_FLOOR
) -> bool:
    """True only if the cell has at least ``floor`` DISTINCT contributors."""
    distinct = {p.contributor_key for p in points}
    return len(distinct) >= floor
