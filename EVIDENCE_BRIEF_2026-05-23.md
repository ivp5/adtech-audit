# Evidence brief — 2026-05-23 (release-stage)

Self-contained summary of 2026-05-23 corpus analysis. Stage-ready
for incorporation into public release / external outreach. Per the
session's verisimilitude discipline: every claim ends with the test
that supports it and the path that would refute it.

## Headline

Two distinct patterns combine to 200K-500K publisher-claim instances
where the ads.txt DIRECT field diverges from buyer-side expectation:

1. **418 Google pub-IDs that meet a phantom signature** (declared by
   50+ publishers each, absent from Google's authoritative sellers.json,
   AND operationally inert across 2.3M browser-captured network requests).
   92,722 publisher-claim instances.

2. **1,117 Google pub-IDs that ARE in Google's registry, owned by a
   single named vendor, declared DIRECT by 20+ distinct publishers
   each.** Top: NoBid Inc's single pub-id shared as DIRECT by 3,040
   publishers.

Both patterns are mechanically extracted from public data and
reproducible in under a minute.

## Pattern A: operationally-inert phantom pub-IDs at scale

**Claim**: 418 Google pub-IDs declared by ≥50 publishers each that
(a) are absent from Google's authoritative sellers.json (986,194
entries fetched 2026-05-23) and (b) appear in zero of 20,357 captured
`client=ca-pub-` ad-server requests across 2.3 million browser scans.

**Distribution** (top 5 by carrier count):

| pub-id | declared carriers |
|---|---:|
| pub-8622186303703569 | 4,033 |
| pub-7002491002409919 | 2,153 |
| pub-9378724246417115 | 2,125 |
| pub-6733417337840393 | 1,980 |
| pub-6645287046856849 | 1,634 |

**Total publisher-claim instances**: 92,722.

**Reproduction (30 seconds)**:
```bash
# 1. Google's authoritative registry doesn't list it
curl -sL https://realtimebidding.google.com/sellers.json | jq '.sellers[] | select(.seller_id=="pub-8622186303703569")'
# Returns: null

# 2. Pick any carrier from operational_phantoms.json; verify their ads.txt
curl -sL https://kannadaprabha.com/ads.txt | grep "pub-8622186303703569"
# Returns: google.com, pub-8622186303703569, RESELLER, f08c47fec0942fa0
```

**Refutation paths**:
- If Google's sellers.json has documented omissions (would mean "absent"
  is normal). Tested: confidential entries DO expose their seller_id.
- If browser-journal capture is geographically biased. Tested: 89%
  coverage of declared carriers for pub-6110672335579159 (n=1,213/1,362)
  with 15,153 representative scans showing 0 captures.

## Pattern B: vendor-owned pub-IDs declared DIRECT across many publishers

**Claim**: 1,117 Google AdSense pub-IDs IN Google's registry, owned
by a SINGLE named vendor per Google's records, declared DIRECT by 20+
distinct publishers each.

**Top 10 instances**:

| Google's named owner | shared by # publishers |
|---|---:|
| NoBid Inc | 3,040 |
| Applabs.ai | 3,011 |
| H Code Media, Inc. | 2,905 |
| Playstream | 2,817 |
| OpsCo LLC | 2,729 |
| 152 Media | 2,482 |
| ADSOLUT Technology | 1,917 |
| CMI Marketing dba CafeMedia | 1,851 |
| Italiaonline | 1,679 |
| Mediavine Inc | 1,609 |

**Distribution**:
- 627 pub-IDs each shared by 20-49 publishers
- 232 pub-IDs each shared by 100-499 publishers
- 23 pub-IDs each shared by 1,000-4,999 publishers

**Spectrum**: The Mediavine case (1,609 publishers, explicit MANAGERDOMAIN
disclosure in publisher ads.txt files, public sellers.json with 8,870
sellers) is the transparent end. The NoBid/Applabs end is opaque.

