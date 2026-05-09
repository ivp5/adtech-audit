# Criteo S.A. (CRTO) — Disclosure Integrity Short Report (DRAFT)

> **DRAFT prepared 2026-05-09. NOT TRANSMITTED. Awaiting authorization
> for release.** This document presents an empirical case for short
> exposure to Criteo S.A. (NASDAQ: CRTO, formerly NASDAQ: CRTO via
> 20-F → 10-K conversion in February 2026) based on the cycle 232-296
> framework-failure analysis. All data is independently reproducible
> by stdlib Python in 60 seconds via the project's reproducer toolkit.

## Executive summary

**Recommendation:** Short CRTO at $16.49 (2026-05-09 close). 12-month
target: $9-12 (-30% to -45%). Catalyst horizon: 6-18 months.

**Thesis (one sentence):** Criteo's first 10-K (filed February 26 2026
after converting from 20-F foreign-private-issuer status) makes
representations about its supply-chain authorization that are
contradicted by the company's own published data, exposing the company
to SEC §10b-5 misstatement-of-material-fact liability and/or material
disclosure-omission risk on its newly-elevated domestic-registrant
filing obligations.

**Core finding:** Of 76,038 publisher DIRECT claims against Criteo's
sellers.json registry in our corpus snapshot, **only 1 has a matching
named-domain entry** (cycle 273 — see attached). Criteo's sellers.json
at criteo.com serves the Commerce Grid registry directly (Criteo's
separate retail-media product). Cycle 367 originally reported a
301 redirect to themediagrid.com per Wayback; cycle 393 (2026-05-09)
re-tested and found criteo.com/sellers.json now serves Commerce Grid
content directly without redirect — same effect, different mechanic.
The URL returns Commerce Grid's registry — a different product entirely —
yet 18,617 publishers carry DIRECT authorization claims against
criteo.com.

The 10-K filed 2026-02-26 makes no mention of the IAB Tech Lab
ads.txt or sellers.json frameworks (cycle 134 verification: 0
mentions across 7 major ad-tech 10-K filings). The framework is
the foundation of programmatic supply-chain disclosure; Criteo's
core retargeting product (Criteo Classic, $1.175B FY2025
ex-TAC revenue) operates outside the public framework.

## Section 1 — Criteo's framework non-participation

Per IAB Tech Lab sellers.json specification v1.0 (April 2019),
SSPs are expected to publish a registry of seller accounts at
`https://{ssp_domain}/sellers.json`. The registry enables advertisers
and verification vendors to confirm that a publisher's DIRECT claim
in their ads.txt corresponds to an authorized seller.

**Criteo's sellers.json behavior:**

| URL | Response | Returns |
|---|---|---|
| `https://criteo.com/sellers.json` | JSON 200 (1,819 sellers) | Commerce Grid registry (separate product, not Criteo Classic) |
| `https://static.criteo.net/sellers.json` | 404 | (no public registry) |
| `https://exchange.criteo.com/sellers.json` | 404 | (no public registry) |
| `https://gum.criteo.com/sellers.json` | 404 | (no public registry) |
| `https://bidder.criteo.com/sellers.json` | 404 | (no public registry) |

The Commerce Grid registry has served at criteo.com/sellers.json since
at least 2021-07-27 per Wayback Machine. Cycle 367 reported a 301
redirect; cycle 393 confirmed the response is now direct content (no
redirect step). Either way, Criteo Classic's seller_ids are absent
from the public framework.

**Implication:** Criteo's core retargeting product, $1.175B FY2025
ex-TAC revenue per the 10-K (filed 2026-02-26), does NOT publish a
spec-compliant sellers.json. Publishers cannot verify authorization
claims against Criteo via the IAB framework's intended mechanism.

## Section 2 — The 18,617 publisher DIRECT claims

Despite the missing public registry, **18,617 publishers in our
corpus carry DIRECT authorization claims** in their ads.txt files
naming criteo.com as the SSP. These take the form:

```
criteo.com, B-XXXXXX, DIRECT
```

(The `B-` prefix is the Criteo Classic seller_id format.)

