# Ad Supply Chain Evidence Package

**74% of "DIRECT" authorization claims in publisher ads.txt files are provably false.**
**0.012% of identity-sharing requests carry valid consent on first visit.**
**Median website shares user identity with 3 companies; the worst shares with 232.**

Data: 112,000 websites crawled, 24 SSP registries (1.11M sellers), 273,000 sync requests analyzed. March 14–18, 2026.

## Quick Start

Open `evidence.html` in any browser. No server required for the narrative and charts.

For live publisher verification (type a domain, see its false claims):

```bash
deno run --allow-net --allow-read evidence_api.ts
# Then open http://localhost:8890/evidence
```

Or query the API directly:

```bash
# Check a publisher
curl "http://localhost:8890/api/verify?publisher=forbes.pl"

# Check an SSP
curl "http://localhost:8890/api/ssp?ssp=google.com"

# Get all SSPs ranked by false claims
curl "http://localhost:8890/api/ssps"

# Full summary
curl "http://localhost:8890/api/summary"
```

## Files

| File | Size | Description |
|---|---|---|
| `BRIEFING.md` | 6KB | Executive summary — start here |
| `evidence.html` | 20KB | Visual evidence brief with interactive verification |
| `evidence_api.ts` | 4KB | Deno server that loads data + serves queries |
| `false_direct_claims.jsonl` | 24MB | 177,897 (publisher, SSP, seller_id) triples with verdicts |
| `supply_chain_summary.json` | 1KB | Aggregate totals |
| `publisher_profiles.jsonl` | 778KB | 4,360 publishers with ads.txt depth |
| `identity_graph.json` | 581KB | 5,816 sync co-occurrence edges across 201 companies |
| `consent_measurement.json` | 28KB | Per-company consent field presence rates |
| `crawl_summary.json` | 1KB | Site distribution and geographic breakdown |

## Reproduce

Every number in the briefing traces to the JSONL:

```bash
# Count false claims
grep -c '"CONTRADICTED"\|"PHANTOM"' false_direct_claims.jsonl
# → 133,010

# Check a specific publisher
grep '"publisher":"forbes.pl"' false_direct_claims.jsonl | python3 -m json.tool

# Count by SSP
grep -o '"ssp":"[^"]*"' false_direct_claims.jsonl | sort | uniq -c | sort -rn | head -10

# Check Google's false claims
grep '"ssp":"google.com"' false_direct_claims.jsonl | grep '"PHANTOM"' | wc -l
# → 13,850
```

## Method

1. **ads.txt harvest**: Downloaded ads.txt from 4,411 publishers (Tranco top-1M). HTML-filtered (42% of raw downloads were HTML error pages, not ads.txt).

2. **sellers.json fetch**: Downloaded sellers.json from 24 SSPs (1.11M total seller entries). Google's is 71% confidential.

3. **Cross-verification**: For each DIRECT claim in ads.txt, looked up the seller_id in the SSP's sellers.json. Three outcomes:
   - **CONTRADICTED**: SSP registry says this seller is INTERMEDIARY, not PUBLISHER
   - **PHANTOM**: seller_id doesn't exist in the SSP's registry at all
   - **PLAUSIBLE**: SSP registry confirms PUBLISHER type

4. **Consent measurement**: Headless browser (Playwright) crawled 110,610 unique sites. All HTTP requests logged. Sync URLs identified by pattern. Consent parameters parsed from query strings.

5. **Identity graph**: Co-occurrence analysis — if Company A and Company B both appear in sync requests on the same page load, they share an edge weighted by frequency.

## Known Weaknesses

See BRIEFING.md § Known Weaknesses. The 74% is a floor. The 95% requires one judgment call. The consent measurement is first-visit only. The crawl is biased toward Western commercial sites.

## License

Data only. No software warranty. Verify independently before citing.
