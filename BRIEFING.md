# Ad Network Market Dynamics

*112K sites crawled, 1.69M HTTP requests, 4,398 publisher ads.txt files, 24 SSP registries (1.11M sellers). Data: 2026-03-14 through 2026-03-18.*

## Supply Chain Authorization Is a Business Model for Fraud

**74-95% of DIRECT authorization claims in ads.txt are provably false.** 177,897 unique (publisher, SSP, seller_id) triples cross-verified against 24 SSP sellers.json registries:

| Category | Count | % | How verified |
|---|---|---|---|
| Contradicted (SSP says INTERMEDIARY) | 66,901 | 37% | seller_type mismatch |
| Phantom (seller_id not in registry) | 66,109 | 37% | seller_id lookup miss |
| Shared "plausible" (5+ pubs claim same PUBLISHER ID) | ~33,000 | ~19% | sharing analysis |
| Genuinely plausible | ~12,000 | ~6% | 1 publisher per ID, or shared 2-4 |

The 74% floor requires zero interpretation — mechanical cross-reference. The 94% adds one judgment: 735 publishers can't all directly control the same SmartAdServer account.

**Why it happens:** Intermediaries distribute template ads.txt blocks with DIRECT instead of RESELLER. DIRECT commands higher CPMs from demand-side platforms and lower SSP fees (Magnite charges intermediaries 1.3pp more than publishers). The intermediary's cut becomes invisible to the buyer.

**Who profits:** Seedtag Advertising SL (724 publishers paste their template), Rich Audience Technologies SL (687), Google-as-intermediary (697), SmartAdServer (736 for one seller_id alone, 6 IDs in the top 20). These companies earn revenue through every publisher who pastes their template without understanding what they authorized.

**Google's role:** 71% of Google's 996K seller registry is marked confidential (is_confidential: true). Every other SSP: 0%. The confidentiality flag makes template injection undetectable — you can't verify a DIRECT claim if the seller's identity is hidden.

## Consent Is Absent, Not Broken

**0.012% of identity-sharing requests carry valid TCF consent on first visit.** 34 genuine consent strings in 272,917 sync requests.

- 67.8% of syncs have no consent parameter at all
- 30.4% have the parameter but it's empty
- 1.7% have unresolved template macros (`${GDPR_CONSENT}`, `[GDPR_CONSENT]`)
- 0 of 2,000 captured Prebid instances configure the consent module
- Empty consent in BidSwitch sync chains dates to 2020 (Wayback evidence)

Server-side enforcement exists but varies: Magnite PBS drops all bidders when consent is missing. Relevant Digital PBS calls bidders regardless. The gate works at Magnite. The pipe to the gate is empty everywhere.

**This measures first-visit behavior** — before the user interacts with the consent banner. Syncs fire, identities propagate, the graph assembles. By the time the user clicks "Accept" or "Reject," 232 companies already know who they are.

## The Identity Graph

**Median site: 3 tracking companies.** 91% of sites have fewer than 10. Quick crawls undercount by 2.4x (entities) and 12x (syncs) vs deep scans. True median for engaged users: likely 5-7.

At the extreme (220 news/media sites, 0.2% of crawl): one page load triggers 1,802 syncs to 232 companies in 10 seconds, three waves. The graph hubs: Trade Desk (15 sync partners), Xandr (14), then Magnite/Criteo/PubMatic/ID5/BidSwitch as connectors. Known users generate 3.1x more revenue than unknown (Disqus identity_source data).

UK sites: 15.1 syncs/site average. German sites: 0.5. Both EU, both GDPR. The difference is publisher configuration, not regulation.

## Key Numbers

| Metric | Value | Source |
|---|---|---|
| False DIRECT (floor) | 74% of 177,897 triples | ads.txt × 24 sellers.json, deduplicated |
| False DIRECT (with sharing) | ~95% | + shared PUBLISHER IDs, 5+ threshold |
| Consent (first visit) | 0.012% (34 of 273K) | sync URL parameter analysis |
| Google sellers confidential | 71% (715K of 996K) | every other SSP: 0% |
| Identity premium | 3.1x revenue | Disqus by identity_source |
| Tracking density | median 3, P99=50, max 294 | 131K scans |
| UK/Germany sync differential | 30x | geographic crawl breakdown |
| Magnite publisher fee range | 8-34% (active), 99% (inactive) | PMG admin endpoint, no auth |
| Prebid median CPM | $0.028 | 445 client-side bids |

## Data

`data/exports/20260318/` — standalone, no live database required:

- `false_direct_claims.jsonl` — 177,897 triples with publisher, SSP, seller_id, registry_type, verdict. Grep for a publisher domain to see their false claims. Grep for a seller_id to see template distribution.
- `supply_chain_summary.json` — totals matching the JSONL exactly
- `publisher_profiles.jsonl` — 4,360 publishers with ads.txt depth + crawl traffic
- `identity_graph.json` — 5,816 sync co-occurrence edges across 201 companies
- `consent_measurement.json` — per-company consent field presence rates
- `crawl_summary.json` — site distribution and geographic breakdown

## Known Weaknesses

1. **Sample**: 4,398 publishers from Tranco top-1M. Biased toward popular Western commercial sites. The relevant population for programmatic authorization, but not the internet.

2. **sellers.json freshness**: Snapshots from 2026-03-17. Contradicted claims (37%) can't change — INTERMEDIARY doesn't become PUBLISHER. Even if all phantom claims resolved, contradicted alone is 37%.

3. **Consent = first visit**: Returning users with consent cookies likely have higher rates. The first-visit case is the privacy-critical one — syncs fire before the user can consent — but should not be generalized.

4. **Sharing analysis**: The ~95% assumes 5+ publishers sharing one PUBLISHER seller_id means at most 1 is legitimate. Multi-domain publishers (Learfield, Bonnier, Postmedia) have legitimate shared DIRECT. The range is 74-95%, not a point estimate.

5. **Quick crawl undercounting**: Median of 3 is from 4-second page loads. Deep scans (12s) see 2.4x more entities. The true median is 5-7 for fully-loaded pages.

6. **Edge case**: 58 of 81K contradicted claims (0.07%) are intermediaries publishing on their own domain. Ambiguous under the spec. Changes nothing at any scale.

## Infrastructure

909 lines of Deno. Crawler (40 parallel, ~2K scans/hr with integrated ads.txt harvest), server (:8889 with dashboard, stats, alerts, proxy, scan), watchdog (auto-restart, RSS monitoring, WAL compaction), ccurl (FFI Chrome TLS, 8-way port race, port affinity learning). ads.txt verifier tool at `/tools/adstxt_verify.html`.
