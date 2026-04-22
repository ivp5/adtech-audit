# Fabricated Authorization: A Large-Scale Analysis of ads.txt Integrity in Programmatic Advertising

## Abstract

The ads.txt standard, introduced in 2017, allows publishers to declare authorized sellers of their advertising inventory. We present the first large-scale cross-verification of these declarations against SSP sellers.json registries. Analyzing 2,096,507 DIRECT authorization claims across 23,283 publishers against 710 SSP registries containing 1.89 million seller entries, we find that 29% of DIRECT claims are unambiguously false — the SSP's own registry classifies the account as INTERMEDIARY, directly contradicting the DIRECT claim. A further 28% reference seller IDs absent from the registry. Together, 57.1% of claims fail verification. The phantom rate (28%) is ambiguous; 100% of numeric phantom IDs fall within valid ranges for their SSP, consistent with either deleted accounts or fabrication. A follow-up fetch of 238 additional SSP registries (covering 224,222 new seller IDs) reclassified only 2.7% of existing phantoms to PLAUSIBLE, indicating fabrication dominates staleness by ~36:1. The contradicted rate (29%) is unambiguous, and represents the largest systematic authorization failure documented in programmatic advertising.

The sharpest single case: Taboola Inc., a publicly-traded ($TBLA, $1.7B revenue) content-recommendation SSP, classifies 1,576 of 1,580 Taboola-account DIRECT claims (99.75%) on its own corporate property taboola.com as phantom relative to its own sellers.json registry. The same pattern recurs on its content property taboolanews.com (3,694 phantom of 3,694 Taboola-account claims, 100%). This is not third-party publisher error: it is an SSP contradicting its own disclosed registry on its own website. A second-sharpest case involves Themoneytizer, a header-bidding wrapper whose ads.txt template at `ads.themoneytizer.com/ads_txt.php` declares `smartadserver.com, 1097, DIRECT`; SmartAdServer's sellers.json classifies seller_id 1097 as INTERMEDIARY named "Themoneytizer." The template has served unchanged since January 2024 and is propagated to 1,108 publisher ads.txt files.

We trace the mechanism to template injection by intermediary companies. 31 intermediaries have seller accounts falsely claimed as DIRECT by over 1,000 publishers each, and cross-referencing against the intermediaries' own registries reveals that 95-100% of these publishers have no business relationship with the intermediary. The false claims originate from the intermediaries themselves — who classify their own accounts as DIRECT on their own websites despite being registered as INTERMEDIARY at the SSPs — and propagate through header bidding wrapper providers. An analysis of 195 wrapper providers via the ads.txt 1.1 MANAGERDOMAIN field shows false rates ranging from 7.8% to 81.4%, demonstrating that active management can reduce but not eliminate contamination. The same methodology applied to 4,992 mobile app-ads.txt files produces a false rate within 0.3 percentage points of the web rate, confirming the structural nature of the finding. All 72 web mega-injector template pairs appear in both markets.

These results demonstrate that the authorization framework produces more false claims than true ones. Nine years after introduction, the false rate has not converged toward zero — it has converged toward 57%. We release the complete dataset, 195-provider scorecard, and verification tools for independent reproduction.

## 1. Introduction

Programmatic advertising transacts approximately $600 billion annually through automated real-time bidding systems [1]. The opacity of these systems — where dozens of intermediaries may participate in a single impression transaction — created opportunities for fraud, most notably domain spoofing, in which attackers sell counterfeit impressions purporting to originate from premium publishers [2,3].

To address this, the Interactive Advertising Bureau (IAB) Tech Lab introduced the ads.txt standard in 2017 [4], followed by the complementary sellers.json specification [5]. Together, these create a two-sided authorization system: publishers declare which companies are authorized to sell their inventory (ads.txt), and SSPs declare the identity and type of each seller in their marketplace (sellers.json). A DIRECT designation in ads.txt indicates the publisher owns the seller account; RESELLER indicates a third party manages it. In sellers.json, accounts are classified as PUBLISHER (owns inventory), INTERMEDIARY (resells), or BOTH.

If the system functioned as designed, a DIRECT claim in a publisher's ads.txt would correspond to a PUBLISHER or BOTH classification in the SSP's sellers.json. When an ads.txt DIRECT claim corresponds to a sellers.json INTERMEDIARY classification, the authorization is contradicted by the very registry it claims to reference. When the seller ID does not appear in the registry at all, the authorization references a phantom account.

Prior work measured adoption and format compliance. Bashir et al. [6] conducted a 15-month longitudinal study of ads.txt adoption, finding that 62% of top-100K sites running RTB ads had adopted the standard by April 2019, and that major exchanges still purchased unauthorized inventory. However, no prior work has measured the *truthfulness* of DIRECT claims at scale — whether the declared relationships actually exist as described.

We present the first such measurement. Our contributions are:

1. **Scale**: Cross-verification of 2,096,507 DIRECT claims across 23,283 publishers against 710 SSP registries (1.89M seller entries), finding a 57.1% false rate that is stable across 11 successive SSP expansions (14→24→37→62→84→178→228→312→417→710→948 SSPs).

2. **Mechanism**: Identification of template injection as the primary mechanism, with 78.5% of contradictions originating from (SSP, seller_id) pairs shared by 100+ publishers. We trace the chain: intermediaries originate false claims on their own websites, wrapper providers distribute them via templates, publishers host them unknowingly.

