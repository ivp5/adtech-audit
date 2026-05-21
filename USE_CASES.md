# Use cases for the ads.txt audit dataset

> Cycle 422: what the data enables, by user role. Includes
> conventional ad-tech applications + paradoxical / adversarial /
> uncommon directions the substrate supports but the project hasn't
> taken a position on.

## Conventional buyer-side (advertiser, agency, DSP)

### 1. Allowlist sanitization
**Tool**: `saas/allowlist_verify.py`. CSV in (DSP allowlist of publisher
domains), CSV out with phantom rate / wrapper tier / cohort signature
/ buy-recommendation per domain.

Output recommendation labels: CLEAN / ACCEPT / REVIEW / DISCOUNT / BLOCK.
Test on 10-domain mix yielded 1 CLEAN, 1 ACCEPT, 3 REVIEW, 2 DISCOUNT,
3 BLOCK — 50% of the test allowlist flagged for action.

### 2. Pre-bid scoring
**Endpoint**: `/api/bidcheck?ssp=...&seller_id=...`. Sub-millisecond
bloom-filter check (36µs negative, 550µs positive+SQL). DSP integrates
inline; bloom-negative bids get blocked or discounted in 36µs.

### 3. Spend exposure quantification
Formula: `annual_programmatic_spend × phantom_rate × wrapper_distortion_factor`.
For the corpus median publisher (26.8% phantom rate), an advertiser
spending $1M/yr on programmatic has roughly $268K/yr exposure to
unverifiable DIRECT inventory.

### 4. Wrapper-driven supply-side selection
**Tool**: `release/WRAPPER_SCORECARD.html`. 104 wrappers ranked by
phantom rate, 8× spread (Cafemedia 6.7% to fourm.jp 52.6%). Brands
choosing wrapper services (publishers) or DSPs choosing inventory
sources can use this scorecard.

### 5. Refund / clawback evidence
Per-claim verdict trail with named legitimate intermediary ("registered
to cafemedia.com / Raptive") provides court-grade evidence for
material-misrepresentation claims.

## Audience profiling / matching

### 6. Fingerprint cohort discovery
**Data**: `saas/data/fingerprint_clusters.jsonl`. 6,443 clusters of
publishers sharing identical ads.txt fingerprints. Apex cluster: 338
college-sports network publishers. Use case: "find publishers similar
to nytimes.com" → look up nytimes' fingerprint, find others in cluster.

### 7. Audience overlap inference
Two publishers with identical fingerprints share inventory paths,
which means advertisers buying through one likely reach the audience
of the other. Frequency-cap and over-targeting implications.

### 8. Per-operator citation network
**Data**: `release/operators/*.html`. Auto-generated profile per
managerdomain + SSP. Shows publisher count, phantom rate against own
registry, role (wrapper vs SSP vs both). Searchable network map.

## Adjacent intelligence (uncommon)

### 9. Ad-tech M&A early signal
The `registry_meta.fetched_at` deltas combined with name-field changes
detect acquisitions before press releases (cycle 420 found
districtm→sharethrough, adtech→yahoo, vdopia→chocolateplatform).
Hedge-fund-grade signal.

### 10. Geopolitical / sanctions inventory mapping
Per-TLD analysis on uncovered SSPs (.ru: 30 SSPs, .cn: many) tells
sanctions-compliance buyers which domains route through Russia-based or
China-based infrastructure.

### 11. Piracy-funding accountability
Cluster fingerprints reveal piracy-aggregator cohorts (mangafire,
dramacool, scan-manga). Cross-reference with advertiser → SSP →
publisher chain identifies which advertisers fund piracy via which
intermediaries.

### 12. Standards-process critique evidence
The dataset is a standing critique of IAB Tech Lab's enforcement
posture. Submit findings as comment to spec-revision RFCs. Force the
framework to evolve toward what its prose claims.

## Paradoxical / inverse-use

### 13. Reverse-litigation defense
A wrapper service sued for misrepresentation could buy our data to
argue "the spec itself is unworkable" — same data used by both sides.

### 14. Insurance underwriting
Wrappers with 42% phantom rate (Themoneytizer) are higher-risk than
6.7% wrappers (Cafemedia). Underwriting input for media-buying
liability insurance.

### 15. Negative-information badges
The most paradoxical: an "audited by IAB ads.txt v1.1" badge has
provably negative information value, since 26.8% of DIRECT claims
fail the spec's own definition. Brands could differentiate by NOT
citing IAB compliance — citing this dataset instead.

### 16. Bounty / pay-for-cleanup market
Advertisers pay publishers to clean their ads.txt before bidding. The
SaaS quantifies the gap; advertisers fund the close.

## Adversarial / borderline

The dataset is dual-use. Documenting all dimensions:

### 17. Fraudster intelligence (NEGATIVE-utility direction)
The 8,392-publisher stub-leak list IS a list of weak-authentication
targets. A bad actor uses this to identify which publisher sites are
easiest to spoof at bid time. The data exposes both fraud AND
fraudability.

### 18. Sanctions-evasion mapping (FOR the evader)
Same data that helps a sanctions-compliant buyer identify .ru flow
helps a sanctions-evader find ad-flow channels operators haven't
blocked.

### 19. Sock-puppet farm coordination detection / evasion
Fingerprint clustering identifies coordinated publisher operations.
Useful for detection AND for evasion (rotate fingerprints to avoid
clustering).

### 20. Pre-acquisition stock pump/dump
Knowing which SSPs are silently being acquired (per #9) creates an
SEC-grade insider-information problem. Hedge-fund-grade signal becomes
hedge-fund-grade insider-trading risk.

### 21. Reputational warfare
Naming and shaming specific operators publicly. Data is true; the
question is whether to weaponize.

## Recommended responsible-use posture

The project's deliverables:
- Open-source code (MIT) — fork freely
- Open dataset (CC0) — use freely
- Reproducer scripts — verify any claim independently

What the project does NOT do:
- Provide private investigations
- File lawsuits
- Send accusations to operators
- Deploy unauthenticated public APIs
- Auto-publish naming-and-shaming content

What we recommend NOT doing with the data:
- Bid-time fraud against weak-authentication publishers
- Sanctions evasion via uncovered-SSP exploitation
- Coordinated reputational attacks without due process
- Insider trading on M&A signals without legal review

The dual-use nature is inherent. Any sufficiently-detailed transparency
dataset is also a vulnerability disclosure. Acknowledge, don't pretend
otherwise.

## What's still missing for full commercial viability

| Gap | Required for |
|---|---|
| Live SaaS deployment | non-technical buyer self-serve |
| Stripe billing integration validation | recurring revenue |
| Bulk API endpoints for DSPs | high-volume buyer use |
| SOC 2 Type II / audit | enterprise procurement |
| Dataset distribution mirror (S3 / IPFS / academic data hub) | researcher independence |
| Privacy review of per-publisher data exposure | regulatory compliance |

These are deploy-time considerations the open-source artifacts don't
address; the project's authors have to make those moves.
