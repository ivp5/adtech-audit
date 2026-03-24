# Evidence Pitch — Ad Supply Chain Authorization Failures

## One-liner

55% of ad supply chain authorization claims are provably false. We have 1.76M cross-verified records. The system produces more unauthorized inventory than authorized.

## The smoking gun

```bash
# What the template claims:
curl -sL https://ads.themoneytizer.com/ads_txt.php | head -1
# → smartadserver.com, 1097, DIRECT

# What the registry says:
curl -sL https://www.equativ.com/sellers.json | jq '.sellers[] | select(.seller_id=="1097")'
# → {"seller_id":"1097","seller_type":"INTERMEDIARY","name":"Themoneytizer",...}
```

The template says DIRECT. The registry says INTERMEDIARY. The system contradicts itself. (Verified live: 2026-03-24)

**The Moneytizer knows this.** They claim DIRECT on their own site AND in the template they distribute to 1,108 publishers — but SmartAdServer's registry says they're INTERMEDIARY. They're making false claims about their own business relationship.

This template has been live since January 2024 ([Wayback Machine proof](https://web.archive.org/web/20240117183838/https://ads.themoneytizer.com/ads_txt.php)). One PHP script, 74 SSPs, 14,758 false claims.

## Why this matters

**For advertisers**: Major SSPs have tens of thousands of false authorization claims each — Lijit (69K), Magnite (62K), Taboola (54K). Your "brand safety" tools verify against a ledger where the entries contradict themselves.

**For publishers**: Your template manager choice determines your false claim rate. CafeMedia-managed: 25% false. Moneytizer-managed: 73% false. A 48 percentage point difference from infrastructure choice alone.

**For everyone**: The authorization system produces MORE false claims (963K) than valid claims (794K). It's not "some fraud in a working system" — the system's primary output IS unauthorized inventory. And it sells anyway. If authorization were enforced, half the market would stop. It doesn't stop, which proves it isn't enforced.

## The proof it's fixable

- **The Guardian**: 7.1% false (careful maintenance)
- **Germany (.de TLD)**: 39% false (vs 63% for Russia/Japan)
- **CafeMedia-managed publishers**: 25% false (vs 55% baseline)

The technology exists. The question is incentive. The system's function is not fraud prevention — it's liability distribution. Everyone can point to their paperwork.

## What we have

- 1,757,362 cross-verified claims across 21,397 publishers
- 84 SSP registries cross-referenced (1.56M seller entries)
- Per-SSP mismatch rates
- Named template injectors with live URLs
- Interactive verification tool
- Documented methodology with self-corrections

## The scale

| SSP | Annual Revenue | False Claims |
|-----|---------------|--------------|
| Lijit/Sovrn | ~$100M | 68,785 |
| Google | $265B | 64,743 |
| Magnite | $620M | 62,495 |
| Taboola | $1.7B | 53,869 |
| PubMatic | $290M | 41,912 |

## How it works (for technical audiences)

Publishers list authorized sellers in ads.txt (DIRECT = direct relationship). SSPs list their sellers in sellers.json (INTERMEDIARY = reseller). These should match. They don't.

**The spec is unambiguous.** IAB ads.txt defines DIRECT as "the Publisher directly controls the account." IAB sellers.json defines INTERMEDIARY as "entity that does not own or control the content." A DIRECT claim for an INTERMEDIARY account is definitionally false under both specs — not an interpretation, a cross-reference.

68% of false claims come from seller IDs each shared by 100+ publishers — statistical impossibility without automated template injection. 3,264 publishers share the same false (rubiconproject.com, 17280) claim; 2,557 share (smartadserver.com, 4071).

## Cite correctly

"55% of DIRECT authorization claims in ads.txt are false" — not "55% of ads are fraudulent." The finding is about the authorization ledger, not the ads themselves.

## Contact

Evidence package available on request:
- `evidence.html` — Interactive verification (runs locally, no server)
- `false_direct_claims.jsonl.gz` — 963K false claims
- Complete methodology documentation

All source data (ads.txt, sellers.json) is publicly served by the respective domains. Verdicts are mechanical cross-reference of public records.

---

## Appendix: Per-SSP breakdown (for deep dives)

| SSP | False Claims | Primary Issue |
|-----|--------------|---------------|
| Lijit/Sovrn | 68.8K | Template injection |
| Google | 64.7K | Phantom IDs (registry 71% confidential) |
| Magnite/Rubicon | 62.5K | Template injection |
| Taboola | 53.9K | 90% phantom on own property |
| OneTag | 50.8K | |
| PubMatic | 41.9K | |
| Index Exchange | 38.9K | |
| OpenX | 36.6K | |
| TripleLift | 33.8K | |

## Appendix: Taboola's self-contradiction

taboolanews.com is Taboola's own content property. Its ads.txt lists 3,841 Taboola seller IDs as DIRECT. Of those, **3,694 (90%) don't exist in Taboola's own sellers.json**.

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
- Google: 44.7% mismatch (but 17K phantom IDs)

This doesn't prove or disprove the antitrust claims. It shows the entire industry operates on a foundation of unverified authorization.
