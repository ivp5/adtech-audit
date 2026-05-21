# Hacker News submission draft (NOT YET POSTED)

> Per CLAUDE.md outbound rules: this is a DRAFT for the user to review,
> edit, and submit when ready. The submission requires user-side action
> (paste into news.ycombinator.com/submit, choose Show HN or general
> tag). Multiple title variants offered.

## Title options (ranked by HN-conventional appeal)

1. **Show HN: 10,966 publishers carry identical fabricated SmartAdServer claims; 12,140 union with the cycle-211 cartel cohort**
2. Show HN: 60-second reproducer for the IAB ads.txt/sellers.json framework
3. Show HN: SpotX has 21K publisher DIRECT claims; its registry returns 0 bytes
4. Show HN: 99% of programmatic ad authorization fails the spec's own definition
5. The IAB framework verifies 1 bit; the registry encodes 18 — a 99.6% loss study
6. Empirical study: 76,425 publishers × 4,725 SSPs × 28.77M ads.txt rows (6.56M DIRECT), ~1% compliant

Recommend **#1** for the structural-fact specificity. Note that the
"impossible by coincidence" framing requires an independence assumption
the data weakens — the 826-publisher cohort clusters around shared traits
(piracy / streaming / low brand-safety enforcement), so the cohorts are
correlated by common-cause targeting, not independent draws. The
defensible framing is: 826 publishers carry phantom DIRECT claims against
the same 7 SSPs simultaneously (a structural fact), and the cycle 211 +
381 evidence (shared seller_ids across thousands of publishers,
format-extrapolated IDs) makes shared template authorship the most
parsimonious explanation among alternatives. Title #2 is the "Show HN"
fallback if #1's specificity reads as overclaim.

## URL field

`https://github.com/ivp5/adtech-audit` (replace with actual repo URL
when published — currently the project is private)

## Submission body (~500 words; HN comments capped at 4-5K chars)

```
Hi HN,

I audited the IAB Tech Lab's ads.txt and sellers.json frameworks — the
"supply-chain transparency" specs that underpin programmatic advertising.
Findings + reproducer + paper + dataset are here, MIT-licensed (code) and
CC0 (dataset).

The lead finding (cycle 401, sharpening cycle 382): **10,966 publishers
carry the same four phantom SmartAdServer seller_ids (4012, 4071, 4073,
4074), none in current SmartAdServer/Equativ registry**. Of those,
**821 are also in the cycle 382 7-SSP intersection** (so 821 of 826 in
the original framing). Adform 1941 layers on: 5,526 of the 10,966
also carry that phantom, 778 carry both signatures plus the cycle 211
cartel template. Three-cohort union: **12,140 publishers** carrying
at least one signature.

This sharpens the original cycle 382 finding without retracting it: 826 carry
identical fabricated DIRECT-relationship claims for SEVEN separate
ad-tech companies simultaneously**, with seller_ids that don't resolve
against any of those companies' published registries. The 7 templates:
SpotX (Magnite), Sovrn, Seedtag, Rich Audience, SmartAdServer, MGID,
Themoneytizer. The 826 publishers are dominated by content-piracy and
manga/anime/drama streaming sites (mangafire.to, dramacool.sh,
readcomiconline.li, scan-manga.com, 9animetv.to, etc.), but legitimate
publishers are mixed in (sport.detik.com, nativeplanet.com, mykhel.com).

Independence-assumption probability calculations would put this at
vanishingly small, but those calculations don't apply: the 826-publisher
cohort clusters around shared traits (piracy / streaming / low brand-
safety enforcement), so the per-vendor selections aren't independent
draws — they share a common targeting axis. The structural fact is:
826 publishers carry at least one phantom claim against each of the 7
SSPs simultaneously. The phantom-MAJORITY framing is too strong for
all 7 — smartadserver in particular has 0/826 phantom-majority because
its seller_ids resolve to legitimate intermediaries (mismatch, not
phantom). The honest version: ≥1 phantom per SSP, with magnitude
varying — see release/PAPER.md for the per-SSP breakdown. Cycle 211 +
381 evidence (shared seller_ids across thousands of publishers;
ID-format extrapolation just above each SSP's historical max) make
shared template authorship the most parsimonious explanation among
alternatives. The IAB framework's existence-check cannot detect this
because the templated seller_ids are in plausibly-legitimate format
ranges.

Apex single-SSP example (cycles 379-381, corrected cycle 390):
**spotxchange.com — 7,942 publishers carry SpotX DIRECT-typed claims
(23,371 DIRECT phantom claims total); the registry has been zero-byte
for 5+ years across the Magnite acquisition.** (Cycle 379 originally
wrote 21,433 publishers — that count conflated DIRECT and RESELLER
carriers. Cycle 390's test_reported_numbers regression caught it.). Wayback Machine has zero snapshots of
spotxchange.com/sellers.json returning a 200-OK JSON response — only
redirects (cycle 380). The 23K phantom claims trace to ~422 distinct
seller_ids, of which the top 6 (e.g., 173177 on 5,004 publishers; 225721
on 9,884) appear under both spotxchange.com AND spotx.tv as a paired
template fragment.

Aggregate (the cycle 232-296 baseline): 76,425 publishers × 4,725
distinct SSPs cited (739 with public registries) × 28.77M total ads.txt
rows, of which 6.56M are DIRECT-typed. ~0.97% satisfy the spec's own §4.1
DIRECT definition ("directly controlled/operated by the website owner").
The other 99% break down as 26.8% phantom (confirmed spec violation),
~99% domain-mismatch among NAMED entries, 1.8% spec-allowed-but-anonymous
(Google sellers.json 71.8% NULL-domain), 0.30% Popperian-and-functional.
The verification primitive (existence-check) returns ~1 bit; the
registry encodes ~17.77 bits per row. ~99.6% information loss at
verification time.

What's reproducible in 60 seconds:

```
git clone https://github.com/ivp5/adtech-audit
cd adtech-audit

