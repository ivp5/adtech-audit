# Template fingerprints — mid-harvest snapshot

_Generated 2026-04-15 against live `evidence.db`. Updates automatically each finalize run._

> **Snapshot pin.** Counts ("3,438 pubs", "27,095 publishers / 42% of corpus", "8,148 publishers / 12.6% of corpus") describe the **2026-04-15 corpus (~64,500 pubs)**. Live corpus is now 76,169 (2026-04-27). Templates A/B/C/D and the phantom-ID library replicate; the publisher denominators have grown ~18%.
>
> **2026-04-27 refinement on Adagio (per ERRATA E-2026-04-27-k).** ERRATA E-2026-04-22-d initially framed Adagio as the template-author layer above the nine "named primary injectors." Live fetch of `https://adagio.io/ads.txt` shows that Adagio's *own* template publishes its block as RESELLER, not DIRECT (the only DIRECT line for adagio.io itself is COMMENTED OUT in their template). Yet 882 publishers carry both `# Adagio_0_6` markers and `rubicon/17280 DIRECT` (Seedtag) on the same file — verified in the database, with paired examples on softonic.se (multiple adagio.io seller_ids RESELLER plus rubicon/17280 DIRECT) and parati.com.ar (same pattern). The DIRECT injection is therefore *not* added by Adagio; it is added by a *separate* aggregator that composes Adagio's RESELLER block side-by-side with Seedtag's DIRECT lines into one rendered file. The composing-aggregator layer is not yet identified by name. Treat Adagio as a *clean template author* whose work gets bundled into a multi-template publisher composition that *also* carries Seedtag's contradictions.
>
> **2026-04-27 corporate-name update on the named injectors (per ERRATA E-2026-04-27-d, -i).** The brand names this document uses (Seedtag, Rich Audience, SunMedia) map to Spanish *sociedad limitada* corporate entities verified against Rubicon's sellers.json across three Wayback snapshots (2021-02-11, 2023-06-15, 2026-04-26):
>
> | Brand | Corporate entity | Country / Authority |
> |---|---|---|
> | Seedtag | Seedtag Advertising SL | Spain — AEPD |
> | Rich Audience | Rich Audience Technologies SL (renamed from Pubnet Publicidad Y Marketing SL between 2021-02 and 2023-06) | Spain — AEPD |
> | SunMedia | VLN Servicios Publicitarios Integrales SL | Spain — AEPD |
> | Themoneytizer | Themoneytizer SA | France — CNIL |
> | SmartAdServer | Equativ SAS (post-merger) | France — CNIL |
>
> Smile Wanted (smilewanted.com), MGID Inc (mgid.com), and Adtelligent Inc (adtelligent.com) are confirmed as INTERMEDIARY in lijit.com/sellers.json (Sovrn registry, contact `support@sovrn.com`); the 244287-eb seller_id used in Template A is confirmed PHANTOM in Lijit's registry — the `-eb` suffix variant does not exist as a Sovrn account.

A template fingerprint is a set of seller_ids that co-occur on publishers at
high frequency. If N publishers all claim the same ~6 phantom seller_ids
together, they are not independently making up those IDs — they are carrying
the same source file.

Sampled from 900-pub slices of each anchor entry. Co-occurrence percentages are
over the sample, restricted to PHANTOM/CONTRADICTED pairs.

## Template A — the "onetag-lijit-ix" ring (anchored by onetag/5d4e & lijit/244287-eb)

| Anchor A (onetag-5d4e, 3,438 pubs) | Anchor B (lijit-244287-eb, 3,477 pubs) |
|---|---|
| 84.6% indexexchange.com/190906 | 90.8% indexexchange.com/190906 |
| 72.8% lijit.com/244287-eb | 75.1% onetag.com/5d4e109247a89f6 |
| 72.0% rubiconproject.com/13510 | 73.1% rubiconproject.com/13510 |
| 69.0% appnexus.com/8233 | 72.4% appnexus.com/8233 |
| 67.7% emxdgt.com/1701 | 71.3% adform.com/1941 |
| 65.3% smartadserver.com/4071 | 71.2% emxdgt.com/1138 |

The two anchors cross-reference each other at ~75%. Both carry
indexexchange.com/190906, rubiconproject.com/13510, and appnexus.com/8233 as
co-present lines. This is one template, shared by ~3,500 publishers, with at
least ~10 phantom seller_ids embedded.

