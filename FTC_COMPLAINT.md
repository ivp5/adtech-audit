# FTC Complaint Draft

## Portal
https://reportfraud.ftc.gov/

## Category
Advertising/Marketing → False or Misleading Advertising

## Summary (for portal)
Major ad-tech companies are representing "DIRECT" publisher relationships that do not exist. 57% of such authorization claims in the ad supply chain are provably false when checked against the sellers' own published registries. The same intermediaries that classify themselves as INTERMEDIARY in their own disclosures are being claimed as DIRECT on thousands of publisher files, many of which trace back to templates the intermediaries themselves distribute.

## Detailed Complaint

I am submitting evidence that major advertising technology companies are systematically misrepresenting their supply chain authorization.

**The finding:** 57% of "DIRECT" authorization claims in publisher ads.txt files are false when cross-referenced against the SSP's own sellers.json registry. This represents 1,198,139 false claims affecting 17,081 publishers (out of 23,283 analyzed across 710 SSP registries; an April 2026 follow-up expanded the registry set to 948 and moved the headline rate by only 0.03 percentage points, demonstrating the finding is not an artifact of registry coverage).

**Why it matters to consumers:** The "DIRECT" label is a material representation in programmatic media buying. Advertisers routinely bid preferentially for DIRECT-authorized inventory on the premise of shorter supply paths, fewer hidden fees, and lower spoofing risk. When the DIRECT label is false, the advertiser is paying for a represented attribute that does not exist; that cost is ultimately priced into consumer products. The magnitude of the supply chain tax itself has been independently measured: the ISBA / PwC Programmatic Supply Chain Transparency Study (May 2020), conducted with 15 advertisers and 12 publishers representing roughly two-thirds of UK premium publisher programmatic revenue, found that approximately 50% of advertiser spend reaches publishers and that 15% is "unattributable" to any specific service. Our finding adds that a majority of the DIRECT designations within that spend are falsified relative to the sellers' own disclosures.

**Scale of affected companies** (top ten by false-claim count, computed 2026-04-22 from `release/false_direct_claims.jsonl`):
- Lijit (Sovrn): 79,453 false claims across 10,882 publishers
- Google: 74,030 false claims across 10,186 publishers (27% phantom; Google's sellers.json is 71% confidential by their own flag, limiting verifiability)
- Magnite (Rubicon Project): 71,944 false claims across 11,970 publishers (of these, 65% are CONTRADICTED — Magnite's own registry classifies the account as INTERMEDIARY)
- Taboola: 63,409 false claims across 2,781 publishers (99.75% of Taboola-account DIRECT claims on taboola.com itself are phantom in Taboola's own registry; 100% on taboolanews.com)
- OneTag: 58,328 false claims
- PubMatic: 48,354 false claims
- Index Exchange: 44,658 false claims
- OpenX: 42,074 false claims
- TripleLift: 39,204 false claims
- AppNexus / Xandr (Microsoft): 33,595 false claims

**The smoking-gun template:** `https://ads.themoneytizer.com/ads_txt.php` is a live URL, served by a named US-operating intermediary (The Moneytizer). Line 1 of that file reads `smartadserver.com, 1097, DIRECT`. SmartAdServer's own sellers.json at `https://smartadserver.com/sellers.json` classifies seller_id 1097 as INTERMEDIARY with the name "Themoneytizer." The template has served this exact content unchanged since at least January 2024 (archived by web.archive.org). It is copied into 1,108 publisher ads.txt files. The intermediary is therefore making a false DIRECT representation about its own account across a thousand-plus publisher properties.

**Evidence:** All data is publicly available. Each publisher serves ads.txt at their domain. Each SSP serves sellers.json at their domain. The cross-reference is mechanical. Complete methodology, row-level evidence (1.2M records), 195-provider wrapper scorecard, and interactive verification tool available at: https://github.com/ivp5/adtech-audit (interactive browser verifier at https://ivp5.github.io/adtech-audit/).

**Why this hasn't been caught:** Verification vendors check that claims *exist* in ads.txt, but not that they are *consistent* with sellers.json. Our cross-reference closes that gap. The check takes two HTTP requests and one seller_id lookup per claim; it is not computationally or technically difficult.

This is not isolated fraud — it is industry-wide systemic misrepresentation propagated by named templates from named intermediaries. We are not alleging criminal intent; we are submitting a measurable, reproducible record of the disclosure gap for the Commission's consideration.

---

## One-click mailto

```
mailto:advertising@ftc.gov?subject=Systematic%20Ad%20Supply%20Chain%20Misrepresentation%20-%20Evidence%20of%201.2M%20False%20Authorization%20Claims&body=I%20am%20reporting%20systematic%20misrepresentation%20in%20the%20digital%20advertising%20supply%20chain.%0A%0A57%25%20of%20%22DIRECT%22%20authorization%20claims%20in%20publisher%20ads.txt%20files%20are%20provably%20false%20when%20cross-referenced%20against%20the%20sellers%27%20own%20sellers.json%20registries.%20This%20affects%201%2C198%2C139%20claims%20across%2017%2C081%20publishers%20%28of%2023%2C283%20analyzed%29.%0A%0AComplete%20evidence%20package%20at%20https%3A%2F%2Fgithub.com%2Fivp5%2Fadtech-audit
```
