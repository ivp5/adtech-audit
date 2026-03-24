# Errata & Self-Audit

Adversarial review of our own findings, March 18, 2026.

## Finding 1: 74% false DIRECT — HOLDS, with caveats

**Spec check: PASSED.** The IAB ads.txt spec defines DIRECT as "the Publisher directly controls the account." The IAB sellers.json spec defines INTERMEDIARY as "entity that does not own or control the content." A DIRECT claim for an INTERMEDIARY account is definitionally false under both specs. This is not an interpretation — it's a cross-reference of two IAB standards.

**Parsing bug found:** 129 of 177,897 seller_ids (0.07%) contain garbled data — spaces, "DIRECT" leaked into the ID field, concatenated filenames. All 129 are classified PHANTOM (garbled ID doesn't exist in any registry). This doesn't change the rate but is a data quality issue. These should be excluded.

**Corrected numbers:** 177,768 valid triples. 133,010 false. 74.8% → rounds to 75%. Effectively unchanged.

**What could still be wrong:** If the industry has collectively reinterpreted DIRECT to mean "authorized relationship" rather than "account control" — which contradicts the spec but might reflect practice — then CONTRADICTED claims (37%) would be reclassified as "technically false but industry-accepted." PHANTOM claims (37%) would remain unambiguously false regardless of interpretation: the seller_id doesn't exist.

## Finding 2: 0.012% consent — HOLDS

**Counter-hypothesis tested:** Could consent be transmitted via cookies or the `__tcfapi` JS API rather than URL parameters?

**Answer: No, for sync chains.** Cookie sync is a redirect chain: Site → SSP A → redirect → SSP B. SSP B receives only the URL. SSP B cannot read Site's cookies or call Site's JS API. The URL parameter is the only mechanism for the receiving party to verify consent in a sync redirect. Our measurement of URL parameters is the correct measurement for sync requests.

**What we didn't measure:** Bid requests (as opposed to sync requests) can carry consent in the POST body. We measured sync consent, not bid consent. The 0.012% applies to identity-sharing (syncs), not to auction participation (bids). This distinction is stated in the briefing but could be clearer.

## Finding 3: "Median 3 companies" — INFLATED

**Problem found:** The entity count includes false positives:
- CDN subdomains counted as tracking (poki-cdn.com, roblox.com infrastructure)
- Same company counted multiple times (mc.yandex.com + mc.yandex.ru = 2 entities, should be 1)
- First-party CMP subdomains counted as third-party tracking (cmp.lemonde.fr)

**Impact:** The median of 3 is likely 2 when deduplicated by parent organization and filtered for actual tracking. Sites with 0 syncs (87,863 scans — the majority) have entities that are analytics/CDN, not identity-sharing.

**What's reliable:** The sync count. A sync URL is definitionally identity-sharing — there's no CDN false-positive for a cookie_sync request. The 272,942 sync requests across the crawl are hard data. The entity count is soft. The top-end numbers (232 companies, 1,802 syncs on jpost.com) are real because at that scale, the false-positive rate is negligible relative to the true signal.

**Recommended correction:** Report "median 3 tracking entities" as "median 2 tracking companies (deduplicated)" or lead with syncs: "70% of tracked sites trigger at least 1 identity sync."

## Google 71% confidential — HOLDS

Verified against the raw data. 715K of 996K Google sellers.json entries have `is_confidential: true`. Every other SSP in our 24-SSP dataset has 0% confidential. This is a factual observation from the registry data.

## Summary of what needed fixing (March 18)

1. **129 garbled seller_ids** should be excluded from the JSONL (0.07% of records)
2. **"Median 3 companies"** should be restated with deduplication caveat or replaced with sync-based metric
3. **Consent measurement** should explicitly state it measures sync requests, not bid requests
4. The 74% and 0.012% survived adversarial review at that dataset size

---

## Update: March 20, 2026 — Dataset expansion

### Rate change: 74% → 68%

The dataset expanded from 177K to 915K triples (11,990 publishers, 87 SSPs). The inclusive false rate dropped from 74% to 68%. The strict contradicted rate dropped from 37% to 34%.

**Why it dropped:** The original dataset was curated from top-1000 publishers where template injection is most concentrated. The expanded dataset includes 7,898 additional publishers from the Tranco long tail (crawled automatically). Smaller publishers have simpler ads.txt files with fewer template-injected entries. The rate converged at 68% — stable across the last 4 SSP expansions (84→86→87 SSPs) and across both curated and crawled populations.

**Is 68% still meaningful?** Yes. The 34% strict rate means one in three DIRECT claims is provably false (SSP says INTERMEDIARY). That rate is a floor — it can only go up as more SSPs publish sellers.json. The 68% inclusive rate adds phantom entries (seller IDs that don't exist). Whether phantoms represent fraud or staleness depends on context, but they are unambiguously not DIRECT publisher relationships.

### Finding 3 correction applied

"Median 3 companies" replaced with "Average 5.1 companies per ad-tech-enabled site." Maximum updated from 232 to 294 (new crawl data). The median was misleading because 38% of crawled sites have zero ad-tech (classified as "clean"), pulling the median down. The average across sites that DO have ad-tech is 5.1.

### Finding 4 added

New finding: "Approximately 5% of the operational ad-tech data economy is properly authorized." Calculated from three independently measured rates: ads.txt adoption (15%), DIRECT claim validity (49%), and authorized company coverage (76%). Known weakness: the multiplication assumes approximate independence. The true figure is 4–6%. The point is the order of magnitude.

### PubMatic "NA" type entries

18 of PubMatic's 6,281 sellers have `seller_type: "NA"` (Not Available — unclassified). Our normalization stored these as type "N", which falls through to PLAUSIBLE in the verdict logic. Strictly, these should be excluded (neither confirmable nor contradictable). Impact: 18 of 915,460 records (0.002%). No reported number changes. These are PubMatic accounts with no name and no type — likely placeholder or deactivated entries.

### Items from March 18 audit — status

1. **Garbled seller_ids:** Excluded in regeneration. ✓
2. **Entity count inflation:** Finding 3 now leads with average (5.1) not median (3). Deduplication caveat in Known Weaknesses. ✓
3. **Consent scope:** Method box now explicitly states "consent analysis covers the 110,610-site subset." ✓

---

## Update: March 23, 2026 — International expansion

### Dataset: 915K → 1.76M claims

Expanded to 21,397 publishers across 42 TLDs via automated international harvest. Registry entries: 1.13M sellers from 45 SSPs.

### Rate change: 68% → 51% overall, 65% covered

**Why it dropped further:** International expansion added publishers with simpler ads.txt files. Many international SSPs don't publish sellers.json (uncovered). Among SSPs WITH registry coverage, the rate remains 64.7%.

**Geographic findings:**
- Japan (.jp): 59% mismatch — global SSPs dominate
- Russia (.ru): 56% mismatch
- Germany (.de): 36% mismatch — strong local SSPs (stroeer, yieldlove, businessad)

**Key insight:** Local SSPs maintain clean registries (0-20% mismatch). Global SSPs are dirty everywhere (80%+ mismatch). Germany's low rate comes from local SSP market share, not cleaner global practices.

### Template injection proof strengthened

SmartAdServer seller_ids 4071, 4012, 4074, 4073 don't exist in their registry yet each is claimed by 2,000+ publishers across 50+ countries. These are fabricated IDs mass-injected via templates.

Google phantom IDs: 110 non-existent pub-XXXXX IDs each claimed by 100+ publishers = 23K template-injected claims.

### Lijit.com registry integration (March 23)

Discovered lijit.com serves Sovrn's sellers.json (7,267 sellers). Cross-referenced against 11,951 UNCOVERED sovrn.com claims. 162 seller_ids are INTERMEDIARY in lijit's registry → 5,960 claims upgraded from PLAUSIBLE to CONTRADICTED.

**Updated totals:**
- CONTRADICTED: 499,709 (was 493,749)
- Total false: 932,094 (was 929,697)

### Betweendigital.com integration (March 23)

Discovered betweendigital.com sellers.json (461 sellers). Cross-referenced against 3,702 UNCOVERED claims. 43 seller_ids are INTERMEDIARY → 2,397 claims upgraded to CONTRADICTED.

### Final totals (March 23, end of day)

- Total claims: 1,757,362
- CONTRADICTED: 503,387 (29%)
- PHANTOM: 459,504 (26%)
- PLAUSIBLE: 793,727 (45%)
- False rate (inclusive): 54.8%
- Publishers: 21,397
- SSPs with registries: 84

**Note (March 24):** The distributed `false_direct_claims_final.jsonl` was generated before the Lijit/Betweendigital integrations. Its actual counts are CONTRADICTED: 493,749 + PHANTOM: 429,988 = 923,737 (52.5%). The headline "55%" reflects the final totals above (54.8%); the JSONL needs regeneration to match.
