# Evidence Pitch — Ad Supply Chain Authorization Failures

## One-liner

55% of ad supply chain authorization claims are provably false. We have 1.76M cross-verified records. The system produces more unauthorized inventory than authorized.

## The smoking gun

```bash
curl -sL https://ads.themoneytizer.com/ads_txt.php | head -1
# Returns: smartadserver.com, 1097, DIRECT
```

SmartAdServer's registry says 1097 = INTERMEDIARY.

**The Moneytizer knows this.** Their own website (`themoneytizer.com/ads.txt`) does NOT include this claim. But their template serves it to 1,108 publishers. They don't eat their own cooking.

This template has been live since January 2024 (Wayback Machine verified). One PHP script, 16 SSPs, 14,758 false claims.

## Why this matters

**For advertisers**: $3B+ in SSP revenue flows through supply chains where majority of authorization claims are false. Your "brand safety" tools check against a system where the rules aren't enforced.

**For publishers**: Your template manager choice determines your false claim rate. CafeMedia-managed: 27% false. Moneytizer-managed: 77% false. A 50 percentage point difference from infrastructure choice alone.

**For everyone**: The authorization system produces MORE false claims (962K) than valid claims (794K). It's not "some fraud in a working system" — the system's primary output IS unauthorized inventory.

## The proof it's fixable

- **The Guardian**: 4.8% false (careful maintenance)
- **Germany (.de TLD)**: 39% false (vs 63% for Russia/Japan)
- **Yieldlove-managed publishers**: 30% false (vs 55% baseline)

The technology exists. The question is incentive.

## What we have

- 1,757,362 cross-verified claims across 21,397 publishers
- 70 SSP registries (1.19M seller entries)
- Per-SSP mismatch rates
- Named template injectors with live URLs
- Interactive verification tool
- Documented methodology with self-corrections

## The scale

| SSP | Annual Revenue | False Rate |
|-----|---------------|------------|
| Magnite | $620M | 86.5% |
| Taboola | $1.7B | 62.7% |
| PubMatic | $290M | 59.7% |
| Index Exchange | $500M | 74.0% |
| Google (ads) | $265B | 44.7% |

## How it works (for technical audiences)

Publishers list authorized sellers in ads.txt (DIRECT = direct relationship). SSPs list their sellers in sellers.json (INTERMEDIARY = reseller). These should match. They don't.

78% of false claims come from seller IDs each shared by 100+ publishers — statistical impossibility without automated template injection. 747 publishers share the exact same 4-company signature (Seedtag + Smile Wanted + NoBid + Rich Audience).

## Contact

Evidence package available on request:
- `evidence.html` — Interactive verification (runs locally, no server)
- `false_direct_claims.jsonl.gz` — 962K false claims (8.7MB)
- Complete methodology documentation

---

## Appendix: Per-SSP breakdown (for deep dives)

| SSP | Mismatch Rate | Claims | Primary Issue |
|-----|---------------|--------|---------------|
| Criteo | 100.0% | 23.1K | PHANTOM — all IDs use wrong format |
| FreeWheel | 90.3% | 21.5K | 90% PHANTOM |
| Magnite/Rubicon | 86.5% | 70.2K | 65% CONTRADICTED (template injection) |
| Lijit/Sovrn | 82.6% | 81.0K | |
| OneTag | 82.0% | 60.5K | |
| Index Exchange | 74.1% | 52.6K | 71% PHANTOM |
| Taboola | 62.7% | 86.0K | 63% PHANTOM |
| PubMatic | 59.7% | 68.3K | |
| Google | 44.7% | 144.8K | 17K unique phantom IDs |

## Appendix: Antitrust context

Magnite and PubMatic have filed antitrust lawsuits against Google. Our data shows the plaintiffs have demonstrably worse supply chain transparency than the defendant:

- Magnite: 86.5% mismatch (65% CONTRADICTED)
- PubMatic: 59.7% mismatch
- Google: 44.7% mismatch (but 17K phantom IDs)

This doesn't prove or disprove the antitrust claims. It shows the entire industry operates on a foundation of unverified authorization.
