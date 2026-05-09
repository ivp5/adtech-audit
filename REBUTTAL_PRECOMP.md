# Rebuttal pre-comp — anticipated objections + remediation paths

> Cycle 396 forward-simulation. If this work is published and an SSP
> or industry body issues a rebuttal, here are the most likely
> objections, the technical response to each, and — for SSPs that
> want to engage constructively — the concrete remediation path.
>
> The goal is not just to defend; it's to make the rebuttal a
> commitment. "Yes, we'll fix X" is the desired endpoint.

## Objection 1: "Your numbers are stale"

**Likely form:** "The corpus is from {date}; our registry has been
updated since; the phantom rate against current data is much lower."

**Technical response:** Cycle 393 severe test ran exactly this
verification on 100 randomly-sampled phantom claims across top 10 SSPs
against current live data (2026-05-09). 86 of 90 verifiable (95.6%)
were still phantom in current live registries. The 4.4% drift was
entirely in rubiconproject.com (4/10), suggesting the corpus's rubicon
snapshot is older than other SSPs.

The reproducer is publicly runnable; anyone (including the SSP) can
reproduce against current live data:
```
python3 tools/reproducer/verify_publisher_claims.py {publisher} {your-ssp}
```

Cycle 388 introduced `scripts/refresh_ssp_if_stale.py` which lazy-refreshes
sellers_registry on read. The corpus self-heals over time as queries
hit different SSPs.

**Remediation path for the SSP:** publish a complete current sellers.json
that lists every seller_id you actually transact with. The phantom rate
against your registry can drop to near zero in one publication step.

## Objection 2: "Your methodology misunderstands the spec"

**Likely form:** "ads.txt §4.1 doesn't require the SSP-side existence
check the way you measured. DIRECT relationships exist between
publishers and intermediaries that we have no obligation to publish."

**Technical response:** Acknowledged and integrated. Cycle 391 read
the lijit.com sellers.json directly: 273657 (NoBid LLC), 278628 (Somo
Media / Unibots), 375328 (Amazon Publisher Services). All registered
as INTERMEDIARY. mangafire.to's "DIRECT" claim against lijit.com via
those seller_ids is the publisher's relationship to the intermediary,
not to lijit. The framework's check confirms the intermediary exists.

The cycle 232-296 work originally framed all such mismatches as
"cartel" / "template injection." Cycle 391 sharpened to: PHANTOM (no
registry record at all) is the spec-violating subset; MISMATCH
(registry has the seller_id, registered to a real intermediary) is
the spec's normal operating mode.

The PHANTOM count is the framework-failure number. For mangafire.to:
- 548 cartel-cohort DIRECT claims
- **188 (34%) PHANTOM** — actual framework failure
- 360 (66%) MISMATCH — legitimate intermediary chain
- 0 MATCH

The 26.8% global phantom rate is specifically PHANTOM — claims with
no registry record at all in any SSP's published list. Not mismatch.

**Remediation path for the SSP:** if your framework reading is that
publishers are entitled to list intermediary seller_ids as DIRECT,
publish that interpretation publicly. The IAB Tech Lab spec text §4.1
is currently ambiguous on this; an SSP-side clarification would
benefit the whole framework.

## Objection 3: "You're cherry-picking; the apex examples are
unrepresentative"

**Likely form:** "spotxchange.com is a defunct registry; mangafire.to
is a piracy site. The framework works fine for legitimate SSPs and
publishers."

**Technical response:** Cycle 401 sharpening: 826 is the cycle 382 7-SSP intersection using mixed filters (DIRECT+RESELLER for 5 SSPs, specific seller_ids for 2). The broader 10,966-publisher cohort is the four-ID smartadserver phantom-template; union with adform 1941 = 12,140. The 826 number (cycle 382)
includes many piracy/streaming sites. Cycle 391 re-examined this — the
cohort clusters around shared-targeting traits (low brand-safety
enforcement). But:

