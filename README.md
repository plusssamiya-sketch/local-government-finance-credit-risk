# Local Government Finance and Credit Risk: Internship-Inspired Portfolio Project

This repository turns fixed-income research internship experience into a public, reproducible portfolio project. It studies how fiscal capacity, land-transfer revenue, bond financing pressure, maturity structure, and market liquidity can be organized to support local-government financing and credit-risk analysis.

The repo uses anonymized sample data. Replace it with public data or carefully anonymized internship-derived data before publishing.

## Portfolio Goal

Show that the internship was not only administrative database maintenance. The project makes visible the analytical workflow behind:

- credit bond primary-market tracking
- local-government financing platform research
- fiscal and land-market indicator monitoring
- issuance, repayment, and net-financing summaries
- yield/spread and maturity analysis
- liquidity and turnover monitoring

## Existing Frameworks Used

The workflow adapts common Python credit-risk and bond-spread analysis patterns:

- clean market/fiscal data
- calculate spread and financing-pressure indicators
- group by region, maturity, and rating segment
- visualize trends and cross-sectional differences
- write an interpretation memo

Relevant public references include credit-spread analysis notebooks/tutorials and recent LGFV risk papers. They are used for structure and variable ideas, not copied text.

## Repository Structure

```text
local-government-finance-credit-risk/
  README.md
  LICENSE
  .gitignore
  data/
    sample_lgfv_credit_data.csv
    README.md
  src/
    analyze_credit_risk.py
  docs/
    data_dictionary.md
    research_memo.md
  outputs/
    README.md
```

## Core Question

How can fiscal indicators, land-market revenue, bond financing pressure, and market pricing variables be combined to describe local-government credit-risk conditions?

## Indicators

- fiscal revenue
- land-transfer revenue
- bond issuance
- repayment
- net financing
- coupon or yield
- benchmark yield
- credit spread
- remaining maturity
- turnover/liquidity
- implied rating segment

## How To Run

Install pandas if needed:

```bash
pip install pandas
```

Run:

```bash
python src/analyze_credit_risk.py
```

Outputs are saved into `outputs/`.

## Confidentiality

Do not upload:

- employer-confidential data
- issuer-confidential notes
- paid Wind database exports
- internal meeting minutes
- identifiable nonpublic issuer analysis

Public portfolio alternatives:

- anonymize province/city/issuer names
- publish only aggregate indicators
- include synthetic sample data
- explain the data schema without redistributing restricted raw data

## CV Positioning

Suggested CV bullet after completion:

> Built a reproducible Python portfolio project modeling local-government finance and credit-risk indicators, combining fiscal revenue, land-transfer revenue, bond issuance, repayment, net financing, maturity, liquidity, and credit-spread metrics.
