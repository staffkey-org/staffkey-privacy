# SPDX-License-Identifier: Apache-2.0
from staffkey_privacy import (
    K_ANONYMITY_FLOOR,
    PrivateRow,
    cap_per_contributor,
    contributor_key,
    meets_k_anonymity,
    to_poolable,
)


def _point(key: str):
    row = PrivateRow(
        user_id=key,
        period="2026-05",
        role="Engineer",
        seniority="Senior",
        stack="Java",
        city="Kraków",
        client_sector="fintech",
        day_rate=950.0,
        days_to_pay=21,
        verified=True,
    )
    return to_poolable(row, salt="test-salt")


def test_to_poolable_drops_user_id():
    p = _point("user-123")
    assert p.contributor_key != "user-123"
    assert not hasattr(p, "user_id")


def test_contributor_key_is_stable_and_salt_dependent():
    assert contributor_key("u", salt="a") == contributor_key("u", salt="a")
    assert contributor_key("u", salt="a") != contributor_key("u", salt="b")


def test_k_anonymity_floor_enforced():
    few = [_point(f"u{i}") for i in range(K_ANONYMITY_FLOOR - 1)]
    enough = [_point(f"u{i}") for i in range(K_ANONYMITY_FLOOR)]
    assert not meets_k_anonymity(few)
    assert meets_k_anonymity(enough)


def test_per_contributor_cap():
    points = [_point("same-user") for _ in range(10)]
    assert len(cap_per_contributor(points, limit=3)) == 3