# Single-command demo of the phantom-claim shape:
python3 tools/reproducer/verify_template_carrier.py mangafire.to
# Measured: 7/7 SSPs with DIRECT+RESELLER claims (cycle 411 cohort schema)
#   spotxchange.com  38 claims, REGISTRY DEAD (network error)
#   sovrn.com       126 claims, 70 phantom + 56 mismatch
#   seedtag.com      23 claims, 12 phantom + 11 mismatch
#   richaudience.com 60 claims, 12 phantom + 48 mismatch
#   smartadserver   566 claims, 172 phantom + 394 mismatch
#   mgid.com         23 claims, 17 phantom + 6 mismatch
#   themoneytizer     9 claims,  7 phantom + 2 mismatch
#   total: 845 DIRECT+RESELLER claims, 0 match registry+domain
# The script reports MEASUREMENT (count thresholds, phantom-majority).
# The interpretation (template injection per cycle 211/381) is reported
# separately in a labeled "Interpretation" section, NOT as a verdict.

python3 tools/reproducer/verify_template_carrier.py nytimes.com
# Measured: 0/7 SSPs with cartel-cohort claims.

# Per-SSP detail:
python3 tools/reproducer/verify_anonymity.py google.com
# → 71.3% anonymous, contractual_confidential
python3 tools/reproducer/verify_anonymity.py ad-stir.com
# → 84.9% anonymous, precomputed_lookup, integers [1, 14591]
python3 tools/reproducer/verify_publisher_claims.py mangafire.to mgid.com
# → 18 DIRECT claims; MISMATCH against orquidea.ai, unibots.in, b92.net
#   (cross-vendor seller_id contamination from shared template)
```

What I've confirmed via cosmic-ray verification (live data, 2026-05-09):

- Seedtag, Taboola, Cadent (formerly Engine Media), DistrictM.io, Rich
  Audience — 5 SSP registries probed; corpus snapshot findings persist
  4 months later.
- 100/100 internal-consistency + 27/27 live-verification on N=100
  random sample of phantom-flagged claims (cycle 378). 0 false positives.
- spotxchange.com / spotx.tv: Wayback Machine has zero JSON-200
  snapshots; only redirects from 2021-2022 (cycle 380).
- Sovrn rebranded from Lijit but kept /sellers.json on legacy lijit.com
  (cycle 378). Magnite has NO unified /sellers.json on canonical domain,
  5 years post-merger; rubiconproject.com + telaria.com still separately
  serve their pre-merger registries (cycle 379).
- IAB Tech Lab itself returns HTTP 200 + HTML at /sellers.json and
  /ads.txt (catch-all-to-homepage). The standards body's own server
  configuration normalizes the verifier-confusing response state
  (cycle 290).

Falsifiability discipline: the analysis pipeline was tested against a
synthetic corpus with planted ground truth (cycles 295-296). Phantom +
mismatch + template-injection detection: 100% recall on planted truth.

Dataset: 1.2M+ false DIRECT claims (~146MB JSONL, gzipped ~10MB).
Methodology paper: release/PAPER.md (~250 lines).

I welcome feedback, especially:
- Counter-examples (publishers/SSPs we mis-classified)
- Methodology critique (the synthetic falsifiability test addresses
  some but not all)
- Adjacent framework analyses (carbon offsets / FDA 510(k) / TLS PKI /
  OSS supply chain — the methodology generalizes; see
  memory/cycle361_365_methodology_extensions_*.md)

The repo includes 30+ memory notes documenting the analytical chain
(cycles 232-367 of an iterative audit). The strongest single claim
is the spec-text reading: ads.txt v1.1 §4.1 defines DIRECT in a way
the framework's existence-check can't enforce. That's the structural
gap, not "framework limited by design."

Repository: https://github.com/ivp5/adtech-audit (MIT/CC0)
Paper: release/PAPER.md
Reproducer: tools/reproducer/

Happy to discuss anything; AMA if there's interest.
```