## Template B — the "themediagrid-DJQVCM" ring (3,270 pubs)

| Co-occurring pair | Share of sample |
|---|---|
| onetag.com/61d88450bdb25bc-OB | 81.9% |
| rubiconproject.com/22884 | 73.6% |
| google.com/pub-8622186303703569 | 60.1% |
| onetag.com/61d88450bdb25bc | 60.0% |
| pubmatic.com/157743 | 58.1% |
| lijit.com/346012 | 57.9% |

A distinct template. Note that this ring uses **different** onetag and lijit
seller_ids from Template A (61d88450bdb25bc vs 5d4e109247a89f6; 346012 vs
244287-eb) — the two templates are NOT the same file.

## Template C — the "CAS SDK" ring (4,869 pubs at 97.2% overlap)

| Pair | Share |
|---|---|
| smartadserver.com/4073 + smartadserver.com/4074 | 97.2% union-overlap |

Both IDs are Dynadmic currency sub-accounts (BRL, MXN) that were classified
INTERMEDIARY under dynadmic.com in the 2022-07 Wayback snapshot and have since
been de-registered from smartadserver.com/sellers.json. The CAS SDK
[App-ads.txt repo](https://github.com/cleveradssolutions/App-ads.txt) still
ships them as DIRECT lines with `060d053dcf45cbf3` as the TAG-ID.

## Why this matters

Template fingerprints are the mechanism proof that would be asked for if anyone
thought the 58–59% false rate was a product of random publisher fabrication:

1. If publishers were fabricating independently, co-occurrence would be near
   zero. Observed: 70–95% on multi-ID pairs.
2. If publishers were making honest errors, the errors would not converge on
   identical multi-ID sets. Observed: three distinct, stable fingerprints.
3. If the SSPs' sellers.json were wrong, the error would be at the SSP side,
   not at the publisher side. But all three SSPs (OneTag, Lijit, IX) agree:
   these IDs do not exist.

The propagation mechanism is template distribution without cross-verification.
The templates are CAS SDK, a PBS-ish ring (A), and a themediagrid-anchored ring
(B). The content of those templates has been constant across a 2x harvest
expansion.

## Template D — Dynadmic TAG-ID `060d053dcf45cbf3` (27,095 publishers / 42% of corpus)

The TAG-ID that appears in the CAS SDK and Digital Turbine templates
(`smartadserver.com, 4073, DIRECT, 060d053dcf45cbf3`) is a Dynadmic-wide
identifier. Tracing all lines carrying this TAG-ID across the harvest:

- **27,095 publishers** carry at least one line tagged `060d053dcf45cbf3`
- **413,136 total line occurrences** on `smartadserver.com` alone
- Spread across 15+ distinct seller_ids: 4125, 1999, 4537, 4926, 1743, 3389,
  4005, 3056, 3436, 4625, 4106, 4288, 3379, 3238, etc. — mostly as RESELLER,
  with 4073/4074 as DIRECT in the CAS/DT variant
- **Also leaked into other SSPs** (much smaller tails): sharethrough (622),
  improvedigital (48), smilewanted (48), contextweb (44), rubiconproject (15),
  pubmatic (8), google (3), appnexus (3), mgid (3), sonobi (2), themediagrid
  (2), yieldmo (2)

Evidence of typo propagation: the TAG-ID shows up under `martadserver.com`
(missing 's', 539 lines), `"smartadserver.com` (28 lines), `smartadserver.comâ`
(12 lines, UTF-8 corruption), `http://smartadserver.com` (13 lines). These
errors propagate intact across publishers because nobody validates ads.txt —
the template file gets copied with whatever typos the original author made.

**Interpretation**: Dynadmic's original partner list (pre-acquisition by SAS
in 2019) contained this TAG-ID. When they were rolled up, the partner list
got absorbed into multiple templates (CAS SDK, Digital Turbine, unknown
others), each of which then propagated to thousands of publishers. The
TAG-ID is therefore a genetic marker of template phylogeny.

## Self-contradiction — publishers asserting DIRECT + RESELLER for the same seller

A DIRECT claim and a RESELLER claim for the same (SSP, seller_id) on the same
publisher's ads.txt are mutually exclusive. A publisher can either directly
control an account or resell through it — not both.

