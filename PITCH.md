# Evidence Pitch — Ad Supply Chain Authorization Failures

> **Snapshot pin.** Numbers below are at the **2026-03-25 corpus** (with 2026-04-22 partial registry refresh). Live state (2026-04-27): 76,169 publishers, 28.7M triples, 1,672 SSP registries — per-company counts are 1.4–2.9× higher. Magnite "65% CONTRADICTED" → 80%. Reproducer at L113 (`taboolanews.com` grep → 3,841) and §Appendix prose (3,694) measure different things — grep matches substrings; prose counts unique seller-id rows. CafeMedia 25% (L29/L37) is the rounded form of the paper's 23.3%.

## One-liner

57% of ad supply chain authorization claims are provably false. We have 2.10M cross-verified records. The system produces more unauthorized inventory than authorized (1.20M false vs 898K plausible).

## The smoking gun (historical, 2026-03-24)

```bash
# What the template claimed:
curl -sL https://ads.themoneytizer.com/ads_txt.php | head -1
# → smartadserver.com, 1097, DIRECT

# What the registry says (still true 2026-04-27):
curl -sL https://smartadserver.com/sellers.json | jq '.sellers[] | select(.seller_id=="1097")'
# → {"seller_id":"1097","seller_type":"INTERMEDIARY","name":"Themoneytizer",...}
```