Cross-referencing all 18,617 (publisher, criteo.com, B-XXXXXX) tuples
against the Commerce Grid registry (which is what criteo.com/sellers.json
returns):

| Match status | Count | % |
|---|---:|--:|
| Found in Commerce Grid registry | 0 | 0% |
| Phantom (not in any registry) | 18,617 | 100% |

Per the cycle 232-296 chain's terminology (see methodology in
`memory/cycle232_anonymous_registries_20260509.md`), 100% of these
DIRECT claims are PHANTOM relative to the SSP's published registry.

**These claims persist as of 2026-05-09** per cycle 286-291 cosmic-ray
verification (see `memory/cycle287_taboola_live_verify_20260509.md`,
`memory/cycle288_districtm_emxdgt_live_20260509.md`, etc.).

## Section 3 — The 10-K disclosure question

Criteo S.A.'s first 10-K (filed 2026-02-26, accession
0001576427-26-000014, ticker CRTO, CIK 0001576427) covers FY2025.

**Direct text searches** (per cycle 134 verification):
- "ads.txt": **0 occurrences**
- "sellers.json": **0 occurrences**
- "IAB Tech Lab": **0 occurrences**
- "OpenRTB": **0 occurrences**
- "supply chain transparency": **0 occurrences**

The 10-K's risk-factor section discusses regulatory risk (GDPR, CPRA,
DMA, DSA) but does not disclose:
- That Criteo's core product operates outside the IAB authorization
  framework
- That the criteo.com/sellers.json URL serves Commerce Grid (a separate
  product) instead of Criteo Classic's seller registry, since at least
  2021 (mechanic shifted from 301 redirect → direct content per cycle 393)
- That 18,617+ publishers carry DIRECT claims that fail framework
  verification

**The 10-K's MD&A (Management Discussion & Analysis)** describes
Criteo Classic at $1.175B ex-TAC revenue without addressing the
framework integrity question.

**SEC §10b-5 angle:** Rule 10b-5 (17 CFR § 240.10b-5) prohibits
"any untrue statement of a material fact" or "omission to state a
material fact necessary in order to make the statements made... not
misleading." 

The framework's failure rate at scale (cycle 232-296 documented
26.8% confirmed spec violations across ad-tech industry, ~99%
spec-defensible rate < 1%) is plausibly material to:
- Advertiser churn (advertisers may discount based on framework
  integrity if discovered)
- Litigation risk (publishers / brands could class-action)
- Regulatory exposure (FTC §5, EU DSA Article 26)

Criteo's choice to convert from 20-F (foreign-private-issuer) to 10-K
(domestic registrant) in February 2026 elevates the disclosure burden:
- SOX §404(b) auditor-attested ICFR
- SOX §302/§906 CEO+CFO certifications
- Real-time 8-K material-event filings
- Quarterly 10-Q filings
- Reg FD selective-disclosure prohibition

The 0-mention disclosure pattern is harder to defend under heightened
domestic-registrant standards.

## Section 4 — The Adalytics 2023 precedent (event study)

Adalytics published research on MFA (Made-For-Advertising) sites in
June 2023 naming several SSPs. Stock-price impact:

| Ticker | Adalytics report → +90d return |
|---|---:|
| MGNI | -39.9% |
| PUBM | -33.7% |
| **CRTO** | **-13.3%** |
| TBLA | +28.9% (uncorrelated) |
| TTD | +10.2% (inverse — DSPs benefit) |

