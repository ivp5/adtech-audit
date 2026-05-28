# PROPOSED correction to PAPER.md abstract — NOT YET APPLIED

> Staged 2026-05-29 PASS-2. This file is a STAGED DIFF for review, not an
> applied edit. PAPER.md is the published thesis; correcting it needs
> explicit approval. Reviewer: approve → apply to PAPER.md lines 15 + 97;
> reject → delete this file.

## Why

Two abstract sentences infer "not staleness → fabrication" from a SPATIAL
re-fetch test (fetch more registries, count reclassifications) that is
structurally blind to TEMPORAL staleness (sellers that WERE in the registry
and got pruned).

EVIDENCE BASIS (corrected after a coverage check). The temporal claim rests
primarily on the coefficient-of-variation discriminator (phantom-count
variance per publisher across 9 snapshots), which is valid for ALL
publishers regardless of whether their file changed — the better instrument.
It was verified to cover the phantom volume, not just a convenient subset:
- stable-file publishers (file unchanged ±2 lines): 83% of publishers but
  only 22% of phantom volume — 3% pinned (CV<0.02), 97% fluctuating.
- changing-file publishers: 17% of publishers but 78% of phantom volume —
  2% pinned, 98% fluctuating.
Both cohorts give the same ~97/3 split, so it holds on the FULL corpus, not
just the stable minority. (The earlier stable-file-only decay test — 69%
rose / 13% fell, 18.9:1 ratchet — is corroborating but covers only the 22%;
the CV discriminator is what generalizes.) The 97/3 split independently
reproduces the project's cycle-468 mechanism decomposition (97.5%
structural / 2.5% misconduct) by an unrelated method. See ERRATA
E-2026-05-29-a, E-2026-05-29-b, E-2026-05-29-c.

The spatial findings themselves are TRUE and kept (2.7% reclassify on
re-fetch; 0.2% on the larger expansion). What changes is the INFERENCE:
"few reclassify on re-fetch" means "few are spatially-stale," NOT
"few are stale" — temporal decay is invisible to that test and dominates.

---

## Line 15 — the phantom sentence

### CURRENT (contradicted clause in **bold**)

> The phantom rate (28%) is ambiguous; 100% of numeric phantom IDs fall
> within valid ranges for their SSP, consistent with either deleted accounts
> or fabrication. A follow-up fetch of 238 additional SSP registries
> (covering 224,222 new seller IDs) reclassified only 2.7% of existing
> phantoms to PLAUSIBLE, **indicating fabrication dominates staleness by
> ~36:1.**

### PROPOSED

> The phantom rate (28%) is dominantly temporal decay, not fabrication.
> 100% of numeric phantom IDs fall within valid ranges for their SSP. A
> follow-up fetch of 238 additional SSP registries reclassified only 2.7%
> of phantoms to PLAUSIBLE — but this re-fetch tests only SPATIAL staleness
> (is the seller in a registry we had not yet fetched) and is blind to
> TEMPORAL staleness (sellers that were in the registry and were later
> pruned). Tracking publishers whose ads.txt stayed fixed across nine
> snapshots, phantom ROSE on 69% and fell on 13% with the file unchanged —
> the publishers did nothing; registries dropped sellers beneath them —
> accumulating 18.9:1 (gained vs cleared). The phantom rate is thus a
> decay-equilibrium metric. A coefficient-of-variation test separates the
> two: 97% of stable-file phantom fluctuates over time (decay; cohort
> median CV 0.14), while 3% is pinned (CV<0.02, fabrication — e.g.
> taboola.com at CV 0.0003). This 97/3 split independently matches our
> mechanism-attribution decomposition (§N). Fabrication is real but a small,
> temporally-pinned minority; the bulk of the phantom rate is registry
> decay acting on copied-and-unmaintained ads.txt blocks.

---

## Line 97 — the stability/ratio bullet

### CURRENT (contradicted clause in **bold**)

> Stability: the false rate is stable across 12 successive SSP expansions …
> The expansion from 710 to 1,108 registries on 2026-04-22 rechecked 75,799
> existing phantoms against 398 newly-fetched registries; 1,196 reclassified
> to PLAUSIBLE, or 0.20% of the total 585,401-row phantom class. **Staleness
> cannot account for more than 0.2% of the phantom class. The
> fabrication-to-staleness ratio is approximately 490:1.**

### PROPOSED

> Stability: the false rate is stable across 12 successive SSP expansions …
> The expansion from 710 to 1,108 registries rechecked 75,799 phantoms
> against 398 newly-fetched registries; 1,196 reclassified to PLAUSIBLE
> (0.20%). **SPATIAL** staleness — phantoms resolved by fetching more
> registries — therefore accounts for ≤0.2% of the class. This does NOT
> bound TEMPORAL staleness (registry pruning over time), which a fixed-file
> longitudinal test shows is the dominant driver (97% of stable-file phantom
> fluctuates with registry churn; 18.9:1 accumulation ratchet). The earlier
> "fabrication-to-staleness ~490:1" figure conflated the two staleness axes
> and is superseded; the corrected estimate is ~3% pinned fabrication /
> ~97% temporal decay (ERRATA E-2026-05-29-a, E-2026-05-29-b).

---

## Apply commands (for the reviewer, once approved)

The two replacements are exact-string edits to release/PAPER.md. The named
apex case studies (Taboola §, named injectors §) are UNCHANGED — they are
the pinned-fabrication 3% and survive (verified CV<0.02). Only the abstract's
corpus-wide fabrication inference is corrected.