3. **Fabrication**: Cross-reference against intermediaries' own registries shows 95-100% of publishers claiming DIRECT for mega-injector intermediaries have no relationship with those companies — the claims are for nonexistent business relationships.

4. **Accountability**: Analysis of 195 wrapper providers via the MANAGERDOMAIN field, producing a graded scorecard (7.8% to 81.4% false rate) showing that active file management can reduce contamination from 66% to 23%.

5. **Cross-market**: Verification of 4,992 mobile app-ads.txt files at approximately the same false rate as web (within 0.3pp), confirming the structural nature across web and mobile inventory.

We release the complete dataset, provider scorecard, and verification tools at https://github.com/ivp5/adtech-audit. An interactive browser-local verifier is at https://ivp5.github.io/adtech-audit/.

## 2. Methodology

### 2.1 Data Collection

**ads.txt harvest.** We probed 184,456 domains for ads.txt files, sourced from the Tranco top-1M popularity ranking and an automated Playwright browser crawler operating on a tiered schedule (4h/24h/72h revisit intervals). Of these, 25,598 domains returned valid ads.txt files containing at least one DIRECT claim. After deduplication by (publisher, SSP, seller_id) triple and filtering of malformed seller IDs (containing spaces, file paths, or non-ASCII characters), 23,283 publishers with 2,096,507 verifiable DIRECT claims remained.

**sellers.json collection.** We fetched sellers.json registries from 710 SSP domains, comprising 1,891,801 seller entries. Sources included direct fetches from SSP domains listed in publisher ads.txt files, the KONTRUSTMEDIA/adsdb open-source repository (543 files, MIT license), and historical batches collected between March 17-25, 2026. Google's registry (994,945 entries) is 71% confidential and was excluded from intermediary classification checks but included in phantom detection. Registry stability was verified by comparing 52,477 entries across two snapshots 5 days apart — 1 reclassification observed (0.002%).

**app-ads.txt collection.** We fetched 5,617 app-ads.txt files from mobile app developer websites via the KONTRUSTMEDIA repository, applying identical parsing and deduplication.

### 2.2 Cross-Verification

For each DIRECT claim (publisher, SSP, seller_id), we looked up the seller_id in the SSP's sellers.json registry:

- **CONTRADICTED**: The registry contains the seller_id with seller_type = INTERMEDIARY. The publisher claims DIRECT; the SSP says otherwise. Unambiguous.
- **PHANTOM**: The seller_id does not appear in the registry. Ambiguous — could represent a deleted account, a typo, or a fabricated ID.
- **PLAUSIBLE**: The registry confirms seller_type = PUBLISHER or BOTH. Consistent with a DIRECT claim.
- **UNCOVERED**: The SSP has no sellers.json registry. Classified as PLAUSIBLE (benefit of the doubt).

Lookups are case-insensitive. SSP domain aliases (e.g., sovrn.com → lijit.com) are maintained in a mapping table with 55 entries.

### 2.3 Template Injection Detection

We identify template injection by counting how many distinct publishers share each (SSP, seller_id) pair with a CONTRADICTED verdict. Pairs shared by 100+ publishers indicate template distribution rather than individual publisher error. We further identify the template source by:

1. Checking the MANAGERDOMAIN field in ads.txt 1.1 files to identify the managing wrapper provider.
2. Fetching known template URLs (e.g., ads.themoneytizer.com/ads_txt.php) and matching their DIRECT lines against the mega-injector pairs.
3. Cross-referencing publishers' ads.txt entries against the intermediary's own sellers.json to determine whether a business relationship exists.

### 2.4 Confidence Testing

- 200 randomly-sampled PHANTOM claims verified: all 200 seller_ids are absent from the registry in any case variant. Zero false positives.
- 50 randomly-sampled CONTRADICTED claims verified: all 50 confirmed as INTERMEDIARY in the SSP registry. Zero false positives.
- Google's effect: Google's 45% false rate is below the 57.1% average, so removing Google from the numerator and denominator leaves the inclusive rate essentially unchanged (moving by less than one percentage point under a range of assumptions about Google's PLAUSIBLE share, which we cannot compute exactly because 71% of Google's registry is confidential). This makes the inclusive rate conservative rather than Google-inflated.
- Stability: the false rate is stable across 11 successive SSP expansions (14→24→37→62→84→178→228→312→417→710→948 SSPs), varying between 55% and 58%. The 948-step was added on 2026-04-22: 238 additional SSP registries fetched, 22,928 existing phantoms rechecked, 2.73% reclassified to PLAUSIBLE. Staleness cannot account for the bulk of the phantom class.

### 2.5 Limitations

1. **Sample bias.** 23,283 publishers from Tranco top-1M plus a crawler piggyback harvest. Biased toward popular Western commercial sites.
2. **Point-in-time.** Registries are March 2026 snapshots. SSPs can reclassify sellers, though our temporal analysis shows this is rare (0.002% over 5 days).
3. **Phantom ambiguity.** 100% of numeric phantom IDs fall within valid ranges for their SSP, consistent with either deleted accounts or plausible fabrication. We report both the strict rate (29%, CONTRADICTED only) and inclusive rate (57%, CONTRADICTED + PHANTOM).
4. **MANAGERDOMAIN adoption.** Only a subset of publishers declare MANAGERDOMAIN, limiting wrapper provider attribution.
5. **First-visit bias.** Consent measurement reflects first-visit crawler behavior. Returning users with existing consent may show different patterns.