The template said DIRECT; the registry said INTERMEDIARY; the system contradicted itself. Verified live 2026-03-24. The template was live unchanged since January 2024 ([Wayback Machine proof](https://web.archive.org/web/20240117183838/https://ads.themoneytizer.com/ads_txt.php)) until at least the last archived snapshot.

**Update — 2026-04-27.** Re-running the first command now returns:
`smartadserver.com, 1097, RESELLER` — not DIRECT. The Moneytizer template
has been corrected. The first five lines are all RESELLER. Whether
correlated with this analysis or unrelated, the contradiction at this
specific seller_id is no longer live. The 1,108 publishers carrying the
template at the snapshot date may or may not have re-synced; testing
at-scale not done. The historical snapshot (March-25 corpus) and the
shipped JSONL still document the contradiction as it stood; the live
state has moved.

## Why this matters

**For advertisers**: Major SSPs have tens of thousands of false authorization claims each — Lijit (79K), Google (74K), Magnite (72K), Taboola (63K). Your "brand safety" tools verify against a ledger where the entries contradict themselves — they check that claims *exist*, not that they're *consistent*. DIRECT inventory commands premium pricing — advertisers pay more for authorization that doesn't exist.

**For publishers**: Your template manager choice determines your false claim rate. CafeMedia-managed: 23.3% false. Moneytizer-managed: 66.2% false. A 43 percentage point difference from infrastructure choice alone. (Source: `wrapper_scorecard.json`, 195 providers graded.)

**For everyone**: The authorization system produces MORE false claims (1.20M) than valid claims (898K). It's not "some fraud in a working system" — the system's primary output IS unauthorized inventory. And it sells anyway. If authorization were enforced, most of the market would stop. It doesn't stop, which proves it isn't enforced. (Observed: CNN has 9+ contradicted Magnite claims; Magnite serves ads on CNN anyway.)

## The proof it's fixable

- **The Guardian**: 7.1% false (careful maintenance)
- **Germany (.de TLD)**: 39% false (vs 63% for Russia/Japan)
- **CafeMedia-managed publishers**: 23.3% false (vs 57% baseline)

The technology exists. The question is incentive. Authorization is theater, not security — the system's function is liability distribution, not fraud prevention. Everyone can point to their paperwork.

## What we have

- 2,096,507 cross-verified claims across 23,283 publishers
- 710 SSP registries cross-referenced (1.89M seller entries); a follow-up fetch of 238 more SSPs on 2026-04-22 moved the headline rate by −0.03 percentage points (fabrication ≈ 36× staleness)
- Per-SSP mismatch rates
- Named template injectors with live URLs
- Interactive verification tool
- Documented methodology with self-corrections

## The scale

| SSP | FY2025 Revenue | False Claims (2026-03-25) | Live count (2026-04-27) | Publishers Affected |
|-----|---------------|--------------:|--------------:|--------------------|
| Lijit (Sovrn) | ~$100M (private) | 79,453 | 211,883 | 10,882 |
| Google | $265B (Alphabet) | 74,030 | 180,633 | 10,186 |
| Magnite (Rubicon) | **$714M** (10-K FY2025) | 71,944 | 193,313 | 11,970 |
| Taboola | **$1.91B** (10-K FY2025; 1st post-20-F) | 63,409 | 151,895 | 2,781 |
| OneTag | private | 58,328 | 168,320 | 9,638 |
| PubMatic | **$283M** (10-K FY2025; only contracting SSP) | 48,354 | 140,148 | 10,786 |
| Index Exchange | private | 44,658 | 125,089 | 10,454 |
| OpenX | private | 42,074 | 110,915 | 9,963 |
| TripleLift | private | 39,204 | 93,705 | 8,848 |
| AppNexus (Xandr/MSFT) | not disclosed in segment reporting | 33,595 | 92,810 | 7,531 |
| SmartAdServer (now Equativ SAS) | private | 33,352 | 98,625 | 7,693 |
| Criteo | **$1.681B** (10-K FY2025; 1st post-20-F) | 23,129 | 76,037 | not yet recomputed |
| LiveRamp (identity) | **$745.6M** (10-K FY2025) | n/a (DSP/identity) | n/a | n/a |
| Trade Desk (DSP) | **$2.896B** (10-K FY2025) | n/a (buyer-side) | n/a | n/a |
| Outbrain → Teads | **$1.30B** (10-K FY2025; CIK reassigned) | (in OB+TEAD line items) | — | — |

## Named template-injection operators (PAPER §1¶3, ERRATA E-2026-04-22-d, E-2026-04-27-d)

| Brand (in our data) | Corporate / SEC entity | Country | Reach (publishers via single seller_id) |
|---|---|---|---|
| Seedtag | **Seedtag Advertising SL** | Spain (Barcelona) | 14,500 (xandr.com 4009) / 14,146 (rubicon 17280) / 14,084 (smartadserver 3050) / etc. — 22+ SSPs, 15,432 unique publishers, 56,825 contradicted DIRECT claims |
| Rich Audience | **Pubnet Publicidad Y Marketing SL** | Spain (Barcelona) | 17,803 (rubicon 13510) / 17,673 (appnexus 8233) / 17,131 (pubmatic 81564) |
| SunMedia | **VLN Servicios Publicitarios Integrales SL** | Spain | 11,551 (smartadserver 1999) / 7,834 (triplelift 8683) |
| Themoneytizer | **Themoneytizer SA** | France (Paris) | 1,108 publishers serving the historic `ads_txt.php` template |
| Adagio (template author) | Adagio (adagio.io) | France (Montpellier) | 882 publishers via `# Adagio_0_6` markers; OWN template is RESELLER, not DIRECT — DIRECT injection comes from a different aggregator that composes Adagio + Seedtag templates side-by-side (E-2026-04-27-k) |

Continuous public classification proof: Wayback snapshot of `rubiconproject.com/sellers.json` from 2021-02-11 confirms `seller_id 17280 = Seedtag Advertising SL, INTERMEDIARY` — meaning the contradiction has been visible to anyone fetching both files for **62+ months**. Same Wayback snapshot also confirms 13510 (Rich Audience), 17960 (Sovrn), 22328 (SunMedia), 22884 (Google) all classified INTERMEDIARY at Rubicon since the same date.

## How it works (for technical audiences)

Publishers list authorized sellers in ads.txt (DIRECT = direct relationship). SSPs list their sellers in sellers.json (INTERMEDIARY = reseller). These should match. They don't.

**The spec is unambiguous.** IAB ads.txt defines DIRECT as "the Publisher directly controls the account." IAB sellers.json defines INTERMEDIARY as "entity that does not own or control the content." A DIRECT claim for an INTERMEDIARY account is definitionally false under both specs — not an interpretation, a cross-reference.

68% of false claims come from seller IDs each shared by 100+ publishers — statistical impossibility without automated template injection. 3,264 publishers share the same false (rubiconproject.com, 17280) claim; 2,557 share (smartadserver.com, 4071).

## Cite correctly

"57% of DIRECT authorization claims in ads.txt are false" — not "57% of ads are fraudulent." The finding is about the authorization ledger, not the ads themselves.

## Contact

Evidence package available on request:
- `evidence.html` — Interactive verification (runs locally, no server)
- `false_direct_claims.jsonl.gz` — 1.20M false claims (612,738 CONTRADICTED + 585,401 PHANTOM)
- Complete methodology documentation

All source data (ads.txt, sellers.json) is publicly served by the respective domains. Verdicts are mechanical cross-reference of public records.

---

## Appendix: Per-SSP breakdown (for deep dives)

| SSP | False Claims | Primary Issue |
|-----|--------------|---------------|
| Lijit (Sovrn) | 79.5K | Template injection |
| Google | 74.0K | Phantom IDs (registry 71% confidential) |
| Magnite/Rubicon | 71.9K | Template injection |
| Taboola | 63.4K | 100% phantom on own property (see below) |
| OneTag | 58.3K | Template injection |
| PubMatic | 48.4K | Template injection |
| Index Exchange | 44.7K | Template injection |
| OpenX | 42.1K | Template injection |
| TripleLift | 39.2K | Template injection |
| AppNexus (Xandr) | 33.6K | Template injection |
| SmartAdServer | 33.4K | Template injection (Moneytizer-origin) |

## Appendix: Taboola's self-contradiction

**taboola.com** (corporate site): 1,580 Taboola seller IDs claimed as DIRECT. **Only 4 are PLAUSIBLE** in Taboola's own sellers.json (24,228 sellers). **1,576 (99.75%) PHANTOM.** Verified against the release `false_direct_claims.jsonl` on 2026-04-22.

**taboolanews.com** (content property): 3,694 Taboola-account DIRECT entries claimed — every single one is PHANTOM in Taboola's own registry. **100% PHANTOM.**

```bash
# Count Taboola DIRECT entries on Taboola's own site
curl -sL https://taboolanews.com/ads.txt | grep "taboola.com.*DIRECT" | wc -l
# → 3841

# Check if seller ID 1007016 exists in their registry
curl -sL https://www.taboola.com/sellers.json | jq '.sellers[] | select(.seller_id=="1007016")'
# → (nothing)
```

Taboola is claiming DIRECT control over accounts that Taboola itself doesn't acknowledge. This isn't a third-party publisher making mistakes — it's the SSP contradicting its own disclosure on its own property.

## Appendix: Antitrust context

Magnite and PubMatic have filed antitrust lawsuits against Google. Our data shows the plaintiffs have demonstrably worse supply chain transparency than the defendant:

- Magnite: 86.5% mismatch (65% CONTRADICTED)
- PubMatic: 59.7% mismatch
- Google: 44.7% mismatch (but ~17K phantom IDs, registry 71% confidential)

This doesn't prove or disprove the antitrust claims. It shows the entire industry operates on a foundation of unverified authorization.

## Appendix: Piracy sites fabricate premium IDs

Streaming piracy sites (soap2day.rs, hdtoday.tv, moviesjoy.is) share an **identical 5,530-line ads.txt** (same MD5 hash). It contains:

- 1,697 DIRECT claims
- 134 GourmetAds entries (a "premium food & lifestyle" network)

Cross-referenced against GourmetAds registry: **64 of 134 are PHANTOM (47.8%)**

Piracy sites are fabricating premium network IDs to bypass brand safety filters and attract food/CPG advertisers. This isn't template copying — it's deliberate ID fabrication.
