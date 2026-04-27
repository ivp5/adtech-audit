# Outreach Targets

> **Snapshot pin.** Per-company counts (Taboola 53,869, PubMatic 41,912, Magnite 62,495, Criteo 23,129) are at **2026-03-25** and **disagree** with FTC_COMPLAINT.md (Taboola 63,409, PubMatic 48,354, Magnite 71,944) — different snapshots, both shipped. Live DB (2026-04-27): Taboola 151,895, PubMatic 140,148, Magnite 193,313, Criteo 76,037. The "55% false rate" cited at L41 is the same as PAPER's 57.1%, rounded down. **Headline DIRECT-only false rate at 2026-04-27 is 61.1% in the verifiable-registry bucket** (28.5% CONTRADICTED + 31.6% PHANTOM, n=6.33M DIRECT). Pick one number per recipient before sending.

> **Corporate-name corrections (2026-04-27).** Three named operators in PAPER §1¶3 are referenced by their brand-domain rather than their registered corporate entity. For regulatory action, address the SL/SAS/SA, not the brand:
>
> | Brand (in our data) | Corporate / SEC entity | Country | Form | Registry source |
> |---|---|---|---|---|
> | SmartAdServer | Equativ SAS | France | SAS | Live `smartadserver.com/sellers.json` contact_email `quality-team@equativ.com` |
> | Seedtag | Seedtag Advertising SL | Spain | SL | Wayback rubicon 2021-02-11 snapshot |
> | Rich Audience | Pubnet Publicidad Y Marketing SL | Spain | SL | Wayback rubicon 2021-02-11 snapshot |
> | SunMedia | VLN Servicios Publicitarios Integrales SL | Spain | SL | Wayback rubicon 2021-02-11 snapshot |
> | Themoneytizer | Themoneytizer SA | France | SA | Per PAPER §1¶3 |
>
> Spanish operators fall under AEPD jurisdiction (Agencia Española de Protección de Datos); French operators under CNIL.

## Media (existing focus)
- AdExchanger, The Trade Desk, Digiday, WSJ/NYT tech desks

## Regulators

### FTC
- Bureau of Consumer Protection (ad fraud = deceptive practices)
- Angle: Advertisers pay 15-30% premium for "DIRECT" authorization that doesn't exist
- Contact: FTC complaint portal + direct to Bureau staff

### SEC  
- Public companies with material exposure (March 2026 corpus counts; 2026-04-27 live counts in parens):
  - **Taboola** (TBLA): 53,869 (live: 151,895) false claims, 96% phantom on own property. **Just converted from 20-F to 10-K 2026-02-25** — first as domestic registrant. FY2025 revenue **$1.91B**. 10-K marketing claim: *"All of our supply partners are directly connected"* — refuted by their own sellers.json on taboola.com (99.75% Taboola-account self-phantom).
  - **PubMatic** (PUBM): 41,912 (live: 140,148) false claims. FY2025 revenue **$283M** — only major SSP with revenue contraction. **Only one of seven major filers to mention "IAB Tech Lab"** (and only re: TCF/GPP, never authorization framework).
  - **Magnite** (MGNI): 62,495 (live: 193,313) false claims. FY2025 revenue **$714M**. Gross-to-net reporting trajectory 18% (2023) → 14% (2024) → 10% (2025) — material change in accounting basis. Also plaintiff in Google antitrust.
  - **Criteo** (CRTO): 23,129 (live: 76,037) false claims. **Just converted from 20-F to 10-K 2026-02-26** — first as domestic registrant. FY2025 revenue **$1.681B** (down 1% YoY, only contraction among non-SSP filers). **criteo.com/sellers.json redirects to themediagrid.com** (Commerce Grid) since at least 2021-07-27 — Criteo Classic retargeting publishes no public sellers.json.
  - **Trade Desk** (TTD): not in false-claim top-10 (DSP, not SSP). FY2025 revenue **$2.896B** (up 21%). 10-K mentions ads.txt: 0; sellers.json: 0; IAB Tech Lab: 0.
  - **Outbrain → Teads** (TEAD): post-merger Mar 2026, CIK 1454938 reassigned. Revenue **$1.30B**.
  - **LiveRamp** (RAMP): not an SSP but identity-graph operator. Revenue **$745.6M** (up 26%).
- Angle: False authorization = misrepresentation of inventory quality.
- 10-K filings make supply-chain representations (Taboola "directly connected", general "premium supply" language) but do NOT mention ads.txt or sellers.json — the IAB framework on which those representations depend. Across all 7 filings combined: **0 mentions of "ads.txt", 0 mentions of "sellers.json"**, 2 mentions of IAB Tech Lab (PubMatic only, TCF/GPP context). The disclosure-integrity issue documented here is invisible in the filers' primary regulatory disclosures. Materiality question for SEC staff under Rule 10b-5 (omission of material facts that would render existing statements misleading).

### EU Data Protection Authorities
- 0.012% valid consent on first visit = systematic GDPR violation
- 717,573 identity sync requests (updated from 272K)
- Angle: This isn't a bug, it's the design
- Contact: Irish DPC (most ad-tech HQs), French CNIL, German BfDI

### DOJ (US v. Google ad-tech antitrust)
- Google: 512K page appearances (91% of observed ad-tech)
- Meta: 51K (9%) — 10:1 dominance ratio
- 28,543 sites run full Google stack (GTM + GAM + Analytics + Ads)
- 93,162 sites bundle GTM + Analytics
- Angle: Quantified vertical integration across 332K page scans
- See: `DOJ_ANGLE.md` for full evidence

## Brand Safety Vendors (expose the gap)

### IAS, DoubleVerify, Oracle MOAT
- They verify ads.txt claims exist
- They DON'T verify claims are consistent with sellers.json
- Our finding: 55% false = their verification is incomplete
- Angle: Are you checking what you claim to check?

## Industry Bodies

### TAG (Trustworthy Accountability Group)
- Certified Ad Fraud list
- Our finding: 3,264 publishers share the same false Rubicon claim
- Angle: How is this "certified trustworthy"?

### IAB
- They wrote the specs (ads.txt, sellers.json)
- Our finding: Specs are being systematically violated
- Angle: Enforcement, not documentation

## Advertiser Associations

### ANA (Association of National Advertisers)
- Represents $400B+ in ad spend
- Their members are the actual victims
- Angle: Your "brand safety" tools verify against a broken ledger

### WFA (World Federation of Advertisers)
- Global scope
- Cross-border supply chain violations

## Academic / Research

### Privacy Researchers
- Arvind Narayanan (Princeton) — web tracking research
- Jonathan Mayer — surveillance capitalism
- Wolfie Christl — corporate surveillance

### Think Tanks
- Electronic Frontier Foundation — adtech surveillance angle
- Mozilla Foundation — web health metrics
- Center for Digital Democracy — consumer protection

### Academic Journals
- PETS (Privacy Enhancing Technologies)
- IMC (Internet Measurement Conference)
- Angle: Methodology is reproducible, data is public
