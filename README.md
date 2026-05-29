# ads.txt Framework Integrity Audit

**30.51% of DIRECT ads.txt claims don't reconcile against the named SSP's sellers.json.**
**That phantom volume is dominantly registry DECAY, not fabrication: a coefficient-of-variation test on per-publisher phantom across 9 snapshots finds ~97% fluctuates with registry churn (decay) and ~3% is temporally pinned (fabrication) — independently reproducing the cycle-468 mechanism decomposition (97.5% structural / 2.5% misconduct) by an unrelated method.**
**Independently, ~4% of observed Prebid bidder calls reach SSPs not declared in ads.txt (IAB-spec strict; Pearson r = 0.15 between declarative and observed rates).**

Corpus: 86,357 publishers · 33.39M ads.txt triples · 6.43M DIRECT claims · 1,548 SSP registries (~3.52M sellers). Crawler-harvest-expanded + dedup-corrected snapshot, **May 29, 2026** (was 74,460 pubs / 28.77M triples / 1,672 SSPs at the May 22 cycle-468 snapshot; the harvest grew publishers ~16% while a registry refresh consolidated to fewer-but-fuller registries — these move independently, see ERRATA E-2026-05-29-a..g).

> **Framing (2026-05-22, sharpened 2026-05-29).** The March 2026 headline ("57% false") was numerically defensible but the implied story (publisher fraud / industry cartel) does not survive structural decomposition. Cycle 468 decomposed phantom volume by mechanism-of-origin (35.2% live-SSP staleness, 23.5% template-driven, 17.1% orphan registries, 10.2% dead-SSP decay, 8.1% Google confidentiality flag, 3.5% Criteo schema migration; **only 2.5% willful-misconduct shape**). PASS-2 (2026-05-29) added the orthogonal temporal-fate axis: phantom RISES on publishers whose ads.txt is UNCHANGED across snapshots (registries prune sellers beneath them; 69% rise vs 13% fall on stable files, 18.9:1 accumulation ratchet) — i.e. the phantom rate is a registry-DECAY-equilibrium metric, and "fabrication" is a small temporally-PINNED minority (Taboola-class, CV<0.02) concentrated at named operators. Both decompositions agree at ~97/3 structural/misconduct. The framework needs a deprecation mechanism, not a fraud investigation. `FTC_COMPLAINT.md` and `DOJ_ANGLE.md` are superseded historical artifacts. Full corrective chain: `ERRATA.md` E-2026-05-22-a..m and E-2026-05-29-a..g (E-2026-05-29-g: registry-mismatch "impersonation" is 86% managed-service; the irreducible fabrication-shaped residual is under 1% of DIRECT).

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

## The Argument (revised 2026-05-22)

The earlier four-finding cartel/fraud framing is superseded. The current structural decomposition:

1. **The 30.51% phantom rate is dominantly framework brittleness, not publisher fraud.** Decomposed by mechanism-of-origin (cycle 468): 35.2% live-SSP staleness, 23.5% template-driven (Taboola 62%, IndexExchange 52%, Yahoo 71%, Outbrain 69%, MGID 70%), 17.1% live-SSP orphan registries (adtech.com, ampliffy, blis, ligadx, exponential, tribalfusion all at 100%), 10.2% dead-SSP decay, 8.1% Google confidentiality flag (IAB-spec-legal), 3.5% Criteo schema migration. The residual 2.5% — isolated low-rate claims in otherwise-clean publishers — is the only bucket compatible with publisher misconduct. PASS-2 (2026-05-29) confirms this by an orthogonal temporal-fate axis: ~97% of phantom fluctuates as registries prune sellers under unchanged ads.txt files (decay), ~3% is temporally pinned (fabrication, e.g. Taboola at coefficient-of-variation 0.0003) — same ~97/3 split, different method. (Was "33.83%" at the May-22 cycle-468 snapshot; 30.51% post-harvest-expansion + dedup.)

