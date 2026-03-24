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
- 272,883 sync requests without valid consent
- Angle: This isn't a bug, it's the design
- Contact: Irish DPC (most ad-tech HQs), French CNIL, German BfDI

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