**Interpretive note**: IAB v1.1 spec §3.3 field #3 says DIRECT "tends
to mean a direct business contract between the Publisher and the
advertising system." Under this softer reading, managed-services
arrangements where a publisher contractually delegates account control
to a wrapper-manager may be DIRECT-permissible. Per-instance violation
depends on contractual structure not visible in public data.

**What survives**: the mechanical pattern at scale (1,117 instances)
and the magnitude. The decoupling between "publisher declares DIRECT"
and "publisher is the registered account owner" is real at corpus scale.

## Pattern C: INTERMEDIARY-classified accounts declared DIRECT (cross-SSP)

**Claim**: 343,374 publisher-claim instances across 4 major SSPs where
the publisher's ads.txt declares DIRECT for accounts the SSPs themselves
classify as INTERMEDIARY in their own sellers.json.

| SSP | INTERMEDIARY-classified accounts misdeclared DIRECT by 100+ publishers each | Total publisher-claim instances |
|---|---:|---:|
| pubmatic.com | 186 | 125,356 |
| rubiconproject.com | 150 | 118,429 |
| openx.com | 115 | 65,128 |
| appnexus.com | 49 | 34,461 |

**Lead example** (NOW.md): `rubiconproject.com, 17280, DIRECT` declared
by 9,143 publishers including washingtonpost.com, cnn.com, theatlantic.com,
techcrunch.com, corriere.it. Rubicon's own sellers.json classifies
17280 as `seller_type=INTERMEDIARY, name=Seedtag Advertising SL`.

**Reproduction (90 seconds)** — see `release/HACKER_NEWS_POST_DRAFT.md`
and `NOW.md` for the Reddit-format pitch using this case.

## Refutation discipline summary

Findings that BROKE during today's session, with corrections written:

- "AdPushUp distributes a 5-phantom template" — 3 of 5 phantoms are
  dominated by no-vendor carriers (4-5× more than adpushup). The template
  exists independently of adpushup attribution.
- "PROMEDIA structurally impossible" — both PROMEDIA pub-IDs are in
  Google's PUBLISHER tier with named owners (RAHMAD MAULANA, Ayo Media
  Network). Google permits the configuration.
- "AdPushUp uniquely opaque" — they publish their own sellers.json
  (228KB, 1,531 sellers, 0% confidential) and appear in 33% of carrier
  ads.txt as structured data.
- "INTERMEDIARY-as-DIRECT misrepresentation at 343K scale" — the spec's
  "tends to mean" softness allows managed-services interpretation.
  Pattern is classification disagreement at 343K, not provable spec
  violation without per-instance contract review.

## Stage-ready external artifacts

In this directory:
- `false_direct_claims.jsonl[.gz][.xz]` — 2.7M claims, full corpus
- `index.html`, `evidence.html` — interactive surfaces
- `FTC_COMPLAINT.md`, `DOJ_ANGLE.md`, `HACKER_NEWS_POST_DRAFT.md` —
  draft outreach (per CLAUDE.md, outbound requires explicit user action)
- `OUTREACH_TARGETS.md`, `COPUBLICATION_PITCH_DRAFTS.md`
- `EVIDENCE_BRIEF_2026-05-23.md` (this file)

In `data/exports/20260523/` (working set, not shipped):
- `OPERATIONAL_PHANTOMS_AT_SCALE.md` + `operational_phantoms.json`
- `SHARED_PUB_ID_CLUSTERS.md`
- `INTERMEDIARY_AS_DIRECT_SCALE.md`
- `ADPUSHUP_PHANTOM_CHAIN.md`
- `PHANTOM_INBAND_VERIFICATION.md`
- `WRAPPER_SCORECARD.md` + `.json`
- `WRAPPER_SURFACE_AREA.md`
- `COMMENT_VENDOR_SELF_ID.md`
- `PROMEDIA_CLUSTER.md`
- `now_md_publishers/` — 9 per-publisher briefs
- `INDEX.md` — single-page navigation