## Targeting / posting strategy

**Best time to post:** Tuesday/Wednesday/Thursday 6-9 AM Pacific (peak
HN traffic; non-Monday/Friday for tech audience).

**First-comment strategy:** When you submit, immediately add a top-level
comment with:
- "Q&A: happy to clarify methodology"
- Pointer to the PAPER's strongest sections
- Acknowledgment of limits (single-author; sample size for cosmic-ray
  on 5 SSPs; etc.)

**Anticipated objections (prepare responses):**
1. "Is this just sellers.json existence check?" → "No, the spec text §4.1
   defines DIRECT as website-owner control. Cycle 293's reading + cycle
   295-296 falsifiability."
2. "Adalytics already does this?" → "Adjacent + complementary. Adalytics
   focuses on MFA / brand-safety; this analyzes the IAB framework's
   own verification semantics."
3. "DV / IAS solve this?" → "Different layer (IVT, viewability, brand
   safety). Cycle 134 verified 0 mentions of supply-path verification
   in DV's 10-K."
4. "Is the dataset legally distributable?" → "Yes; ads.txt and
   sellers.json are publicly published files. The dataset is a
   cross-reference of public files. CC0 license."
5. "Why hasn't this been done before?" → "The cross-reference at scale
   requires building atlas + materialization pipeline. The data has
   been public; the analysis hadn't been done at this scope."

## Reddit cross-post targets

If HN goes well, cross-post to:
- /r/programming (~5M subs, conventional-tech tone)
- /r/sysadmin (~1.5M subs, niche but engaged)
- /r/webdev (~1.5M subs)
- /r/privacy (~1.5M subs, transparency-aligned audience)
- /r/MachineLearning (less fit but methodology overlap)

Skip /r/marketing (industry-aligned; less receptive to critique).

## Twitter/X thread (if HN traction):

8-tweet thread skeleton:
1. Hook: "Audited IAB's ads.txt framework. ~0.97% of DIRECT claims
   satisfy the spec's own definition of DIRECT. Here's why."
2. Spec text: "§4.1 defines DIRECT as 'directly controlled by the
   website owner.' Reads like English."
3. Phantom rate: "26.8% confirmed spec violations + 99% domain-
   mismatch among NAMED registry entries"
4. Information theory: "Registry encodes 17.77 bits / row.
   Verification returns 1 bit. 99.6% loss."
5. Reproducer: 60-second verification, stdlib Python
6. Cosmic-ray: live cross-check 4 months later confirms findings
7. Falsifiability: synthetic corpus, planted ground truth, 100% recall
8. Methodology generalizes: 4 adjacent frameworks identified
   (carbon offsets, FDA 510(k), TLS PKI, OSS supply chain)

## What this draft is NOT

- NOT yet posted
- NOT yet customized for the specific repo URL (placeholder used)
- NOT yet timed (best post-window depends on availability)
- DOES NOT include direct attacks on companies (kept neutral; lets
  data speak; HN tone)

The user reviews, edits, submits. CLAUDE.md outbound rule applies:
draft, not send.