- **654,502 self-contradictions** across the corpus
- **24,817 publishers (38% of current 64K pool)** have ≥1 self-contradiction
- **6,665 publishers** have ≥20 self-contradictions
- Top conflicting pairs are mostly Template-A constituents:
  `rubiconproject.com/13510` (4,871 pubs), `smartadserver.com/4071` (4,252),
  `appnexus.com/8233` (4,230), `smaato.com/1100004890` (4,178),
  `smartadserver.com/4073` (3,573), `smartadserver.com/4074` (3,616),
  `rubiconproject.com/22884` (3,531)

The mechanism: publishers adopt multiple monetization templates. Template A
adds a line as DIRECT, template B adds the same seller as RESELLER. Nobody
deduplicates. The file ends up internally inconsistent.

This is independent from the sellers.json cross-reference — a publisher's
ads.txt can be self-contradictory BEFORE you even check the SSP registry.
The file is not a testament to anything; it is a sedimentary deposit of
every template that ever touched the publisher.

## The piracy / grey-market mega-template (≈11,000 lines, ~6,665 pubs)

The most-contradicted publishers cluster in the piracy / scanlation / chat /
conspiracy ecosystem. They share a ~11,000-line ads.txt template at 53–70%
line-identical overlap.

| Publisher | Total lines | Overlap with `scan-manga.com` |
|---|---:|---:|
| scan-manga.com | 11,476 | base |
| www.mgeko.cc | 13,603 | 7,290 (53.6%) |
| readcomiconline.to | 11,048 | 6,270 (56.8%) |
| readcomiconline.li | 11,048 | 6,270 (56.8%) |
| mangaread.org | 10,606 | 6,183 (58.3%) |
| leercapitulo.re | 11,016 | 6,471 (58.7%) |
| mangabuddy.me | 10,490 | 6,173 (58.8%) |
| whatreallyhappened.com | 9,381 | 5,525 (58.9%) |
| mangago.me | 11,081 | 6,788 (61.3%) |
| mangago.zone | 11,288 | 7,308 (64.7%) |
| talkwithstranger.com | 9,479 | 6,617 (69.8%) |

Normal ads.txt is 50–500 lines. This template is 20–200× larger. Publishers
adopting it inherit every contradiction, every phantom, every obsolete
relationship the template has accumulated. Grey-market ad tech is the
incumbent in the cumulative-template equilibrium — there is no clean path
out once the template has been installed, because removing lines would drop
inventory and revenue.

Piracy / grey-market publishers are neither the origin nor a tail effect of
the false-rate problem. They are the end state that every publisher drifts
toward as templates accumulate unchecked.

## The phantom library — cross-template Google ID reuse

Tracing 218 phantom Google seller_ids found on `scan-manga.com` back across
the full corpus reveals that phantom IDs are not template-specific
fabrications. **117 of 218 (54%) are claimed as DIRECT by ≥100 other
publishers.** Median propagation per phantom is 135 publishers; max reach
is 3,537 publishers for `google.com/pub-8622186303703569`.

Cross-template overlap on the top 5 phantom Google IDs:

| Phantom Google ID | Template A | Template B | Template C (CAS) | Reach |
|---|---:|---:|---:|---:|
| `pub-8622186303703569` | 1,368 | 1,970 | 2,178 | 3,537 |
| `pub-7002491002409919` | 883 | 1,123 | 1,215 | 1,894 |
| `pub-9378724246417115` | 707 | 674 | 962 | 1,846 |
| `pub-6733417337840393` | 986 | 955 | 1,103 | 1,744 |
| `pub-6645287046856849` | 568 | 804 | 961 | 1,421 |

Every major template — A (onetag-lijit-IX ring), B (themediagrid), C (CAS
SDK) — embeds the same phantom Google IDs. The phantom IDs precede the
templates. They are library components that template authors copy from
prior templates (or from each other) without verification.

**Overall Google-phantom scale**:
- Google DIRECT claims in corpus: 331,887
- Google PHANTOM claims: 146,433 (**44.1%**)
- Top 25 phantom Google IDs collectively carried by **8,148 unique publishers
  (12.6% of corpus)**

All phantom IDs use the canonical `pub-XXXXXXXXXXXXXXXX` format that Google
itself issues. They cannot be distinguished from real IDs by format alone.
Only a runtime check against `sellers.json` can flag them — a check that
DSPs do not perform at bid time.

The mechanism is not random fabrication. It is **shared template infrastructure
inheriting a phantom ID library across generations**. The phantoms persist
because the templates persist, and the templates persist because the publishers
that install them never diff against sellers.json.
