# Co-publication outreach drafts (NOT TRANSMITTED)

> Per CLAUDE.md: drafts only. The user reviews, edits, sends if/when
> appropriate. Per cycle 355 first-90-days priority #4, this is the
> co-publication pitch path. Two drafts: The Markup (investigative),
> Adalytics (industry research).

## Draft A — The Markup pitch

**To:** Aaron Sankin (investigative ad-tech), `aaron.sankin@themarkup.org`
**Subject (option 1):** Empirical study of IAB ads.txt framework — 99% spec-violation rate
**Subject (option 2):** Co-publication opportunity: 76,425-publisher framework integrity audit

```
Hi Aaron,

I'm reaching out because The Markup's investigative ad-tech work
(particularly the Citizen Browser project) is exactly the model for
publishing the empirical study I've completed. I'd like to discuss
co-publication.

The findings:

- 76,425 publishers × ~3,600 SSPs × 28.77M ads.txt DIRECT claims
  audited against IAB sellers.json registries
- ~0.97% of DIRECT claims satisfy the IAB ads.txt v1.1 spec's own
  definition of DIRECT (§4.1: "directly controlled/operated by the
  website owner")
- 26.8% confirmed spec violations (phantom — no registry record)
- ~99% of NAMED registry-matched claims have publisher_domain ≠
  registry_domain (the spec's website-owner-control requirement is
  contradicted across 49 of 49 major SSPs)
- 84% of bid-stream gdpr_consent= parameter values are EMPTY under
  gdpr=1, a TCF v2 MUST-NOT-process violation

The methodology is independently reproducible by stdlib Python in 60
seconds (the project ships verify_anonymity.py + verify_publisher_claims.py).
No project-specific dependencies. The synthetic-corpus falsifiability
test (cycle 295-296 in the chain) demonstrated 100% recall on planted
ground truth for phantom + mismatch + template-injection.

Live verification (2026-05-09) against 5 SSPs (Seedtag, Taboola,
Cadent, Rich Audience, IAB Tech Lab itself) confirms findings persist
4 months after corpus snapshot. The IAB Tech Lab's own server returns
HTTP 200 + HTML at the spec-mandated /sellers.json and /ads.txt paths
— catch-all-to-homepage configuration that confuses verifiers.

A 1.2M-row dataset of false-DIRECT claims is ready (CC0 license).
A formal paper draft is ready (release/PAPER.md, ~250 lines). The
methodology generalizes to 4 adjacent attestation frameworks (carbon
offsets, FDA 510(k), TLS PKI, OSS supply chain) — each with its own
phantom-rate analysis path.

What I'm proposing:

- The Markup publishes a written-for-readers piece on the cycle
  232-367 findings (3-5 weeks editorial timeline)
- I provide the data, methodology, reproducer access, and live
  cosmic-ray verification capability
- Joint authorship or attribution per The Markup's standards
- The Markup's editorial team retains full editorial control;
  technical accuracy review available from me

Why The Markup specifically:
- The Markup's prior ad-tech work (Citizen Browser, ANA referencing)
  has methodological credibility
- Investigative-journalism + technical-empirical hybrid is the right
  shape for this finding
- Adalytics has parallel work but is industry-research-oriented; The
  Markup's general-public reach is broader

What I'd like from this conversation:
- 30-minute call to walk through the methodology + findings
- Discuss editorial fit and timeline
- Identify any open questions before deeper engagement

Thank you for your time. I've been an admiring reader of your work.

[Your name]
[Your contact]
[Repository URL when public]
```

## Draft B — Adalytics pitch

