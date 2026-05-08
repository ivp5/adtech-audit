# Hacker News submission draft (NOT YET POSTED)

> Per CLAUDE.md outbound rules: this is a DRAFT for the user to review,
> edit, and submit when ready. The submission requires user-side action
> (paste into news.ycombinator.com/submit, choose Show HN or general
> tag). Multiple title variants offered.

## Title options (ranked by HN-conventional appeal)

1. **Show HN: 60-second reproducer for the IAB ads.txt/sellers.json verification framework**
2. Show HN: 99% of programmatic ad authorization fails the spec's own definition
3. The IAB ads.txt framework verifies 1 bit; the registry encodes 18 — a 99.6% information-loss study
4. Empirical study: 76,425 publishers × 3,600 SSPs × 28.77M DIRECT claims, ~1% spec-compliant

Recommend **#1** — Show HN format, neutral curiosity, hooks via "60-second"
quickstart (HN audience values reproducibility).

## URL field

`https://github.com/ivp5/adtech-audit` (replace with actual repo URL
when published — currently the project is private)

## Submission body (~500 words; HN comments capped at 4-5K chars)

```
Hi HN,

I've been auditing the IAB Tech Lab's ads.txt and sellers.json
authorization frameworks — the "supply-chain transparency" specs that
underpin programmatic display advertising. Findings + reproducer + paper
+ dataset are here, MIT-licensed (code) and CC0 (dataset).

The headline number: ~0.97% of corpus DIRECT authorization claims satisfy
the IAB ads.txt v1.1 spec's own definition of DIRECT, which §4.1 specifies
as "directly controlled/operated by the website owner." The other 99% break
down as:

- 26.8% phantom (no registry record at all — confirmed spec violation)
- ~99% domain-mismatch among NAMED registry entries (registry says X
  owns the seller_id; publisher claiming DIRECT is on a different domain
  Y, contradicting the spec's website-owner-control requirement)
- 1.8% spec-allowed-but-anonymous (Google's sellers.json publishes 71.8%
  of entries with NULL domain via is_confidential=1 — IAB-spec-allowed
  but verification-defeating)
- 0.30% Popperian-and-functional (registry has it, exact pub_domain match,
  AND the SSP actually fires on the publisher's page)

The verification primitive (existence-check) returns ~1 bit per claim; the
registry encodes ~17.77 bits of attribution per row. ~99.6% information
loss at verification time. The spec was designed for a publisher-market
structure (small direct relationships) that no longer exists at scale.

What's reproducible in 60 seconds:

```
git clone https://github.com/ivp5/adtech-audit
cd adtech-audit
python3 tools/reproducer/verify_anonymity.py google.com
# → 71.3% anonymous, contractual_confidential
python3 tools/reproducer/verify_anonymity.py ad-stir.com
# → 84.9% anonymous, precomputed_lookup, integers [1, 14591]
python3 tools/reproducer/verify_publisher_claims.py cnn.com google.com
# → 0/7 externally-falsifiable; 4 mismatches resolve to wbd.com
#   (CNN's parent — legitimate intra-corporate routing, but the framework
#    can't distinguish from fabrication)
```

What I've confirmed via cosmic-ray verification (live data, 2026-05-09):

- Seedtag, Taboola, Cadent (formerly Engine Media), DistrictM.io, Rich
  Audience — all 5 SSP registries probed; cycle-snapshot findings persist
  4 months later.
- IAB Tech Lab itself returns HTTP 200 + HTML at /sellers.json and
  /ads.txt (catch-all-to-homepage). The standards body's own server
  configuration normalizes a verifier-confusing response state.

Falsifiability discipline: the analysis pipeline was tested against a
synthetic corpus with planted ground truth. Phantom + mismatch +
template-injection detection: 100% recall on planted ground truth.

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
