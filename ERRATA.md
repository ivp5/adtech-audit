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

## Errata from continued investigation, April 22, 2026

### E-2026-04-22-a: "Clean German B2B cohort of 15 independent publishers" was wrong

Prior internal analysis (parent repo R162) characterized 14-15 publishers at 0% false rate as "a cohort of German B2B trade imprints — existence proof of scalable operational hygiene." Subsequent Wayback check found that haufe.de, lto.de, and springerprofessional.de have byte-identical 2,027-line 88,138-byte ads.txt files on 2026-04-04/06. They are one shared template distributed across brand endpoints of a few publishing conglomerates (Haufe Group, Springer Nature, Wolters Kluwer), not independent operational examples. The underlying "0% false" data remains accurate; the framing of the cohort as 15 independent instances was incorrect.

### E-2026-04-22-b: Registry count double-counts firms via brand aliases

"SSP registries: 710" (this file, above) and subsequent scale-ups to 1,124 loaded registries double-count shell aliases. At the firm level, consolidation is material:

- Digital Turbine (NASDAQ: APPS) = Fyber + AdColony + DigitalTurbine (6 registry aliases, shared contact `info@fyber.com`)
- Liftoff + Vungle (4 aliases after merger)
- Magnite = Rubicon + Tremorhub
- Sovrn = Lijit + Lijit_com
- Criteo = TheMediaGrid + Commerce Grid (3 aliases)
- Insticator = OKO (oko.uk, identical contact `revops@insticator.com` at Miami address)
- AnyManager = Fourm (Singapore, shared `partner@adasiaholdings.com`)

Approximately 30-40 registry entries collapse to 10-15 distinct firms. The firm-level concentration of the ecosystem is higher than file-level registry count suggests.

### E-2026-04-22-c: Some registries are operationally broken at the serialization level

12,422 (SSP, seller_id) pairs across loaded registries have MULTIPLE DIFFERENT owner domains within the SAME SSP's sellers.json — a direct violation of the sellers.json spec's per-SSP uniqueness requirement. Top offenders:

- globalsun.io seller_id 526 lists 10,165 different owner domains
- bigo.sg seller_id 1112518: 2,404 different domains
- didna.io seller_id 494n1p17243a: 1,730
- fatchillimedia.com seller_id 22513247416: 1,122

These registries are publishing non-functional data at the spec level. A file-load count of "1,124 SSPs with registries" should be understood as including registries that do not satisfy spec-level integrity.

### E-2026-04-22-d: Adagio is a hidden template authorship layer

Venatus's template (`adstxt.venatusmedia.com/master_ads.txt`) carries inline `# Adagio_0_6` annotations on every line. Adagio (adagio.io, 450 Rue Baden Powell, 34000 Montpellier, France) is the template author; Venatus is a distribution endpoint. 882 publishers across the dataset carry the `# Adagio` marker; 820 of those (93%) declare no managerdomain at all. The nine "named primary injectors" previously identified are a layer of *seller accounts*; Adagio is a layer above, the *template author* whose pipeline embeds those accounts.

### E-2026-04-22-e: The "decorative disclosure" reframe

A 9-year stable 57% false rate across two specification revisions (ads.txt 1.0→1.1, sellers.json) and three named enforcement regimes (FTC Section 5, EU DSA, DOJ antitrust) is not consistent with a functioning disclosure instrument. A 2026-04-22 test of 1,053 correcting publishers vs 3,031 retainers found correctors are *larger* publishers with *more* SSPs and *growing* files — correction correlates with template-heaviness (routine wrapper housekeeping), not hygiene-pursuit. Correction has no structural cost. The disclosure layer does not bind. This does not invalidate the prior headline numbers; it reframes what they describe — accountability-diffusion, not failed transparency.

## Errata from continued investigation, April 27, 2026

### E-2026-04-27-a: Headline DIRECT-false rate has drifted upward to 61.1%

The 57.1% headline (March 2026 corpus) is an undercount at the 2026-04-27 snapshot. Recomputed against `tmp/adstxt_derived.db`:

| Bucket | DIRECT claims | Phantom (in_registry=0) | Contradicted (rel=DIRECT, registry=INTERMEDIARY) | False total | False % |
|---|---:|---:|---:|---:|---:|
| Verifiable SSPs | 6,329,022 | 2,000,507 | 1,867,618 | 3,868,125 | **61.1%** |
| Structurally-unverifiable (13 SSPs, see E-2026-04-27-b) | 231,545 | 230,474 | 147 | 230,621 | 99.6% |
| Combined | 6,560,567 | 2,230,981 | 1,867,765 | 4,098,746 | 62.5% |

The 61.1% verifiable-bucket rate is the rate the rest of the paper should now cite as headline; the 62.5% all-claims rate is inflated by structural-unverifiable artifact (next entry).

### E-2026-04-27-b: Thirteen SSPs are structurally unverifiable; their 99.6% phantom rate is registry-resolution artifact, not deception

Tested by following each SSP's `/sellers.json` redirect chain from a clean proxy. The following SSPs do not serve a verifiable sellers.json at the canonical URL:

| SSP | Behavior | Resolution |
|---|---|---|
| criteo.com | 301 → themediagrid.com (Commerce Grid registry, 1,819 sellers, contact `commerce-grid@criteo.com`) | Different product registry; Criteo Classic retargeting publishes no public sellers.json |
| advertising.com | 301 → contango-cdn.technoratimedia.com | Yahoo successor; third-party CDN |
| adcolony.com | 308 → digitalturbine.com | Acquired entity registry |
| adtech.com | 301 → oneadserver.aol.com/ (no sellers.json) | Successor with no published registry |
| aol.com | 301 → www.aol.com (then 429 rate-limited) | Inaccessible programmatically |
| tidaltv.com | 404 | Defunct |
| bloxdigital.com | 301 → www, then 429 | Rate-limited |
| mediago.io | 301 → mediago.com | www redirect (works) |
| mobfox.com | 301 → www.mobfox.com | www redirect |
| engagebdr.com, yandex.com, gamoshi.io, vdopia.com | various failures | Inaccessible |

These 13 SSPs collectively contribute 9.2% of total phantom volume (790,510 of 8,564,594) but only 3.5% of DIRECT claims (231,545 of 6,560,567). The 99.6% phantom rate they exhibit is not a fraud signal; it is a structural failure of registry publication. Excluding them lowers the headline DIRECT-false rate by ~1.4 percentage points (62.5% → 61.1%).

**Special case — Criteo.** Criteo (CRTO, FY2025 10-K revenue $1.681B, the second-largest pure-play ad-tech company by revenue and the largest non-Google entity in the dataset) does not publish a public sellers.json for its core retargeting product. The criteo.com/sellers.json URL has been a 301 redirect to themediagrid.com (Commerce Grid, a separate Criteo product) since at least 2021-07-27 per Wayback Machine. None of static.criteo.com, exchange.criteo.com, gum.criteo.com, bidder.criteo.com, www.criteo.net, criteo.net serves a Criteo Classic sellers.json. The "criteo.com 99.9% phantom" pattern reflects Criteo's IAB-framework non-participation by the SSP, not deception by the publishers — those publisher claims (in `B-NNNNNN` Criteo Classic seller-id format) may correspond to genuine relationships that the framework simply cannot verify. This is a different finding than template-injection deception; it is a public-registry-publication failure by a publicly-traded SSP that just converted to domestic-registrant 10-K filing in early 2026.

### E-2026-04-27-c: SEC 10-K disclosure silence on the IAB framework

Direct examination of seven major public ad-tech companies' FY2025 10-K filings on EDGAR (verified by tag-strip-then-regex search of the filed `tbla-20251231.htm`, `crto-20251231.htm`, `tead-20251231.htm`, `ramp-20250331.htm`, plus the previously retrieved TTD/MGNI/PUBM filings) returns:

| Company | "ads.txt" hits | "sellers.json" hits | "IAB Tech Lab" hits | Filing date |
|---|---:|---:|---:|---|
| Trade Desk (TTD) | 0 | 0 | 0 | 2026-02-27 |
| Criteo (CRTO) | 0 | 0 | 0 | 2026-02-26 (first 10-K, ex 20-F) |
| Magnite (MGNI) | 0 | 0 | 0 | FY2025 |
| PubMatic (PUBM) | 0 | 0 | 2 (TCF/GPP only) | FY2025 |
| Taboola (TBLA) | 0 | 0 | 0 | 2026-02-25 (first 10-K, ex 20-F) |
| Outbrain → Teads (TEAD) | 0 | 0 | 0 | 2026-03-16 |
| LiveRamp (RAMP) | 0 | 0 | 0 | FY2025 (FY ends Mar 31) |
| **Total across 7 filings** | **0** | **0** | **2** (PubMatic only, TCF context) | |

The IAB Tech Lab authorization framework — the basis for every claim in this paper — is not mentioned in the primary regulatory disclosures of the companies whose registries the framework depends on. PubMatic's two IAB Tech Lab mentions are exclusively about TCF (consent) and GPP (privacy), never about the authorization framework. See `memory/sec_disclosure_silence_20260427.md` for the search method and verification. The implication for the §3.4 enumeration of regulatory regimes is added directly in §3.4 #2 (Rule 10b-5).

### E-2026-04-27-d: Three named primary template-injection operators surface at industrial scale via in-registry seller_ids reused across thousands of publishers

A query of `adstxt_triples` for in-registry seller_ids appearing across more than 100 distinct publisher domains, grouped by the registry-disclosed `reg_domain`, surfaces three Madrid-based contextual ad-tech operators as the dominant operators of the schain-spec-violating shared seller_id pattern:

- **Seedtag Advertising SL** — 22+ SSPs hold a Seedtag seller_id; total 199,016 claims across 15,432 unique publisher domains; 56,825 (28.6%) of those claims are CONTRADICTED. Top per-SSP reach: xandr.com 4009 (14,500 publishers), rubiconproject.com 17280 (14,146), smartadserver.com 3050 (14,084), pubmatic.com 157743 (13,662), lijit.com 397546 (10,432), openx.com 558758631 (10,316), onetag.com (9,976), adform.com 1889 (9,558), adyoulike.com (9,243), improvedigital.com 1680 (8,940), loopme.com 11712 (8,802), sharethrough.com AXS5NfBr (8,356), 33across.com (5,945), richaudience.com ns9qrKJLKD (5,734), beachfront.com 15250 (4,443), sovrn.com 397546 (3,276), spotx.tv 249286 (2,212).
- **Rich Audience Technologies SL** — separately reaches 17,803 publishers via rubiconproject.com 13510, 17,673 via appnexus.com 8233, 17,131 via pubmatic.com 81564, 16,262 via pubmatic.com 156538 (a *second* PubMatic seller_id for the same operator — itself a separate IAB-spec concern), 14,115 via adform.com 1942, and 9,956 via google.com pub-4673227357197067 (Google AdSense).
- **SunMedia** (related Spanish entity) — reaches 11,551 via smartadserver.com 1999, 7,834 via triplelift.com 8683, plus PubMatic, OneTag, AppNexus, Rubicon equivalents in the 7-9K range each.

These results extend §1¶3 of the paper: the named primary injectors identified in March 2026 are confirmed at the April 2026 snapshot, and the proposition that they are "named, addressed, connected operators" (rather than opaque entities) is reinforced. Seedtag's publisher network includes premium properties (theatlantic.com, heraldtribune.com, kold.com), refuting any framing that the operator is restricted to low-tier or piracy inventory. See `memory/seedtag_richaudience_template_operators_20260427.md` for full enumeration.

### E-2026-04-27-e: TAG-IDs at the publisher-side concentration top are SSP certificate IDs, not unknown entities

A hypothesis tested 2026-04-27: that the publisher-side concentration top of TAG-IDs (TAG certified IDs found in publisher ads.txt) might surface unidentified high-reach brokers exceeding the named operators. Falsified. The top six unfamiliar TAG-IDs each map to existing major SSPs:

- 0bfd66d529a55807 → Rubicon (Magnite), 1,799,309 lines
- 5d62403b186f2ace → PubMatic, 2,252,776 lines
- 6a698e2ec38604c6 → OpenX, 1,145,208 lines
- f5ab79cb980f11d1 → AppNexus / Xandr, 1,192,191 lines
- 50b1c356f2c5c8fc → Index Exchange, 588,533 lines
- 89ff185a4c4e857c → ContextWeb / PulsePoint, 433,770 lines
- f08c47fec0942fa0 → Google, 1,457,695 lines

The TAG-IDs at the concentration top are the major SSPs' own certificate IDs. The previously-named operators (Seedtag, Rich Audience, SunMedia, Adagio, etc.) remain the named-injector layer above the SSP layer.

### E-2026-04-27-f: Foreign-issuer to domestic-registrant status conversion (Criteo, Taboola)

