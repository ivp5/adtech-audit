# Evidence Pitch — Ad Supply Chain Authorization Failures

## One-liner

57% of ad supply chain authorization claims are provably false. We have 2.10M cross-verified records. The system produces more unauthorized inventory than authorized (1.20M false vs 898K plausible).

## The smoking gun

```bash
# What the template claims:
curl -sL https://ads.themoneytizer.com/ads_txt.php | head -1
# → smartadserver.com, 1097, DIRECT

# What the registry says:
curl -sL https://smartadserver.com/sellers.json | jq '.sellers[] | select(.seller_id=="1097")'
# → {"seller_id":"1097","seller_type":"INTERMEDIARY","name":"Themoneytizer",...}
```

The template says DIRECT. The registry says INTERMEDIARY. The system contradicts itself. (Verified live: 2026-03-24)

**The Moneytizer knows this.** They claim DIRECT on their own site AND in the template they distribute to 1,108 publishers — but SmartAdServer's registry says they're INTERMEDIARY. They're making false claims about their own business relationship.

This template has been live since January 2024 ([Wayback Machine proof](https://web.archive.org/web/20240117183838/https://ads.themoneytizer.com/ads_txt.php)). One PHP script, 74 SSPs, 14,758 false claims.

## Why this matters

**For advertisers**: Major SSPs have tens of thousands of false authorization claims each — Lijit (79K), Google (74K), Magnite (72K), Taboola (63K). Your "brand safety" tools verify against a ledger where the entries contradict themselves — they check that claims *exist*, not that they're *consistent*. DIRECT inventory commands premium pricing — advertisers pay more for authorization that doesn't exist.

**For publishers**: Your template manager choice determines your false claim rate. CafeMedia-managed: 25% false. Moneytizer-managed: 73% false. A 48 percentage point difference from infrastructure choice alone.

**For everyone**: The authorization system produces MORE false claims (1.20M) than valid claims (898K). It's not "some fraud in a working system" — the system's primary output IS unauthorized inventory. And it sells anyway. If authorization were enforced, most of the market would stop. It doesn't stop, which proves it isn't enforced. (Observed: CNN has 9+ contradicted Magnite claims; Magnite serves ads on CNN anyway.)

## The proof it's fixable

- **The Guardian**: 7.1% false (careful maintenance)
- **Germany (.de TLD)**: 39% false (vs 63% for Russia/Japan)
- **CafeMedia-managed publishers**: 25% false (vs 57% baseline)

The technology exists. The question is incentive. Authorization is theater, not security — the system's function is liability distribution, not fraud prevention. Everyone can point to their paperwork.

## What we have

- 2,096,507 cross-verified claims across 23,283 publishers
- 710 SSP registries cross-referenced (1.89M seller entries); a follow-up fetch of 238 more SSPs on 2026-04-22 moved the headline rate by −0.03 percentage points (fabrication ≈ 36× staleness)
- Per-SSP mismatch rates
- Named template injectors with live URLs
- Interactive verification tool
- Documented methodology with self-corrections

## The scale

| SSP | Annual Revenue | False Claims | Publishers Affected |
|-----|---------------|--------------|--------------------|
| Lijit (Sovrn) | ~$100M | 79,453 | 10,882 |
| Google | $265B | 74,030 | 10,186 |
| Magnite (Rubicon) | $620M | 71,944 | 11,970 |
| Taboola | $1.7B | 63,409 | 2,781 |
| OneTag | private | 58,328 | 9,638 |
| PubMatic | $290M | 48,354 | 10,786 |
| Index Exchange | private | 44,658 | 10,454 |
| OpenX | private | 42,074 | 9,963 |
| TripleLift | private | 39,204 | 8,848 |
| AppNexus (Xandr/MSFT) | — | 33,595 | 7,531 |
| SmartAdServer | private | 33,352 | 7,693 |

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
