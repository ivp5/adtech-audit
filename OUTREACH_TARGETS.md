# Outreach Targets

## Media (existing focus)
- AdExchanger, The Trade Desk, Digiday, WSJ/NYT tech desks

## Regulators

### FTC
- Bureau of Consumer Protection (ad fraud = deceptive practices)
- Angle: Advertisers pay 15-30% premium for "DIRECT" authorization that doesn't exist
- Contact: FTC complaint portal + direct to Bureau staff

### SEC  
- Public companies with material exposure:
  - Taboola (TBLA): 53,869 false claims, 96% phantom on own property
  - PubMatic (PUBM): 41,912 false claims
  - Magnite (MGNI): 62,495 false claims (also plaintiff in Google antitrust)
  - Criteo (CRTO): 23,129 false claims
- Angle: False authorization = misrepresentation of inventory quality
- 10-K filings claim "premium supply" — claims contradict this

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