- Cycle 392 ran the same scan against king.com (Candy Crush, Activision
  Blizzard parent), zynga.com (FarmVille), rovio.com (Angry Birds).
  All three carry phantom-majority claims against multiple cartel
  SSPs. Mobile-app cohort, billion-dollar publishers, same pattern.
- Cycle 305 short-thesis matrix covered CRTO, MGNI, TBLA, TEAD —
  publicly-traded ad-tech tickers. Same framework gaps.
- The 26.8% phantom rate is corpus-wide (76,425 publishers). The
  apex examples are not the average; they're the tail. The average is
  the headline.

**Remediation path:** scope the conversation to specific publisher-SSP
pairs the SSP wants to dispute. The reproducer per-pair is decisive;
cherry-picking-vs-not becomes a measurable disagreement, not a
rhetorical one.

## Objection 4: "The tooling is inflammatory / accusatory"

**Likely form:** "Calling our publisher network a 'cartel carrier' is
defamatory."

**Technical response:** Cycle 391 already softened the verdict
language. `verify_template_carrier.py` now reports MEASUREMENT
(`phantom-majority`, count thresholds) and prints interpretation in a
separately-labeled section that explicitly says "this script does NOT
itself prove injection." The script-as-it-stands measures shape; it
doesn't assert causation.

The cycle 211 "named injection cartel" framing in older memory notes
is documented as overstated. PAPER.md and HN draft post-cycle 391
read: "phantom-majority across N SSPs simultaneously" with "consistent
with multi-SSP template injection" as cycle 211/381 inference, not
as direct evidence.

**Remediation path:** if the SSP feels its specific seller_ids or
publishers are being mischaracterized, point us to the registry
evidence. We update against material (cycle 391 was an update).

## Objection 5: "This is competitor research dressed up as
methodology"

**Likely form:** Adalytics or similar accusation: "you're working for
a competitor; this is hit-piece economics."

**Technical response:** The repository is private; the work has no
named author; the dataset is CC0; the reproducer is MIT. There's no
competitor brand attached. The cycle 232-395 chain is single-author
empirical work with public reproducibility. PAPER.md's structure is
academic.

**Remediation path:** any party can run the reproducer and verify or
falsify the claims independently. The methodology is more transparent
than typical industry research.

## Objection 6: "Your fix proposals are infeasible"

**Likely form:** "Even if we publish a complete sellers.json, the
publisher-side template-injection (cycle 211/381 cohort) won't go
away just because our list is fuller."

**Technical response:** Correct. The 188-of-548 PHANTOM (cycle 391
mangafire.to breakdown) is the SSP-side fix. The remaining 360 MISMATCH
is publisher-side: those are legitimate intermediary chains the
publisher chose to authorize. No SSP can fix that side.

The 826-cohort's exposure to coordinated injection isn't an SSP problem
to solve. It's a publisher-side problem (the cycle 211 named-injector
template authors) and a chain-of-trust governance problem (no party in
the supply path verifies on behalf of the publisher).

**Remediation path:** SSPs can: (a) publish complete current
sellers.json (kills PHANTOM rate against their registry); (b) flag
publishers whose claims fail their own existence-check at bid time
(SSPs already do this internally; making it public would be a
transparency win); (c) push IAB Tech Lab for §4.1 clarification.

Publishers can: run the reproducer against their own ads.txt,
discover which lines fail framework verification, fix.

## What the rebuttal should NOT achieve

This pre-comp is not about silencing rebuttal. It's about anticipating
the most-likely shapes so:

- We don't get caught by an objection we haven't already documented
- The conversation shifts from "are these numbers right" to "given
  these numbers, what should change"
- The SSP's options are clear: refuse to engage (worst optics);
  rebut (we have the response staged); commit to remediation (best
  outcome for everyone)

The work is severe-tested (cycle 393), documented (PAPER.md), open
(reproducer, dataset, methodology). A rebuttal that engages
substantively is welcome. A rebuttal that doesn't is its own data.
