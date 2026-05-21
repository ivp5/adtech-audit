# adtech-audit receipts kit — verify any claim, no internet, no install

This kit lets anyone — journalist, regulator, plaintiffs' counsel,
academic peer reviewer — verify every claim made by this project. The
contents are sufficient and self-pointing: every fact is either
directly measured in `receipts.db` or has a live URL anyone can re-run.

## Contents

| File | Purpose | Size |
|---|---|---|
| `receipts.db.xz` | Compressed SQLite of every measurement | ~4.4 MB |
| `verify_claim.py` | Offline CLI: looks up any claim against the DB | 18 KB |
| `verify.py` | Live CLI: scans any publisher's ads.txt vs sellers.json | 2 KB |
| `RECEIPTS.md` | This file | — |

## Quickstart

```bash
# verify_claim.py auto-decompresses receipts.db.xz on first run; or
# decompress manually:
xz -dk receipts.db.xz                        # → receipts.db (~20 MB), keeps .xz
python3 verify_claim.py --provenance         # show manifest + hash
python3 verify_claim.py --premium            # premium publisher audit
python3 verify_claim.py --edgar              # EDGAR disclosure-gap URLs
python3 verify_claim.py --ssp google.com     # per-SSP fab rate
python3 verify_claim.py techcrunch.com       # any-publisher lookup
python3 verify_claim.py --aberrations        # micro-anomalies (amplification)
python3 verify_claim.py --aberrations --surface A1_pub_internal --limit 10
python3 verify.py example.com                # live ads.txt vs sellers.json scan
```

## What's in `receipts.db`

Fifteen tables. Current row counts (sealed at snapshot time, recoverable
via `SELECT COUNT(*) FROM <table>`):

- **`pair_prevalence`** — 277,589 rows. Every (SSP, seller_id) pair we
  observed in any publisher's ads.txt, with how many publishers cite it
  and how many of those citations resolve in the SSP's sellers.json
  registry. This is the substrate of every fab claim.

- **`ssp_fab_rate`** — 1,036 SSPs aggregated. Phantom rate per SSP.

- **`publisher_audit`** — 76,170 publishers. Per-domain count of
  valid / phantom / contradicted / impersonation claims.

- **`premium_publisher_audit`** — 28 pinned premium news domains across
  three cohorts: US flagship (NYT/WaPo/WSJ/Reuters/Bloomberg/Guardian/
  BBC/CNN/Vox/Atlantic/etc.), international (Le Monde/El País/Spiegel/
  Asahi/SCMP/etc.), specialty (ProPublica/ArsTechnica/Wired).
  Snapshot timestamp included.

- **`signature_carriers`** — 8 cohort signatures (cycle211_named_injection,
  smartadserver_4id, adform_1941, google_adsense_fabricated,
  ru_piracy_template, iab_spec_example_unfilled, etc.). Number of
  publishers carrying each, top-10 exemplars.

- **`publisher_managerdomain`** — 20,385 publisher → wrapper-service
  attributions via the IAB ads.txt v1.1 MANAGERDOMAIN directive.

- **`wrapper_audit`** — 384 wrappers (threshold: ≥2 publishers). Pooled
  false-rate per wrapper service (CafeMedia/Raptive, Mediavine,
  TheMoneytizer, Freestar, plus long-tail managed services).

- **`edgar_grep`** — 75 EDGAR full-text-search queries across 15 public
  ad-tech and platform-owner SEC filers (DV/IAS/MGNI/PUBM/CRTO/TTD/
  TBLA + GOOGL/META/AMZN/MSFT + CMCSA/DIS/NFLX/WBD). Each row carries
  the query URL plus the hit count we observed.

- **`external_citations`** — 16 external facts: DOJ Brinkema verdict +
  remedies trial, ANA $26B benchmark, DV class action, Kubient SEC
  precedent, IAB Tech Lab specs (sellers.json, ads.txt, AAMP),
  EU DSA Art. 39, EU AI Act, UK ICO RTB ruling, FTC dark patterns
  report, NYT v. OpenAI, COPPA enforcement, ISBA/PwC 2020 supply-chain
  study, ANA 2020 precursor.

- **`named_findings`** — 16 curated headline-grade findings, each with
  a `verifiable_via` SQL/shell snippet a reviewer can re-run.

- **`snapshot_chain`** — hash-chained snapshot history. Each row records
  the as-built sha256 of the receipts.db at that build, plus the prior
  build's hash. Tamper-evidence over the build history.

- **`manifest`** — schema version, snapshot timestamp, corpus source
  bytes, methodology, license terms.

- **`publisher_confidence_summary`** — per-publisher continuous
  confidence aggregates (cycle 2026-05-21 amplification layer). The
  previous tier scheme collapsed each claim to one of 6 buckets; this
  layer computes a continuous confidence ∈ [0, 1] per (publisher, SSP,
  seller_id) DIRECT pair by fusing 11 signals via log-odds, then rolls
  up per-publisher: `mean`, `p10`, `p50`, `p90`, `sd`, `n_very_low`,
  `n_very_high`, plus `frac_paper`, `frac_operational`,
  `frac_phantom_explicit` (the fraction of pairs whose signals fired).

- **`ssp_confidence_summary`** — per-SSP equivalent: `n_publishers`,
  `n_pairs`, plus distribution stats over per-publisher mean
  confidence. Identifies SSPs whose pub-population is structurally
  bimodal (one tier clean, another targeted-injected).

- **`pair_aberrations_top`** — top-500-per-surface specific anomalies.
  Three surfaces: **A1 publisher-internal pair outliers** (one pair
  >= 2σ below the publisher's other pairs — micro-injection
  candidates), **A2 SSP-internal publisher outliers** (one publisher
  >= 2σ below the SSP's pub-mean distribution — targeted-campaign
  candidates), **A3 cross-SSP coherence violations** (publishers
  spanning ≥3 confidence tiers across ≥4 SSPs — wrapper-mixed
  portfolios). Each row is a specific tuple a reviewer can open.

