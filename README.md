# Ad Supply Chain Evidence Package

**68% of "DIRECT" authorization claims in publisher ads.txt files are false.**
**0.012% of identity-sharing requests carry valid consent on first visit.**
**Approximately 4% of the operational ad-tech data economy is properly authorized.**

915,460 cross-verified triples. 87 SSP registries (860K sellers). 142,000 websites crawled. 11,990 publisher ads.txt files. March 14–20, 2026.

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
curl "http://localhost:8890/api/verify?publisher=cnn.com"
curl "http://localhost:8890/api/ssp?ssp=google.com"
curl "http://localhost:8890/api/ssps"
curl "http://localhost:8890/api/summary"
```

## The Argument

This is not three separate findings. It is one system.

1. **Authorization is forged.** 34% of DIRECT claims are contradicted by the SSP's own registry (seller classified as INTERMEDIARY). Another 34% reference seller IDs that don't exist. Stable across 8 successive SSP expansions and across both curated and independently crawled publisher populations.

2. **Consent is absent.** 0.012% of cookie sync requests carry valid TCF consent on first visit. 77% have no consent parameter at all. The consent banner appears 2–5 seconds after identity has already been shared.

3. **Identity proliferates.** Average ad-tech-enabled site shares user identity with 5.1 companies. The worst shares with 294 in 10 seconds. 422,000 sync requests captured across 142,000 sites.

4. **The structure.** 85% of ad-tech-enabled sites have no ads.txt at all. Of the 15% that do, 68% of DIRECT claims are false. Of the companies actually observed on those pages, 24% operate outside any authorization framework. Net: ~4% of ad-tech activity falls within functioning authorization. Nine years after ads.txt was introduced, the false rate has not converged toward zero.

## Files

| File | Description |
|---|---|
| `evidence.html` | Visual evidence brief with interactive verification (4 findings) |
| `evidence_api.ts` | Deno server — loads data into memory, serves queries |
| `false_direct_claims.jsonl.gz` | 915,460 (publisher, SSP, seller_id) triples with verdicts (gzipped) |
| `supply_chain_summary.json` | Aggregate totals — two rates reported (strict 34%, inclusive 68%) |
| `publisher_profiles.jsonl` | Per-publisher ads.txt depth and crawl traffic |
| `identity_graph.json` | 5,816 sync co-occurrence edges across 201 companies |
| `consent_measurement.json` | Per-company consent field presence rates |
| `crawl_summary.json` | Site distribution and geographic breakdown |
| `ERRATA.md` | Self-audit: what we got wrong and corrected |

## Two Rates

- **34% strict** (310,989 claims): The SSP's sellers.json explicitly classifies the account as INTERMEDIARY, but the publisher claims DIRECT. No ambiguity.
- **68% inclusive** (623,242 claims): Adds phantom seller IDs that don't exist in the registry. Could be stale, fabricated, or (for Google) hidden behind the confidentiality flag.

Both rates are stable across 8 successive SSP expansions (14→24→37→62→63→84→86→87 SSPs) and across both curated (top-1000) and independently crawled (long-tail) publisher datasets.

## The Template Economy

16 intermediary accounts appear in more than half of all ads.txt files analyzed. The most ubiquitous (Rubicon seller_id 17960) is in 61% of files. These entries arrive via templates distributed by intermediaries to thousands of publishers.

904 (SSP, seller_id) pairs appear in 1,000+ publisher files each. This is not individual publisher configuration — it is industrial-scale template injection.

## Reproduce

```bash
gunzip false_direct_claims.jsonl.gz

# Strict false count (CONTRADICTED only)
grep -c '"CONTRADICTED"' false_direct_claims.jsonl
# → 310,989

# Inclusive false count (CONTRADICTED + PHANTOM)
grep -cE '"CONTRADICTED"|"PHANTOM"' false_direct_claims.jsonl
# → 623,242

# Check a specific publisher
grep '"publisher": "cnn.com"' false_direct_claims.jsonl | python3 -m json.tool | head -20

# Top SSPs by false claims
grep -o '"ssp": "[^"]*"' false_direct_claims.jsonl | sort | uniq -c | sort -rn | head -10
```

## Method

1. **ads.txt harvest**: 75,216 domains probed (Tranco top-1M + automated crawler piggyback). 12,965 valid ads.txt files recovered. 11,990 publishers with verifiable DIRECT claims.

2. **sellers.json fetch**: 87 SSP registries (860K total seller entries). Google's 650K-entry registry is 71% confidential. All registries stored locally with fetch timestamps.

3. **Cross-verification**: For each DIRECT claim, looked up the seller_id in the SSP's sellers.json:
   - **CONTRADICTED**: SSP explicitly says INTERMEDIARY
   - **PHANTOM**: seller_id not in registry (ambiguous)
   - **PLAUSIBLE**: SSP confirms PUBLISHER or BOTH type
   - Deduplicated by (publisher, SSP, seller_id). Malformed seller_ids filtered.

4. **Crawl observation**: Playwright browser crawled 142,630 unique sites (Tranco 1M, tiered scheduling). 2.6M HTTP requests matched against 603 known ad-tech domains (240 companies). Compared observed companies against declared ads.txt entries to measure unauthorized tracking.

5. **Consent measurement**: 272,917 cookie sync URLs parsed for TCF consent parameters. First-visit only.

6. **Identity graph**: Co-occurrence of tracking companies on the same page load. 201 companies, 5,816 weighted edges.

## Known Weaknesses

1. **Sample bias**: 11,990 publishers from Tranco top-1M. Biased toward popular Western commercial sites.
2. **Point-in-time**: SSPs can reclassify sellers. Registries are March 17–19, 2026 snapshots.
3. **Phantom ambiguity**: 34% of claims are phantom. That's why we report both the strict (34%) and inclusive (68%) rates.
4. **First-visit consent**: The 0.012% rate measures first-visit behavior. Returning users may show higher rates.
5. **Google confidentiality**: 71% of Google's sellers.json is confidential. Excluding Google, the strict rate is 38%.
6. **4% estimate**: The net authorization figure multiplies three independent rates. The individual measurements are solid; the multiplication assumes independence, which is approximate.

## License

Data only. No software warranty. All source data (ads.txt, sellers.json) is publicly served by the respective domains. Verdicts are mechanical cross-reference, not editorial judgment. Verify independently before citing.
