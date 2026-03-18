# Ad Supply Chain Evidence Package

**53% of "DIRECT" authorization claims are explicitly contradicted by the SSPs' own registries.**
**A further 35% reference seller IDs that don't exist. Inclusive false rate: 70%.**
**0.012% of identity-sharing requests carry valid consent on first visit.**

657,286 cross-verified triples. 63 SSP registries (811K sellers). 125,000 websites crawled. 9,415 publisher ads.txt files. March 14–19, 2026.

## Quick Start

Open `evidence.html` in any browser. No server required for the narrative and charts.

For live publisher verification (type a domain, see its false claims):

```bash
# Decompress the data first
gunzip false_direct_claims.jsonl.gz

# Start the API
deno run --allow-net --allow-read evidence_api.ts
# Open http://localhost:8890/evidence
```

Or query the API directly:

```bash
curl "http://localhost:8890/api/verify?publisher=defence24.pl"
curl "http://localhost:8890/api/ssp?ssp=google.com"
curl "http://localhost:8890/api/ssps"
curl "http://localhost:8890/api/summary"
```

## Files

| File | Description |
|---|---|
| `evidence.html` | Visual evidence brief with interactive verification |
| `evidence_api.ts` | Deno server — loads data into memory, serves queries |
| `false_direct_claims.jsonl.gz` | 657,286 (publisher, SSP, seller_id) triples with verdicts (gzipped) |
| `supply_chain_summary.json` | Aggregate totals — two rates reported (strict 53%, inclusive 70%) |
| `publisher_profiles.jsonl` | 4,360 publishers with ads.txt depth and crawl traffic |
| `identity_graph.json` | 5,816 sync co-occurrence edges across 201 companies |
| `consent_measurement.json` | Per-company consent field presence rates |
| `crawl_summary.json` | Site distribution and geographic breakdown |
| `ERRATA.md` | Self-audit: what we got wrong and corrected |

## Two Rates

This dataset reports two false rates because the evidence has two tiers of strength:

- **53% strict** (228,638 claims): The SSP's own sellers.json explicitly classifies the account as INTERMEDIARY, but the publisher claims DIRECT. No ambiguity.
- **70% inclusive** (457,037 claims): Adds phantom seller IDs that don't exist in the SSP's registry. These could be stale, fabricated, or (for Google) hidden behind the confidentiality flag.

Both rates are stable across 5 successive SSP expansions (14→24→37→62→63 SSPs). The convergence is the strongest evidence that these are structural rates, not measurement artifacts.

## Who's Doing It

The 228,638 contradicted claims trace to a small number of intermediary companies whose accounts are falsely claimed as DIRECT by hundreds to thousands of publishers:

| Intermediary | SSP Accounts | Publishers Affected |
|---|---|---|
| Seedtag | Rubicon 17280, Lijit 397546 | 1,500+ |
| Google (as intermediary) | Rubicon 22884, PubMatic 159855 | 1,300+ |
| Rich Audience | Rubicon 13510, AppNexus 8233 | 1,200+ |
| SmartAdServer/Equativ | Rubicon 16114, SmartAdServer 4016 | 1,200+ |
| SmileWanted | Lijit 346012 | 1,000+ |
| Sharethrough | Sharethrough AXS5NfBr | 900+ |
| Conversant | Conversant 100141 | 900+ |

617 intermediary accounts (each claimed as DIRECT by 100+ publishers) account for 66% of all contradicted claims. Template injection, not individual publisher errors.

## Reproduce

```bash
gunzip false_direct_claims.jsonl.gz

# Strict false count (CONTRADICTED only)
grep -c '"CONTRADICTED"' false_direct_claims.jsonl
# → 228,638

# Inclusive false count (CONTRADICTED + PHANTOM)
grep -c '"CONTRADICTED"\|"PHANTOM"' false_direct_claims.jsonl
# → 457,037

# Check a specific publisher
grep '"publisher":"defence24.pl"' false_direct_claims.jsonl | python3 -m json.tool | head -20

# Top SSPs by false claims
grep -o '"ssp":"[^"]*"' false_direct_claims.jsonl | sort | uniq -c | sort -rn | head -10

# Find Seedtag's Rubicon account across publishers
grep '"seller_id":"17280"' false_direct_claims.jsonl | grep rubiconproject | wc -l
# → 1,440 publishers
```

## Method

1. **ads.txt harvest**: 10,024 files downloaded from publisher domains (Tranco top-1M + crawler harvest). HTML-filtered (42% of raw downloads were HTML error pages, not ads.txt).

2. **sellers.json fetch**: 63 SSP registries (811K total seller entries). Google's 650K-entry registry is 71% confidential. All registries stored locally with fetch timestamps.

3. **Cross-verification**: For each DIRECT claim, looked up the seller_id in the SSP's sellers.json:
   - **CONTRADICTED**: SSP explicitly says INTERMEDIARY
   - **PHANTOM**: seller_id not in registry (ambiguous — could be stale, fabricated, or confidential)
   - **PLAUSIBLE**: SSP confirms PUBLISHER or BOTH type
   - Deduplicated by (publisher, SSP, seller_id). Malformed seller_ids filtered.

4. **Consent measurement**: Headless Playwright browser crawled 125,000 unique sites. 273,000 sync URLs parsed for TCF consent parameters. First-visit only.

5. **Identity graph**: Co-occurrence of tracking companies on the same page load. 201 companies, 5,816 weighted edges.

## Known Weaknesses

1. **Sample bias**: 9,415 publishers from Tranco top-1M. Biased toward popular Western commercial sites.
2. **Point-in-time**: SSPs can reclassify sellers. Registries are March 17–18, 2026 snapshots.
3. **Phantom ambiguity**: 35% of claims are phantom — could be stale, fabricated, or behind Google's confidentiality flag. That's why we report both the strict (53%) and inclusive (70%) rates.
4. **First-visit consent**: The 0.012% rate measures first-visit sync behavior. Returning users with consent cookies may show higher rates.
5. **Google confidentiality**: 71% of Google's sellers.json is confidential. Google contributes 47,815 phantom claims and 0 contradicted. Excluding Google, the strict rate is 55%.

## License

Data only. No software warranty. All source data (ads.txt, sellers.json) is publicly served by the respective domains. Verdicts are mechanical cross-reference, not editorial judgment. Verify independently before citing.
