# Data Dictionary

| Variable | Description |
| --- | --- |
| `period` | Monthly period. |
| `region` | Province/city/region name or anonymized code. |
| `issuer_group` | Anonymized issuer or issuer-group code. |
| `fiscal_revenue` | Fiscal revenue indicator, consistent units. |
| `land_transfer_revenue` | Land-transfer revenue indicator, consistent units. |
| `bond_issuance` | Credit bond issuance amount. |
| `repayment` | Bond repayment amount. |
| `net_financing` | Issuance minus repayment. |
| `weighted_yield` | Weighted bond yield or YTM/YTE. |
| `benchmark_yield` | Benchmark yield used to calculate credit spread. |
| `credit_spread` | Generated as `weighted_yield - benchmark_yield`. |
| `remaining_maturity` | Remaining maturity in years. |
| `turnover` | Turnover or liquidity proxy. |
| `implied_rating` | Implied rating segment, anonymized if needed. |

## Confidentiality Check

Before publishing, confirm that no row contains:

- nonpublic issuer names
- internal rating comments
- unreleased research conclusions
- paid database raw redistribution
- meeting minutes or internal source notes

