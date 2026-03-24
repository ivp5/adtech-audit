# FTC Complaint Draft

## Portal
https://reportfraud.ftc.gov/

## Category
Advertising/Marketing → False or Misleading Advertising

## Summary (for portal)
Major ad-tech companies are selling "DIRECT" publisher relationships that don't exist. 55% of authorization claims in the ad supply chain are provably false. Advertisers pay 15-30% premium for this false authorization.

## Detailed Complaint

I am submitting evidence that major advertising technology companies are systematically misrepresenting their supply chain authorization.

**The finding:** 55% of "DIRECT" authorization claims in publisher ads.txt files are false when cross-referenced against the SSP's own sellers.json registry. This represents 962,891 false claims across 21,397 publishers.

**Why it matters to consumers:** Advertisers believe they are buying premium, directly-authorized inventory. Instead, they are paying a 15-30% price premium for authorization that does not exist. This inflated cost is passed through to consumers in higher product prices.

**Scale of affected companies:**
- Google: 64,743 false claims
- Magnite: 62,495 false claims  
- Taboola: 53,869 false claims (96% phantom on their own property)
- PubMatic: 41,912 false claims

**Evidence:** All data is publicly available. Each publisher serves ads.txt at their domain. Each SSP serves sellers.json at their domain. The cross-reference is mechanical. Complete methodology and interactive verification tool available at: [URL]

**Why this hasn't been caught:** Verification vendors check that claims *exist* in ads.txt, but don't verify that they're *consistent* with sellers.json. Our cross-reference reveals the gap.

This is not isolated fraud — it's industry-wide systemic misrepresentation.

---

## One-click mailto

```
mailto:advertising@ftc.gov?subject=Systematic%20Ad%20Supply%20Chain%20Misrepresentation%20-%20Evidence%20of%20955%2C000%20False%20Authorization%20Claims&body=I%20am%20reporting%20systematic%20misrepresentation%20in%20the%20digital%20advertising%20supply%20chain.%0A%0A55%25%20of%20%22DIRECT%22%20authorization%20claims%20in%20publisher%20ads.txt%20files%20are%20provably%20false.%20This%20affects%20962%2C891%20claims%20across%2021%2C397%20publishers.%0A%0AComplete%20evidence%20package%20available%20on%20request.
```
