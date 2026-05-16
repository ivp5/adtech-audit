# adtech-audit receipts kit — verify any claim, no internet, no install

This kit lets anyone — journalist, regulator, plaintiffs' counsel,
academic peer reviewer — verify every claim made by this project. The
contents are sufficient and self-pointing: every fact is either
directly measured in `receipts.db` or has a live URL anyone can re-run.

## Contents

| File | Purpose | Size |
|---|---|---|
| `receipts.db.xz` | Compressed SQLite of every measurement | ~4 MB |
| `verify_claim.py` | Offline CLI: looks up any claim against the DB | 15 KB |
| `verify.py` | Live CLI: scans any publisher's ads.txt vs sellers.json | 2 KB |
| `RECEIPTS.md` | This file | — |

## Quickstart

```bash
# verify_claim.py auto-decompresses receipts.db.xz on first run; or
# decompress manually:
xz -dk receipts.db.xz                        # → receipts.db (~22 MB), keeps .xz
python3 verify_claim.py --provenance         # show manifest + hash
python3 verify_claim.py --premium            # premium publisher audit
python3 verify_claim.py --edgar              # EDGAR disclosure-gap URLs
python3 verify_claim.py --ssp google.com     # per-SSP fab rate
python3 verify_claim.py techcrunch.com       # any-publisher lookup
python3 verify.py example.com                # live ads.txt vs sellers.json scan
```

## What's in `receipts.db`

Twelve tables. Current row counts (sealed at snapshot time, recoverable
via `SELECT COUNT(*) FROM <table>`):

- **`pair_prevalence`** — 277,589 rows. Every (SSP, seller_id) pair we
  observed in any publisher's ads.txt, with how many publishers cite it
  and how many of those citations resolve in the SSP's sellers.json
  registry. This is the substrate of every fab claim.

- **`ssp_fab_rate`** — 1,036 SSPs aggregated. Phantom rate per SSP.

- **`publisher_audit`** — 76,170 publishers. Per-domain count of
  valid / phantom / contradicted / impersonation claims.

- **`premium_publisher_audit`** — 14 pinned premium news domains.
  Snapshot timestamp included.

- **`signature_carriers`** — 8 cohort signatures (cycle211, sovrn-eb,
  smartadserver-4id, etc.). Number of publishers carrying each, top-10
  exemplars.

- **`publisher_managerdomain`** — 20,385 publisher → wrapper-service
  attributions via the IAB ads.txt v1.1 MANAGERDOMAIN directive.

- **`wrapper_audit`** — 261 wrappers. Pooled false-rate per wrapper
  service (CafeMedia/Raptive, Mediavine, TheMoneytizer, Freestar, etc.)

- **`edgar_grep`** — 35 EDGAR full-text-search queries. Each row carries
  the query URL plus the hit count we observed. A reader who clicks the
  URL gets the current count.

- **`external_citations`** — 8 external facts (DOJ Brinkema verdict,
  ANA $26B benchmark, DV class action, etc.) with source URLs.

- **`named_findings`** — 12 curated headline-grade findings, each with
  a `verifiable_via` SQL/shell snippet a reviewer can re-run.

- **`snapshot_chain`** — hash-chained snapshot history. Each row records
  the as-built sha256 of the receipts.db at that build, plus the prior
  build's hash. Tamper-evidence over the build history.

- **`manifest`** — schema version, snapshot timestamp, corpus source
  bytes, methodology, license terms.

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

Two builds from the same corpus produce byte-identical data tables
modulo three timestamp columns (`snapshot_chain.snapshot_ts`,
`manifest.snapshot_iso`, `premium_publisher_audit.snapshot_ts`) and
the EDGAR live counts (which reflect SEC's index at fetch time).
The `--skip-edgar` flag to `build_receipts.py` produces builds
without live EDGAR data for fast comparison.

## License

- `verify_claim.py`, `verify.py` — MIT
- `receipts.db` data — CC0 (public domain dedication)
- This README — CC0

No warranty. The data reflects the state of the IAB Tech Lab spec
implementations at snapshot time. Operator behavior may evolve. Re-run
the reproducer periodically to compare current state against historic.