2. **The IAB framework has no SSP-death propagation channel (cycle 467).** 287,249 DIRECT claims to known-dead SSPs persist across 25,239 publishers (33.7% of corpus). RhythmOne (Tremor-acquired 2019, 7 years dead) still in 14,973 publishers (20.18%). Advertising.com (Yahoo legacy, 9 years dead) in 12.65%. When SSPs consolidate, no notification reaches publishers, networks, wrapper vendors, or IAB Tech Lab itself. Entries persist for years.

3. **28.6% of phantom lives in 1,102 centrally-managed templates (cycle 466).** 10,723 publishers (14.4% of corpus) publish IDENTICAL ads.txt files inherited from publisher-network parents: Vox/SB Nation (95 properties), Newsquest UK (82), Gannett (72), Black Press Canada (102), FanSided (115), IAC (63), Townsquare radio (62), Booking Holdings cheapflights cluster (62), plus a piracy mega-template (83 properties at 733 phantom each). Individual properties don't author their own ads.txt — they inherit it.

4. **The two failure modes are nearly independent (cycle 465).** Pearson r=0.15 between per-publisher declarative phantom rate and observed-unauthorized-bidder rate (n=66 X-Ray-observed pubs). Premium publishers exemplify the decoupling: the Condé Nast cluster (vogue, wired, arstechnica, bonappetit, epicurious) all show identical 22-23% declarative phantom with ZERO observed unauthorized. Centrally-managed ads.txt template carrying inherited phantom entries + property-level Prebid configs that operate cleanly.

5. **Identity proliferation and consent absence findings remain.** The cycle 458-468 decomposition focused on the authorization-side measurement; the privacy/identity findings from the original four-finding brief (0.012% valid TCF consent on first visit; average 5.1 identity-sharing companies per ad-tech-enabled site; 24% of observed companies operating outside any authorization framework) are unaffected by this revision.

**Net policy framing**: the IAB ads.txt framework defines registration (2017) but not deregistration. Nine years of SSP industry consolidation accumulated as ghost entries the framework was never designed to shed. Remediation scales by O(1,102 cluster managers) + IAB-spec extension, not O(86,000 publishers).

## Files

| File | Description |
|---|---|
| `evidence.html` | Visual evidence brief with interactive verification (4 findings) |
| `evidence_api.ts` | Deno server — loads data into memory, serves queries |
| `false_direct_claims.jsonl.gz` | 1,198,139 false (publisher, SSP, seller_id) triples — CONTRADICTED + PHANTOM only (gzipped) |
| `supply_chain_summary.json` | Aggregate totals — two rates reported (strict 29%, inclusive 57%) |
| `publisher_scores.json` | Pre-computed risk scores for 23,283 publishers (936KB) |
| `ssp_scores.json` | Per-SSP false claim tallies across 710 SSPs (~85KB) |
| `publisher_profiles.jsonl` | Per-publisher ads.txt depth and crawl traffic |
| `identity_graph.json` | 5,816 sync co-occurrence edges across 201 companies |
| `consent_measurement.json` | Per-company consent field presence rates |
| `crawl_summary.json` | Site distribution and geographic breakdown |
| `ERRATA.md` | Self-audit: what we got wrong and corrected |

## Two Rates

- **29% CONTRADICTED** (612,738 claims): The SSP's sellers.json explicitly classifies the account as INTERMEDIARY, but the publisher claims DIRECT. No ambiguity.
- **57% inclusive** (1,198,139 claims): Adds phantom seller IDs that don't exist in the registry. Could be stale, fabricated, or (for Google) hidden behind the confidentiality flag. We fetched 238 additional registries after the main snapshot; 2.7% of the existing phantoms reclassified (staleness-to-fabrication ratio ~1:36), headline unchanged.
- **62% verifiable** (among 710 SSPs with registries): When limited to SSPs where verification is possible, the false rate is higher because uncovered SSPs are excluded.

Both rates are stable across successive SSP expansions (14→24→37→62→84→178→228→312→417→710→948 SSPs) and across both curated (top-1000) and independently crawled (long-tail) publisher datasets.

