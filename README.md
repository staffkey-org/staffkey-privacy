# staffkey-privacy

**The open, auditable anonymization layer of [Staffkey](https://staffkey.pl).** Apache-2.0 licensed.

Operated by **META Project** (named data controller). Methodology, k-anonymity thresholds, and
"what never leaves your device" are documented at **https://staffkey.pl/metodologia**.

This package is deliberately small, dependency-free, and free of any network/database I/O so the
developer audience can read it in full and verify the privacy claim: that only *derived,
anonymized* points ever cross the private→pool boundary, and that no benchmark cell below the
**k-anonymity floor** is ever published.

It contains:
- `PrivateRow` → `to_poolable()`: strips identity, keeps only derived scalars + dimensions.
- `contributor_key()`: HMAC pseudonymization for per-contributor accounting (not reversible to a
  user id; rotating the salt unlinks future contributions).
- `cap_per_contributor()`: per-contributor caps (anti-gaming / robustness).
- `meets_k_anonymity()`: the k≥N floor gate (`K_ANONYMITY_FLOOR`).

> **Scope of this license:** only this package is open source. The Staffkey dataset, the
> aggregation service, the backend, and the benchmark itself are proprietary. Open source ≠ open
> data. See [`LICENSING.md`](LICENSING.md).
>
> **Honesty note:** publishing this code proves *what the logic does*. In the hosted product the
> logic runs server-side, so this proves the logic, not that a given server runs exactly this
> build. See the methodology page (§ "what open-sourcing does and doesn't prove") at
> https://staffkey.pl/metodologia.

## Develop

```bash
uv sync --extra dev      # or: pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Contributing

Contributions are accepted under the **Developer Certificate of Origin (DCO)** — sign commits
with `git commit -s`. "Staffkey" and "META Project" are not covered by any code license here.