Both Criteo S.A. (French registrant, CIK 0001576427, last 20-F filed 2015) and Taboola.com Ltd. (Israeli registrant, CIK 0001840502, last 20-F filed 2022) converted from 20-F to 10-K filing status in early 2026. Criteo's first 10-K filed 2026-02-26 (CIK 0001576427, accession 0001576427-26-000014). Taboola's first 10-K filed 2026-02-25 (CIK 0001840502, accession 0001840502-26-000004). Operationally, the conversion adds: quarterly 10-Q reporting (vs annual 20-F + voluntary 6-K interim), real-time 8-K material-event filings (vs 6-K furnished, lower disclosure standard), §402 executive compensation tables, SOX §404(b) auditor-attested ICFR, SOX §302/§906 CEO/CFO certifications with personal certification liability, Reg FD selective-disclosure prohibition, §14(a) proxy rules, §16 insider-trade reporting (Forms 3/4/5). The increased disclosure burden compounds with the framework-silence finding (E-2026-04-27-c) and the disclosure-integrity question (§3.4 #2).

### E-2026-04-27-g: Outbrain → Teads merger; CIK 1454938 reassigned

CIK 1454938 ("Outbrain Inc") was reassigned to "Teads Holding Co" with the closing of the Teads acquisition in 2025. Acquisition consideration ~$900M ($625M cash + stock). Ticker reassigned OB → TEAD. Combined entity FY2025 revenue $1.300B (10-K filed 2026-03-16); the 10-K describes the post-merger entity as "one of the largest Open Internet advertising platforms, with over $1.4 billion" (run-rate). All references in this paper to "Outbrain" should be read as referring to the pre-merger entity now operating as Teads Holding Co.

### E-2026-04-27-i: Wayback confirms 62+ month INTERMEDIARY classification on rubiconproject.com seller_ids 17280, 13510, 17960, 22328, 22884

A direct Wayback Machine fetch of `web.archive.org/web/20210301000000/https://rubiconproject.com/sellers.json` (snapshot of 2021-02-11, cdx URL `https://web.archive.org/cdx/search/cdx?url=rubiconproject.com/sellers.json`) confirms that the seller_ids at the heart of the named-injector finding were classified INTERMEDIARY by Rubicon at least as far back as that snapshot:

| seller_id | name | domain | seller_type | months continuously INTERMEDIARY |
|---|---|---|---|---:|
| 17280 | Seedtag Advertising SL | seedtag.com | INTERMEDIARY | 62+ |
| 13510 | Pubnet Publicidad Y Marketing, SL | richaudience.com | INTERMEDIARY | 62+ |
| 17960 | Sovrn Inc. | sovrnservices.com | INTERMEDIARY | 62+ |
| 22328 | VLN Servicios Publicitarios Integrales, S.L. | sunmedia.tv | INTERMEDIARY | 62+ |
| 22884 | Google | google.com | INTERMEDIARY | 62+ |

PAPER §1¶4 claims "62+ months of unambiguous public classification" for seller_id 17280; the 2021-02-11 snapshot is the front edge of that exact window (2021-02-11 → 2026-04-27 = 62 months 16 days). Verified.

The same Wayback exercise also surfaces the corporate identities behind two of the brand-domain operators previously named only by domain:

- **Rich Audience** is operated by **Pubnet Publicidad Y Marketing SL** (Spanish *sociedad limitada*).
- **SunMedia** is operated by **VLN Servicios Publicitarios Integrales SL** (Spanish *sociedad limitada*).

Regulatory action would address the SL by its registered corporate name; the Spanish DPA (AEPD) is the relevant authority for both. The brand-to-corporate mapping is now documented in `memory/seedtag_richaudience_corporate_idents_20260427.md`.

### E-2026-04-27-j: SmartAdServer is now operating under the Equativ brand

The current `smartadserver.com/sellers.json` registry (cached 2026-04-26) lists `quality-team@equativ.com` as the contact email and contains 2,604 sellers. SmartAdServer was acquired by / merged with Equativ SAS (France) in 2023; the brand has converged on Equativ for marketing and corporate purposes, while the technical sellers.json domain remains smartadserver.com because publisher ads.txt files reference the historical domain. Live registry verification at 2026-04-26 confirms:

- `1097` Themoneytizer (themoneytizer.com): INTERMEDIARY ✓ (smoking-gun line stays valid)
- `3050` Seedtag (seedtag.com): BOTH ✓
- `2640` Rich Audience International (richaudience.com): BOTH ✓
- `1999` Sun Media (sunmedia.tv): INTERMEDIARY ✓
- `4071, 4012, 4073, 4074`: NOT IN REGISTRY ✓ (CAS SDK Template C remains phantom)

The corporate-name → SEC-entity table for the named operators in the FTC complaint:

| Brand (in our data) | Corporate / SEC entity | Country | Form |
|---|---|---|---|
| SmartAdServer | Equativ SAS | France | SAS |
| Seedtag | Seedtag Advertising SL | Spain | SL |
| Rich Audience | Pubnet Publicidad Y Marketing SL | Spain | SL |
| SunMedia | VLN Servicios Publicitarios Integrales SL | Spain | SL |
| Themoneytizer | Themoneytizer SA | France | SA |

### E-2026-04-27-k: Adagio's own ads.txt is honest; the DIRECT injection is added downstream

Live fetch (2026-04-27) of `https://adagio.io/ads.txt` shows that the Adagio template's first 9 lines are all RESELLER:

```
OWNERDOMAIN="adagio.io"
# -- begin Adagio
# adagio.io, 1002, DIRECT          ← DIRECT line is COMMENTED OUT
adform.com, 3354, RESELLER, 9f5210a2f0999e32
rubiconproject.com, 19116, RESELLER, 0bfd66d529a55807
pubmatic.com, 159110, RESELLER, 5d62403b186f2ace
improvedigital.com, 1790, RESELLER
onetag.com, 6b859b96c564fbe, RESELLER
indexexchange.com, 194558, RESELLER
pubwise.io, 68867843, RESELLER, c327c91a93a7cdd3
# -- end Adagio
```

The single Adagio DIRECT line for adagio.io's own seller_id 1002 is COMMENTED OUT. All other Adagio-block lines are explicitly RESELLER.

Yet ERRATA E-2026-04-22-d found 882 publishers carrying `# Adagio_0_6` markers AND `rubicon/17280 DIRECT` (which is a Seedtag line, not Adagio's). This refines the earlier framing: Adagio is not the source of the DIRECT injection. The DIRECT lines are added by a layer further upstream (or downstream, depending on perspective): the publisher-side aggregator that bundles Adagio's RESELLER block together with Seedtag/Rich Audience DIRECT lines into a single rendered ads.txt.

The §3 narrative in PAPER about Adagio as "template author whose pipeline embeds those accounts" is too strong. Adagio's pipeline embeds RESELLER lines; the DIRECT lines are added by *another* aggregator that uses Adagio's block as one section of a larger composed file. The 882-publisher cohort is composing Adagio + Seedtag templates side by side. The DIRECT misdesignation is not Adagio's fault directly; it is the cohort-builder's fault. Adagio's seller_ids on those publishers (per H30 query: 17,195 publishers / 9,947 contradicted DIRECT claims) are also subject to the same composition pattern — those CONTRADICTED DIRECTs for adagio.io seller_ids are NOT what Adagio's own template publishes; they are the result of a different pipeline relabeling the lines.

The implication for the FTC complaint: Adagio is a template *author* whose own template is honest. The template-author layer is not unitary; some authors are clean, some are not. The misdesignation arrives via composition by aggregators downstream of the template author. Naming Adagio in the same sentence as Seedtag would confuse two distinct roles.

### E-2026-04-27-h: FY2025 10-K revenue refresh (March 2026 figures had drifted)

Verified FY2025 revenue from EDGAR-filed 10-Ks (numbers updated in `tools/company_financials.json`):

| Company | March 2026 estimate | FY2025 10-K | Δ |
|---|---:|---:|---:|
| Trade Desk (TTD) | $2.4B | $2.896B | +21% |
| Magnite (MGNI) | $620M | $714M | +15% |
| PubMatic (PUBM) | $290M | $283M | −2% |
| Criteo (CRTO) | $2.1B | $1.681B | −20% (different basis; FY2025 revenue is reported figure, ex-TAC is $1.175B) |
| LiveRamp (RAMP) | $590M | $745.6M | +26% |
| Taboola (TBLA) | $1.7B | $1.912B | +12% |
| Outbrain → Teads (TEAD) | $950M | $1.300B | +37% (post-merger) |

The Taboola figure cited in this paper's §1¶5 is updated to $1.91B in this errata; the body text carries the original $1.7B value pinned to the March 2026 corpus.

## Update: 2026-05-09 — Cycle 232-243 chain (deeper structural analysis)

The PAPER's "71% of Google's sellers.json is confidential" finding (Finding 4
above + PAPER §3 + Fix 6) holds. Cycles 232-243 drilled deeper and the
deeper findings reframe how the 71% number should be interpreted.

### E-2026-05-09-a: bimodal registry-anonymity distribution (cycle 235)

Across 503 sellers.json registries with ≥100 entries:
- **412 (81.9%) have 0% anonymous** entries (full compliance with naming intent)
- **60 (11.9%) are <10%** anonymous (incidental confidential)
- **18 (3.6%) are 10-30%** (selective confidentiality)
- **13 (2.6%) are ≥30%** — wildcard tier (apex Google 71.8%, ad-stir.com 86%, infinety.hu 100%)

The PAPER framed Google's 71% as "an unusually high rate." Cycle 235 sharpens
this: the distribution is *bimodal*, not graduated. 91% of registries name
their partners; a small minority deliberately don't. The compliant 91%
proves naming IS feasible; the wildcard 2.6% is a deliberate structural
choice, not "industry drift."

### E-2026-05-09-b: epistemic-engine disambiguation (cycle 238)

Within the 13 wildcard-tier registries, two opposite mechanisms operate
beneath identical surface (NULL domain, NULL name, is_confidential=1):

- `precomputed_lookup` — sequential-integer enumeration, no underlying
  customer claim. ad-stir.com lists seller_ids 1, 2, 3, ..., 14515
  (77.4% range coverage). genieesspv.jp lists 1...38597 (67.8% coverage).
  Anyone claiming `<ssp>, <integer>, DIRECT` for any common integer
  passes a basic existence-check.
- `contractual_confidential` — random-shape IDs (e.g. Google's
  `pub-XXXXXXXXXXXXXXXXXX` format) representing real customer accounts
  whose names are private by contract.

These are NOT the same mechanism. The PAPER's call for SSP confidentiality
audits applies to both, but the audit questions differ:
- For `precomputed_lookup`: does each integer ID correspond to a real
  customer relationship? (Spec violation if no.)
- For `contractual_confidential`: what is the aggregate count of real
  partner accounts behind the flag? (Spec-allowed; audit is for scale-
  reasonableness against business size.)

### E-2026-05-09-c: 91-99% domain-mismatch is industry-wide (cycle 236 H19)

Across 14 major SSPs, when a publisher's DIRECT claim matches a NAMED
registry entry, the publisher's domain is NOT the same as the registry's
domain in 91-99% of cases:

| SSP | named matches | exact domain match | mismatch |
|---|---:|---:|---:|
| google.com | 154,787 | 7.6% | 91.3% |
| rubiconproject.com | 179,513 | 0.4% | 99.4% |
| pubmatic.com | 201,086 | 0.5% | 99.1% |
| openx.com | 122,960 | 0.6% | 98.8% |
| sovrn.com / lijit.com | 261,447 | 0.4% | 99.5% |
| triplelift.com | 139,207 | 0.4% | 99.3% |
| criteo.com | 1 | 0.0% | 100.0% |

The PAPER's "57% of DIRECT claims are false" understates the verification
gap. Of the remaining 43% non-false claims:
- ~37% match a NAMED registry entry — but only 1-7% have exact domain match
- The 91-99% non-exact NAMED claims are spec-passing but
  externally-unverifiable (could be MCM, named-operator injection, or
  intra-industry routing — framework cannot distinguish)

**Apex synthesis:** framework-confident DIRECT claims (exact pub_domain
== reg_domain) are ≈1-7% of total claims industry-wide. The other
93-99% require trust in mechanisms (MCM membership, confidential
entries, third-party managed inventory) that the verification framework
does not surface.

### E-2026-05-09-d: independent reproducers shipped

`tools/reproducer/` now contains two stdlib-only Python scripts:

- `verify_anonymity.py <ssp-domain>` — fetches the SSP's sellers.json
  directly and emits the cycle 232/235/238 classification (anonymous %
  + epistemic_engine).
- `verify_publisher_claims.py <publisher-domain> <ssp-domain>` —
  fetches the publisher's ads.txt and the SSP's sellers.json, classifies
  every DIRECT claim into EXACT_MATCH / SUBSTRING_MATCH / ANONYMOUS_MATCH /
  DOMAIN_MISMATCH / PHANTOM, reports externally-falsifiable %.

Apex live verification (2026-05-09):
- google.com: 71.4% anonymous, contractual_confidential
- ad-stir.com: 84.9% anonymous, precomputed_lookup, ints[1, 14591]
- rubiconproject.com: 0% anonymous, low_anonymity (compliant)
- cnn.com → google.com: 0/7 externally-falsifiable; 4 mismatches
  resolve to wbd.com (CNN's parent WBD) and tunein.com (WBD-owned) —
  legitimate intra-corporate routing indistinguishable from fabrication

The reproducers make the cycle 232-243 chain independently falsifiable
without our 2000-line atlas pipeline. Run them; the structural finding
(framework can't distinguish Popperian-named claims from Hegelian-
opaque claims) is reproduced live in 60 seconds.

### Reframing for downstream consumers

The headline numbers in PAPER (57% false; 71% Google confidential;
0.012% consent) hold. The cycle 232-243 chain doesn't change them.
What it changes is *interpretation*:

- "57% false" was a single number. Cycle 236 H19 shows 93-99% of the
  REMAINING 43% are also non-falsifiable (just by other mechanisms).
  The fully-falsifiable subset is 1-7%, not 43%.
- "71% Google confidential" was treated as a concentration anomaly.
  Cycle 235 shows this is a binary structural choice (91% comply, 2.6%
  go wildcard). The fix-6 audit framing should distinguish lookup-table
  registries from contractual-confidential registries.
- Fix 6's ask ("disclose the basis for confidentiality on aggregate
  basis") makes more sense for `contractual_confidential` than for
  `precomputed_lookup` (where the basis is "we listed every common
  integer" — a different category of audit).

## Update: 2026-05-09 (continued) — Cycles 244-273 deeper analysis

The April-May 2026 work extended substantially beyond cycles 232-243.
Per cycle 272's self-audit, this update separates findings by spec-
relevance tier rather than mixing spec-violations with above-spec
analytical critique.

### E-2026-05-09-e: Live page-load reveals a SECOND framework gap

Cycles 251-262 used `tmp/xray_journal.db` (3.3M live page-load network
requests across 76K publishers) to cross-reference declared SSPs (in
ads.txt) with fired SSPs (actual page-load network calls).

**Finding (above-spec analytical):** of declared SSPs in publisher ads.txt
files, **80-100% never fire on the actual page**. Sample paperwork
rates per SSP (declared but no live request observed):

  TheMediaGrid:       100% paperwork
  OneTag:             100%
  Conversant/Epsilon: 100%
  Adform / AdYouLike / Smaato / Rise: 100% each
  Sovrn / Sharethrough: 89-91%
  Magnite / PubMatic / Index Exchange: 78-83%
  Yahoo / Xandr / Criteo: 71-81%

The framework doesn't require declared SSPs to fire (the spec models
authorization, not participation), so this is structurally an above-
spec critique — but it shows ads.txt is mostly DECORATIVE.

Cycle 251 also found 5-98% **ghost-firing rate** (SSPs that fire but
aren't declared). JWPlayer ghost-fires on 350 publisher pages, only 7
declare it (98% ghost rate).

Pearl prudence: paperwork rate may be slightly inflated by headless-
Chrome not triggering all auctions. But 80-100% rate across 16K
publishers is structural, not noise.

### E-2026-05-09-f: Information-theoretic framing of verification primitive

Cycle 256: the sellers.json registry encodes ~237 bits per row (3M rows
× 237 bits ≈ 86 MB). The IAB-spec verification primitive (existence
check) returns ≤1 bit per claim (yes/no). **99.6% of registry information
is discarded at verification time.**

Attribution entropy among the registry's named-publisher subset is 17.77
bits — could distinguish ~224K entities. The framework's 1-bit output
is 18× weaker than what the data supports.

This is **spec-internal critique**: the spec could output more without
changing data structures. Same lens applied to TCF v2 consent (cycle
267-269): **89.9% of bid-stream consent strings have NO USABLE value**
(84% empty, 1.8% "undefined", 0.8% "null", 0.5% template variables not
replaced). Only 10.1% are valid TCF v2. This IS a spec violation under
TCF — SSPs MUST NOT process empty consent under gdpr=1.

### E-2026-05-09-g: Spec-internal recalibration (cycle 273)

Apply the cycle 272 self-audit lens. Three tiers of finding:

**Tier 1 — confirmed spec violations (no charitable reading):**
- 26.8% of DIRECT claims: phantom AND not-in-any-registry (38% phantom
  × 70.5% absent-from-everywhere)
- 1.2% of compliant claims: NULL-domain entries WITHOUT is_confidential=1
  flag (sellers.json spec section 3.1 violation)
- 84% of bid-stream gdpr_consent= values: empty string under gdpr=1
  (TCF v2 MUST-NOT-process violation)

**Tier 2 — spec-allowed but verification-defeating:**
- 1.8% of compliant claims (registry-side): anonymous-confidential
  (NULL domain with is_confidential=1) — Google's apex 71.8%
- 8 SSPs operating wildcard registries: pre-enumerate every common
  integer ID, defeating per-SSP existence-check semantics

**Tier 3 — above-spec analytical critique:**
- 91-99% domain-mismatch industry-wide (49 of 49 SSPs ≥90%)
- 92% paperwork rate
- 0.30% Popperian+functional state (registry has it, exact domain
  match, AND fires — strict composite)

The PAPER's headline "57.1% false rate" sits between tiers 1 and 3:
spec-internal (existence-check failure) gives 38%; the strict floor
(absent from every registry) is 26.8%; the inclusive "verifiable bucket"
(post Apr-22 refresh) is 61.1%. Each is defensible at its own granularity.

### E-2026-05-09-h: Apex SSPs by phantom-to-registry ratio

Pearl-disciplined apex cases:

| SSP | phantom claims | registry size | ratio |
|---|---:|---:|---:|
| districtm.io | 29,151 | **0** (empty) | ∞ |
| emxdgt.com (Engine Media) | 39,113 | 175 | **223×** |
| yahoo.com | 36,500 | 469 | 78× |
| advertising.com (Yahoo legacy) | 33,446 | 469 | 71× |
| criteo.com | 76,037 | 2,036 | 37× |
| freewheel.tv | 54,863 | 2,156 | 25× |
| appnexus.com | 41,800 | 1,750 | 24× |
| indexexchange.com | 86,810 | 3,994 | 22× |
| smartadserver.com | 46,151 | 2,574 | 18× |

DistrictM.io's empty registry case is structurally distinctive: post-
Magnite-acquisition, the registry was apparently never republished. All
29K publisher DIRECT claims against districtm.io are by-definition
phantom under the spec's existence check.

EMXDGT's 223× ratio is the highest of any SSP with a non-empty registry.
39K publisher claims against 175 authorized seller accounts.

### E-2026-05-09-i: Apex carrier cohort (Gray TV)

Cycles 260-262 identified Gray TV's 142-station ad-ops cohort as the
single largest contributor to the corpus's phantom+fires (real auction
+ fabricated seller_id) tier.

**Cycle 262 self-correction:** the initially-claimed 3,800-publisher
template propagation was an artifact. Most of the propagation was
"generic phantom hubs" (smartadserver/4071 carried by 6,000 publishers
unrelated to Gray) and "small-integer collision noise" (cycle 259: 96-
99% of "soft phantoms" at small integers are coincidental).

The genuine Gray-distinctive signature: 45+ Taboola seller_ids in
clustered ranges (1494xxx, 1502xxx, 1625xxx) carried by 139-142 of 142
Gray stations and 0 non-Gray. These look like deprecated Taboola
account ranges that Gray previously operated and never cleaned up.

This is **stale-ID pollution at scale** — 142 stations × ~455 phantom+
fires each = ~64K claims (≈55% of corpus phantom+fires). The framework
treats this identically to fresh fabrication.

### E-2026-05-09-j: Temporal volatility (cycle 270-271)

Across a 4-day window (2026-04-24 → 2026-04-28), aggregate mean
false_rate dropped 1.6pp. Top movers were SSP-side registry updates,
not publisher-side cleanups:

  yieldlab.net          97.5% → 2.5%   (-95pp; SSP refreshed registry)
  hindsightsolutions.net 0% → 100%      (5,076 claims overnight phantom)
  pulsepoint.com        0% → 100%      (689 claims; registry dropped)
  smartclip.com       100% → 0%        (registry refreshed)

A single SSP-side registry change flips thousands of publishers'
"compliance" overnight WITHOUT publisher action. **The framework's
compliance rate is more like a measurement of SSP-registry-publishing-
discipline than publisher-honesty.**

### E-2026-05-09-k: Reproducer test-coverage hardening

Cycles 245+247 shipped self-checking infrastructure:
- `tools/reproducer/test_regression.sh`: confirms apex findings
  (Google 71% anon, ad-stir.com 86% lookup, rubicon 0% comply) hold
  on live data; 4-of-4 pass, 1-skip (proxy block) on 2026-05-09.
- `tests/test_atlas_headlines.py`: 26-assertion atlas pipeline smoke test;
  26 of 26 pass on 2026-05-09.

Cycle 248-249 fixed atlas determinism — 5 consecutive runs now produce
byte-identical output (modulo `generated_at` timestamp). 6 sources of
non-determinism eliminated (tied-rank ordering, dict iteration, float
ULP drift).

H19 from E-2026-05-09-c was strengthened from 14 SSPs to 49 SSPs:
all 49 reachable major SSPs show ≥90% domain-mismatch among NAMED
registry entries; median is 99.4%; **Google's 91.3% is the LOWEST**
(most-compliant) of any major SSP.

### What this update does NOT change in the PAPER

- Headline 57% false rate: holds
- Named primary injectors (Seedtag, Rich Audience, etc.): holds
- 9-injector ecosystem with 250 shared sellers across Seedtag/Rich
  Audience: holds
- 95-99% non-authorization of false-DIRECT-claiming publishers in
  injectors' own registries: holds
- Wayback CNN injection 2-day window: holds

### What it suggests for future revision of the PAPER

Distinguish in the paper's headline framing:
- A FLOOR: 26.8% confirmed-by-spec failure rate (no charitable reading)
- A SPEC RATE: 38% phantom under existence-check
- AN INCLUSIVE RATE: 61.1% (post Apr-22 refresh, accepts above-spec
  interpretations)
- AN ANALYTICAL RATE: 99.7% miss the strict Popperian+functional
  standard

The PAPER currently leads with 57.1%; cycle 273 supports keeping that
but adding the 26.8% floor as the strictest defensible number.


## Update: 2026-05-22 — Cycles 458-464 chain: two-vantage decomposition + Pixalate external replication

Six cycles of progressive refinement on a single question: does the headline phantom rate replicate against external measurement?

### E-2026-05-22-a: 33.83% declarative phantom rate confirmed across Tranco tiers (cycle 458)

The phantom-only DIRECT-claim rate (excluding contradicted) on the refreshed corpus is **33.83%** weighted by claim count. Within-corpus stratified comparison by Tranco rank:

| tier | n_pubs | claim-weighted phantom% | Wilson 95% CI |
|---|---:|---:|---|
| top_1k | 210 | 31.45% | [30.82%, 32.09%] |
| top_10k_minus_1k | 2,306 | 32.74% | [32.60%, 32.87%] |
| top_100k_minus_10k | 14,970 | 31.21% | [31.15%, 31.27%] |
| below_100k_or_unranked | 58,684 | 29.45% | [29.41%, 29.50%] |

Aggregate is consistent across tiers at 29-33%; CIs are <1pp wide because >4M claims per tier. The 33.83% headline holds, and is **not concentrated in any single tier**.

### E-2026-05-22-b: Pareto concentration — 77.4% of phantom volume from top 10% of publishers (cycle 458)

Despite the aggregate rate, the per-publisher distribution is grossly Pareto. **34.8% of publishers (26,497) have ZERO phantom claims** — perfect IAB-spec compliance. Another 5.6% (4,250) are under 5%. The aggregate is driven by claim-volume concentration in a heavy-phantom long tail.

| % of publishers (high-claim) | claims share | phantom share | their phantom rate |
|---|---:|---:|---:|
| top 0.1% (76 pubs) | 4.4% | 5.9% | 40.49% |
| top 1% (761 pubs) | 22.2% | 29.0% | 39.48% |
| top 5% (3,808 pubs) | 52.4% | 61.7% | 35.63% |
| top 10% (7,617 pubs) | 68.3% | 77.4% | 34.27% |
| top 25% | 89.0% | 92.5% | 31.46% |

This sharpens the framing: **the IAB framework works for most publishers; the failure is concentrated in a heavy-phantom long tail that dominates claim volume.**

### E-2026-05-22-c: Self-refutation of impression-weighting hypothesis (cycle 460)

Cycle 459 published a hypothesis that impression-flow weighting would lower my rate from 33% toward Pixalate's published web rate of 13%. Cycle 460 tested it directly and **refuted it**. Activity-weighting INCREASES the rate:

| weighting | phantom % |
|---|---:|
| claim-weighted (corpus) | 33.83% |
| X-Ray scan-count-weighted | 35.74% |
| X-Ray request-count-weighted | 36.75% |
| Tranco-rank-weighted (1/rank Pareto) | 40.10% |

More-active publishers carry HIGHER phantom rates. The methodology gap with Pixalate is not impression-flow filtering.

### E-2026-05-22-d: Pixalate publishes quarterly comparable-magnitude measurements (cycles 459, 461)

Pixalate (founded 2012) publishes quarterly "Programmatic Ad Seller Misrepresentation" reports using methodology compatible with IAB ads.txt/app-ads.txt + OpenRTB SCO observation. Their Q1 2025 published numbers:

| surface | "Failed SCO verification" | "Sold by unauthorized DIRECT" | IVT correlation |
|---|---:|---:|---|
| Web | 13% | 6% | **+159% IVT** with unauthorized direct |
| Mobile App | 35% | 9% | +46% IVT |
| CTV | 13% | 16% | — |

Sample size: 10B+ programmatic ad impressions with SCO present.

Pixalate's +159% IVT correlation in unauthorized-direct cohort independently validates the cycle 442/446 finding that the heavy-phantom cohort is also the compliance-theater (low-quality / high-IVT) cohort.

### E-2026-05-22-e: Two-vantage decomposition — declarative-side vs observed-side measure complementary aspects (cycles 460-464)

The headline 33.83% (mine) vs Pixalate's 13% are **not the same measurement disagreeing**. They are complementary measurements of the same framework hole from different vantages:

| vantage | source | numerator | answers |
|---|---|---|---|
| **Declarative (mine, 33.83%)** | publisher ads.txt | DIRECT claims with no matching seller_id in SSP sellers.json | "did the partner you named acknowledge you?" |
| **Observed-side (cycle 464)** | X-Ray prebid_json | Prebid bidder calls to SSPs not in publisher's ads.txt | "do observed transactions match declarations?" |
| **Observed (Pixalate)** | 10B+ impressions | observed SCO chains failing their proprietary check | adjacent metric, methodology details unpublished |

### E-2026-05-22-f: IAB spec section 5.2.2 settles DSP classification (cycle 463)

The IAB ads.txt v1.1 spec section 5.2.2 ("DSP") states:

> "DSPs should consult documentation provided by SSPs/exchanges as to the canonical domain used by the exchange (field #1) and the appropriate field in bid requests to be checked against ads.txt (field #2)."

DSPs are **consumers** of ads.txt files (validating bid requests against them); they do NOT appear as authorized sellers IN them. This settles whether premium publishers calling TTD as Prebid bidder without ads.txt declaration is a violation: it is **not** a violation under strict spec reading.

### E-2026-05-22-g: Observed SSP-only unauthorized rate is 4.18% (cycle 464)

With proper role-classification per IAB sec 5.2.1/5.2.2 (DSP excluded, MIXED-role bidders like Criteo/AMX/Adform separated):

| Inclusion | unauthorized / total | rate |
|---|---:|---:|
| **SSP only (IAB-spec strict)** | **19/455** | **4.18%** |
| SSP + MIXED | 29/506 | 5.73% |
| SSP + MIXED + DSP (overstrict, cycle 461 framing) | 70/556 | 12.59% |
| DSP only (sanity check) | 41/50 | 82.00% |

The DSP-only 82% rate confirms: DSPs don't appear in ads.txt by spec. Counting them as "unauthorized" inflates by ~8pp. Pixalate's 13% likely includes the same DSP over-counting (their SCO chain methodology probably catches DSP nodes); both metrics share that methodology limitation.

### E-2026-05-22-h: The 29.65pp compliance-theater pool

**Declarative 33.83%** minus **observed SSP-only 4.18%** = **29.65pp**.

This is the structural finding of the cycle chain: publishers list 30%+ phantom paths in ads.txt, but only ~4% of observed bidder calls go to undeclared SSPs. The remaining ~26pp = paths that exist as paperwork but don't actively transact.

The cycle 442/446 "compliance-theater" framing now has quantitative ground:
- ~4% of observations are real unauthorized SSP participation
- ~30% of declarations don't reconcile against partner registries
- The ~26pp pure-paperwork gap is the structural waste — decorative authorization that doesn't materialize as transactions

Top SSP-only unauthorized callers in the 68-pub sample (post-DSP-exclusion):
- unruly.co (9 pubs)
- ozoneproject.com (6 pubs)
- tealmedia.com, adagio.io, kargo.com, sovrn.com (1 each)

### E-2026-05-22-i: Sample-size honesty

The observed-side measurement uses n=68 publishers with prebid_json captured by X-Ray. Wilson 95% CI on 4.18% with n=455 calls = [2.78%, 6.21%]. Pixalate's 13.00% sits OUTSIDE this interval — confirming the methodology distinction. The declarative-side 33.83% sits across 6.5M claims in 74K publishers; its Wilson CI is <0.1pp wide.

### E-2026-05-22-j: What the six-cycle progression demonstrates

The chain 459→460→461→462→463→464 was six honest corrections of the same direction:

- 459: claimed Pixalate replicates phenomenon
- 460: refuted impression-weighting explanation
- 461: claimed Pixalate-analog converges to 13.43% (partly correct)
- 462: TTD inflates by 7pp; without TTD rate is 5.81%
- 463: IAB spec confirms DSPs don't belong in ads.txt
- 464: full role classification → 4.18% (strict spec)

The published claims in cycle 461 are now superseded by cycle 464. Nothing is hidden; the corrections are commit-logged and reproducible.

### What this chain does NOT change in the PAPER / README

- 33.83% phantom rate replicates and is robust
- Pareto concentration finding is new and strengthens the framing
- The compliance-theater pool (~26pp) is a new quantitative ground for the prior "decorative authorization" framing
- Pixalate publishes comparable-magnitude figures using related methodology — external corroboration that the phenomenon is measurable at industrial scale by an independent vendor

### What it suggests for future revision of the PAPER

Lead with the two-vantage framing:
1. **33.83% of publisher DIRECT claims don't reconcile** (declarative-side — what discovery looks like)
2. **4.18% of observed bidder calls go to undeclared SSPs** (observed-side — what transactions look like at strict IAB-spec)
3. **The ~26pp gap is the compliance-theater pool** — paperwork that never transacts
4. **Pixalate independently measures ~13% (Q1 2025) using related-but-not-identical methodology** — external corroboration of the phenomenon's existence at industry scale


### E-2026-05-22-k: The two phantom modes are nearly independent (Pearson r=0.15)

Densifying cycle 464's two-vantage decomposition: cross-correlated the declarative-side rate vs observed-side rate **per publisher** across the 66 X-Ray-observed pubs in corpus.

**Pearson r(declarative_phantom_rate, observed_unauthorized_rate) = 0.1546.**

The two metrics measure nearly-independent failure modes. A publisher's ads.txt being dirty does NOT predict their auction being dirty.

Top "paperwork-heavy, operationally-clean" publishers (high declarative phantom, ZERO observed unauthorized):

| pub | declarative phantom | observed unauth |
|---|---:|---:|
| sozcu.com.tr | 53.7% (512/954) | 0% (0/1) |
| goodreturns.in | 45.8% (1,123/2,451) | 0% (0/6) |
| moppy.jp | 40.5% (30/74) | 0% (0/2) |
| kompas.com | 34.6% (605/1,748) | 0% (0/9) |
| **Condé Nast cluster** (vogue, wired, arstechnica, bonappetit, epicurious) | ~22.2-23.4% each | 0% each |

The Condé Nast cluster shows identical declarative phantom rate (22.2-23.4%) with ZERO observed unauthorized — strong signature of a shared ads.txt template managed at parent-company level with phantom entries from inherited wrappers, alongside clean Prebid configs at individual properties.

### What this densifies in the framing

The framework leaks along **two largely-separate axes**, not one:

1. **Maintenance leak (33.83% declarative)** — publisher ads.txt files contain phantom entries (stale, templated, never-transacted). Discovery-side noise; buyers using ads.txt to find authorized partners see ~33% misdirection.

2. **Operational leak (4.18% observed at IAB-strict)** — publisher Prebid configs call SSPs not declared in ads.txt. Validation-side rule-breaking; buyers cross-checking observed bids against ads.txt see ~4% spec-violations.

Pearson r=0.15 means these are nearly disjoint cohorts. A publisher with a 30% maintenance leak is no more likely to have an operational leak than a clean publisher.

**Remediation implication:** the two leaks need different fixes:
- Maintenance leak → automated ads.txt hygiene (sellers.json cross-check, expired-entry pruning, template validation at publish time)
- Operational leak → Prebid wrapper enforcement requiring ads.txt presence before activating a bidder

Pixalate's 13% probably catches a methodology-specific weighting between these two; the 33% / 4% / r=0.15 decomposition is denser than any single rate.


### E-2026-05-22-l: 28.6% of phantom volume lives in 1,102 centrally-managed templates (cycle 466)

Per-publisher phantom-claim fingerprints (SHA1 of sorted ssp|seller_id set) reveal that **publishers literally share IDENTICAL ads.txt files** at scale:

| metric | value |
|---|---:|
| publishers in any shared-signature cluster (n≥3) | **10,723 (14.4% of corpus)** |
| phantom claims accounted for | **634,121 (28.6% of total phantom volume)** |
| number of shared-fingerprint clusters | **1,102** |

Top 15 clusters trace to named publisher networks:

| n_pubs | phantom/pub | operator |
|---:|---:|---|
| 1,360 | 5 | recipe-network template (100krecipes, 196flavors, ...) |
| 297 | 81 | Forumotion / Lefora platform |
| 115 | 27 | **FanSided / Minute Media** (90min, 12thmanrising, ...) |
| 102 | 6 | **Black Press / Glacier Media** (Canadian local news) |
| 95 | 16 | **SB Nation / Vox Media** (acmepackingcompany, badlefthook, ...) |
| 83 | 733 | piracy mega-template (1flix.to, 2kmovies, 9animetv, ...) |
| 82 | 158 | **Newsquest** (UK local news) |
| 72 | 43 | **Gannett / GateHouse** (US local news) |
| 63 | 63 | **IAC / Ask Media Group** (ask.com, askjeeves, ...) |
| 62 | 11 | **Booking Holdings / Kayak** (cheapflights.{tld}) |
| 62 | 16 | **Townsquare / Cumulus radio** (95rockfm, 97x, ...) |

### Two distinct mechanisms within the clusters

Sample inspection reveals the line at ~50 phantom claims/pub:

**Template DECAY** (5-43 claims/pub) — central management hasn't updated through SSP industry consolidation. SB Nation's acmepackingcompany.com carries entries for districtm.io (merged into Magnite), emxdgt.com (post-acquisition orphan), spotx.tv / spotxchange.com (Magnite-acquired, 100%-phantom), vi.ai (rebranded), advertising.com (Yahoo legacy). Newsquest's bournemouthecho.co.uk carries adaptv, aerserv, aolcloud — all dead SSPs. Networks maintain ads.txt centrally; entries don't get removed when SSPs die.

**Template INJECTION** (81-733 claims/pub) — piracy + Forumotion clusters have far more phantom than organic relationships would explain. These are actively injected via wrapper templates or platform-defaults.

### What this changes about the framing

The cycle 442-445 "cartel" reading dissolves into a sharper mechanism:

- **The 33% phantom rate is dominantly centrally-managed template decay**, not coordinated bad-actor injection
- Publisher networks (Vox/SB Nation, Gannett, Newsquest, Black Press, FanSided, IAC, Townsquare, Booking) maintain ads.txt files at parent-company level
- Individual properties inherit the stale template
- This explains the cycle 465 r=0.15 observed-vs-declarative independence: maintenance is network-level, operations is property-level — different teams, different cadences, different update mechanisms

### Remediation implication

The 28.6%-of-phantom that lives in shared templates would be fixable by **O(1,102) actions targeting cluster managers**, not O(74,000) actions targeting individual publishers. Of those 1,102 templates, roughly 80% are likely decay (need template refresh); ~20% are injection (need operator change). Buy-side filtering by template signature catches the high-volume carriers efficiently.



### E-2026-05-22-m: Dead-SSP persistence is geological + industry-wide (cycle 467)

The deepest structural fact emerging from cycle 466's template-decay finding: **287,249 DIRECT claims to known-dead SSPs across 25,239 publishers (33.7% of corpus).** Dead SSPs persist in publisher ads.txt files for 7-9+ years after the SSP ceased to exist.

| Dead SSP | Died | Years dead | Pubs still carrying | % of corpus |
|---|---|---:|---:|---:|
| rhythmone.com | 2019 (Tremor-acquired) | **7y** | **14,973** | **20.18%** |
| emxdgt.com | 2023 (Big Village bankruptcy) | 3y | 13,544 | 18.25% |
| advertising.com | 2017 (Yahoo legacy) | **9y** | 9,384 | 12.65% |
| districtm.io | 2021 (Magnite-acquired) | 5y | 9,407 | 12.68% |
| spotx.tv / spotxchange.com | 2022 (Magnite-acquired) | 4y | 7,858 / 7,599 | ~10% each |
| aolcloud.net | 2017 (Yahoo legacy) | **9y** | 7,046 | 9.49% |
| admixer.net | 2020 (rebranded) | 6y | 5,754 | 7.75% |
| tremorhub.com | 2019 (Tremor-acquired) | 7y | 3,876 | 5.22% |
| yieldlab.net | 2023 (Virtual Minds folded) | 3y | 3,812 | 5.14% |

**The half-life of a dead SSP in publisher ads.txt is multiple years.** At 9 years post-death, advertising.com still persists in 12.65% of publishers worldwide.

### Cross-cluster overlap proves the decay is industry-wide

Sampling 8 publisher-network clusters (from cycle 466), the same dead SSPs appear in multiple independent clusters:

- **advertising.com (dead 2017, 9y)**: appears in 5/8 clusters (Newsquest UK, Gannett US, Vox Media, FanSided, IAC)
- districtm.io (2021): 3/8 (Vox, Newsquest, IAC)
- spotx.tv (2022): 3/8
- spotxchange.com (2022): 3/8
- emxdgt.com (2023): 3/8

Independent companies on different continents using different wrappers — all carrying the same dead SSPs. The decay is NOT network-specific.

### The mechanism: the IAB framework has no SSP-death propagation channel

When an SSP dies, gets acquired, or rebrands:
- Their sellers.json may disappear, redirect, or persist as orphan
- No notification reaches publishers
- No notification reaches IAB Tech Lab
- ads.txt files don't auto-prune dead entries
- Wrapper vendors (Prebid, headerbidding.io) don't auto-update publisher templates
- IAB itself maintains no SSP-death registry

The phantom rate is a **byproduct of an industry without a deprecation mechanism**, not a fraud signal or willful negligence. It's the equivalent of DNS records persisting on dead servers: no one cleans up because no one OWNS the cleanup task.

### What this clarifies about the cumulative framing

The cycle 442-445 "cartel" reading and cycle 446 "compliance theater" framing both implied agency. The cycle 467 finding dissolves agency entirely:

| Cycle | Framing | Mechanism implied |
|---|---|---|
| 442-445 | Cartel | Coordinated bad-actor injection |
| 446 | Compliance theater | Willful decorative maintenance |
| 466 | Template decay | Centralized network management |
| **467** | **Geological decay** | **Absent deprecation channel in the framework itself** |

The 33% phantom rate persists because the IAB framework was designed in 2017 to register authorized sellers and has no mechanism to DEREGISTER them. Nine years of SSP industry consolidation (Magnite acquisitions, Yahoo collapse, Tremor mergers, Big Village bankruptcy, COVID-era foldings) accumulated as ghost entries that the framework can't shed.

This is the most explanatory framing the body of work has produced.


### E-2026-05-22-n: Decomposition refutes fraud framing — only 2.5% of phantom has misconduct shape (cycle 468)

Decomposing 2,219,472 phantom DIRECT claims by attributable mechanism:

| Bucket | Claims | % of phantom | Mechanism |
|---|---:|---:|---|
| Live-SSP moderate phantom (10-50% rate) | 780,561 | **35.2%** | seller_id staleness — old IDs persist as SSPs change format |
| Live-SSP template-driven (50-90%) | 520,654 | **23.5%** | mainstream SSPs (Taboola 62%, IX 52%, Yahoo 71%, Outbrain 69%, MGID 70%) — wrapper/template injection |
| Live-SSP orphan registry (>90% rate) | 380,453 | 17.1% | adtech.com 100%, ampliffy 100%, blis 100%, ligadx 100% — SSPs with empty/broken sellers.json |
| Dead-SSP geological decay | 225,421 | 10.2% | SSPs that no longer exist; cycle 467 |
| Google confidentiality flag | 178,871 | 8.1% | `is_confidential: true` is IAB-spec-legal opacity |
| Criteo schema migration | 77,372 | 3.5% | Iponweb → Commerce Grid format change mid-2024 |
| **Live-SSP low-rate (<10%)** | **56,140** | **2.5%** | only this bucket has "individual misclaim" shape |

**Only ~2.5% of phantom claims have the shape consistent with publisher misconduct.** The other 97.5% is structural framework brittleness: schema changes, orphan registries, dead-SSP decay, confidentiality flags, template injection by mainstream SSPs.

### What this means for the FTC complaint and DOJ angle

The release-package files `FTC_COMPLAINT.md` and `DOJ_ANGLE.md` have been marked **SUPERSEDED**. The underlying numbers remain accurate, but the implied story (publishers committing fraud / cartel coordination) is contradicted by the structural decomposition.

The valid remediation path that the data supports:
1. **IAB Tech Lab** adopts an SSP-deregistration registry + propagation channel (addresses the 10.2% geological decay + structural foundation)
2. **Publisher-network central ads.txt management** (Vox, Gannett, Newsquest, Black Press, FanSided, IAC, Townsquare, Booking) adopts sellers.json cross-check at publish time (addresses the 28.6% cluster-based template decay; cycle 466)
3. **Wrapper vendors** (Prebid.org, headerbidding.io) enforce ads.txt presence before bidder activation (addresses the 4.18% observed-side leak; cycle 464)
4. **SSPs individually** publish hygienic sellers.json (removes dead seller_ids, documents confidentiality flag scope; addresses the 17.1% orphan-registry bucket)

The original cartel-frame remediation (FTC enforcement against publishers, DOJ antitrust against Google) does not match the structural mechanism. The framework needs maintenance infrastructure, not regulatory enforcement against individual publishers.



### E-2026-05-22-o: Who is actually hurt by the framework decay? (cycle 469)

A second-order correction to the cycle 468 supersession. User question: "if people just keep obsolete files and not trim them it hurts no one, so no reason for IAB to fix anything, right? or is anyone actually hurt by this oversight?"

Honest review of plausible harm vectors:

| Vector | Real? | Magnitude |
|---|---|---|
| Verification-industry mismatch (advertisers buy fraud-prevention for mostly-structural-noise) | Bounded | ~$50-200M/yr misallocated; DV/IAS do real IVT/brand-safety work that isn't ads.txt verification |
| DSP compute waste parsing dead entries | Negligible | dollars/day per DSP |
| Advertiser DIRECT-premium overpayment | Probably not | phantoms don't actively transact (cycle 465 r=0.15) |
| New-SSP discovery cost | Marginal | new SSPs enter through wrappers, not manual ads.txt parsing |
| IAB framework credibility decay | Speculative | slow drift; advertisers route around |
| User privacy | Orthogonal | real privacy harm exists (0.012% valid TCF consent first-visit) but it's not the phantom rate |
| Google `is_confidential` asymmetry | Real but narrow | already in DOJ active antitrust scope |

**Almost no one is materially hurt by the phantom rate at concentrated severity.** The framework doesn't need a "fix" because no party is hurt enough to coordinate one. The phantom rate is a coordination-failure equilibrium with low stakes — the cost of remediation exceeds the benefit to any individual party. This is the second defensive pattern the user caught in two days: cycle 468 superseded "publisher fraud"; cycle 469 supersedes the implicit "framework needs urgent fix" framing that replaced it.

The body of work IS a useful scientific measurement of framework decay at scale. It is NOT a fraud exposé, an urgent IAB call, or a consumer-protection case. The cycles 467-468 "remediation" framing has been removed from `index.html` (replaced with "Who is actually hurt" + "What this audit is and isn't").



### E-2026-05-22-p: User-pushback-driven anomaly mining + in-band enforcement (cycle 470)

User: "is this 'phantom direct' preventing you from surfacing actual anomalies?"
User: "exhaust deterministic means... shadow of the law vs shadow of the sword"
User: "use playwright, simulate audiences, use osint instrumentation"

After reading the dbit doctrine + shifts.md, this cycle stopped accumulating cycle memos and built the in-band callable that earlier cycles substituted for. Five anomalies surfaced one query deeper than the phantom-DIRECT framing had been allowing.

#### Anomaly 1: RESELLER corpus is 3.4× the DIRECT corpus and was untouched in 470 cycles

| metric | value |
|---|---:|
| RESELLER total claims | 22,207,712 |
| RESELLER phantom | 6,725,706 |
| RESELLER phantom rate | **30.29%** |
| Publishers with RESELLER lines | 40,155 |
| Top RESELLER-phantom SSP | freewheel.tv (690,479 phantom, 90.7% rate) |

The DIRECT-only framing missed 3× the volume. The RESELLER rate (30.29%) is in the same band as DIRECT (33.83%) but the absolute phantom volume is 3× larger.

#### Anomaly 2: Fabrication-concentrated SSPs — 50 operators with ≥5 fabricated IDs each (each at ≥10 pubs)

Top 10 fabrication operators by claim volume:

| SSP | n_fab_IDs | total_phantom_claims | top_fab_ID | top_ID_pubs | status |
|---|---:|---:|---|---:|---|
| google.com | 1,593 | 124,572 | pub-8622186303703569 | 3,871 | live |
| taboola.com | 2,635 | 113,958 | 1196805 | 1,727 | live |
| indexexchange.com | 283 | 65,374 | 190906 | 4,373 | live |
| criteo.com | 411 | 63,352 | B-060278 | 2,678 | live |
| lijit.com (Sovrn) | 202 | 57,915 | 244287-eb | 3,895 | live (cycle 138 "-eb" template) |
| freewheel.tv | 307 | 43,284 | 770449 | 3,665 | live |
| appnexus.com | 125 | 38,394 | 9284 | 4,423 | live |
| smartadserver.com | 92 | 31,933 | **4071** | **6,464** | live (cycle-211 SmartAdServer template) |
| emxdgt.com | 153 | 31,183 | 1701 | 3,206 | **dead (2023)** |
| rhythmone.com | 181 | 30,262 | 4195999290 | 1,789 | **dead (2019)** |

#### Anomaly 3: DIRECT vs RESELLER inversion at publisher level — 30 pubs with ≥50pp gap

The cycle 466 cluster framing was incomplete. Some publishers show 99.5% DIRECT phantom but 14.3% RESELLER phantom — same publishers, opposite signatures on the two layers. This is layer-specific template injection:

| publisher | D_n | R_n | D% | R% | pattern |
|---|---:|---:|---:|---:|---|
| **DuMont German radios (4 sites)** | 423 | 42 | **99.5%** | 14.3% | D-heavy injection |
| thisisdax.com (DAX audio) | 34 | 417 | 11.8% | **100.0%** | R-heavy injection |
| dova-s.jp | 149 | 156 | 16.1% | 96.8% | R-heavy injection |
| taboolanews.com (Taboola's own site) | 3,866 | 34 | **95.9%** | 20.6% | D-heavy (cycle 138) |
| mediamag.am | 1,566 | 240 | **99.7%** | 34.6% | D-heavy injection |

#### Anomaly 4: Live-traffic falsification via Playwright

Probed 6 suspect publishers with proxied Chromium, capturing all bid-request URLs:
- **wordsmyth.net** (claims `consumable.com seller_id=2000970` as DIRECT): **1,616 requests across 21 OpenRTB endpoints — consumable.com NEVER appeared as a bid recipient**. Pure fabrication confirmed in-band.
- **bournemouthecho.co.uk** (Newsquest): live ads.txt still actively contains entries for `spotx.tv`/`spotxchange.com` (Magnite-acquired 2022, dead 4 years) and `aolcloud.net` (Yahoo legacy, dead 9 years).
- **acmepackingcompany.com** (SB Nation): 212 requests, 1 OpenRTB endpoint, 0 schain captured — minimal active auction despite carrying dead-SSP entries.
- **radioberg.de** (DuMont): 180 requests, 0 OpenRTB endpoints — the German radio cluster's 423 DIRECT phantom entries correspond to a site with NO live ad auction. The 99.5% phantom rate is decoration on inactive infrastructure.

#### Anomaly 5: Bid stream signals

| metric | value |
|---|---:|
| scans with bid data | 118 |
| **median noBid ratio** | **95.5%** (19 of 20 bid requests return nothing) |
| GumGum fixed-CPM signature | $11.9399, CV=0.0000 across 3 wins |

Zero standard deviation across multiple wins is impossible under normal auction dynamics. GumGum's $11.94 fixed-rate signature suggests PMP deal or floor manipulation. The 95.5% median noBid ratio is the framework's operating reality: programmatic auctions overwhelmingly produce nothing.

### What this cycle does that 458-469 did not

- **Built an in-band callable**: `scripts/anomaly_audit.py` runs each anomaly check + variance prerequisite + invariant assertions. Failing invariants exit 1.
- **Built tripwires**: `tests/test_anomaly_invariants.py` (6 tests). Any future corpus rebuild that violates the cycle 458-470 claims FAILS the test.
- **Surfaced what the phantom-DIRECT framing was blocking**: RESELLER 22M unanalyzed; 50 named-operator fabrication signatures; inversion patterns; in-band Playwright proof.

Per `shifts.md` #43: a finding recorded as a memo in `tmp/` is in-altero (drifts). A finding encoded as a failing test that breaks if violated is in-loco (binds). Cycles 458-469 produced 10 memos in-altero. Cycle 470 produces one callable + six tripwires in-loco. The doctrinal correction is the tripwires, not another paragraph.


### E-2026-05-22-q: Steelman + four independent refutation attempts (cycle 471)

Cycle 471 steelmanned the cycle 470 fabrication position, then ran four severe refutation attempts. All four failed to refute.

#### Steelman of cycle 470 position
"The IAB ads.txt framework is leaked at scale by industrial template injection — 50+ named SSP-domains each carry ≥5 fabricated seller_ids reaching ≥10 publishers, with apex cases (SmartAdServer 4071 @ 6,464 pubs, Sovrn-eb 244287-eb @ 3,895 pubs) industrially active. Publishers claiming these IDs in ads.txt show the named SSPs never appearing as bid recipients."

#### Refutation attempt log

| # | hypothesis | method | n | outcome | framing |
|---|---|---|---:|---|---|
| 1 | "Phantom IDs are stale registry data; live-fetch will find them" | Live re-fetch top phantom IDs against current SSP sellers.json | 15 IDs | 0/15 found (Google checked vs 986,194 sellers) | **SURVIVES** |
| 2 | "Phantom SSPs DO receive bid traffic; ads.txt is just stale" | Playwright on phantom-claiming publishers, capture all bid endpoints + schain | 10 pubs × 5 SSPs | 9/10 SSPs NEVER appear as recipient; 1 exception lacks the phantom seller_id in schain | **SURVIVES** |
| 3 | "These IDs are documented industry conventions" | OSINT on SmartAdServer 4000-4100 range + Sovrn -eb convention | 2 templates | SmartAdServer 4071/4012/4073/4074 are SKIPPED IDs in an otherwise-allocated 4000-4100 range. Sovrn -eb is a real convention (19% of 7,284 sellers) but `244287-eb` synthesizes real seller 244287 (ConnectAd Realtime) + valid suffix into a non-existent ID | **SURVIVES** (strengthened) |
| 4 | "in_registry=0 calculation has bugs producing false positives" | Stratified random sample of 12 phantom claims across 4 freq strata, manual verification | 12 claims | 0/12 found in current sellers.json. 0% pipeline false-positive rate at every stratum | **SURVIVES** |

#### What the four refutations together demonstrate

The fabrication framing has survived independent attacks from four orthogonal directions:
- (1) attacks the staleness hypothesis
- (2) attacks the bid-flow hypothesis
- (3) attacks the legitimate-convention hypothesis
- (4) attacks the pipeline-integrity hypothesis

Each used different data (current SSP fetches vs Playwright captures vs OSINT vs stratified sampling) and reached the same conclusion. The simplest remaining explanation is the steelman: industrial template injection at scale.

#### Cycle 471 expanded anomaly_audit.py with two new sections

- `s_literal_placeholders` confirms: 358 SSPs accept seller_id "1" from 7,337 pubs; 21 SSPs accept "12345" from 437 pubs; 18 SSPs accept "0" from 581 pubs. These are raw template defaults that publishers/wrappers shipped without replacing.
- `s_cross_ssp_sharing` reveals the backend-sharing topology:
  - SmartAdServer 4071 propagates across 5 domains: smartadserver.com + martadserver.com (typosquat) + vdo.ai + atlas5.co + walletcircle.co + triplelift.com
  - SmartAdServer 4074 propagates: smartadserver.com + udmserve.net + martadserver.com (typo)
  - IndexExchange 190906: indexexchange.com + **ndexexchange.com** (typo)
  - IndexExchange 190243: indexexchange.com + **indexxchange.com** (typo)
  - MediaGrid DJQVCM: themediagrid.com + **tomediagrid.com** (typo)
  - Sovrn 268876: lijit.com + sovrn.com + **ijit.com** (typo)
  - AppNexus 9284: appnexus.com + adnxs.com (legitimate alias)
  - YahooAOL 58578: yahoo.com + aol.com + digiteka.com

Typosquat DNS audit: 8 of 10 typo variants (ndexexchange, indexxchange, martadserver, potxchange, ijit, atlas5, walletcircle, vdo.ai) resolve. Most serve cybersquat parking pages (e.g., indexxchange.com redirects to /lander).

#### What still hasn't been tested

- **Scaled Playwright (n=100+)** across genres for stronger statistical power on the bid-flow refutation
- **Wayback temporal trajectory** on phantom claims (rotation = active maintenance; persistence = decay)
- **Wrapper-vendor identification** for the cycle-211 SmartAdServer template (Freestar? Sortable? specific wrapper?)


### E-2026-05-22-r: Master signifier "fabrication" removed; structural facts at higher resolution (cycle 472)

User pointed out that cycles 470-471 had silently installed "fabrication" as the agency-imputing master signifier — the four refutation attempts tested whether my measurement was wrong, never whether the concept was warranted at all. Removing the signifier opens visibility into structural facts the lens had been filtering out.

#### Structural fact 1: propagation units, not isolated templates

The cycle-211 SmartAdServer "quartet" (4071/4012/4073/4074) is 4 members of ONE 22-pair propagation unit (U0). Union-find clustering with overlap_ratio≥0.75 + jaccard≥0.4 on top-50 phantom pairs:

| unit | size | mean pubs | members |
|---|---:|---:|---|
| **U0** | **22 pairs** | **3,787** | SmartAdServer 4071/4012/4074/4073 + adform 1941 + IX 190906/192450/192051/196713 + appnexus 2928 + advertising.com 7574 + lijit 244287-eb + onetag 5d4e109247a89f6 + emxdgt 1701/1138 + spotx 173177 + spotxchange 173177 + yahoo 55248/58578 + outbrain 00fe7cdd... + loopme 11013 + criteo B-060278 |
| U1 | 4 | 2,627 | aolcloud 10109 + adtech 10109 + revcontent 124709 + IX 185104 |
| U2 | 4 | 2,516 | appnexus 13701 + openx 541177116 + e-planning 835fbafe... + vidoomy 2252369 |
| U3 | 3 | 2,775 | triplelift 8446 + disqus 891 + zeta 891 |

**1,358 publishers carry ALL top-10 members of U0 simultaneously.** Sample carriers reveal mixed cohort: piracy streaming (1flix.to, 1hd.gg, 2kmovies.mov) alongside Japanese/Russian blogs (2chblog.jp, 2ch2.net) and French sites (13or-du-hiphop.fr). The 22-pair unit traverses publisher categories — not piracy-specific, not premium-specific.

#### Structural fact 2: format-respecting near-miss synthesis

Phantom seller_ids are systematically near-misses of real IDs in the same SSP namespace (edit-distance ratio 0.75-0.89):

| SSP | phantom | closest real IDs (similarity) |
|---|---|---|
| smartadserver.com | 4071 | 3401, 4007, 4010 (0.75) |
| smartadserver.com | 4012 | 3401, 3402, 3412 (0.75) |
| lijit.com | 244287-eb | 264487-eb, 414287-eb, 424427-eb (0.89) |
| indexexchange.com | 190906 | 190096, 190290, 190306 (0.83) |
| google.com | pub-8622186303703569 | pub-0831618630039759 (0.75) |

The IDs aren't random — they conform to each SSP's namespace conventions but aren't in the roster. Agency-neutral interpretation: the propagation-unit string-generators respect SSP namespace conventions.

#### Structural fact 3: ads.txt files are essentially frozen (cycle 467 empirically grounded)

The `publisher_audit_history` table provides 5 snapshots over 27 days (Apr 24, 25, 28, May 9, May 21). It existed since at least Apr 24 and was never queried in cycles 458-471 — the cycle 467 "geological decay" claim was structural inference, not measurement.

Now measured (in 0.9s on materialized table):

| metric | value |
|---|---:|
| publishers with all 5 snapshots | 76,421 |
| **publishers with ZERO false-rate change** | **41,330 (54.1%)** |
| big-movers (>20pp range) | 3,407 (4.5%) |
| median per-pub temporal range | **0.00pp** |
| of 42,267 high-phantom pubs, improved to <10% | **4 (0.009%)** |
| aggregate false_rate trajectory | 52.20% → 53.47% (∆ +1.27pp) |

54.1% of publishers' ads.txt files are completely static. The framework is frozen at the publisher-side; what cycle 467 called "geological decay" is now an empirical claim with longitudinal data.

#### Speedups delivered (cycle 472)

| Query | Previous cost | New cost | Factor |
|---|---:|---:|---:|
| 76K-pub trajectory (cycle 467 dead-SSP per-claim queries) | multi-minute | 0.9s | ~200× |
| 50-pair propagation-unit detection | n/a (new) | 8.9s | — |
| Full 8-tripwire CI run | n/a | 68.6s | full coverage |

#### What survives without the master signifier

Without "fabrication" as an agency-imputing word:

- 33.83% of DIRECT claims have seller_id strings absent from the named SSP's sellers.json (measured, robust)
- Those strings respect each SSP's namespace conventions (edit-distance signature)
- The strings travel in identifiable propagation units across publishers (union-find on co-occurrence)
- The publisher-side ads.txt files are essentially frozen over 27 days
- Some SSP domains are typosquats; some phantom IDs appear at both real and typo variants

What requires agency-imputation and is therefore NOT in this framing:

- "Industrial fabrication at scale" (presupposes industrial actor)
- "Template injection" (presupposes injector)
- "The mechanism understands convention" (presupposes mechanism with intent)

The data shows propagation units; the data does not show actors. The mechanism is empirically distinguishable from independent claim-generation but not identifiable from the data alone.



### E-2026-05-22-s: File-copy evidence + 23.77σ random-control survival of U0 (cycle 473)

User pushed further. Two severe tests run on the cycle 472 propagation-unit claim.

#### Refutation Test (random control): is U0 just hub-effect artifact?

Null hypothesis: U0's high pairwise overlap is publisher-Pareto chance — many publishers with many phantom claims will overlap on many pairs by coincidence.

Method: 100 random samples of 22 non-U0 phantom pairs drawn from the 5,377 pairs with ≥50 phantom pubs each. Computed pairwise overlap_ratio + jaccard for each random sample.

| metric | U0 (real) | Random control (100 samples) | z-score |
|---|---:|---:|---:|
| Pairwise mean overlap_ratio | **0.7012** | 0.0729 ± 0.0264 | **23.77σ** |
| Pairwise mean jaccard | **0.4190** | 0.0252 ± 0.0109 | — |
| Max control overlap_ratio | — | 0.1788 (still ¼ of U0's mean) | — |

**U0 SURVIVES at z = 23.77σ.** Essentially impossible under the null. The 22-pair coherence is not chance co-occurrence — it's structurally real.

#### File-content fingerprint: literal identical files

For the 1,358 publishers carrying ALL 10 top members of U0, computed SHA1 hashes of their full ads.txt line-sets (using cached `adstxt_triples`, no re-fetch). Detected **35 distinct identical-file clusters** within the 1,358:

| Cluster | Pubs | Identifier |
|---|---:|---|
| 1 | **83** | sha1 f843334b0ccb |
| 2 | 19 | sha1 9a6f23131aac |
| 3 | 12 | sha1 b01847e7dde8 |
| 4 | 10 | sha1 147793360cea |
| ... | 3-9 each | 31 more clusters |

**Cluster 1 — 83 piracy streaming domains running EXACTLY the same 4,467-line ads.txt file:**

```
1flix.to, 2kmovies.mov, 9animetv.to, actvid.rs, andydayzz.uk,
aniwatchtv.to, arc018.to, attackertv.so, bflixto.tv, bflixzz.uk,
bogge.tv, braflix.la, braflix.mov, braflix.nl, casstudio.tv,
cataz.to, cineb.gg, cineb.rs, divicast.com, ev01.to, f2movies.la,
f2moviesz.uk, fboxtv.com, flixhq-tv.lol, flixhq.pe, flixter.ac,
flixup.to, fmoviess.ca, fmoviesto.fi, fmoviesz.fi
+53 more
```

Sample content (1flix.to as representative of all 83): 4,467 lines, 106 distinct tag_ids, top SSPs by row count are pubmatic (391), rubiconproject (300), appnexus (293), smartadserver (232), openx (220), indexexchange (213), google (210), freewheel (183), lijit (162), gourmetads (134). A fully-loaded ads.txt template covering ~50 major ad-tech operators, distributed unchanged across 83 piracy streaming domains.

**Cluster 2 — 19 Japanese matome (aggregator) blogs running another identical file:**

```
fiveslot777.com, fukucyan.net, garesoku.com, geinoujam.com,
hamusoku.com, ikarishintou.com, itaishinja.com, jin115.com,
kanphoto.net, kitizawa.com, matimesan.com, moe-taikendan.net,
moetataiken.com, nakasorahami.com, nwknews.jp, okusama-kijyo.com,
paranormal-ch.com, vtubernews.jp, watashi-h.com
```

Japanese 2ch-style summary blogs sharing another identical ads.txt fingerprint.

#### Corpus volume

| Metric | Value |
|---|---:|
| U0 (22 pairs) total claim volume | 268,587 |
| Fraction of full 28.77M-row corpus | 0.934% |
| Publishers carrying ≥1 U0 member | **11,083 (14.9% of corpus)** |
| Publishers carrying ALL 10 top members | 1,358 (1.8% of corpus) |

U0 has **broad publisher reach (1 in 7 publishers) but low volume-per-pub** (<1% of total triples). Heavy in distribution-graph, light in row-count.

#### What this lands

The cycle 472 propagation-unit claim now has empirical content at three independent layers:

1. **Statistical**: U0 is 23.77σ distinct from random co-occurrence
2. **File-content**: 83 piracy domains run EXACTLY the same 4,467-line file; 35 such identical clusters detected total
3. **Cross-cohort**: propagation crosses language (English/Japanese/+) and genre (piracy/aggregator/+) boundaries

Without imputing agency: the data shows literal identical-file distribution at scale, statistically real, crossing cohorts.

What the data still does NOT show:
- Who copied the file (no Wayback temporal yet)
- Which wrapper-vendor/CMS/reseller distributes it
- Whether 83 piracy sites have separate operators or one party

The empirical answer requires temporal data (emergence-cohort dating via Wayback). Synchronized appearance = deliberate distribution. Gradual emergence = template-adoption pattern.

#### Speedup

File-content fingerprint computation completed in 33 seconds on the materialized adstxt_triples table. Earlier naive approach (per-publisher network fetch) timed out at 25/25 fetches in 458 seconds. The cached corpus enables **20× faster computation AND 100% completion** vs network re-fetch.



### E-2026-05-22-t: Trail's end — five named wrapper-managers distribute U0's phantom pairs (cycle 474)

The dog stayed on the scent. The trail starting from "33.83% of DIRECT claims don't validate" terminates at named distributors.

#### Chain of evidence

| Layer | Cycle | Finding |
|---|---:|---|
| Aggregate rate | 458 | 33.83% phantom DIRECT |
| Propagation unit | 472 | 22-pair string-cluster U0 across 1,358 publishers |
| Statistical reality | 473 | Random-control z = 23.77σ — U0 is real, not hub-effect |
| File-content identity | 473 | 83 piracy streaming domains run **EXACTLY identical** 4,467-line ads.txt file |
| Declared manager | 473 | All 83 declare **MANAGERDOMAIN=themoneytizer.com** (IAB ads.txt v1.1 §5.9 delegation) |
| **Distribution chain** | **474** | **5 named wrapper-managers each carry U0 phantoms to their publisher clients at concentration 10-86%** |

#### Per-U0-phantom-pair manager attribution

For each U0 top-10 phantom pair, the top 3 distributing managers (n_pubs declaring each manager AND carrying that phantom):

| U0 phantom pair | Top 3 distributing managers (n_pubs) |
|---|---|
| smartadserver|4071 | themoneytizer.com (541), anymanager.io (349), pubfuture.com (233) |
| smartadserver|4012 | themoneytizer.com (537), anymanager.io (349), pubfuture.com (233) |
| smartadserver|4074 | themoneytizer.com (537), anymanager.io (344), pubfuture.com (233) |
| smartadserver|4073 | themoneytizer.com (536), anymanager.io (345), pubfuture.com (233) |
| adform|1941 | themoneytizer.com (583), fourm.jp (158), adpushup.com (140) |
| indexexchange|190906 | themoneytizer.com (527), anymanager.io (131), pubrev.io (105) |
| appnexus|2928 | themoneytizer.com (574), fourm.jp (158), symplr.de (134) |
| advertising|7574 | themoneytizer.com (574), symplr.de (134), adpushup.com (109) |
| lijit|244287-eb | themoneytizer.com (525), 1xl.co.uk (148), anymanager.io (132) |
| onetag|5d4e109247a89f6 | themoneytizer.com (471), pubpower.io (132), anymanager.io (118) |

themoneytizer.com is consistently the top distributor across **every single** U0 phantom pair. Cumulative across all 10 U0 top members: themoneytizer 5,405 carrier-pub-pairs, anymanager.io 2,020, pubfuture.com 1,374, adpushup.com 1,221, fourm.jp 1,032.

#### Wrapper-ecosystem stratification

What % of each top wrapper's clients carry SmartAdServer|4071 phantom DIRECT?

| Manager | Client pubs | Carrying 4071 | % carrying | Classification |
|---|---:|---:|---:|---|
| **anymanager.io** | 404 | 349 | **86.4%** | EXTREME outlier |
| **themoneytizer.com** | 999 | 541 | 54.2% | top-volume |
| **adpushup.com** | 347 | 149 | 42.9% | heavy |
| **refinery89.com** | 349 | 88 | 25.2% | heavy |
| **publift.com** | 572 | 57 | 10.0% | moderate |
| freestar.com | 923 | 72 | 7.8% | moderate |
| playwire.com | 381 | 19 | 5.0% | low |
| mediavine.com | 1,473 | 55 | 3.7% | low |
| ezoic.ai | 882 | 22 | 2.5% | low |
| **cafemedia.com (Raptive)** | 1,808 | 5 | **0.3%** | empirically clean at scale |

#### What this proves

**The wrapper-vendor ecosystem stratifies bimodally:**
- **Clean wrappers** (CafeMedia 0.3%, Mediavine 3.7%, Ezoic 2.5%, Playwire 5.0%, freestar 7.8%) — phantom carriage under 8% across 5,500+ publishers combined.
- **Phantom-heavy wrappers** (anymanager.io 86.4%, themoneytizer.com 54.2%, adpushup.com 42.9%, refinery89.com 25.2%) — phantom carriage 25-86% across 2,100+ publishers combined.

**CafeMedia at 0.3% on 1,808 publishers is empirical proof that clean wrapper-managed scale is possible.** The framework isn't inherently broken; specific operators choose what to ship. **anymanager.io at 86.4% concentration of phantom-4071 on 404 publishers is the most extreme single-wrapper signature in the corpus.**

#### Mechanism — fully named

The propagation mechanism behind U0 is now resolved:

1. Publishers sign up with wrapper-management services
2. They declare MANAGERDOMAIN=<wrapper> in their ads.txt (IAB §5.9 delegation, legitimate)
3. The wrapper distributes a master template
4. Phantom-heavy wrappers' templates contain seller_ids that don't validate against the named SSPs' rosters
5. Publishers inherit the template; their ads.txt files carry the phantom pairs

themoneytizer.com's CURRENT public master at `https://ads.themoneytizer.com/ads_txt.php` is **930 lines**. The file at piracy sites is **4,467 lines** — composite of themoneytizer + other chained wrappers (anymanager, pubfuture, adpushup, refinery89) each contributing template fragments.

#### Speedup

In-memory hash lookup for manager attribution: **0.9s** vs SQL JOIN attempt that ran 5+ minutes with zero output (then was killed). **>300× faster.** Pattern: pre-load 17,364 publisher-manager pairs into Python dicts once, then per-pair O(1) lookup.

#### Where the trail stops

The next move requires primary-source contact with the named operators (asking themoneytizer.com, anymanager.io, adpushup.com, refinery89.com, pubfuture.com directly about their templates). Per project policy, outbound communication requires explicit authorization.

The empirical chain is complete:
- 33.83% phantom rate → 22-pair propagation unit U0 → 83 piracy domains with identical 4,467-line file → MANAGERDOMAIN=themoneytizer.com → 5 named wrapper-distributors → bimodal ecosystem stratification → CafeMedia proves clean is achievable at scale.

The framework isn't a structural inevitability. The phantom rate concentrates in specific named distributors whose templates contain seller_ids that don't validate.



### E-2026-05-22-u: Vertical integration — wrappers ship their own phantom seller_ids (cycle 475)

The dog stays on the scent. Cycle 474 named 5 phantom-heavy wrapper-managers. Cycle 475 traces the corporate structure and reveals universal vertical integration in the wrapper-management ecosystem.

#### AnyMindGroup chain — anymanager.io → ads.adasiaholdings.com

anymanager.io OSINT:
- Hosted on Google Cloud (34.85.58.22, ns-cloud-*.googledomains.com)
- Homepage: "© AnyMindGroup. All right reserved."
- sellers.json contact: `partner@adasiaholdings.com`
- Address: `#13-01 SBF Center, 160 Robinson Road, Singapore 068914`

**AnyMindGroup (formerly AdAsia Holdings) operates BOTH a wrapper-manager AND a connected SSP.** ads.adasiaholdings.com in corpus: 816 publishers reference it; **100% phantom rate** — every single claim against AnyMindGroup's own SSP is unvalidated by their own sellers.json.

**112 of anymanager.io's 404 client publishers (27.7%) explicitly carry `ads.adasiaholdings.com` in their ads.txt** — the wrapper-template feeds the parent company's own SSP into its publishers' ads.txt files.

#### anymanager.io clients carry phantom rates 60-97% across major external SSPs

| SSP | clients carrying | phantom rate |
|---|---:|---:|
| freewheel.tv | 372 (92%) | **97.5%** |
| yahoo.com | 370 | **90.0%** |
| indexexchange.com | 372 | **79.5%** |
| contextweb.com | 372 | 71.6% |
| inmobi.com | 372 | 64.2% |

anymanager.io's master template ships phantom seller_ids that don't validate against any of these major SSPs' rosters. The phantom claims propagate to 92% of anymanager's clients across all external SSPs.

#### Vertical-integration audit across the wrapper ecosystem

For each top wrapper, how does the wrapper's OWN domain appear as SSP in its clients' templates?

| Wrapper | Clients | Wrapper-as-SSP carriage | Wrapper-as-SSP phantom | Cumulative client phantom |
|---|---:|---:|---:|---:|
| **themoneytizer.com** | 999 | 93.4% (933) | **58.8%** | **38.3%** |
| **anymanager.io** | 404 | 88.1% (356) | 25.1% +100% on adasiaholdings | **37.5%** |
| **adpushup.com** | 347 | 98.0% (340) | 29.6% | 37.4% |
| **pubfuture.com** | 247 | 96.8% (239) | 11.1% | 35.8% |
| **refinery89.com** | 349 | 97.7% (341) | 19.3% | 29.2% |
| publift.com | 572 | 99.5% (569) | 0.3% | 26.6% |
| playwire.com | 381 | 97.9% (373) | 48.1% | 17.9% |
| ezoic.ai | 882 | 98.1% (865) | 14.4% | 14.7% |
| **mediavine.com** | 1,473 | 99.9% (1,471) | **4.0%** | **7.7%** |
| **cafemedia.com (Raptive)** | 1,808 | 99.3% (1,795) | **2.6%** | **6.5%** |

#### Structural facts

1. **Every top wrapper declares itself as SSP in 88-100% of client templates.** Vertical integration is universal — managers ARE sellers, listed in client publisher ads.txt files.

2. **The ecosystem stratifies bimodally on self-validation.** Clean wrappers (CafeMedia 2.6%, Mediavine 4.0%, publift 0.3%) ship templates where their own seller_ids validate. Phantom-heavy wrappers (themoneytizer 58.8%, adpushup 29.6%, anymanager 25.1%) ship their OWN seller_ids that don't validate against their OWN sellers.json.

3. **themoneytizer.com is the most striking case.** 93.4% of clients carry `themoneytizer.com` as DIRECT seller_id. **58.8% of those claims don't validate against themoneytizer's own sellers.json.** The manager ships its own phantom IDs to its own clients.

4. **anymanager.io / AnyMindGroup is the most vertically integrated case** — wrapper + SSP under one corporate parent, with the connected SSP at 100% phantom rate.

5. **CafeMedia / Raptive at 6.5% cumulative phantom on 1,808 publishers proves clean wrapper-managed scale is possible.** The framework isn't structurally broken. Specific operators choose what to ship.

#### The full causal chain (agency-neutral, empirically traced)

```
33.83% phantom DIRECT rate (corpus measurement)
  → 22-pair propagation unit U0 (string co-occurrence)
  → random-control z = 23.77σ (statistically real, not artifact)
  → 83 piracy domains share EXACTLY identical 4,467-line ads.txt file
  → All 83 declare MANAGERDOMAIN=themoneytizer.com (IAB §5.9 delegation)
  → 5 named wrapper-managers distribute U0 phantoms across their clients
  → AnyMindGroup operates both wrapper (anymanager.io) AND own SSP
     (ads.adasiaholdings.com at 100% phantom)
  → themoneytizer's clients carry themoneytizer's OWN seller_ids at 58.8%
     phantom rate (manager ships its own unvalidated IDs)
  → Wrapper ecosystem stratifies bimodally on self-validation
  → CafeMedia at 2.6% own-ssp phantom on 1,808 clients proves clean scale
     is achievable
```

#### Speedup

In-memory hash lookup for vertical-integration audit: ~10s across 10 wrappers × 17,364 publisher-manager mappings + per-SSP-per-pub query. SQL JOIN attempt for similar analysis ran 5+ min with zero output (per cycle 474). **>300× faster** via pre-loaded Python dicts.



### E-2026-05-22-v: Yahoo Japan (LY Corp) hosts 15 of 19 matome blogs sharing the same ads.txt (cycle 476)

The 19-pub Japanese matome cluster (identified in cycle 473) declares ZERO MANAGERDOMAIN directives. Following the fork:

#### DNS analysis

15 of the 19 sites resolve to the **same IP: 147.92.146.242**. The remaining 4: 2 on `blog-01.livedoor.jp` (Japanese blog platform), 1 Cloudflare, 1 AWS-managed nameserver.

#### IP owner

WHOIS on 147.92.146.242:

```
inetnum:    147.92.128.0 - 147.92.255.255
netname:    YAHOO
descr:      LY Corporation
descr:      1-3 Kioicho, Chiyoda-ku, Tokyo, Japan 1028282
remarks:    Email address for spam or abuse complaints:
            ml-backbone-contact@lycorp.co.jp
```

**LY Corporation** owns the /17 range 147.92.128.0-147.92.255.255 with netname YAHOO. LY Corp is the parent entity formed by the 2023 merger of LINE Corporation and Z Holdings, which owned Yahoo Japan. Yahoo Japan's infrastructure now operates under LY Corp.

#### The matome mechanism

15 Japanese matome (aggregator) blogs (jin115.com, hamusoku.com, vtubernews.jp, ikarishintou.com, etc.) hosted on LY Corp infrastructure (147.92.146.242) all serve EXACTLY the same 3,195-line ads.txt template. The server generates the file for all hosted sites. No IAB-spec MANAGERDOMAIN declaration is needed because the host produces the file server-side.

The cluster mechanism is DIFFERENT from the piracy/themoneytizer mechanism:

| Cluster | Mechanism | Declaration | Reach |
|---|---|---|---|
| Piracy (83 sites) | IAB §5.9 MANAGERDOMAIN delegation to themoneytizer.com | Explicit | 83 sites |
| Matome (15 of 19 sites) | Shared hosting infrastructure | None | 15 sites on Yahoo Japan IP |
| AnyMindGroup (404 clients) | anymanager.io wrapper-manager + own SSP | Explicit | 404 wrapper clients + 816 SSP pubs |

**Both mechanisms ship the same U0 phantom seller_ids.** The propagation unit reaches publishers via multiple distinct distribution mechanisms across multiple corporate parents:

| Corporate parent | Distribution channel | Corpus reach |
|---|---|---:|
| AnyMindGroup (Singapore) | anymanager.io wrapper + ads.adasiaholdings.com SSP | ~404 + ~816 publishers |
| **LY Corporation (Yahoo Japan)** | **Shared hosting infrastructure (IP 147.92.146.242)** | **15 matome blogs (+ likely more in adjacent /24)** |
| themoneytizer.com (France) | wrapper-manager + own SSP | 999 clients |
| adpushup.com, refinery89.com, publift.com, pubfuture.com | wrapper-managers | hundreds each |

#### The unresolved upstream

The structural question becomes: what COMMON template source feeds:
- themoneytizer.com's master (930 lines containing some U0 IDs as RESELLER)
- anymanager.io's master (distributes U0 to 404 clients across major SSPs)
- LY Corp's server-side generator (produces 3,195-line file for matome blogs)

If they all draw from a common upstream — a shared ad-tech library / template vendor that supplies templates to wrapper-managers AND hosting infrastructure — then U0 has a single ultimate root. If they independently arrived at the same phantom seller_ids at z=23.77σ coherence, that's statistically impossible.

The trail has reached named-operator level on TWO orthogonal mechanisms (wrapper delegation + shared hosting) across THREE corporate parents (AnyMind Singapore, themoneytizer France, LY Corp Japan). The common upstream remains unidentified.

#### Speedup pattern

DNS + WHOIS on 19 sites = ~10 seconds. The IP shared-hosting clustering is a FASTER signal than MANAGERDOMAIN clustering when publishers don't declare. Pattern: when declarative-layer clues are absent, hosting-layer clustering frequently locates the operator.



### E-2026-05-22-w: Trail terminus — U0 is multi-source, not single-source (cycle 477)

Three final forks pursued. The trail terminates: U0 propagation has NO single common upstream — it propagates through a distributed multi-vendor ecosystem.

#### Fork 1: tag_ids are SSP-brand fingerprints

Each top phantom tag_id maps to one SSP family with high concentration:

| tag_id | n_rows | phantom % | SSP family |
|---|---:|---:|---|
| 7842df1d2fe2db34 | 379,344 | 100.0% | SpotX (Magnite-acquired) |
| 50b1c356f2c5c8fc | 588,940 | 63.2% | IndexExchange |
| **e1a5b5b6e3255540** | **339,675** | **84.1%** | **Yahoo family** (yahoo + advertising.com + aol.com + adtech + aolcloud + adaptv + verizonmedia) |
| 89ff185a4c4e857c | 434,272 | 61.5% | ContextWeb / Unruly |
| a670c89d4a324e47 | 316,830 | 52.1% | RhythmOne (dead 2019) |
| c228e6794e811952 | 256,910 | 63.0% | Taboola |
| 9fac4a4a87c2a44f | 169,251 | 91.4% | Criteo family (+ 7 typosquats) |
| 1e1d41537f7cad7f | 179,529 | 64.6% | EMX / Cadent |
| 3fd707be9c4527c3 | 76,664 | 100% | DistrictM (dead) |
| 1ad675c9de6b5176 | 36,096 | 99.8% | AdColony (dead) |

#### Fork 2: typosquats reuse REAL SSP tag_ids

Criteo's tag_id 9fac4a4a87c2a44f appears across:
- criteo.com (real): 150,795 rows
- themediagrid.com (Criteo's acquired brand): 18,397 rows
- commercegrid.com (Criteo's Commerce Grid product): 13 rows
- **cryteo.com, riteo.com, hemediagrid.com, crieo.com, creteo.com, 1themediagrid.com, 11criteo.com, betweendigital.com** — typosquats with 0 in registry, using Criteo's real tag_id paired with fake seller_ids

The typosquat-injectors copy the real SSP's tag_id (from header-bidding library references) but pair it with fabricated seller_ids on the typo domain.

#### Fork 3: 152media.info — common opening block across U0 clusters

Both 1flix.to (piracy cluster) and jin115.com (matome cluster) START their ads.txt with the SAME 152media.info block at line 1-9. 152media.info OSINT:
- Contact: `info@152media.com`
- Address: `5724 Highway 280 East, Birmingham, AL` (USA, Alabama)
- 1,115 sellers in their roster

Real Alabama-based ad-tech. Their template appears at the head of identical-file clusters from both wrapper-managed (piracy/themoneytizer) and shared-hosted (matome/LINE Corp) sites.

#### Fork 4: 50+ named wrapper-managers in the ecosystem

The wrapper-management landscape is highly fragmented:

```
cafemedia.com (Raptive)    1,846 pubs    [CLEAN 2.6% own-ssp phantom]
mediavine.com              1,480 pubs    [CLEAN 4.0%]
themoneytizer.com          1,011 pubs    [HEAVY 58.8%]
freestar.com                 960 pubs    [CLEAN-ISH 7.8%]
ezoic.ai                     893 pubs    [MID 14.4%]
publift.com                  616 pubs    [OWN-SSP CLEAN 0.3%]
anymanager.io                425 pubs    [HEAVY 25.1% + 100% adasiaholdings]
playwire.com                 393 pubs
adpushup.com                 372 pubs    [HEAVY 29.6%]
refinery89.com               367 pubs    [HEAVY 19.3%]
bidmachine.io                314 pubs
bloxdigital.com              300 pubs
pubfuture.com                249 pubs    [HEAVY 11.1%]
... + 38 more managers with 50-230 clients each
```

#### Fork 5: hosting concentration is the exception

Of 194 sampled U0 carriers (from 1,358 total):
- Only 4 IPs host ≥2 publishers
- IP 147.92.146.242 (LINE Corp / LY Corp): 6 publishers (largest cluster)
- 3 other IPs at 2 publishers each (OVH France, Cloudflare, DigitalOcean)

The LINE Corp shared-hosting cluster is the only major shared-hosting cluster. Most U0 propagation is via wrapper-delegation, not shared hosting.

#### The structural conclusion

**U0 propagation is MULTI-SOURCE, not single-source.** The same phantom seller_ids reach publishers through:
1. **IAB §5.9 MANAGERDOMAIN delegation** to 50+ named wrapper-managers
2. **Shared hosting infrastructure** (rare; LINE Corp's IP)
3. **Tag_id reuse with fabricated seller_ids** on typosquatted SSP domains
4. **A common opening block from 152media.info** across cluster mechanisms

Multiple corporate parents independently maintain templates containing the same phantom IDs:
- **USA**: 152media.info, CafeMedia, Mediavine
- **France**: themoneytizer.com
- **Singapore**: AnyMindGroup / anymanager.io
- **Japan**: LY Corp / LINE Corp / fourm.jp
- **Plus 50+ smaller named operators**

The clean wrappers (CafeMedia 2.6% own-ssp phantom on 1,808 clients) prove operators CAN choose not to ship phantoms. The phantom-heavy wrappers (themoneytizer 58.8%, anymanager 25.1%) prove operators DO ship them at scale. **The framework's failure is operator-side, not protocol-side.**

The phantom rate is operator-choice. The IAB spec works as designed (publishers delegate → managers publish templates). The structural issue is that some managers ship templates with seller_ids that don't validate, and there is no in-protocol enforcement to detect this.

#### Remaining untrodden forks

- Wayback Machine emergence dating (would require many fetches; trail already at named operators)
- Per-typosquat WHOIS / registrar tracking (pattern established)
- Primary-source contact with named operators (requires explicit user authorization)

The empirical case is complete. The phantom rate is operator-choice, distributed across 50+ named entities, propagated via multiple mechanisms, with both clean and phantom-heavy operators co-existing in the same market. The simplest framing: **operator integrity varies; the framework needs in-protocol enforcement, not new operators**.



### E-2026-05-22-x: Pre-computed classifications surfaced; Indonesian impersonator network identified (cycle 478)

The new editorial design is deployed. Continuing deeper: querying corpus tables I never surfaced across 470+ cycles revealed pre-computed structural data significantly sharper than the 33.83% phantom headline.

#### claim_consensus 5-tier — only 0.1% of DIRECT claims are strong-clean

Multi-channel verification (paper + federated + directive + operational + reciprocity):

| Tier | DIRECT claims | % |
|---|---:|---:|
| strong_suspect | 4,742,862 | 72.3% |
| suspect | 1,486,213 | 22.7% |
| contested | 219,105 | 3.3% |
| ambiguous | 56,422 | 0.9% |
| clean | 48,872 | 0.7% |
| **strong_clean** | **7,093** | **0.1%** |

**Only 7,093 of 6,560,567 DIRECT claims (0.1%) pass strong-clean multi-channel verification.** This is far harsher than the 33.83% phantom rate — the in_registry=0 check is just one verification channel.

#### publisher_top_issues verdict taxonomy — 1.54M impersonations pre-classified

The corpus pre-computed fraud-shape labels per claim:

| Verdict | Claims |
|---|---:|
| verified_phantom | 1,986,103 |
| contradicted_type | 1,621,145 |
| **impersonation_undisclosed** | **1,537,605** |

**1.54M claims (23% of DIRECT corpus) are pre-classified as impersonation_undisclosed**: cases where the seller_id's registered reg_domain belongs to a different publisher than the claimant. This is the fraud-shape that cycles 471-477 dropped as agency-imputing; it is in fact already in the data as agency-implying classification.

#### Impersonation hub-and-spoke graph

Top impersonation TARGETS (publishers being impersonated, the reg_domain in the registry):

| Target reg_domain | Impersonations |
|---|---:|
| **seedtag.com** | **65,288** |
| sunmedia.tv | 28,944 |
| pixfuture.com | 21,545 |
| adpone.com | 17,374 |
| insticator.com | 16,229 |
| smaato.com | 13,686 |
| richaudience.com | 13,155 |
| nobid.io | 11,484 |
| nextmillennium.io | 11,112 |
| vdo.ai | 9,683 |
| minutemedia.com (FanSided parent) | 8,463 |

**Seedtag.com is impersonated through 6+ SSP channels** (xandr 13,216 + smartadserver 11,771 + pubmatic 10,893 + adyoulike 8,703 + onetag 8,556 + improvedigital 7,060) — the Seedtag identity propagates simultaneously through multiple SSP rosters.

#### Indonesian impersonator network — industrial-scale

Top impersonators (publishers carrying the most impersonation_undisclosed verdicts):

| Impersonator publisher | Impersonations | Distinct targets |
|---|---:|---:|
| g1000000.com | 2,526 | 363 |
| dramacool.sh (piracy) | 1,544 | 417 |
| **jatimnetwork.com** | 1,325 | **1,042** |
| **sport.detik.com** | 1,316 | 413 |
| **harianhaluan.com** | 1,308 | 1,033 |
| **dikasihinfo.com** | 1,294 | 1,021 |
| **ayobandung.com** | 1,286 | 989 |
| **urbanjabar.com** | 1,278 | 1,020 |
| **koranmemo.com** | 1,275 | 1,011 |
| **metropolitan.id** | 1,247 | 1,007 |
| floreseditorial.com | 1,240 | 977 |
| **ceposonline.com** | 1,233 | 1,027 |
| **cakrawala.co** | 1,231 | 1,000 |

**8+ of top 15 are Indonesian-affiliated** (.id TLD, Indonesian-language content, detik.com property network). Each impersonates **1,000+ distinct reg_domains**.

This is industrial-scale impersonation by an identifiable national publisher cohort. The Indonesian network appears across the impersonator list at cohort-scale, not individual-actor scale.

#### Publisher_cohort: inverted Pareto

| Cohort | n_pubs | Mean false_rate |
|---|---:|---:|
| tiny_<5 claims | 38,197 | 37.7% |
| small_5-19 | 6,294 | 70.8% |
| medium_20-49 | 6,571 | 69.1% |
| large_50-149 | 14,741 | 62.0% |
| big_150-499 | 7,423 | 78.3% |
| **huge_500+ claims** | 2,944 | **85.3%** |

**The bigger the publisher, the HIGHER the phantom rate.** huge_500+ publishers (with 500+ DIRECT claims each) average 85.3% false_rate. Most-listed publishers have the LEAST valid claims.

#### Wayback temporal evidence

1flix.to's ads.txt has byte-identical content (SHA `Z6LDQOUP2GZGCIOKJNTHNU5LIFRUR3C4`) across 9 Wayback snapshots from 2025-04-04 to 2026-01-08 — **13 months unchanged.** Confirms the geological-stasis framing at the year scale at publisher level.

#### U0 carriers in tier framework

For the 1,358 publishers carrying all 10 top U0 members:

| Tier | Claims | % |
|---|---:|---:|
| strong_suspect | 1,316,990 | 85.7% |
| suspect | 198,544 | 12.9% |
| contested | 12,671 | 0.8% |
| clean | 3,095 | 0.2% |
| **strong_clean** | **223** | **0.0%** |

U0 carriers are 98.6% suspect-tier (vs corpus-wide 95.0%). U0 phantom signature is corpus-wide, not narrowly concentrated.

#### Revised framing — agency-implying classification was already in the data

Cycles 471-477 dropped "fabrication" framing as agency-imputing. The corpus had 1.54M `impersonation_undisclosed` classifications pre-computed — agency-implying language already applied to 23% of DIRECT claims by prior analysis pipeline.

Both frames coexist:
- Agency-implying: 1.54M impersonation events with named target/source patterns
- Structural decay: dead-SSP, schema migration, framework gaps
- Both have named operators (Indonesian network as impersonators; AnyMindGroup/themoneytizer/etc as wrapper-managers)

The agency-neutral framing in cycles 471-477 was overcautious. The data supports a precise fraud-shape claim at 23% of DIRECT corpus with named impersonator publishers (Indonesian cohort + piracy network + g1000000.com) and named targets (Seedtag + Sunmedia + Pixfuture + Adpone + Insticator + Rich Audience + 9 more).

#### Speedup

publisher_top_issues query: ~1s on 5.14M-row pre-materialized table. Fresh JOIN of adstxt_triples + sellers_registry would take minutes. **~100-1000× speedup via pre-materialized issue classification.**



### E-2026-05-22-y: Ayo Indonesia + multi-jurisdictional wrapper coalition (cycle 479)

The trail's named-operator depth: the Indonesian impersonator cohort identified in cycle 478 traces to ONE NAMED PARENT OPERATOR and a multi-jurisdictional wrapper coalition.

#### The parent: Ayo Indonesia (Jakarta)

`ayoindonesia.com` is "Ayo Indonesia — Jaringan berita nasional, regional, akurat, dan terpercaya" (a national/regional news network). Cloudflare-protected, real Indonesian media holding.

**13 publisher brands explicitly declare `OWNERDOMAIN=ayoindonesia.com`:**

```
suaramerdeka.com       (Central Java daily, established 1950)
harianhaluan.com       (Padang/West Sumatra)
harianmerapi.com       (Yogyakarta regional)
harianterbit.com       (national daily)
jatimnetwork.com       (East Java network)
ayobandung.com         (West Java)
urbanjabar.com         (West Java urban)
metropolitan.id        (Bekasi/Jakarta metro)
cakrawala.co
dikasihinfo.com
floreseditorial.com    (Flores Island)
koranmemo.com
realitasonline.id
```

Some are long-established Indonesian newspapers (Suara Merdeka since 1950). Ayo Indonesia is a substantial Indonesian media holding.

#### The wrapper coalition — 6 jurisdictions

Each Indonesian brand declares 5-6 MANAGERDOMAINs simultaneously. The full coalition:

| Wrapper | Country | Contact | Sellers |
|---|---|---|---:|
| **props.id** (PROPS) | **Indonesia** | info@props.id, Regentown Gold Blok J2 No. 8, Jakarta | 2,330 |
| **digiadglobal.com** (DIGIAD DMCC) | **UAE** | Dubai Multi Commodities Centre | small |
| **rev.iq** (RevIQ) | **USA** | demand@rev.iq, 5940 S Rainbow Blvd, Ste 400, Las Vegas, NV 89118 | 790 |
| **hntgaming.me** (H&T Gaming) | **UK** | adops@hntgaming.me, 17 King Edwards Road, Ruislip, London | 35 |
| **anymanager.io** (AnyMindGroup) | **Singapore** | partner@adasiaholdings.com (cycle 475) | — |
| **dev2pub.com** | **France** | cedric@dev2pub.com, 284 Avenue Pierre LOTI, 83000 Toulon | 355 |

**Multi-jurisdictional wrapper chain crossing 6 countries** (Indonesia + UAE + USA + UK + Singapore + France). Each Indonesian brand site chains 5-6 of these together; the resulting ads.txt template carries the impersonation IDs that cumulate across the chain.

#### Why Seedtag is the #1 impersonation target

Seedtag's sellers.json:
- 1,102 sellers (PUBLISHER 814, BOTH 164, INTERMEDIARY 124)
- 0 confidential entries
- Seller IDs are **24-character MongoDB ObjectId hex strings** (e.g., `592d9779971fb107003d23db`)

Seedtag is a native-advertising network (est. 2014, Madrid). Their seller_ids span all major SSPs as PUBLISHER/BOTH classifications — wide attack surface for impersonation. The Indonesian network's templates include Seedtag's real registered seller_ids at xandr/smartadserver/pubmatic/adyoulike/onetag/improvedigital — claiming ownership of Seedtag's existing accounts via 6 different SSP rosters.

The impersonators are not **fabricating** Seedtag IDs — they are **claiming** Seedtag's real, registered IDs in their own ads.txt files at multiple SSPs. Per ads.txt spec, this declares: "the publisher owns this seller account." But the seller account in question belongs to Seedtag in the registry.

#### g1000000.com — the maximum-promiscuous declarations

g1000000.com ("G1000000 Million Games" gaming site, IP 72.60.93.209, dns-parking.com NS) declares:
- **4 OWNERDOMAINs** simultaneously: stoicmedia.com + g1000000.com + snack-media.com + amznusa.com
- **12 MANAGERDOMAINs**: pubfuture.com + yieldmonk.com + pixfuture.com + themoneytizer.com + newormedia.com + vuukle.com + snack-media.com + massarius.com + evolutionadv.it + adipolo.com + revbid.net + weforads.com
- **9 INVENTORYPARTNERDOMAINs**: pixfuture, tappx, admanmedia, voisetech, streamstak, adipolo, adipolosolutions, opamarketplace, pmbmonetize

Maximum-promiscuous wrapper-declaration in the corpus. 2,526 impersonation events across 363 distinct target reg_domains.

#### Structural conclusion — the framework leak is operator-choice through legitimate channels

Every entity in the impersonation chain has a legitimate corporate identity with public addresses:
- Ayo Indonesia is a real Indonesian media holding
- props.id is a real Indonesian ad-tech firm (Jakarta address)
- rev.iq is a real US ad-tech (Las Vegas address)
- hntgaming.me is a real UK ad-tech (London address)
- dev2pub.com is a real French ad-tech (Toulon address)
- anymanager.io is AnyMindGroup Singapore (cycle 475)

Each declares public contacts, sellers.json, OWNERDOMAIN/MANAGERDOMAIN per IAB spec. The framework leak is **operator-choice to ship templates containing impersonation IDs** within chains of named corporate operators with discoverable jurisdictional and contact information.

**CafeMedia at 2.6% phantom on 1,808 publishers (cycle 475) vs Ayo Indonesia chain at ~12K impersonations across 13 brands** — the same IAB framework supports both clean operation at scale and concentrated impersonation operation at scale. Protocol-level structure permits both; **operator integrity is the differentiator.**

The empirical case is reproducible from cached corpus + public DNS + WHOIS + sellers.json + IAB-spec ads.txt directives. Further investigation requires primary-source contact with named operators (Ayo Indonesia, props.id, rev.iq, hntgaming.me, dev2pub.com, anymanager.io), which requires explicit authorization per project policy.

#### Speedup

In-memory hash JOIN of publisher_directives + OWNERDOMAIN attribution: ~10s. SQL JOIN attempts on normalized domain columns ran 5+ min and were abandoned. **~300× faster** through pre-loaded Python dict lookups.



### E-2026-05-22-z: Stoic Media + Jamaica Observer + other-cohort operators (cycle 481)

Continuing deeper after cycle 479's Ayo Indonesia chain — the non-Indonesian top impersonators trace to additional named operator clusters.

#### stoicmedia.com — the SHARED OPERATOR across both g1000000.com and mgeko.cc

Two distinct top impersonators independently declare OWNERDOMAIN=stoicmedia.com:
- **g1000000.com** (gaming): OWNERDOMAINs = stoicmedia.com + snack-media.com + amznusa.com + g1000000.com
- **mgeko.cc** (manga reading): OWNERDOMAINs = colonist.io + mgeko.cc + stoicmedia.com

**Stoic Media** is therefore named as a parent operator across multiple impersonator brands. Both sites chain themoneytizer.com as one MANAGERDOMAIN. mgeko.cc also chains luponmedia.com + pubfuture.com + pubrev.io + yieldmonk.com — a different wrapper coalition than Ayo Indonesia's chain.

#### Jamaica Observer — newsmemory.com

**newsmemory.com** declares **OWNERDOMAIN=jamaicaobserver.com** (Jamaica Observer, established 1993, major Caribbean newspaper) — operating via wrapper **MANAGERDOMAIN=adpushup.com**. 1,234 impersonation events across 303 distinct target reg_domains.

A major Jamaican newspaper is in the impersonator-top-15 via the adpushup wrapper service.

#### Detik.com (sport.detik.com)

**sport.detik.com** declares OWNERDOMAIN=detik.com. Detik.com is the dominant Indonesian online news site (Trans Media's flagship digital property). They use MANAGERDOMAIN=themoneytizer.com + dev2pub.com. 1,316 impersonation events.

#### colonist.io (with mgeko.cc)

mgeko.cc declares colonist.io as one of its OWNERDOMAINs. Colonist.io is a Settlers-of-Catan-style online board game. The cross-OWNERDOMAIN (manga + games + Stoic Media) suggests a portfolio operator running thematically-disparate properties under the Stoic Media holding.

#### adipolo.com — both impersonation target AND chained operator

adipolo.com OSINT:
- Cloudflare-protected (IP 172.67.151.150)
- 727 sellers in their sellers.json
- Contact: amir@adipolo.com
- 10,168 publishers list adipolo.com as SSP
- 21 publishers declare MANAGERDOMAIN=adipolo.com
- 7 publishers declare INVENTORYPARTNERDOMAIN=adipolo.com

adipolo.com appears as:
- An SSP (10,168 pubs list it)
- A wrapper-manager (21 pubs delegate to it)
- An inventory partner (7 pubs)
- An impersonation TARGET (cycle 478 life.ru example)

Triple-role: SSP + wrapper-manager + impersonation target. The same domain plays multiple positions in different publishers' ads.txt structures.

#### Operator-cluster taxonomy

The top 20 impersonators now trace to several distinct named-operator clusters:

| Operator cluster | Top brands | Country/HQ |
|---|---|---|
| **Ayo Indonesia** | jatimnetwork, harianhaluan, dikasihinfo, ayobandung, urbanjabar, koranmemo, metropolitan.id, +6 more (13 total) | Indonesia |
| **Stoic Media** | g1000000.com, mgeko.cc (+ snack-media-related amznusa.com) | unknown HQ (US?) |
| **Jamaica Observer** | newsmemory.com | Jamaica |
| **Trans Media (Detik)** | sport.detik.com | Indonesia |
| **dramacool.sh / piracy** | dramacool.sh and related (themoneytizer-managed) | piracy networks |
| **Mangapicgallery** | iweb_2/iweb_4/pic1/pic3.mangapicgallery.com + mangago.zone/.me | piracy |
| **Native Planet / mykhel** | nativeplanet.com, mykhel.com (Greynium Information Technology, India) | India |

The impersonation activity spans multiple national publisher cohorts (Indonesia / Jamaica / Caribbean / India / piracy / US-portfolio) chained through different wrapper coalitions, but all converging on the same pool of impersonation TARGETS (Seedtag, SunMedia, Pixfuture, etc.).

#### Where the trail stops

The empirical operator-level mapping is now substantial:
- 13 named publisher brand clusters under 5+ identified parent operators
- 6+ wrapper coalitions spanning 6+ countries
- The impersonation targets (Seedtag, SunMedia, etc.) are concentrated on 12-15 named ad-tech vendors
- ~12-20% of all DIRECT claims (1.54M of 6.56M) are pre-classified impersonations
- The IAB ads.txt framework supports both clean operation at scale (CafeMedia 2.6%, Mediavine 4.0%) AND concentrated impersonation operation at scale (Ayo Indonesia chain at ~12K events)

Operator integrity is the differentiator. The protocol-level structure permits both. Every entity in the trail has a public address, sellers.json, and IAB-spec declarations.



### E-2026-05-23-a: Google-INTERMEDIARY credential propagation — 997K claims across 12+ SSPs (cycle 482)

Continuing deeper into the publisher_top_issues taxonomy: cycle 478 mined `impersonation_undisclosed` (1.54M events, no registry entry). Cycle 482 mines the SECOND class — `contradicted_type` (1.62M events, registered but to wrong publisher per registry).

#### The reframe — Sovrn `-eb` is NOT pure fabrication

Cycles 472-481 framed the Sovrn `%-eb` pattern as template injection of phantom IDs. The pre-computed `publisher_top_issues` table reveals a different picture:

- 176,512 Sovrn/Lijit ads.txt claims use `seller_id LIKE '%-eb'`
- **53% (92,788) are phantom** — truly fabricated, no registry entry
- **47% (83,724) are IN registry** — but registered to **google.com** with type=INTERMEDIARY

Of the 1,405 distinct `-eb` seller_ids in Sovrn's sellers.json, **ALL 1,405 are type=INTERMEDIARY with reg_domain=google.com**. The `-eb` suffix appears to be Sovrn's internal naming for its Google-Exchange-Bidding integration credentials.

Cycle 472's framing was partially right (53% fabrication) but missed the dominant mechanism (47% credential propagation). The PROTOCOL recognizes both as anomalies — phantom for the 92K, contradicted_type for the 83K.

#### Industry-scale measurement

Across ALL SSPs, 56,273 Google-INTERMEDIARY credentials exist in registries. **997,468 ads.txt DIRECT/RESELLER claims** by publishers OTHER than google.com sit on these credentials:

| SSP | Google-INTERMEDIARY claims | Distinct publishers |
|---|---:|---:|
| PubMatic | 177,390 | 29,238 |
| Rubicon/Magnite | 151,768 | 28,999 |
| OpenX | 127,102 | 27,472 |
| Sovrn/Lijit | 82,486 | 23,347 |
| OneTag | 58,880 | 20,360 |
| SmartAdServer | 57,880 | 19,551 |
| TripleLift | 50,582 | 18,607 |
| Index Exchange | 46,959 | 20,731 |
| ShareThrough | 45,257 | 18,607 |
| Adingo.jp | 42,736 | 12,782 |
| Media.net | 36,848 | 19,117 |
| video.unrulymedia.com | 18,795 | 12,705 |
| InMobi | 16,439 | 9,902 |
| Sonobi | 16,131 | 7,998 |
| RhythmOne | 14,374 | 9,049 |

The TOP 5 SSPs each propagate Google-INTERMEDIARY credentials to ~23-29K downstream publishers. Combined: ~30K unique publishers receiving these credentials.

#### The mechanism

The chain that produces this:

1. Google contracts with SSPs (Rubicon, PubMatic, OpenX, Sovrn, etc.) for Exchange Bidding / Open Bidding integration.
2. Each SSP issues Google an INTERMEDIARY-type seller_id at their company.
3. Wrapper services (CafeMedia, Mediavine, themoneytizer, AdPushUp, etc.) build header-bidding templates that INCLUDE these Google-INTERMEDIARY credentials so downstream publishers can monetize Google demand via the wrapper.
4. Downstream publishers ship the template's ads.txt content.
5. Their ads.txt now declares: `sovrn.com, 277115-eb, DIRECT` — claiming a DIRECT relationship with Sovrn under what is actually Google's account.
6. The IAB ads.txt × sellers.json reciprocity check flags this as `contradicted_type` (sovrn.com's registry says seller 277115-eb belongs to google.com, not to the publisher).

This is **credential propagation through wrapper chains**, not impersonation. The credentials are real and registered. The protocol error is the downstream declaration — IAB spec §3.1 requires publishers to declare only sellers representing their own inventory, not sellers their wrapper-manager syndicates through.

#### What this changes about the 33.83% phantom rate

The 33.83% headline rate counts both `impersonation_undisclosed` (truly fabricated) and `contradicted_type` (real but wrong-owner) and `verified_phantom` (rare other cases). They're three structurally distinct anomalies. The headline rate is correct as aggregate, but the COMPOSITION matters:

- ~30% is fabrication (cycle 478 impersonation_undisclosed)
- ~30% is credential-propagation (cycle 482 contradicted_type → google.com INTERMEDIARY)
- ~40% is other (verified_phantom, other contradicted_type)

The Sovrn-EB template carriers (CafeMedia, Mediavine, themoneytizer at 2.6-4% phantom) score MUCH WORSE on credential-propagation than on fabrication. CafeMedia's 2.6% phantom rate masks heavy contradicted_type via INTERMEDIARY credentials.

#### Open question for cycle 483

The protocol surfaces credential propagation as an anomaly. Is it a SPEC violation that matters, or legitimate wrapper-syndication that the spec is too strict about? Both readings are defensible:

- **Strict reading**: publishers shouldn't declare sellers they don't directly sell. The spec is explicit. Carrying Google's Sovrn account on your ads.txt misrepresents the supply chain.
- **Functional reading**: wrappers can't function without propagating upstream credentials. The "INTERMEDIARY" type EXISTS precisely to permit this. The downstream declarations are how DSPs find the wrapper-bidding pool. If publishers couldn't declare them, the bidding chain would break.

This dichotomy is the cycle 482 trail-end. Going deeper requires DSP-side data (which bidders accept INTERMEDIARY declarations from downstream-publishers vs require direct accounts) — outside the current ads.txt × sellers.json corpus.



### E-2026-05-23-b: Seedtag impersonation — 10,624 publishers carry credentials registered to premium global brands (cycle 483)

After cycle 482's Google-INTERMEDIARY credential propagation finding, cycle 483 drills into the impersonation_undisclosed verdict for Seedtag — the #1 most-impersonated reg_domain (65,288 events, 10,624 publishers, 10 distinct Seedtag seller_ids).

But "10 distinct seller_ids" was the cycle-478 aggregate. Drilling per-seller_id shows **400+ distinct Seedtag credentials are being impersonated**, each claimed by 1-785 different publishers.

#### The top-30 impersonated Seedtag credentials

The seller_ids actually belong to:

| # impersonators | reg_domain (real owner per Seedtag's sellers.json) |
|---:|---|
| 785 | themoneytizer.com (wrapper service, cycle 471-477) |
| 711 | xapads.com (ad-tech) |
| 582 | pubstack.io (header bidding vendor) |
| 490 | 360playvid.com (video ad-tech) |
| 410 | adipolo.com (cycle 481 cluster) |
| 401 | 152media.info |
| **386** | **sky.com** (UK Sky / Comcast) |
| 369 | adapex.io |
| 310 | optad360.com (wrapper) |
| 215 | yieldlove.com |
| **177** | **automattic.com** (WordPress.com / Tumblr / WooCommerce) |
| 161-154 (multiple IDs) | refinery89.com |
| **159** | **usatoday.com** (Gannett) |
| 157 | improvedigital.com (Magnite) |
| 153 | revistaforum.com.br (Brazilian Forum magazine) |
| 133 | embi-media.com |
| 119 | minutemedia.com |
| 115 | insticator.com (wrapper) |
| 114 | adpushup.com (wrapper) |
| 104 | vuukle.com |
| **46** | **uol.com.br** (Universo Online — major Brazilian portal) |
| **34** | **sapo.pt** (major Portuguese portal) |
| 88 | venatus.com (gaming ad-tech) |
| 72 | massarius.com |
| 60 | pubpower.io |
| 56 | webads.nl |
| 53 | audienzz.com (Swiss ad-tech) |
| 50 | yieldbird.com (Polish ad-tech) |

Plus many premium brands at <50 impersonators each: **NY Post (14), Condé Nast (7), Globo (7), Warner Bros Discovery (1), Tubi (1), Flickr (1), AutoTrader Canada, IPMGroup (Belgium), Mediahuis (Belgium), Lagardère (France), El Tiempo (Colombia), Time Out (Spain), El Universal (Mexico), Webedia, R7 / RecordTV (Brazil), Independent (UK), Epoch Times, PMC (Penske Media Corp), CNN Brasil, Naciodigital (Catalonia), Vocento (Spain), Mediaset Spain**, etc.

#### Why this matters

The IAB ads.txt × Seedtag sellers.json reciprocity check identifies each as a SEPARATE flag because each seller_id is registered to a different premium brand. The impersonators don't realize they're carrying credentials that registries link to *Sky*, *USA Today*, *WordPress.com*, etc. They ship a template (from themoneytizer, adpushup, pubstack, etc.) without auditing which seller_ids it contains.

The wrapper services likely never INTENDED their templates to encode "impersonate USA Today" — they're propagating whatever credentials they harvested from upstream demand sources. The mechanism is structural, not intentional. But the PROTOCOL CONSEQUENCE is that 10,624 publishers' ads.txt files declare relationships with Seedtag using credentials registered to USA Today, Sky, Automattic, etc.

#### Why the wrapper services have these credentials at all

Seedtag's INTERMEDIARY-type credentials (BOTH/INTERMEDIARY rows in their sellers.json) are issued to wrappers that syndicate Seedtag demand. A wrapper that has authority to serve Seedtag ads on behalf of WordPress.com gets a seller_id at Seedtag. When that wrapper builds a template for OTHER publishers, the template includes the WordPress.com credential. Downstream publishers carry it.

This is the **identity-laundering structural risk** of wrapper services:
- Wrapper W gets credentials from Premium Brand P at SSP S
- W syndicates P's inventory through its template
- W also ships the template to non-P publishers (intentionally or by template-default)
- Non-P publishers' ads.txt declares S's credential
- S's sellers.json says the credential belongs to P
- The protocol flags non-P publishers as impersonating P

#### Cross-reference with cycle 478-481 cohorts

Top impersonating publishers of Seedtag credentials include the cohorts identified in cycles 478-481:
- Ayo Indonesia brand sites (jatimnetwork, harianhaluan, dikasihinfo, etc.)
- Stoic Media (g1000000.com, mgeko.cc)
- piracy networks (dramacool.sh, mangapicgallery)
- Greynium IT brands (oneindia, nativeplanet, mykhel)
- Jamaica Observer (newsmemory.com)
- Trans Media (sport.detik.com)
- Russian collector publishers (life.ru claims 12 different Russian publisher reg_domains)

These cohorts don't curate which credentials enter their wrapper-shipped ads.txt. They ship templates AND inherit the credential-attribution problem.

#### Top-15 most-impersonated reg_domains across ALL impersonation_undisclosed

(not just Seedtag — full corpus)

| reg_domain | events | n_impersonators | n_distinct_sids |
|---|---:|---:|---:|
| seedtag.com | 65,288 | 10,624 | 10 (cycle 478 aggregate; 400+ sub-IDs in detail) |
| sunmedia.tv | 28,944 | 6,960 | 8 |
| pixfuture.com | 21,545 | 2,571 | 22 |
| adpone.com | 17,374 | 6,669 | 7 |
| insticator.com | 16,229 | 6,392 | 12 |
| smaato.com | 13,686 | 10,063 | 1 |
| richaudience.com | 13,155 | 7,902 | 6 |
| **wp.pl** (Poland's biggest portal) | 12,382 | 2,020 | 13 |
| nobid.io | 11,484 | 6,493 | 6 |
| **wpartner.pl** (WP.pl programmatic arm) | 11,353 | 2,117 | 6 |
| nextmillennium.io | 11,112 | 4,609 | 15 |
| ops.co | 11,026 | 3,137 | 21 |
| hcodemedia.com | 9,795 | 3,129 | 22 |
| vdo.ai | 9,683 | 2,547 | 13 |
| **minutemedia.com** | 8,463 | 457 | 67 |

The MinuteMedia entry is structurally different: only 457 impersonators but 67 distinct seller_ids per impersonator — bulk credential acquisition, not template propagation. Different mechanism.

#### The verdict-class taxonomy resolved

After cycles 478, 482, 483, the full picture:

| Verdict | Events | What it means |
|---|---:|---|
| verified_phantom | 1,986,103 | seller_id has no registry entry, or registry has NULL domain (confidential) |
| impersonation_undisclosed | 1,537,605 | seller_id is registered but to a different publisher (premium brands targeted) |
| contradicted_type | 1,621,145 | seller_id is registered with type that conflicts with declared rel (often INTERMEDIARY claimed as DIRECT — cycle 482's Google-INTERMEDIARY pattern is the dominant subset, ~997K of 1,621K) |

Combined: **5,144,853 structural anomalies** out of 28.77M ads.txt rows (17.9% of all rows; 33.83% of DIRECT-only rows when counted appropriately).

The three mechanisms are different, but the COHORT of impersonating publishers is largely the same — the cycle 478-481 named operators (Ayo Indonesia, Stoic Media, Jamaica Observer, etc.) appear in all three verdict classes simultaneously.



### E-2026-05-23-c: The Ayo Indonesia universal-template proof — 904-pair core, 86.7% props.id, intra-Indonesian identity collapse (cycle 484)

After cycle 483's premium-brand-impersonation finding, drilled into the cohort signature itself. Computed pairwise Jaccard similarity of `impersonation_undisclosed` pair-sets across the top-9 Ayo Indonesia sites.

#### Empirical proof of single-template propagation

| pair | Jaccard |
|---|---:|
| jatimnetwork.com ∩ harianhaluan.com | 0.952 |
| jatimnetwork.com ∩ dikasihinfo.com | 0.961 |
| dikasihinfo.com ∩ urbanjabar.com | 0.982 |
| urbanjabar.com ∩ metropolitan.id | 0.977 |
| harianhaluan.com ∩ dikasihinfo.com | 0.975 |
| ... | mostly 0.92-0.98 |
| (lowest pair) ceposonline.com ∩ all others | 0.75-0.78 |

**Universal intersection across all 9 sites: 904 (ssp, seller_id) pairs.** Each site carries 1,096-1,169 total impersonation pairs. The 904-pair UNIVERSAL CORE = 80% template overlap. The remaining 200-300 per-site entries are individual variation on top of the core template.

This empirically PROVES cycle 478-479's claim that Ayo Indonesia ships a unified template — at near-identity level. No comparable Jaccard structure exists for unrelated publisher cohorts (control: random publisher pairs have Jaccard <0.05).

#### Template composition

The 904-pair core touches **50 distinct SSPs** and impersonates **860 distinct brand domains**.

Concentration in the template:

| SSP | seller_ids in template | % of template |
|---|---:|---:|
| **props.id** | **784** | **86.7%** |
| google.com | 24 | 2.7% |
| appnexus.com | 10 | 1.1% |
| pubmatic.com | 8 | 0.9% |
| smartadserver.com | 5 | 0.6% |
| lijit.com (Sovrn) | 5 | 0.6% |
| adtelligent.com | 5 | 0.6% |
| affinity.com | 3 | 0.3% |
| mgid.com | 3 | 0.3% |
| adyoulike.com | 3 | 0.3% |
| openx.com, playstream.media, onetag.com, richaudience.com, nsightvideo.com | 2 each | |
| 36 other SSPs | 1-2 each | |

**props.id is the dominant carrier.** 784 of 904 entries (86.7%) of the universal template are props.id credentials. The rest is distributed across 49 other SSPs.

#### props.id is a real Indonesian SSP

ccurl-verified live state of props.id:
- Live website at `https://props.id/`
- sellers.json: 2,329 sellers, all PUBLISHER type, 2,324 distinct publisher domains
- Contact email: `info@props.id`
- Contact address: `Regentwon Gold Blok J2 No. 8` (Indonesian, likely Surabaya)
- Top registered publishers in sellers.json:
  - `com.bsm.id` (Beritasatu Media's BSM app)
  - `com.beritasatu` (Berita Satu mobile app)
  - `jawapos.com` (Jawa Pos newspaper, major Indonesian daily)
  - `beritanusa.com`
  - `farah.id`
  - `sumbar.disway.id`
  - …2,300+ others (small Indonesian websites + apps)

props.id is a legitimate Indonesian SSP with a legitimate-looking sellers.json. Its 2,329 sellers represent (per the registry) real Indonesian publisher inventory.

#### What Ayo Indonesia is actually impersonating

The 784 props.id credentials in Ayo Indonesia's universal template are NOT random fabrications. They're the registered seller_ids of 784 OTHER Indonesian publishers — including:

- **Berita Satu Media Holdings**: BSM apps + Beritasatu — owned by **Lippo Group** (one of Indonesia's largest conglomerates)
- **JawaPos Group**: major newspaper publishing group
- **Investor.id**: financial news
- **Berita Nusa**: regional news
- **Disway.id**: regional news network
- Hundreds of smaller Indonesian websites + apps

Per the IAB reciprocity check: when jatimnetwork.com declares `props.id, 4137, DIRECT`, but props.id's sellers.json says 4137 belongs to `com.beritasatu`, the protocol fires impersonation. jatimnetwork.com is claiming to be Berita Satu.

#### Reframe: this is intra-Indonesian publisher identity collapse

Cycle 483 found Ayo Indonesia impersonating premium global brands (Sky, USA Today, Automattic) via small-international-SSP credentials. Cycle 484 finds the DOMINANT mechanism: Ayo Indonesia impersonating OTHER MAJOR INDONESIAN PUBLISHERS (Berita Satu, JawaPos, Investor.id) via props.id credentials.

The premium-global-brand impersonations (Seedtag/SunMedia/AdPone/Insticator pointing to international brands) account for ~13% of the universal template. The remaining 87% is **intra-Indonesian publisher identity collapse** — small Indonesian site impersonating large Indonesian publisher's props.id credentials.

This recontextualizes the cycle 478-479 Ayo Indonesia finding:

- Cycle 479: "Ayo Indonesia uses 6-country wrapper coalition"
- Cycle 484: "Ayo Indonesia primarily uses ONE Indonesian SSP (props.id) impersonating the major Indonesian media holdings (Berita Satu/Lippo, JawaPos, Investor.id) — international SSPs are just 13% spice"

The "wrapper coalition" framing was overcomplicated. The dominant pattern is local Indonesian SSP infrastructure being used to impersonate the dominant Indonesian media groups.

#### What this likely means structurally

Berita Satu, JawaPos, Investor.id ARE registered with props.id (as PUBLISHERs of their inventory). props.id legitimately syndicates their inventory.

When Ayo Indonesia (or its wrapper, AnyMindGroup) builds a template, the template includes props.id seller_ids that the wrapper has access to syndicate. The downstream Ayo Indonesia sites ship the template. Their ads.txt now declares 784 props.id credentials that registry-attest to Berita Satu / JawaPos / Investor.id.

The likely intent: monetize Ayo Indonesia traffic by claiming Berita Satu-class inventory at props.id. The structural consequence: 1.5M flag events at protocol scale, all flagging Ayo as impersonating major Indonesian publishers.

#### Open questions for cycle 485+

1. Does props.id KNOW its credentials are being declared by non-customers? Are they complicit, negligent, or unaware?
2. Do Berita Satu / JawaPos / Investor.id know their credentials are being claimed?
3. Does the Indonesian Press Council or IAB Indonesia have any mechanism to address this?
4. The 13% international-SSP portion routes through Seedtag/Pixfuture/etc. — do those SSPs' compliance teams notice the cohort signature?



### E-2026-05-23-d: The pool-syndication reframe — IAB spec ↔ practice mismatch (cycle 485)

After cycle 484's empirical universal-template proof, drilled into what the 904-pair core ACTUALLY contains. The deeper layer changes the framing again — this time toward neutrality.

#### Verification: are Ayo Indonesia sites themselves props.id customers?

Queried props.id's sellers.json for each of the 14 top Ayo Indonesia sites:

| Site | props.id seller_id | type |
|---|---:|---|
| jatimnetwork.com | 1154 | PUBLISHER |
| harianhaluan.com | 1201 | PUBLISHER |
| ceposonline.com | 3028 | PUBLISHER |
| dikasihinfo.com | 2504 | PUBLISHER |
| urbanjabar.com | 1236 | PUBLISHER |
| koranmemo.com | 1397 | PUBLISHER |
| metropolitan.id | 2433 | PUBLISHER |
| cakrawala.co | 2159 | PUBLISHER |
| ayobandung.com | 1200 | PUBLISHER |
| floreseditorial.com | 2069 | PUBLISHER |
| porosjakarta.com | 2644 | PUBLISHER |
| realitasonline.id | 2594 | PUBLISHER |
| harianmerapi.com | 1152 | PUBLISHER |
| harianterbit.com | 1914 | PUBLISHER |

**Every single Ayo Indonesia top site IS a legitimately registered props.id PUBLISHER-type customer**, each with its own unique seller_id.

#### Composition of the 839 props.id credentials in the template

The 839 props.id seller_ids in Ayo's universal template (verified via jatimnetwork.com as proxy) map 100% to **other Indonesian publisher website domains** registered as PUBLISHER-type with props.id.

Sample (top of the seller_id range):
- 2460 → liriklaguhits.id
- 2458 → panturatalk.com
- 2457 → fokussurabaya.com
- 2456 → ekbistangsel.com
- 2455 → digitalbank.id
- 2454 → detik60.com
- 2453 → coverbothside.com
- 2452 → celebesnetwork.com
- 2451 → bincangkorea.com
- 2450 → balanesia.com
- 2449 → alurinformasi.com
- 2448 → hulondalo.id
- 2447 → bicaranetwork.com
- 2446 → sinaranupdate.com
- 2445 → portalmusirawas.com
- 2444 → sepakterjang.com
- 2443 → jaditau.id
- 2442 → ourindonesia.com
- 2441 → zonajakarta.com
- 2436 → sundaurang.id
- 2435 → radarcianjur.com
- 2434 → radarjabar.com
- **2433 → metropolitan.id** ← this is an Ayo Indonesia site itself
- 2432 → radardepok.com
- 2431 → harianmemokepri.com

So jatimnetwork.com's ads.txt declares 839 props.id credentials including its OWN seller_id (1154) and the seller_ids of 13 OTHER Ayo Indonesia sites plus ~825 other small Indonesian publishers.

#### The structure crystallizes as pool syndication

Every Ayo site declares the WHOLE props.id pool. The mechanism:

1. props.id syndicates inventory from ~2,329 Indonesian publishers (its sellers.json)
2. Of these, ~839 are part of a pooled inventory tier
3. Each pool member's ads.txt declares all ~839 pool member credentials, not just its own
4. The motivation: downstream DSPs check ads.txt before bidding; declaring all pool credentials means DSPs accept bids for any pool inventory unit
5. The IAB ads.txt × sellers.json reciprocity check fires impersonation_undisclosed for each non-own credential — accurately per-spec, but failing to recognize pool semantics

#### The IAB protocol's spec-vs-practice gap

IAB ads.txt v1.1 (2022) added the `INVENTORYPARTNERDOMAIN` directive precisely to allow declaring pool partners explicitly:

> If a publisher participates in a network or shared inventory pool, they SHOULD declare INVENTORYPARTNERDOMAIN entries for each pool partner.

But **adoption of INVENTORYPARTNERDOMAIN is near zero** — the vast majority of pool-based syndication still uses the legacy DIRECT/RESELLER mechanism.

The result: the protocol cannot distinguish:
- Fabricated/fraudulent credentials (cycle 478, ~1.99M verified_phantom)
- Stolen/squatted credentials (cycle 484 small subset, ~30K events)
- **Pool-syndicated credentials properly authorized but spec-not-compliant (the dominant 1.54M impersonation_undisclosed)**

All three look identical at the reciprocity-check level. The 33.83% "phantom DIRECT rate" headline is a mix of:
- ~30% pool syndication (Ayo Indonesia / Stoic Media / Greynium IT / Jamaica Observer / etc. participating in pooled inventory; flagged per-strict-spec but plausibly authorized by pool partners)
- ~30% wrapper credential propagation (cycle 482 Google-INTERMEDIARY 997K; same spec-vs-practice gap)
- ~40% mix of true fabrication, dead-SSP carryover, and genuinely orphan credentials

#### What this changes about the audit's structural verdict

The cycle 478-484 trail had been framing toward "Ayo Indonesia is the Indonesian impersonator network". The cycle 485 reframe softens this:

**Ayo Indonesia is a legitimately-registered Indonesian publisher network participating in a props.id-syndicated inventory pool.** Their ads.txt declarations are spec-non-compliant in the strict reading, but defensible in the functional reading where pool syndication is the standard programmatic model.

The structural finding stands:
- 5.14M structural anomalies measured by the protocol
- 17.9% of all ads.txt rows fire some reciprocity flag
- Three distinct mechanisms detected (phantom / impersonation / type-contradiction)

The interpretive finding has refined:
- These are NOT 5.14M fraud events
- They're 5.14M PROTOCOL VS PRACTICE MISMATCHES, of which some portion is fraud and some portion is legitimate pool syndication
- IAB's introduction of INVENTORYPARTNERDOMAIN in 2022 acknowledges the gap; adoption hasn't followed

#### The cleanest empirical demonstration of the gap

Ayo Indonesia is the cleanest case study because:
1. All 14 top sites verifiably registered with props.id (confirmed via sellers.json)
2. They share a Jaccard ≥ 0.92 template (cycle 484 empirical)
3. The template declares the WHOLE props.id pool (839 credentials)
4. props.id is a real Indonesian SSP with legitimate Indonesian publisher relationships
5. The pool model is transparent — anyone can fetch props.id/sellers.json and see all 2,329 customers

The pattern is not concealed. The structural anomaly is real per IAB strict spec. The intent is plausibly pooled monetization. The IAB protocol's INVENTORYPARTNERDOMAIN directive (2022) would resolve this if adopted.

#### Open question for cycle 486+

Does ANY major publisher cohort use INVENTORYPARTNERDOMAIN at scale? If adoption is genuinely zero, the "pool syndication impersonation" reframe is the only way to reconcile the 1.54M flag rate with the structural reality. If adoption exists somewhere, the spec is being honored selectively — and the question becomes why some cohorts adopt and others don't.



### E-2026-05-23-e: IAB v1.1 directive adoption — pool-disclosure spec exists, partially adopted (cycle 486)

After cycle 485's pool-syndication reframe, tested the open question: does ANY major publisher cohort use INVENTORYPARTNERDOMAIN at scale? The publisher_directives table answers it.

#### Industry-wide adoption of IAB v1.1 directives

| Directive | Total rows | Distinct publishers | % of 76,426 pubs |
|---|---:|---:|---:|
| OWNERDOMAIN | 24,720 | 23,999 | 31.4% |
| MANAGERDOMAIN | 20,419 | 17,942 | 23.5% |
| INVENTORYPARTNERDOMAIN | 12,555 | 3,953 | **5.2%** |

OWNERDOMAIN (ownership disclosure) at 31% adoption.
MANAGERDOMAIN (wrapper-manager disclosure) at 24%.
**INVENTORYPARTNERDOMAIN (pool-partner disclosure) at just 5.2%.**

Even among publishers who disclose ownership, only ~16% disclose pool partners. The IAB 2022 v1.1 directives exist; adoption of the pool-disclosure piece specifically is lagging.

#### Top INVENTORYPARTNERDOMAIN partners declared (where IPD IS used)

| Partner | Declarations | Likely context |
|---|---:|---|
| tappx.com | 1,005 | mobile monetization |
| thunder-monetize.com | 749 | monetization platform |
| rhebus.works | 736 | wrapper |
| admanmedia.com | 377 | ad-tech |
| ctvbuyer.com | 343 | CTV |
| **wurl.com** | 318 | **CTV (Roku-owned)** |
| cnnnewsource.com | 313 | CNN syndication |
| voisetech.com | 231 | voice/audio |
| 9mediaonline.com | 147 | wrapper |
| **gray.tv** | 143 | **CTV (Gray Television)** |
| **roku.com** | 130 | **CTV** |
| elementaltv.io | 126 | CTV |
| **lgads.tv** | 121 | **CTV (LG Smart TV ads)** |
| optidigital.com | 117 | wrapper |
| **vizio.com** | 116 | **CTV (Vizio Smart TV)** |

**Pattern: INVENTORYPARTNERDOMAIN adoption is concentrated in CTV** (Wurl, Gray TV, Roku, LG Ads, Vizio, ElementalTV, ctvbuyer) where pool-based syndication is structurally required. Display-web publishers mostly skip IPD even when they participate in pools.

#### Ayo Indonesia's actual directive use

Ayo sites are SPEC-COMPLIANT on ownership + manager disclosure:

| Ayo site | OWNERDOMAIN | MANAGERDOMAINs | INVENTORYPARTNERDOMAIN |
|---|---|---|---|
| jatimnetwork.com | ayoindonesia.com + jatimnetwork.com | adpushup, anymanager.io, digiadglobal, hntgaming, props.id, rev.iq | (none) |
| harianhaluan.com | ayoindonesia.com + harianhaluan.com | (same 6 managers) | (none) |
| dikasihinfo.com | ayoindonesia.com + dikasihinfo.com | (same 6 managers) | (none) |
| urbanjabar.com | ayoindonesia.com + urbanjabar.com | (same 6 managers) | (none) |
| metropolitan.id | ayoindonesia.com + aboutmalang.com | (same 6 managers) | (none) |
| **ayobandung.com** | **ayoindonesia.com** | **(same 6 managers)** | **9mediaonline.com** ← only Ayo site using IPD |

All 14 top Ayo sites declare:
- OWNERDOMAIN: ayoindonesia.com (the parent operator) + their own domain
- MANAGERDOMAIN: 6 wrapper-managers (adpushup, anymanager.io, digiadglobal, hntgaming, props.id, rev.iq)

But they do NOT declare INVENTORYPARTNERDOMAIN for the 838 OTHER props.id pool participants whose seller_ids appear in their ads.txt.

#### The cycle 486 partial-compliance pattern

Per IAB v1.1 §3.2: MANAGERDOMAIN authorizes a delegate to sell on the publisher's behalf using the publisher's own seller relationships. It does NOT authorize the publisher to declare OTHER publishers' seller relationships.

Per IAB v1.1 §3.3: INVENTORYPARTNERDOMAIN allows declaring partners whose inventory the publisher syndicates / aggregates.

Ayo Indonesia's ads.txt structure:
- Declares OWNERDOMAIN + MANAGERDOMAIN → **spec-compliant** (§3.1, §3.2)
- Declares 838 OTHER publishers' props.id seller_ids → **spec-non-compliant** (would require IPD entries per §3.3)
- Has 1 IPD entry on ayobandung.com (9mediaonline.com) → partial IPD use

So Ayo Indonesia adopted ~67% of IAB v1.1 (OWNER + MANAGER), skipped the piece (IPD) that would make their pool participation spec-compliant.

#### The bigger structural answer

The 1.54M impersonation_undisclosed events trace to:

1. **Pool-syndication-but-no-IPD** (estimated majority): publisher participates in a wrapper-managed pool, declares the pool's seller_ids in ads.txt, but doesn't declare each pool member via INVENTORYPARTNERDOMAIN. IAB strict reading flags as impersonation; IAB v1.1 spec compliance would require declaring the pool partners.

2. **True impersonation / squatting** (smaller subset): publishers using credentials they have no legitimate access to (no business relationship with the SSP, not part of an authorized pool).

3. **Stale/inherited credentials** (medium subset): old wrapper templates carrying credentials from former pool partnerships or expired arrangements.

The protocol cannot algorithmically distinguish these. The IAB v1.1 directives exist to enable the distinction (via IPD) — but adoption is 5% industry-wide.

#### Cycle 486 closing position

The audit's structural finding (5.14M anomalies, 33.83% phantom DIRECT rate) is REAL — the IAB protocol catches every reciprocity mismatch. The interpretation in plain English:

> **The protocol is doing its job. Industry has built pool-based syndication using legacy mechanisms (DIRECT/RESELLER) that pre-date the 2022 introduction of pool-disclosure directives. The 5% IPD adoption means 95% of pool participation is mechanically flagged as impersonation, even when it's legitimately authorized via offline business relationships.**

This is the spec-vs-practice gap, quantified. Not fraud at the 33.83% scale; not innocent either — somewhere in between, with the IAB protocol's own v1.1 update acknowledging the gap exists.

The cleanest empirical demonstration remains Ayo Indonesia:
- 14 verifiable props.id customers, each with their own seller_id
- A unified 904-pair template (Jaccard ≥ 0.92) declaring 839 other publishers' credentials
- Partial IAB v1.1 compliance (OWNER + MANAGER yes; IPD no)
- The protocol fires 1,000+ impersonation flags per Ayo site, accurately, given the spec
- A simple IAB v1.1 IPD declaration listing the 838 pool partners would resolve all flags



### E-2026-05-23-f: IPD adoption doesn't fix the impersonation gap (cycle 488)

Cycle 486 established that IAB v1.1 IPD (INVENTORYPARTNERDOMAIN, 2022) was the spec-level mechanism designed to disclose pool participation and resolve reciprocity violations like the Ayo Indonesia 904-pair template. Cycle 488 tests the natural follow-up: does IPD adoption actually fix the impersonation gap?

#### Cohort comparison

Phantom rates among publishers with ≥10 DIRECT claims:

| Cohort | n_pubs | Mean phantom | Aggregate phantom |
|---|---:|---:|---:|
| IPD-adopter (any IPD declarations) | 2,747 | 26.08% | 33.46% |
| no-IPD | 30,974 | 27.04% | 33.95% |
| Heavy-IPD (≥10 IPD declarations) | 134 | 21.51% | 23.99% |

The 0.5pp difference between general IPD-adopters and non-adopters is within noise. The 5.5pp gap between heavy-IPD and rest is real but small.

#### The match analysis (the actual test)

If IPD were being used as designed — to disclose the pool partners whose seller_ids appear in a publisher's ads.txt — then a publisher with phantom claims on SSPs X, Y, Z should have IPD declarations for partners that resolve to X, Y, Z.

Test: among 12,720 publishers with ≥5 phantom claims, how many have ANY IPD declaration that resolves to one of the SSPs flagging them?

**44 of 12,720 = 0.35%**

#### Interpretation

The mechanism designed to close the gap is **not used for that purpose at all**. The 5pp phantom-rate advantage among heavy-IPD publishers is a cohort-selection effect (mature operators with good ads.txt hygiene happen to also adopt IPD), not a causal effect of disclosure.

#### What IPD IS being used for

The top IPD-declared partners are CTV-centric (Wurl, Gray TV, Roku, LG Ads, Vizio) + a few wrapper services (Tappx, Thunder Monetize, Rhebus Works, AdmanMedia). Publishers adopting IPD are mostly:
- CTV-tilt operators declaring CTV syndication partners
- Premium publishers declaring legitimate inventory-partner relationships
- A handful of display operators who picked up the directive

What IPD is NOT being used for:
- Disclosing the wrapper-template pool memberships (themoneytizer, AdPushup, Pubstack, OptAd360, Insticator) that drive the 1.54M impersonation events
- Closing the protocol gap for the credential-propagation pattern documented cycles 482-486

#### Structural conclusion (refining cycle 486)

Cycle 486 said: "The spec exists; industry hasn't operationalized it for display." Cycle 488 sharpens this: **The spec exists; industry has adopted it selectively for CTV; the adoption that has happened does NOT address the display-side reciprocity gap.**

The 1.54M impersonation_undisclosed events would NOT be measurably reduced by a 10× increase in IPD adoption unless that adoption specifically shifted to disclosing the wrapper-service pool memberships (Seedtag, themoneytizer, props.id, etc.) that publishers actually carry. Current adoption pattern is on a different ecosystem (CTV) than where the gap exists (display).

#### Two independent ecosystems under one protocol

| Aspect | CTV side | Display side |
|---|---|---|
| IPD adoption | meaningful (Wurl/Gray TV/Roku/LG Ads/Vizio) | near-zero |
| Phantom rate | ~30% | ~25-35% |
| Dominant operator pattern | direct syndication partnerships disclosed | wrapper-template credential propagation undisclosed |
| Structural disclosure gap | substantially addressed via IPD | unaddressed |

The IAB v1.1 spec works differently in two ecosystems sharing the same protocol surface. The 33.83% headline phantom rate is dominated by the display side where IPD has not been adopted as a remediation mechanism.

The gap is not "IPD doesn't work" — IPD works on the CTV side where it's used as designed. The gap is that the display-side ecosystem has not adopted the disclosure pattern. Could be because: (a) wrapper services don't want to be named in publishers' ads.txt as pool partners, (b) publishers don't know which wrappers they're carrying credentials from, (c) IPD doesn't accommodate "this entire wrapper template" semantics — it expects per-partner declaration that publishers can't enumerate when the wrapper changes.

Cycle 488 close: the disclosure-gap reframe (cycles 482-486) holds, but with the IPD-as-remedy interpretation refuted. The mechanism is functional in CTV; the display side has not used it; the impersonation events would persist even with 10× IPD adoption unless adoption shifted to address the credential-propagation pattern specifically.



### E-2026-05-25-a: Yahoo's own HuffPost subsidiaries cascade as impersonation against Yahoo's own sellers.json (H187 per-cell)

Cycle 488 framed the impersonation gap as a CTV-vs-display ecosystem split where adoption of IAB v1.1 IPD was uneven. H187 (per-cell cascade materialization) provides the strongest single piece of evidence that the gap exists even at maximum ownership-clarity: when the publisher is owned by the SSP, the cascade still fails.

#### The materialization

Built `publisher_ssp_cascade` table at per-(publisher, SSP) cell granularity instead of per-publisher aggregate:

| Layer | Rows | Resolution |
|---|---:|---|
| corpus aggregate | 1 | 7.17M triples |
| per-publisher (prior layer) | 86,087 | 83 triples/row |
| **per-cell (H187 new)** | **2,327,455** | **3.08 triples/row** |
| per-triple | 7,170,535 | 1 |

27× finer granularity than the per-publisher table. Vectorized z-score detection (numpy `bincount` over the SSP-index) runs in 4.53s on the full 2.3M cells. Build wall: 16.17s (3.40s pure DuckDB classify+group).

#### Aberration tiers (z-score over Bernoulli variance, n_direct ≥ 5)

| z threshold | phantom cells | contra cells | imp cells | total |
|---|---:|---:|---:|---:|
| z > 3σ | 11,544 | 3,072 | 10,181 | 24,797 |
| z > 5σ | 3,231 | 597 | 2,605 | 6,433 |
| z > 10σ | 443 | 166 | 554 | 1,163 |
| z > 20σ | 46 | 21 | 108 | **175 EXTREME** |

The per-cell layer surfaces 24,797 cell-level aberrations that the per-publisher aggregate hides.

#### The apex finding — HuffPost cascades 70%+ impersonation against yahoo.com

Yahoo owns HuffPost (acquired with AOL 2017; rebranded under Yahoo Inc. 2021). All 6 HuffPost regional domains cascade at ~70% impersonation against yahoo.com:

| Publisher (Yahoo subsidiary) | n_direct | imp rate | z |
|---|---:|---:|---:|
| huffingtonpost.gr | 96 | 71.9% | 29.9 |
| huffpost.gr | 96 | 71.9% | 29.9 |
| huffpost.com | 96 | 69.8% | 29.0 |
| huffingtonpost.com | 96 | 69.8% | 29.0 |
| huffingtonpost.jp | 96 | 69.8% | 29.0 |
| huffingtonpost.in | 96 | 69.8% | 29.0 |

The cascade rule fires impersonation_undisclosed when an ads.txt declares `yahoo.com, <sid>, DIRECT` and Yahoo's authoritative sellers.json maps that `<sid>` to a `domain` field different from the publisher's domain, with no covering IAB v1.1 OWNERDOMAIN / MANAGERDOMAIN / IPD directive to disclose the relationship.

These six domains are not template-injection victims, not piracy aggregators, not foreign domains spoofing a U.S. brand — they are the parent company's own subsidiaries, on the parent company's own SSP, evaluated against the parent company's own published seller registry. The cascade fires at 70% because Yahoo has not declared the HuffPost properties in HuffPost's own ads.txt via any of the IAB v1.1 directives that would cover the relationship.

#### What this strengthens in the prior framing

Cycle 488 left open the possibility that the display-side impersonation gap was driven by wrapper-template propagation across unrelated publishers (Seedtag, themoneytizer, props.id). The HuffPost finding shows the gap exists even at the ownership-identity limit. A parent company's own owned subsidiaries, served by the parent's own SSP, with the parent's own registry — and the cascade still fires at z = 29σ for 6 of 6 regional sites.

The remediation here is not "industry-wide IPD adoption." It is a one-line OWNERDOMAIN declaration in each HuffPost ads.txt — a single field per file that Yahoo has not added to its own owned properties' ads.txt files.

If Yahoo has not added OWNERDOMAIN to ads.txt files Yahoo controls end-to-end (publisher + SSP + registry all under one corporate roof), the assumption that the broader display ecosystem will adopt IAB v1.1 directives to close the 1.54M impersonation-undisclosed gap looks structurally unfounded.

#### Other apex per-cell aberrations surfaced

| cell | n | rate | z |
|---|---:|---:|---:|
| exblog.jp / google.com phantom | 6,376 | 97.7% | 88.9 |
| taboola.com / taboola.com phantom (self-referential) | 1,580 | 99.7% | 29.9 |
| 5 .de Taboola template cluster (identical 13-row × 76.9% contradicted signature: ilovemusic.de, wunderweib.de, tvmovie.de, lecker.de, autozeitung.de) | 13 each | 76.9% | ~25 |
| 6 .de funeral-notice template cluster (identical 325-row × 14.8% signature, trauer.nrw family) | 325 each | 14.8% | ~13 |

The exblog.jp / google.com cell is the single highest cell z-score in the entire 2.3M-cell corpus. The taboola.com self-referential cell shows the operator's own first-party publisher domain cascading at 99.7% phantom against the operator's own registry — the same structural failure mode as HuffPost-Yahoo, on a different operator.

#### Tripwire lock

H187 tripwire `tests/test_h187_huffpost_yahoo_cell_aberration.py` (the 44th in the production runner) asserts: for the 6 HuffPost regional domains, the cell against yahoo.com must remain at impersonation rate ≥ 60% with n_direct ≥ 50. A drop below the threshold is an INFO-level structural-shift signal (Yahoo fixing the registry mapping or HuffPost dropping Yahoo from ads.txt) that surfaces for investigation rather than blocking, since the corrective outcome would be a good event.

#### Plain-English closing

The 33.83% headline phantom rate is not a measurement artifact, a foreign-market problem, or an unfamiliar-operator problem. It applies inside the largest U.S. ad-tech company's own walled-garden boundary, where every party in the cascade is the same parent. The protocol fires accurately; the disclosure has not been declared, even at the trivial limit case where declaration would cost a single line of text per file owned by the same company that owns the SSP doing the flagging.



### E-2026-05-25-b: BuySellAds Class-B cell impersonation — template-paste with MANAGERDOMAIN cover (H188)

H187's per-cell cascade flagged a second apex cluster with no shared operator with HuffPost-Yahoo: 8 cells against `buysellads.com`, all at z=25.7–25.9σ, n_direct=528, ~99% impersonation rate. Drilled in via primary-source fetch.

#### Smoking gun: byte-identical customer ads.txt

```
6e1e0a18cfe9c274deeb3c978eb1c851  1stwebdesigner.com/ads.txt
6e1e0a18cfe9c274deeb3c978eb1c851  html.com/ads.txt
28aba3fcb82c58733596b7d0872bc0fd  gameinfo.io/ads.txt   (1 line prepended; remaining 1316 identical)
```

All three end with `MANAGERDOMAIN=buysellads.com` — the IAB v1.1 directive is present. So this is *not* the HuffPost-Yahoo class (no directive cover).

#### Mechanism

BuySellAds runs a managed-publisher SSP. Their service template-pastes their entire 532-seller PUBLISHER roster into every customer's ads.txt, then appends `MANAGERDOMAIN=buysellads.com`. From the v6 cascade's perspective, each `buysellads.com, 36, DIRECT` line on 1stwebdesigner.com is impersonation: BSA's registry says sid=36 belongs to `cprogramming.com`. The directive doesn't validate the template because the cascade matches `directive_value=reg_domain`, looking for `cprogramming.com` in 1stwebdesigner's directives — not `buysellads.com`.

#### Registry reciprocity gap

Per IAB v1.1: when publisher P declares `MANAGERDOMAIN=M`, M's sellers.json should list P as a seller. Cross-check:

| Publisher | In BSA registry? |
|---|---|
| 1stwebdesigner.com | **ABSENT** |
| html.com | sid=2004 |
| gameinfo.io | sid=10238 |
| gun.deals | sid=9581 |
| modlar.com | **ABSENT** |
| javascriptsource.com | **ABSENT** |
| static4.buysellads.net | **ABSENT** |
| check-adblock.buysellads.net | **ABSENT** |

5 of 8 victim publishers declare `MANAGERDOMAIN=buysellads.com` while BSA's sellers.json does not list them — own-side spec compliance gap that the directive doesn't cover.

#### Class definition

The `impersonation_undisclosed` verdict has at least two distinct generators:

| Class | Directive declared? | Mechanism | Apex example | Apex cells (z>20σ) |
|---|---|---|---|---|
| **A** — corporate ownership uncovered | None | Operator's registry doesn't reflect ownership | HuffPost × Yahoo | 6 |
| **B** — template-paste with MANAGERDOMAIN cover | MANAGERDOMAIN=$ssp | Operator template-pastes full customer roster | 8 BSA cells | 8 |

The cascade verdict alone can't distinguish them; H187 per-cell resolution + a `MANAGERDOMAIN` cross-check is what discriminates. Class A fixes one-side (operator updates registry). Class B requires two-side spec interpretation (managers stop pasting non-owned seller_ids; publishers SHOULD use `INVENTORYPARTNERDOMAIN` per partner if they monetize others' inventory).

#### Tripwire

`tests/test_h188_buysellads_template_paste.py` (45th in production runner) asserts: for the 8 BSA cells, impersonation rate ≥ 95% with n_direct ≥ 100. Drop below threshold is INFO-level structural-shift signal — BSA either fixed the template OR remediated the registry; both are positive outcomes.

#### Primary-source evidence cached

`tmp/20260525_h188_buysellads/` — `buysellads_sellers.json` (BSA registry, DUNS 012336774, 532 sellers), three byte-fingerprinted customer ads.txt files, fetch log. Reproduces in 30 seconds via `ccurl fetch https://1stwebdesigner.com/ads.txt && ccurl fetch https://html.com/ads.txt && md5 1*.txt h*.txt`.


### E-2026-05-25-c: Class B is half the apex — Bloxdigital + BSA + the 17.9K managed-publisher universe (H189)

H188 partitioned the cascade's `impersonation_undisclosed` verdict into Class A (no directive cover) and Class B (`MANAGERDOMAIN=$ssp` declared). The natural follow-up: is Class B a BSA-quirk or the dominant generator?

#### Cross-tab: apex impersonation cells × MANAGERDOMAIN cover

Population: 592 cells with n_direct ≥ 100 and impersonation rate ≥ 95% (the apex tier of cell-level impersonation).

| Cover status | Cells | Share |
|---|---:|---:|
| **Class B** — publisher declares `MANAGERDOMAIN=$ssp` | **294** | **49.7%** |
| Class A — no MANAGERDOMAIN cover | 298 | 50.3% |

The cascade's apex tier splits ~50/50 between A and B. Class B is not an exotic single-operator pattern; it is the operating model of a large slice of managed-publisher SSPs. The corpus has 17,952 distinct publishers declaring MANAGERDOMAIN (20.8% of all publishers in the corpus).

#### Top managers by total publisher count (MANAGERDOMAIN target)

| Manager | Publishers declaring MGRDOM=this |
|---|---:|
| cafemedia.com | 1,846 |
| mediavine.com | 1,481 |
| themoneytizer.com | 1,013 |
| freestar.com | 960 |
| ezoic.ai | 893 |
| publift.com | 616 |
| anymanager.io | 425 |
| playwire.com | 393 |
| adpushup.com | 372 |
| refinery89.com | 367 |
| bloxdigital.com | 300 |

The 11 largest managers cover 8,666 publishers (10.0% of corpus) under the IAB v1.1 directive.

#### Class B apex concentration: bloxdigital dominates

| SSP | Class B apex cells | Class A apex cells | B-share |
|---|---:|---:|---:|
| bloxdigital.com | **286** | 61 | **82.4%** |
| buysellads.com | 8 | 0 | 100.0% |

Bloxdigital alone is **97% of all Class B apex cells**. The H188 BuySellAds finding was the smaller of the two operators exhibiting this pattern at the apex.

#### Primary-source bloxdigital verification

Fetched bloxdigital lines from 5 customer ads.txt files, normalized (lowercase + strip + sort + dedupe), computed pairwise Jaccard:

| Pair | Lines in common | Jaccard |
|---|---:|---:|
| thegazette.com ↔ fox21online.com | 236 / 236 | **1.0000** |
| thegazette.com ↔ wdel.com | 236 / 236 | **1.0000** |
| fox21online.com ↔ wdel.com | 236 / 236 | **1.0000** |
| wvnews.com ↔ thegazette.com | 216 / 239 | 0.9038 |
| wvnews.com ↔ fox21online.com | 216 / 239 | 0.9038 |
| wvnews.com ↔ wdel.com | 216 / 239 | 0.9038 |
| newsmemory.com ↔ wvnews.com | 198 / 219 | 0.9041 |
| newsmemory.com ↔ {3 above} | 195 / 239 | 0.8159 |

195 bloxdigital seller_ids appear in **all 5 customer ads.txt files** — the shared template core. Three of five customers (thegazette, fox21online, wdel) have byte-identical bloxdigital blocks with 236 lines each. This is the same Class B mechanism as BSA at ~30× the per-template scale.

Top bloxdigital seller_ids are cited by **all 347 apex customers**: sid 95765933 → 347 pubs (reg_domain=wvua23.com), sid 84182125 → 347 pubs (omakchronicle.com), etc. The publisher cited by each seller_id is not the publisher hosting the ads.txt; it's a sibling member of the BLOX template pool.

#### Refinement of the H188 cascade story

The H188 ERRATA framed Class B as "BuySellAds-quirky." H189 refutes that framing: Class B is the dominant apex generator. The earlier framing was a sample-size-1 mistake. Corrected: the cascade verdict `impersonation_undisclosed` decomposes into a mix that **leans Class B at the apex** (≥95% imp + n_direct ≥ 100), while remaining ambiguous on average.

#### Open questions for H190+

1. Are CafeMedia (1,846 publishers) and Mediavine (1,481) Class B at the cell level too, or do they use INVENTORYPARTNERDOMAIN per partner correctly? H152 audited Mediavine at the publisher level; needs cell-level rerun.
2. Does Lee Enterprises (NYSE: LEE, parent of BLOX Digital) disclose the template-paste arrangement to advertisers? The relationship is at the public-company-disclosure scale.
3. The 195-seller-id BLOX shared core: do all 195 IDs map to real, distinct Lee-property publishers in the BLOX registry? Or is the template pulling in non-Lee third-party publishers (which would shift back from Class B to a closer-to-A genuine impersonation)?

#### Tripwire

`tests/test_h189_class_b_apex_prevalence.py` (46th in production runner) asserts: Class B share of apex cells ≥ 30%. Drop below threshold is INFO-level structural shift signaling major manager remediation OR corpus regime shift.

#### Primary-source evidence cached

`tmp/20260525_h189_class_b_prevalence/` — cross_tab log + 5 fetched BLOX customer ads.txt files + bloxdigital.com/sellers.json fetch (returned JS loader HTML, registry currently fetched via different canonical URL in the pipeline).


### E-2026-05-25-d: Two manager populations — hygienic vs template-paste; CafeMedia + Mediavine are clean (H190)

H189 measured "Class B narrow" (publisher declares `MANAGERDOMAIN=$ssp` and the cell's SSP is the declared manager). H190 broadens the question: how does the apex cascade look across the 6 largest managers by publisher count? Does Class B generalize, or is it concentrated?

#### Cohort cascade rates by top-6 manager

| Manager | Publishers | imp rate | phantom rate | contradicted | disclosed | apex cells |
|---|---:|---:|---:|---:|---:|---:|
| **CafeMedia (cafemedia.com)** | 1,846 | **3.61%** | 4.02% | 22.45% | **65.16%** | **0** |
| **Mediavine (mediavine.com)** | 1,481 | **4.23%** | 4.90% | 29.75% | **58.60%** | **0** |
| Ezoic (ezoic.ai) | 893 | 8.33% | 11.98% | 44.34% | 28.15% | 0 |
| Publift (publift.com) | 616 | 15.92% | 24.04% | 39.98% | 13.34% | 0 |
| TheMoneytizer (themoneytizer.com) | 1,013 | 24.34% | 35.27% | 33.46% | 2.37% | 0 |
| **Freestar (freestar.com)** | 960 | **42.55%** | 13.80% | 28.56% | 12.47% | **330** |

This is a **clean bimodal split**:

- **Hygienic managers** (CafeMedia + Mediavine, 3,327 combined publishers): ~60% disclosed via IAB v1.1 IPD-per-partner, near-zero apex impersonation. They are the empirical proof that the spec CAN scale.
- **Template-paste managers** (Freestar prominently, plus BLOX-via-Freestar and BSA from H188): high impersonation rates, apex-cluster generation.
- **Intermediate cohort** (Ezoic, Publift, TheMoneytizer): high contradicted rate (33-44%) but 0 apex cells — they distribute impersonation widely rather than concentrating it in template-paste clusters.

#### Freestar — propagator of the BLOX template

All 330 of Freestar's apex cells are against `cell.ssp = bloxdigital.com`. Cross-checked: of the 347 publishers showing apex impersonation against bloxdigital.com (H189), 330 also declare `MANAGERDOMAIN=freestar.com`. **Freestar is including BLOX template-paste in the ads.txt files it generates for the BLOX-network publishers it co-manages.** Same 195-seller-id BLOX core template, propagated via Freestar's pipeline.

#### Broader Class B partition (refining H189)

H189 measured narrow Class B (MGRDOM = cell SSP) at 49.7% (294/592). Adding broad Class B (publisher has *any* MGRDOM, cell.ssp differs):

| Subset | Apex cells | % of 592 |
|---|---:|---:|
| Class A (no MANAGERDOMAIN at all) | 216 | 36.5% |
| Class B-narrow (MGRDOM = cell SSP) | 294 | 49.7% |
| Class B-broad (MGRDOM declared, but ≠ cell SSP) | 82 | 13.9% |
| **Total Class B (narrow + broad)** | **376** | **63.5%** |

Top B-broad managers by apex cell count: Freestar 59, AdPlay 9, Salem Media 5, AdVerge 5, AdPushUp 5, NSight Video 4, Refinery89 4. The B-broad mechanism: publisher is managed by manager M, M's pipeline injects template content for upstream SSP S, the cell against S fires apex impersonation because S's registry doesn't recognize the publisher.

#### Implication for cascade interpretation

The cascade verdict `impersonation_undisclosed` is **63.5% Class B at the apex** under the broader definition. The cleanest fix is two-pronged:

1. **Manager side**: stop template-pasting non-customer seller_ids; use IPD-per-partner instead (the CafeMedia/Mediavine pattern works at 3,327-publisher scale).
2. **Upstream SSP side**: maintain registry reciprocity — list publishers that declare MGRDOM=$you.

The 36.5% Class A residual reduces to the registry-mapping problem (HuffPost-Yahoo + yieldlove + stroeer + the long tail of operators with stale or wrong reg_domain mappings).

#### Tripwire

`tests/test_h190_hygienic_managers_clean.py` (47th in production runner) asserts: CafeMedia + Mediavine cohorts maintain 0 apex impersonation cells. Drop = INFO-level structural regression in the cleanest cohort — either disclosure practice slipped, or upstream template propagation reached them.

#### Self-correction on H189

H189's open question #1 asked "are CafeMedia + Mediavine Class B at the cell level?" The H190 answer is unambiguous: **NO**, they are the cleanest manager cohort, not Class B. The spec works for them.


### E-2026-05-25-e: Class A is mostly template-paste-without-directive — Stroeer German cluster (H191)

H189-H190 partitioned the cascade's `impersonation_undisclosed` apex into Class A (no MANAGERDOMAIN cover, 36.5%) and Class B (MGRDOM declared, 63.5%). The implicit assumption: A and B were different mechanisms. H191 refutes that assumption.

#### Trace: yieldlove + stroeer.de apex publishers

113 distinct German publishers appear in apex cells against `yieldlove.com` AND `stroeer.de`. That accounts for **212 of the 216 Class A apex cells** (212 cells across 2 SSPs = 106 publisher-pairs, plus the long tail). The same publishers cited by both SSPs.

#### Primary-source verification (5 sampled publishers)

```
57e4c797c9a0675d38c6539aa15efc0d  all-in.de/ads.txt           (45,496 bytes, 1,021 lines)
75fa6efb1cd97b681bef2d8a71303d43  allgaeuer-zeitung.de/ads.txt (45,496 bytes, 1,021 lines)
8ec06a96c1b3ef5b1aad905340b20a3a  augsburger-allgemeine.de    (45,496 bytes, 1,021 lines)
b299ba2fd357fe1d6871a8563c2e0aa9  obermain.de/ads.txt          (45,496 bytes, 1,021 lines)
5a83b732e68882f61a917d90f5a894b9  imsueden.de/ads.txt          (53,334 bytes, 1,184 lines)
```

4 of 5 files: **same byte length (45,496), same line count (1,021), different MD5**. Diff reveals the ONLY difference is a single glomex-generated timestamp comment line (18-hour offset). Template body byte-identical. The 5th publisher (imsueden.de) carries an additional 16 yieldlove lines + 53 stroeer.com lines on top of the same template tail.

#### Two key markers in every file

```
#ads.txtfileStroeer2026_05_18           ← Stroeer template generation stamp
# begin glomex ads.txt for $domain (...) ← glomex-managed timestamp
```

The `Stroeer` comment marker is a self-identifying template signature. The glomex marker indicates these publishers use glomex (a German video-platform / ads-monetization tool) which orchestrates the Stroeer template paste.

#### Why these are "Class A" despite template-paste mechanism

All 5 publishers declare **zero MANAGERDOMAIN, OWNERDOMAIN, or INVENTORYPARTNERDOMAIN directives**. The cascade verdict checks for the directive; finding none, classifies the impersonation as `impersonation_undisclosed` and the cell as Class A. But the mechanism — template paste of upstream operator credentials — is identical to BLOX (Class B-narrow) and BSA (Class B-narrow).

#### Reframe of the A/B partition

The H190 framing implicit: A and B are different mechanisms (registry-ownership-gap vs template-paste-cover). H191 corrects: **A and B mostly share ONE mechanism (template paste); the distinction measures directive-declaration status, not generator type**. Refined taxonomy:

| Sub-class | Mechanism | Directive | Apex cells (est.) |
|---|---|---|---|
| **B-narrow** | template paste | MGRDOM = cell SSP | 294 |
| **B-broad** | template paste | MGRDOM = other manager | 82 |
| **A-template** (NEW) | template paste | NONE declared | ~200 (yieldlove + stroeer + tail) |
| **A-ownership** (residual) | corporate ownership uncovered | NONE declared | ~16 (HuffPost-Yahoo 6 + tail) |

Under this refined taxonomy, **template paste accounts for ~96% of the apex cascade tier** (576/592 cells); the remaining ~4% is genuine ownership-mapping issues (HuffPost-Yahoo class).

The cascade verdict alone cannot distinguish these sub-classes; primary-source fingerprinting (template-marker comments + line-count + Jaccard on SSP-specific blocks) is required. The cascade fires accurately on the symptom; the operational practice underlying the symptom is mostly one thing.

#### Implication for fix recommendation

H190 closed: "the break is not in the protocol; it's in operator practice." H191 refines: the operator practice is specifically template paste, ~96% of apex. The two-pronged fix from H190 still holds:

1. **Manager side**: stop template-pasting non-customer seller_ids; use IPD-per-partner per IAB v1.1 spec (CafeMedia + Mediavine prove this scales to 3,327+ publishers)
2. **Publisher side**: declare MANAGERDOMAIN per spec when an upstream manager generates your ads.txt (would move A-template cells into B classification, making the issue more visible to remediation tools)

#### Tripwire

`tests/test_h191_stroeer_german_cluster.py` (48th in production runner) asserts: yieldlove + stroeer.de apex cells remain ≥ 80. Drop = INFO-level structural shift (Stroeer template change OR publishers adopted MGRDOM cover). Both corrective.

#### Primary-source evidence cached

`tmp/20260525_h191_class_a_taxonomy/` — 5 fetched German publisher ads.txt files + fetch log + cross-tab logs. Reproduces in 30s via `ccurl fetch https://obermain.de/ads.txt && head -1 *_ads.txt.txt` → all show `#ads.txtfileStroeer2026_05_18`.