## The Template Economy

16 intermediary accounts appear in more than half of all ads.txt files analyzed. The most ubiquitous (Rubicon seller_id 17960) is in 61% of files. These entries arrive via templates distributed by intermediaries to thousands of publishers.

2,033 (SSP, seller_id) pairs appear in 100+ publisher files each; 80 pairs appear in 1,000+ files. This is not individual publisher configuration — it is industrial-scale template injection.

## Reproduce

```bash
gunzip false_direct_claims.jsonl.gz

# Strict false count (CONTRADICTED only)
grep -c '"CONTRADICTED"' false_direct_claims.jsonl
# → 612,738

# Inclusive false count (CONTRADICTED + PHANTOM)
grep -cE '"CONTRADICTED"|"PHANTOM"' false_direct_claims.jsonl
# → 1,198,139

# Check a specific publisher
grep '"publisher":"cnn.com"' false_direct_claims.jsonl | python3 -m json.tool | head -20

# Top SSPs by false claims
grep -oE '"ssp":"[^"]*"' false_direct_claims.jsonl | sort | uniq -c | sort -rn | head -10
```

## Method

1. **ads.txt harvest**: 184,456 domains probed (Tranco top-1M + automated crawler piggyback). 25,598 with valid DIRECT claims. 23,283 publishers cross-verified (17,081 of them have at least one false claim).

2. **sellers.json fetch**: 710 SSP registries (1.89M total seller entries). Google's 994K-entry registry is 71% confidential (excluded from intermediary checks). All registries stored locally with fetch timestamps.

3. **Cross-verification**: For each DIRECT claim, looked up the seller_id in the SSP's sellers.json:
   - **CONTRADICTED**: SSP explicitly says INTERMEDIARY
   - **PHANTOM**: seller_id not in registry (ambiguous)
   - **PLAUSIBLE**: SSP confirms PUBLISHER or BOTH type
   - Deduplicated by (publisher, SSP, seller_id). Malformed seller_ids filtered.

4. **Crawl observation**: Playwright browser crawled 142,630 unique sites (Tranco 1M, tiered scheduling). 2.6M HTTP requests matched against 603 known ad-tech domains (240 companies). Compared observed companies against declared ads.txt entries to measure unauthorized tracking.

5. **Consent measurement**: 272,917 cookie sync URLs parsed for TCF consent parameters (first-visit only, March-18 measurement on the 110,610-site subset; see `consent_measurement.json`). The headline "0.012%" is computed against this 272,917 base — 34 valid TCF strings observed. The 721,129-sync figure cited elsewhere refers to total syncs captured across the full crawl; the consent rate was not re-measured at that scale.

6. **Identity graph**: Co-occurrence of tracking companies on the same page load. 201 companies, 5,816 weighted edges.

## Known Weaknesses

1. **Sample bias**: 23,283 publishers from Tranco top-1M + crawler piggyback. Biased toward popular Western commercial sites.
2. **Point-in-time**: SSPs can reclassify sellers. Registries are March 17–25, 2026 snapshots, with a 2026-04-22 re-fetch of 238 additional SSPs that moved the headline by −0.03pp.
3. **Phantom ambiguity**: 28% of claims are phantom. That's why we report both the strict (29%) and inclusive (57%) rates. The R150 expansion rechecked 22,928 phantoms against newly-fetched registries; 97.3% stayed phantom.
4. **First-visit consent**: The 0.012% rate measures first-visit behavior. Returning users may show higher rates.
5. **Google confidentiality**: 71% of Google's sellers.json is confidential. Excluding Google, the inclusive rate barely moves (~56.7% on conservative assumptions); the strict rate drops because Google's CONTRADICTED class is near zero.
6. **~5% estimate**: The net authorization figure multiplies three independent rates. The individual measurements are solid; the multiplication assumes independence, which is approximate.

## License

Data only. No software warranty. All source data (ads.txt, sellers.json) is publicly served by the respective domains. Verdicts are mechanical cross-reference, not editorial judgment. Verify independently before citing.
