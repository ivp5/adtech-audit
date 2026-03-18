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

## Summary of what needs fixing

1. **129 garbled seller_ids** should be excluded from the JSONL (0.07% of records)
2. **"Median 3 companies"** should be restated with deduplication caveat or replaced with sync-based metric
3. **Consent measurement** should explicitly state it measures sync requests, not bid requests
4. The 74% and 0.012% survive adversarial review
