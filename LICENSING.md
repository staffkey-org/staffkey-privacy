# Licensing — the open-core split

Staffkey is **open-core**. The moat is the **data + network effect, not the code**, so the part
that earns trust is open and auditable, while the part that protects the dataset stays closed.
**Open source ≠ open data.**

| Component | License | Why |
|---|---|---|
| Anonymization layer (this repo) | **Apache-2.0** | Auditable proof that only derived, anonymized, k-anonymous points leave the private store. Dependency-free, no I/O — readable in full. Apache (not MIT) for the patent grant; (not AGPL) to stay employer-friendly for the developer audience. |
| Backend service, API, dashboard | **Proprietary** | The product. |
| Aggregation service | **Proprietary** | Builds the dataset — part of the moat. |
| The dataset / benchmark | **Proprietary** | Protected by the EU *sui generis* database right + trade secret + contract. Never published. |

The proprietary backend **imports** this open package rather than copying it, so the boundary is
physical, not just documentary.

**Contributions:** by Developer Certificate of Origin (DCO): sign commits with `-s`.
**Trademark:** "Staffkey" and "META Project Tomasz Mierzwa" are not covered by any code license here.