**To:** Krzysztof Franaszek (Adalytics founder), via Adalytics website
contact form (Adalytics doesn't publish direct email)
**Subject:** Empirical study extending Adalytics methodology — 99% spec-violation rate

```
Hi Krzysztof,

Adalytics' work on supply-path verification is closest to what I've
been doing for the past year. I'd like to share findings that may be
complementary or competitive — your judgment.

The work:

- 76,425-publisher × ~3,600-SSP audit of IAB ads.txt v1.1 framework
- ≈0.97% of DIRECT claims satisfy the spec's own DIRECT definition
  (§4.1: "directly controlled by the website owner")
- 26.8% confirmed phantom; ~99% domain-mismatch on named matches
- Methodology with planted ground-truth synthetic test (100% recall
  on phantom + mismatch + template-injection)
- Live cosmic-ray verification against 5 SSPs (2026-05-09): findings
  persist 4 months after corpus snapshot
- Reproducer in stdlib Python, MIT-licensed; dataset CC0

Specific points where my work touches Adalytics-published findings:

- Adalytics' MFA report (2023) named MGNI/PUBM/CRTO and was followed
  by 13-40% stock declines over 90 days. The cycle 305 short-thesis
  matrix in this work extends that by cross-referencing the cycle
  232-296 findings against the named ad-tech tickers' SOX-filed 10-Ks.

- The cycle 184-186 named-operator template injection finding (Seedtag,
  Rich Audience, SmartAdServer, Insticator, etc.) extends the publisher-
  side documentation to the SSP-side: ~65,288 publisher claims tagged
  `impersonation_undisclosed` against rubicon's registry attribute
  the seller_id to Seedtag.

I'm not asking for Adalytics' validation of the work — I'm asking
about possible complementary engagement:

Option 1: Adalytics publishes its own version (Adalytics has the press
relationships; my work has the methodological depth + reproducer).
We co-attribute or you simply cite the public dataset.

Option 2: We jointly develop a piece that extends Adalytics' MFA work
into the framework-integrity dimension. Co-authored piece.

Option 3: You see this as competitive. Fair; I appreciate hearing so.

A 1.2M-row dataset is ready under CC0. The reproducer is stdlib Python.
A formal paper is in release/PAPER.md. The repository will be MIT-
licensed when public.

Brief 20-minute call to discuss?

[Your name]
[Your contact]
[Repository URL when public]
```

## Draft C — Backup pitches

If both A and B decline, secondary targets:

**WSJ Patience Haggin** (ad-tech beat reporter):
- Lead: "Empirical evidence the IAB framework certifies <1% of
  programmatic authorization claims as spec-compliant"
- Angle: securities-law angle on TBLA/CRTO 10-K filings
- Length: shorter pitch, ~250 words

**Bloomberg Gerry Smith** (advertising industry):
- Lead: similar to WSJ but with macro angle
- Less ad-tech-specific reporter; need broader framing

**FT Anna Nicolaou** (media):
- Lead: framework-integrity story with regulatory angle (EU DSA + DOJ
  Brinkema ruling context)
- FT readership skews European / regulatory; good fit for EU DSA hook

**ProPublica or NYT (David Streitfeld):** general investigative
ad-tech; longer timeline, possibly higher-impact

## Pitch sequence (suggested)

Week 1: Send Draft A (The Markup) — best fit for empirical-investigative.
Week 2 (if no response): Send Draft B (Adalytics) — direct competitor /
collaborator.
Week 3-4: WSJ / Bloomberg if both A and B decline.

Track responses; adjust narrative based on which angle resonates.

## What this draft is NOT

- Not customized to specific facts about each recipient (pitch
  personalization is recommended pre-send)
- Not yet sent
- Does not include the actual repository URL (placeholder)
- Does not include the user's name / contact

Per CLAUDE.md: drafts only. The user reviews, customizes, sends from
their own email account. The DRAFT format is a starting point, not a
ready-to-send template.

## Anticipated outcomes by branch

**If The Markup accepts (~25% probability):**
- 4-12 weeks editorial timeline
- Significant general-public reach (NYT-syndication, etc.)
- Major boost to OSS launch (cycle 368) traction
- Possible follow-on press cycle

**If Adalytics accepts (~15% probability):**
- 2-6 weeks parallel publication / cross-promotion
- Industry-press reach (AdExchanger, Adweek)
- Most-targeted audience for cycle 305 short thesis
- Smaller mainstream reach

**If WSJ/Bloomberg/FT accepts (~15% probability):**
- Tier-1 financial press impact
- Direct relevance to short-thesis market reaction
- Possible regulatory inquiry response

**If all decline (~45% probability):**
- Self-publish via Substack / Medium / direct release
- Lower initial reach but unconstrained narrative control
- Build reach via cycle 368 HN launch + SEO over 6-12 months
- This is still a viable path; not a failure
