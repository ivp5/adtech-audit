# Descriptive claims (non-SQL-verifiable)

Cycle 481 (2026-05-22): per simplification directive, descriptive claims
that require Python-computed analyses (cross-DB correlations, hash-set
clustering, multi-bucket decompositions) live here instead of
CLAIMS.jsonl. They are documented in ERRATA + memory but not auto-run
by `tools/claims.py evaluate-all` — that framework only runs SQL claims
that evaluate to scalars.

These are still **claims** — just verified by reading the cited
artifact (memory/cycle_*.md), not by SQL.

## C028: Pearson correlation between declarative and observed phantom rates

**Prose:** Pearson r=0.1546 between per-publisher declarative phantom rate and observed unauthorized rate (n=66 X-Ray-observed pubs)

**Expected value:** 0.15

**Note:** The two phantom modes are nearly independent. Computed in Python by joining adstxt_triples phantom aggregates per pub with xray_journal.db prebid_json bidder lists. n=66 pubs.

**Cited in:** ERRATA.md:E-2026-05-22-k, memory/cycle_465_two_phantom_modes_independent_20260522.md

---

## C029: shared-fingerprint publisher clusters

**Prose:** 1,102 shared-fingerprint clusters span 10,723 publishers (14.4% of corpus) and account for 634,121 phantom claims (28.6% of total)

**Expected value:** 10723

**Note:** Computed in Python via SHA1 hash of sorted phantom (ssp,seller_id) set per pub. Exact-match only (Jaccard 1.0). Loose-match clustering would find more.

**Cited in:** ERRATA.md:E-2026-05-22-l, memory/cycle_466_template_decay_structure_20260522.md

---

## C032: phantom volume in low-rate bucket (potential misconduct shape)

**Prose:** 56,140 phantom claims (2.5% of total) are in the <10% per-SSP phantom rate bucket — the only bucket with shape consistent with individual publisher misconduct

**Expected value:** 56140

**Note:** Decomposition computed in Python by binning each SSP's phantom rate and summing phantom counts within bins. Buckets: <10% (accidental shape), 10-50% (staleness), 50-90% (template-driven), >90% (orphan/dead). Only the <10% bucket has the publisher-misconduct shape; the other 97.5% has identifiable structural mechanisms.

**Cited in:** ERRATA.md:E-2026-05-22-n, memory/cycle_468_fraud_framing_falsified_20260522.md

---