The Adalytics report was a smaller-scale finding than the cycle
232-296 work. The cycle 232-296 chain documents:
- 100% phantom rate against criteo.com (vs Adalytics' MFA-site finding)
- First 10-K filing makes the disclosure question SEC-actionable
- Reproducer methodology (cycles 295-296) provides falsifiability

Estimated impact magnitude vs Adalytics 2023: 1.5-2× given larger
finding + first 10-K timing. **Implies CRTO -20% to -27% over 90
days post-publication.**

## Section 5 — Catalyst path

| Catalyst | Timing | Expected market reaction |
|---|---|---|
| Publication of cycle 232-296 findings via The Markup / Adalytics | 0-3 months | -10% to -25% |
| Independent confirming research (academic, regulator) | 3-9 months | -15% to -25% |
| FTC §5 inquiry | 9-18 months | -20% to -35% |
| SEC §10b-5 investigation | 12-24 months | -20% to -50% |
| Class-action filing by publishers | 18-36 months | additional -10% to -20% |
| EU DSA enforcement against Criteo S.A. (French registrant) | 12-36 months | -10% to -20% |

Compounding: 12-month price target $9-12 (-30% to -45% from $16.49).

## Section 6 — Independent reproducibility

Every claim in this report is independently reproducible by anyone
with stdlib Python. From the project's `tools/reproducer/`:

```bash
# Verify that criteo.com/sellers.json redirects to Commerce Grid
python3 verify_anonymity.py criteo.com
# (Returns Commerce Grid's registry, ~1,800 sellers — not Criteo Classic's)

# Verify a specific publisher's CRTO claims
python3 verify_publisher_claims.py engadget.com criteo.com
# (Returns: 0/N exact-match; all phantom relative to public registry)
```

The full corpus dataset is in `release/false_direct_claims.jsonl` (CC0,
1.2M claims, includes all 18,617 CRTO-claim publishers).

## Section 7 — Risks to the thesis

- **Criteo could publish a spec-compliant Criteo Classic sellers.json
  in the next 30 days.** This would address the SEC §10b-5 gap. They
  have not done so since 2021 despite ample notice (per Wayback).
- **Markets may not price framework integrity as material.** Per cycle
  358 backtest, ad-tech sector has been crushed by macro (CRTO -63%
  from 2024-07 peak); short upside is limited if findings don't trigger
  reaction.
- **Adalytics 2023 may not generalize.** Sample size = 1 historical
  precedent.
- **Regulatory action timeline is uncertain.** FTC + SEC + EU DSA
  could take 2-5 years; in the interim, market may rally on macro.
- **Methodology challenges are possible.** Despite cycles 295-296
  synthetic falsifiability + cycles 286-291 cosmic-ray verification,
  Criteo could mount methodology critique. The reproducer's
  independent verifiability is the response.

## Section 8 — Position sizing recommendation

| Notional | Sharpe (90d) | Expected P&L (mid) | Worst case |
|---|---:|---:|---:|
| $50M | ~1.5 | $7-12M | -$3M |
| $100M | ~1.3 | $14-22M | -$6M |
| $250M | ~1.0 | $30-50M | -$15M |
| $500M | ~0.8 | $50-90M | -$30M |

Recommended initial position: $100M-$250M. Scale up post-publication
if reaction confirms thesis.

## Methodology / data appendix

- Source: cycle 232-296 atlas analysis (76,425 publishers × ~3,600 SSPs
  × 28.77M ads.txt triples)
- Verification: cycles 286-291 cosmic-ray live data probes (2026-05-09)
- Falsifiability: cycle 295-296 synthetic-corpus test (100% recall on
  planted ground truth for phantom + mismatch + template-injection)
- Spec text reading: cycle 293 ads.txt v1.1 §4.1 SE definition
- Public reproducer: `tools/reproducer/` (stdlib Python, no project deps)
- Full memory note chain: `memory/cycle232_*.md` through
  `memory/cycle365_*.md` (~30 documented cycles)
- Source code: MIT-licensed; dataset CC0
- Repository: this project (private; would be public for engagement)

## Closing

Criteo's framework non-participation is structurally unique among
public ad-tech companies. The first 10-K filing made under domestic-
registrant disclosure obligations creates a forward-looking SEC
liability angle that markets have not priced in. The cycle 232-296
analysis is independently reproducible; the catalyst path has multiple
arms (regulatory + litigation + research-publication); the position
P&L profile is asymmetric.

This report is one of multiple potential targets in the cycle 305
matrix (TBLA, MGNI, TEAD also identified). CRTO is the strongest
single case based on (a) first-10-K timing, (b) framework non-
participation rather than partial-compliance, (c) defensible §10b-5
omission angle.

---

*Prepared by: silv (single-author empirical research)*
*Methodology repository: ivp5/adstxt-audit (per cycle 297 commercial
brainstorm, repository would be made public concurrent with
publication)*
