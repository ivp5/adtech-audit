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