## Verifying the central claims

Each claim in the project's outputs maps to a query you can run here:

| Claim | Verify with |
|---|---|
| "Across DV, IAS, MGNI, OpenX, Criteo 10-Ks: 0 mentions of `sellers.json`" | `verify_claim.py --edgar` (re-run any URL) |
| "17% of unique pair claims have no registry match" | `SELECT SUM(n_phantom)*1.0/SUM(n_publishers) FROM pair_prevalence;` |
| "Premium publishers also affected (TechCrunch 94%, NYT 30%, BBC 21%)" | `verify_claim.py --premium` |
| "Top-volume SSPs: Google 43%, Taboola 62%, IndexExchange 52%" | `verify_claim.py --ssp google.com` |
| "12,499 publishers carry the cycle211_named_injection signature" | `verify_claim.py --signature cycle211_named_injection` |
| "TheMoneytizer wrapper: 998 publishers, 83% pooled false-rate" | `SELECT * FROM wrapper_audit WHERE managerdomain='themoneytizer.com';` |
| "ANA quantified $26B/yr programmatic waste" | `SELECT * FROM external_citations WHERE fact_id='ana_q2_2025_benchmark';` |
| "Continuous per-pair confidence (replaces 6-tier verdict)" | `SELECT mean_confidence, p10_confidence, p90_confidence FROM publisher_confidence_summary WHERE domain='nytimes.com';` |
| "Micro-aberrations the binary tier buried" | `SELECT * FROM pair_aberrations_top WHERE surface='A1_pub_internal' ORDER BY metric DESC LIMIT 10;` |
| "SSPs with bimodal publisher confidence (clean vs targeted-injection split)" | `SELECT ssp, n_publishers, mean_pub_confidence, n_pubs_very_low, n_pubs_high FROM ssp_confidence_summary WHERE n_pubs_very_low > 5 AND n_pubs_high > 5;` |

## Methodology in one paragraph

For each publisher's `ads.txt` (per IAB Tech Lab spec v1.1), we extract
each `(SSP, seller_id, rel)` triple. For each declared SSP, we fetch
the SSP's `sellers.json` (per IAB Tech Lab spec v1.0). A claim is
**valid** if the seller_id appears in the SSP's registry with matching
seller_type. **phantom** if absent entirely. **contradicted_type** if
present but with a different seller_type. **impersonation_undisclosed**
if present but with a different reg_domain. Each verdict is recorded
with the snapshot timestamp.

The reproducer (release/verify.py, MIT license, ~46 lines stdlib) lets
anyone re-run this against any publisher in seconds.

## Provenance

The 14GB primary corpus is upstream of this file. The receipts file
is built atomically (Theo Tso rename pattern) so partial-build states
are never committed to the canonical filename. Every measurement has
either a snapshot timestamp, a live URL, or a primary-source citation
attached. The `manifest` table records the corpus source bytes, schema
version, methodology, and snapshot ISO timestamp.

### Integrity model

The published artifact is **`receipts.db.xz`** (immutable, sealed
once per build). Its sha256 is in **`receipts.db.xz.sha256`** (BSD
format: `<hash>  receipts.db.xz`). Verify with:

```
shasum -a 256 -c receipts.db.xz.sha256
```

The extracted `receipts.db` is mutable (SQLite VFS may touch headers
on open) so its disk hash is NOT verifiable in isolation; the
`snapshot_chain.self_sha256` value is the hash the .db had at build
time and is informational, NOT a self-validating identifier. The
canonical hash lives in the sidecar over the .xz.

**Limitation:** if an attacker controls both the .xz and the .sidecar,
they can substitute a forged pair. For court-grade evidence, sign the
sidecar with a key whose public counterpart was published before the
relevant date (e.g. via Git tag, IPFS pin, or third-party timestamp
service). This kit does NOT ship signed checksums — that step is
manual and external.

### Reproducibility

**Bytes ARE reproducible** (as of cycle 441, 2026-05-22).

Two consecutive `python3 saas/build_receipts.py --deterministic` runs
now produce byte-identical `receipts.db`, `receipts.db.xz`, and
`receipts.db.xz.sha256`. Verified by direct comparison of the artifact
SHAs across runs.

The root cause of the cycle-438 byte-non-determinism was a single
variable: `refresh_edgar_counts.py` was stamping wall-clock
`int(time.time())` into the `fetched_ts` column on 75 EDGAR-grep rows
each build. Cycle 441 plumbs the deterministic `now = corpus_db.mtime`
through to the refresher so the timestamp is stable across rebuilds.
All other writes already used `now`.

**Verification path:**
```bash
# Byte equality (now reliable):
shasum -a 256 -c receipts.db.xz.sha256
# Content equality (also reliable, independent of build determinism):
xz -dc your_receipts.db.xz | sqlite3 - \
  "SELECT COUNT(*), SUM(false_rate_pct) FROM publisher_audit"
```

The sha256 sidecar IS a build reproducibility proof: if you rebuild
from source with `--deterministic` and the same input snapshot
(`adstxt_derived.db`, `amplification.db`), the sidecar will match.
Cycles 438-440 had a caveat here that is now obsolete.

## License

- `verify_claim.py`, `verify.py` — MIT
- `receipts.db` data — CC0 (public domain dedication)
- This README — CC0

No warranty. The data reflects the state of the IAB Tech Lab spec
implementations at snapshot time. Operator behavior may evolve. Re-run
the reproducer periodically to compare current state against historic.
