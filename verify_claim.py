#!/usr/bin/env python3
"""
verify_claim.py — offline claim verifier against receipts.db.

Companion to release/verify.py (live ads.txt × sellers.json verifier).
This tool reads only the local receipts.db file — no internet — and
lets anyone audit any claim made by the project.

Usage:
  python3 verify_claim.py example.com                 # any-publisher lookup
  python3 verify_claim.py --ssp google.com            # SSP-level fab rate
  python3 verify_claim.py --signature cycle211_named_injection
  python3 verify_claim.py --premium                   # pinned premium pubs
  python3 verify_claim.py --edgar                     # EDGAR query URLs
  python3 verify_claim.py --provenance                # manifest + file hash

Designed for: journalists, regulators, plaintiffs' counsel, academic
peer reviewers. The receipts file is the truth; this tool is read.

Provenance: every fact carries either a runnable EDGAR URL or a corpus
snapshot timestamp. The receipts.db is built from the 14GB primary
corpus; this 4MB-xz file is sufficient to verify every public claim.

License: MIT (this script). Receipts data: CC0.
"""
import argparse
import gzip
import hashlib
import sqlite3
import sys
from pathlib import Path

# ── INOCULATION 3: stdlib feature probe ───────────────────────────────
# Minimal Python distributions (some Alpine images, embedded builds,
# Docker python:slim variants in years past) ship without _lzma compiled
# in. The kit's canonical artifact is .xz; without lzma we cannot
# decompress. Surface a HELPFUL error instead of `ModuleNotFoundError`.
try:
    import lzma
except ImportError:
    print('ERROR: this Python lacks the `lzma` stdlib module.', file=sys.stderr)
    print('  The kit ships receipts.db.xz which requires lzma to decode.',
          file=sys.stderr)
    print('  Workarounds:', file=sys.stderr)
    print('    1. Run `xz -dk receipts.db.xz` from the CLI to extract',
          file=sys.stderr)
    print('       receipts.db directly, then re-run this script.',
          file=sys.stderr)
    print('    2. Install Python from python.org (stdlib-complete) or '
          'use the system Python.', file=sys.stderr)
    print(f'  Your interpreter: {sys.executable} ({sys.version.split()[0]})',
          file=sys.stderr)
    sys.exit(2)

DEFAULT_RECEIPTS = Path(__file__).resolve().parent / 'receipts.db'


def open_receipts(path: Path) -> sqlite3.Connection:
    if not path.exists():
        # Try xz first (preferred, ~4 MB) then gz (legacy, ~9 MB)
        for ext, decompress in (('.db.xz', lzma.decompress),
                                ('.db.gz', gzip.decompress)):
            cand = path.with_suffix(ext)
            if cand.exists():
                print(f'decompressing {cand} → {path}', file=sys.stderr)
                path.write_bytes(decompress(cand.read_bytes()))
                break
    if not path.exists():
        print(f'ERROR: {path} not found.', file=sys.stderr)
        print('Download from project release page or rebuild from corpus.',
              file=sys.stderr)
        sys.exit(1)
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)


def normalize_domain(d: str) -> str:
    return (d.lower().strip()
            .removeprefix('https://').removeprefix('http://').removeprefix('www.')
            .rstrip('/'))


def cmd_live_verify(domain: str) -> int:
    """Cycle 435: bridge frozen receipts → live world. Fetches ads.txt +
    sellers.json AT THIS MOMENT and produces a verdict against current
    reality, not against the receipts.db snapshot. Implements verify.py
    logic inline (no import dependency on the sibling script).

    The frozen receipts.db verdict is what the project ships. But every
    verdict ages: registries change, ads.txt is updated, publishers add
    or remove partners. Without a live re-check, a user reading the
    frozen verdict has no way to know if it still reflects reality.
    This bridge gives them BOTH numbers when they want them.
    """
    from urllib.request import Request, urlopen
    from collections import Counter
    import json as _json, csv as _csv
    from functools import lru_cache

    def fetch(url: str) -> str:
        return urlopen(
            Request(url, headers={'User-Agent': 'verify_claim/live'}),
            timeout=20
        ).read().decode('utf-8', 'replace')

    @lru_cache(maxsize=None)
    def load_registry(ssp: str):
        # cycle 434: a few SSPs publish sellers.json at a non-canonical URL
        OVERRIDES = {
            'google.com':       'https://realtimebidding.google.com/sellers.json',
            'doubleclick.net':  'https://realtimebidding.google.com/sellers.json',
            'sovrn.com':        'https://lijit.com/sellers.json',
            'genieesspv.jp':    'https://r.genieesspv.jp/sellers.json',
        }
        url = OVERRIDES.get(ssp, f'https://{ssp}/sellers.json')
        try:
            sellers = _json.loads(fetch(url)).get('sellers') or []
        except Exception:
            return None
        pubs, inter = set(), set()
        for s in sellers:
            sid = str(s.get('seller_id', '')).lower()
            stype = (s.get('seller_type') or '').upper().strip()
            (inter if stype == 'INTERMEDIARY' else pubs).add(sid)
        return pubs, inter

    print(f'=== {domain} (LIVE — fetched at query time) ===')
    try:
        body = fetch(f'https://{domain}/ads.txt').lstrip('﻿')
    except Exception as e:
        print(f'  could not fetch ads.txt: {e}')
        return 2
    tally = Counter()
    for fields in _csv.reader(line.split('#', 1)[0] for line in body.splitlines()):
        if len(fields) < 3 or fields[2].strip().upper() != 'DIRECT':
            continue
        ssp = fields[0].strip().lower()
        seller_id = fields[1].strip().lower()
        reg = load_registry(ssp)
        verdict = ('UNCOVERED' if reg is None
                   else 'PLAUSIBLE'    if seller_id in reg[0]
                   else 'CONTRADICTED' if seller_id in reg[1]
                   else 'PHANTOM')
        tally[verdict] += 1
    total = sum(tally.values())
    if not total:
        print('  no DIRECT lines found')
        return 2
    print(f'  total_direct claims        : {total:>7}')
    print(f'  PLAUSIBLE (in registry)    : {tally["PLAUSIBLE"]:>7}  '
          f'({100*tally["PLAUSIBLE"]/total:.1f}%)')
    print(f'  PHANTOM (no registry)      : {tally["PHANTOM"]:>7}  '
          f'({100*tally["PHANTOM"]/total:.1f}%)')
    print(f'  CONTRADICTED (type wrong)  : {tally["CONTRADICTED"]:>7}  '
          f'({100*tally["CONTRADICTED"]/total:.1f}%)')
    print(f'  UNCOVERED (SSP unreachable): {tally["UNCOVERED"]:>7}  '
          f'({100*tally["UNCOVERED"]/total:.1f}%)')
    false = tally['PHANTOM'] + tally['CONTRADICTED']
    print(f'  combined false-rate (live) : {100*false/total:>6.2f}%')
    return 0


def cmd_domain(con, domain: str, *, live_too: bool = False) -> int:
    domain = normalize_domain(domain)
    row = con.execute(
        'SELECT total_direct, direct_valid, direct_phantom, '
        '       direct_contradicted, direct_impersonated, false_rate_pct '
        'FROM publisher_audit WHERE domain = :d',
        {'d': domain}).fetchone()
    if not row:
        print(f'No measurement on file for {domain}.')
        print('Possible: not in our crawl set, or coverage gap.')
        print('Try: python3 verify_claim.py --live ' + domain)
        if live_too:
            print()
            return cmd_live_verify(domain)
        return 2
    td, dv, dp, dc, di, rate = row
    print(f'=== {domain} (from receipts.db) ===')
    print(f'  total_direct claims        : {td:>7}')
    print(f'  valid (in registry)        : {dv:>7}  ({100*dv/max(td,1):.1f}%)')
    print(f'  phantom (no registry)      : {dp:>7}  ({100*dp/max(td,1):.1f}%)')
    print(f'  contradicted (type wrong)  : {dc:>7}  ({100*dc/max(td,1):.1f}%)')
    print(f'  impersonation (domain)     : {di:>7}  ({100*di/max(td,1):.1f}%)')
    print(f'  combined false-rate        : {rate:>6.2f}%')
    pinned = con.execute(
        'SELECT snapshot_ts FROM premium_publisher_audit WHERE domain = :d',
        {'d': domain}).fetchone()
    if pinned:
        print(f'  [pinned premium publisher] snapshot epoch: {pinned[0]}')

    # Cycle 2026-05-21: surface continuous-confidence detail if the
    # amplification layer is present in this build.
    try:
        amp = con.execute(
            'SELECT n_pairs, mean_confidence, sd_confidence, '
            'p10_confidence, p50_confidence, p90_confidence, '
            'n_very_low, n_very_high, frac_paper, frac_operational, '
            'frac_phantom_explicit '
            'FROM publisher_confidence_summary WHERE domain = :d',
            {'d': domain}).fetchone()
    except sqlite3.OperationalError:
        amp = None  # table not in this build
    if amp:
        n, m, sd, p10, p50, p90, nvl, nvh, fp, fo, fpe = amp
        print(f'\n  --- amplification (continuous confidence ∈ [0,1]) ---')
        print(f'  pairs scored               : {n:>7}')
        print(f'  mean confidence            : {m:>6.3f}  (sd={sd:.3f})')
        print(f'  confidence percentiles     : p10={p10:.3f}  '
              f'p50={p50:.3f}  p90={p90:.3f}')
        print(f'  pairs at very_low (<0.05)  : {nvl:>7}  ({100*nvl/max(n,1):.1f}%)')
        print(f'  pairs at very_high (>=0.95): {nvh:>7}  ({100*nvh/max(n,1):.1f}%)')
        print(f'  signal fractions           : '
              f'paper={fp:.2f}  operational={fo:.2f}  '
              f'phantom_explicit={fpe:.2f}')
        # Aberration count
        try:
            a_rows = list(con.execute(
                'SELECT surface, COUNT(*) FROM pair_aberrations_top '
                'WHERE domain = :d GROUP BY surface',
                {'d': domain}))
            if a_rows:
                print(f'  aberrations flagged        : '
                      + ', '.join(f'{s.split("_")[0]}={n}' for s, n in a_rows))
        except sqlite3.OperationalError:
            pass

    # Cycle 435 — bridge frozen → live. The receipts.db verdict above is
    # frozen at the snapshot timestamp. If the user passes --live, also
    # do a real-time fetch of the publisher's current ads.txt + each
    # cited SSP's current sellers.json and produce a fresh verdict.
    # The DELTA between frozen and live tells the user whether the
    # receipt is still trustworthy or has been outrun by the world.
    if live_too:
        print()
        cmd_live_verify(domain)
    return 0


def cmd_ssp(con, ssp: str) -> int:
    ssp = ssp.lower().strip()
    row = con.execute(
        'SELECT total_claims, phantom_claims, valid_claims, '
        '       distinct_publishers, sellers_in_registry, false_rate_pct '
        'FROM ssp_fab_rate WHERE ssp = :s', {'s': ssp}).fetchone()
    if not row:
        print(f'No measurement on file for SSP {ssp}.')
        return 2
    total, phantom, valid, n_pubs, regsize, rate = row
    print(f'=== {ssp} (from receipts.db) ===')
    print(f'  total DIRECT claims        : {total:>9,}')
    print(f'  phantom claims             : {phantom:>9,}  ({100*phantom/max(total,1):.1f}%)')
    print(f'  valid claims               : {valid:>9,}')
    print(f'  publishers citing this SSP : {n_pubs:>9,}')
    print(f'  sellers in own registry    : {regsize:>9,}')
    print(f'  false-rate against registry: {rate:>8.2f}%')
    print()
    print(f'=== Top 15 phantom seller_ids for {ssp} ===')
    print(f'  {"seller_id":<32} {"n_pubs":>8} {"phantom":>10} {"rate":>8}')
    for sid, n_p, n_ph, r in con.execute(
        'SELECT seller_id, n_publishers, n_phantom, phantom_rate '
        'FROM pair_prevalence WHERE ssp = :s AND n_phantom > 0 '
        'ORDER BY n_phantom DESC LIMIT 15', {'s': ssp}
    ):
        print(f'  {(sid or "")[:32]:<32} {n_p:>8,} {n_ph:>10,} {r:>7.2f}%')
    return 0


def cmd_signature(con, sig: str) -> int:
    row = con.execute(
        'SELECT n_publishers, exemplar_publishers, description '
        'FROM signature_carriers WHERE signature = :s', {'s': sig}).fetchone()
    if not row:
        print(f'No signature {sig}. Available signatures:')
        for (s, n) in con.execute(
            'SELECT signature, n_publishers FROM signature_carriers ORDER BY n_publishers DESC'
        ):
            print(f'  {s:30s}  {n:,} publishers')
        return 2
    n, ex, desc = row
    print(f'=== Signature: {sig} ===')
    print(f'  Description : {desc}')
    print(f'  Publishers  : {n:,}')
    print(f'  Exemplars (top 10 by pair count):')
    for d in (ex or '').split(','):
        if d.strip():
            print(f'    • {d.strip()}')
    return 0


def cmd_premium(con) -> int:
    print('=== Premium publisher false-rate (pinned snapshot) ===')
    print(f'  {"domain":<24} {"direct":>7} {"false%":>7}')
    for d, td, rate in con.execute(
        'SELECT domain, total_direct, false_rate_pct '
        'FROM premium_publisher_audit ORDER BY false_rate_pct DESC'
    ):
        print(f'  {d:<24} {td:>7} {rate:>6.2f}%')
    return 0


def cmd_edgar(con) -> int:
    print('=== EDGAR disclosure-gap queries (live URLs to re-run) ===')
    print()
    print('Each URL returns JSON with "hits.total.value" — the count of')
    print('SEC filings by that issuer containing the term. A count of 0')
    print('means the term is absent from that issuer\'s SEC filings.')
    print()
    cur = None
    for ticker, company, term, url in con.execute(
        'SELECT ticker, company, term, search_url FROM edgar_grep '
        'ORDER BY ticker, term'
    ):
        if ticker != cur:
            print(f'\n  {ticker} — {company}')
            cur = ticker
        print(f'    "{term}":')
        print(f'      {url}')
    return 0


def cmd_report(con, target: str, out_path: Path | None = None) -> int:
    """Cycle I: generate a press-ready Markdown report on any target."""
    target = normalize_domain(target) if '.' in target else target.lower().strip()
    lines = []
    lines.append(f'# adtech-audit report: `{target}`')
    lines.append('')

    # Try as publisher
    pub = con.execute(
        'SELECT total_direct, direct_valid, direct_phantom, '
        'direct_contradicted, direct_impersonated, false_rate_pct '
        'FROM publisher_audit WHERE domain = :d', {'d': target}).fetchone()
    if pub:
        td, dv, dp, dc, di, rate = pub
        lines.append('## Publisher audit')
        lines.append('')
        lines.append(f'`{target}` has **{td:,} DIRECT** seller relationships declared in its '
                     f'`ads.txt`. Of these, **{dv:,} ({100*dv/max(td,1):.1f}%) are verified** '
                     f'against the named SSP\'s own `sellers.json` registry.')
        lines.append('')
        lines.append('| Verdict | Count | % |')
        lines.append('|---|---:|---:|')
        lines.append(f'| valid (in SSP registry) | {dv:,} | {100*dv/max(td,1):.1f}% |')
        lines.append(f'| phantom (no registry record) | {dp:,} | {100*dp/max(td,1):.1f}% |')
        lines.append(f'| contradicted (wrong seller_type) | {dc:,} | {100*dc/max(td,1):.1f}% |')
        lines.append(f'| impersonation (wrong domain) | {di:,} | {100*di/max(td,1):.1f}% |')
        lines.append('')
        lines.append(f'**Combined false-rate: {rate:.2f}%.**')
        lines.append('')
        # Wrapper attribution
        wrappers = list(con.execute(
            'SELECT managerdomain FROM publisher_managerdomain WHERE domain = :d',
            {'d': target}))
        if wrappers:
            lines.append('### Wrapper attribution (MANAGERDOMAIN)')
            lines.append('')
            for (m,) in wrappers:
                wa = con.execute(
                    'SELECT n_publishers, pooled_false_rate_pct FROM wrapper_audit '
                    'WHERE managerdomain = :m', {'m': m}).fetchone()
                if wa:
                    lines.append(f'- `{m}` (managing {wa[0]:,} publishers; pooled '
                                 f'false-rate {wa[1]:.1f}%)')
                else:
                    lines.append(f'- `{m}`')
            lines.append('')

    # Try as SSP
    ssp = con.execute(
        'SELECT total_claims, phantom_claims, valid_claims, distinct_publishers, '
        'sellers_in_registry, false_rate_pct FROM ssp_fab_rate WHERE ssp = :s',
        {'s': target}).fetchone()
    if ssp:
        total, phantom, valid, n_pubs, regsize, rate = ssp
        lines.append('## SSP audit')
        lines.append('')
        lines.append(f'**`{target}`** receives **{total:,} DIRECT** authorization '
                     f'claims across **{n_pubs:,} publishers**. Its own `sellers.json` '
                     f'registry contains **{regsize:,}** seller records.')
        lines.append('')
        lines.append(f'**{phantom:,} ({rate}%) of claims** reference seller_ids absent '
                     f'from {target}\'s registry.')
        lines.append('')
        # Top phantom seller_ids
        lines.append('### Top phantom seller_ids (by publisher reach)')
        lines.append('')
        lines.append('| seller_id | publishers citing | phantom % |')
        lines.append('|---|---:|---:|')
        for sid, n_p, n_ph, r in con.execute(
            'SELECT seller_id, n_publishers, n_phantom, phantom_rate '
            'FROM pair_prevalence WHERE ssp = :s AND n_phantom > 0 '
            'ORDER BY n_phantom DESC LIMIT 10', {'s': target}):
            lines.append(f'| `{sid}` | {n_p:,} | {r:.1f}% |')
        lines.append('')

    # Try as wrapper
    wrap = con.execute(
        'SELECT n_publishers, pooled_total_direct, pooled_phantom, '
        'pooled_false_rate_pct FROM wrapper_audit WHERE managerdomain = :m',
        {'m': target}).fetchone()
    if wrap:
        n_pubs, total, phantom, rate = wrap
        lines.append('## Wrapper audit')
        lines.append('')
        lines.append(f'**`{target}`** is declared as MANAGERDOMAIN by **{n_pubs:,} '
                     f'publishers**. Pooled across all DIRECT claims of those '
                     f'publishers: {phantom:,} of {total:,} ({rate}%) are false.')
        lines.append('')
        lines.append('### Sample of managed publishers')
        lines.append('')
        sample = list(con.execute(
            'SELECT pm.domain, pa.total_direct, pa.false_rate_pct '
            'FROM publisher_managerdomain pm '
            'JOIN publisher_audit pa ON pa.domain = pm.domain '
            'WHERE pm.managerdomain = :m '
            'ORDER BY pa.false_rate_pct DESC LIMIT 10',
            {'m': target}))
        for d, td, r in sample:
            lines.append(f'- `{d}` ({td:,} claims, {r}% false)')
        lines.append('')

    if not (pub or ssp or wrap):
        lines.append(f'No record found for `{target}` (neither publisher, SSP, nor wrapper).')
        return 2

    # Provenance footer
    lines.append('---')
    lines.append('## Provenance')
    lines.append('')
    for k, v in con.execute(
        'SELECT key, value FROM manifest WHERE key IN '
        '("snapshot_iso","corpus_publishers","corpus_ssps","corpus_pair_prevalence",'
        '"methodology","reproducer_repo","data_license") ORDER BY key'
    ):
        lines.append(f'- **{k}**: {v}')
    lines.append('')
    lines.append('Reproducer: `python3 verify.py ' + target + '` (live ads.txt × sellers.json scan).')

    out = '\n'.join(lines)
    if out_path:
        out_path.write_text(out)
        print(f'wrote {out_path} ({len(out):,} chars)', file=sys.stderr)
    else:
        print(out)
    return 0


def cmd_aberrations(con, surface: str | None = None, limit: int = 20) -> int:
    """Cycle 2026-05-21 + 428: surface micro-aberrations detected via
    the amplification layer. Four surfaces:
      A1_pub_internal   — pair below publisher's other pairs (rank-pctile)
      A2_ssp_internal   — publisher below SSP-pub mean (rank-pctile)
      A3_xssp_coherence — publisher spans >=3 confidence tiers across SSPs
      A5_pair_template  — per-(ssp, seller_id) industrial-template ranking
                           (cycle 428; surfaces template authors directly)
    """
    try:
        sql = ('SELECT surface, rank, domain, ssp, seller_id, confidence, '
               'metric, context_mean, context_n FROM pair_aberrations_top')
        params: dict = {}
        if surface:
            sql += ' WHERE surface = :sf'
            params['sf'] = surface
        sql += f' ORDER BY surface, rank LIMIT {int(limit)}'
        rows = list(con.execute(sql, params))
    except sqlite3.OperationalError:
        print('No pair_aberrations_top in this build (amplification layer missing).')
        return 2
    if not rows:
        print(f'No aberrations on file' + (f' for surface={surface}' if surface else ''))
        return 2
    print(f'=== Pair aberrations (top {limit} {("for " + surface) if surface else "per surface"}) ===')
    print()
    cur = None
    for sf, rk, d, ssp, sid, conf, met, cm, cn in rows:
        if sf != cur:
            cur = sf
            description = {
                'A1_pub_internal':   '(pair in pub bottom 1%)',
                'A2_ssp_internal':   '(pub in SSP-pub bottom 1%)',
                'A3_xssp_coherence': '(pub spans >=3 tiers across SSPs)',
                'A5_pair_template':  '(per-pair template ranking — domain field = n_pubs carrying)',
            }.get(sf, '')
            print(f'  ── {sf} {description} ──')
        # A5's `domain` field holds n_pubs count instead of a publisher domain
        if sf == 'A5_pair_template':
            print(f'    #{rk:>3}  pubs={d:>5}  ssp={ssp:<25} sid={(sid or "")[:32]:<32} '
                  f'conf={conf:>5.3f}  logit={met:>6.2f}')
        else:
            print(f'    #{rk:>3} {d:<32} ssp={ssp:<22} sid={(sid or "")[:18]:<18} '
                  f'conf={conf:>5.3f}  metric={met:>6.2f}  ctx_mean={cm:>5.3f}  ctx_n={cn}')
    return 0


def cmd_templates(con, limit: int = 20) -> int:
    """Cycle 428: shortcut for --aberrations --surface A5_pair_template.
    Shows the industrial template authors directly."""
    return cmd_aberrations(con, surface='A5_pair_template', limit=limit)


def cmd_findings(con) -> int:
    """Cycle H: surface the curated headline findings."""
    print('=== Named findings (curated headline-grade examples) ===')
    print()
    cur = None
    for fid, hl, expl, verify, sev in con.execute(
        'SELECT finding_id, headline, explanation, verifiable_via, severity '
        'FROM named_findings ORDER BY severity, finding_id'
    ):
        if sev != cur:
            print(f'\n  ── {sev.upper()} ──')
            cur = sev
        print(f'\n  • {hl}')
        # Wrap explanation
        words = expl.split()
        line = '    '
        for w in words:
            if len(line) + len(w) > 78:
                print(line.rstrip())
                line = '    ' + w + ' '
            else:
                line += w + ' '
        if line.strip():
            print(line.rstrip())
        print(f'    Verify: {verify}')
    return 0


def cmd_provenance(con, path: Path) -> int:
    print('=== Provenance manifest ===')
    for k, v in con.execute('SELECT key, value FROM manifest ORDER BY key'):
        if v and len(v) > 76:
            v = v[:73] + '...'
        print(f'  {k:30s}: {v}')
    print()
    # The canonical published hash is in the .xz.sha256 sidecar (BSD
    # format: '<hash>  <filename>'). The .db's own disk hash CAN'T match
    # any stored value, because writing the snapshot_chain row mutates
    # the file after its hash was computed. We report both, and tell the
    # reviewer where the source of truth lives.
    xz = path.with_suffix('.db.xz')
    sidecar = path.with_suffix('.db.xz.sha256')
    if xz.exists():
        xz_h = hashlib.sha256(xz.read_bytes()).hexdigest()
        print(f'  receipts.db.xz (canonical artifact)')
        print(f'    bytes         : {xz.stat().st_size:,}')
        print(f'    sha256        : {xz_h}')
        if sidecar.exists():
            published = sidecar.read_text().split()[0]
            ok = '✓ matches sidecar' if xz_h == published else \
                 '✗ DRIFT — sidecar says ' + published
            print(f'    vs sidecar    : {ok}')
            print(f'    sidecar file  : {sidecar.name}')
        else:
            print(f'    (no sidecar present — run shasum -a 256 receipts.db.xz '
                  f'to compute and publish)')
    if path.exists():
        h = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f'  receipts.db (transient — re-extracted from .xz)')
        print(f'    bytes         : {path.stat().st_size:,}')
        print(f'    as-built sha256 from snapshot_chain (informational only):')
        chain_row = con.execute(
            'SELECT self_sha256 FROM snapshot_chain '
            'ORDER BY snapshot_ts DESC LIMIT 1').fetchone()
        if chain_row:
            print(f'      {chain_row[0]}')
        print(f'    disk sha256   : {h}')
        print(f'    (disk hash WILL differ from as-built — writing the chain '
              f'row mutates the file)')
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        prog='verify_claim',
        description='Offline verifier for adtech-audit claims. '
                    'Reads receipts.db; no internet required.',
    )
    p.add_argument('--receipts', type=Path, default=DEFAULT_RECEIPTS)
    p.add_argument('--ssp')
    p.add_argument('--signature')
    p.add_argument('--premium', action='store_true')
    p.add_argument('--edgar', action='store_true')
    p.add_argument('--findings', action='store_true',
                   help='Show curated headline findings (default if no other flag)')
    p.add_argument('--report', metavar='TARGET',
                   help='Generate Markdown report on TARGET (publisher, SSP, or wrapper)')
    p.add_argument('--out', type=Path, default=None,
                   help='Write report to file instead of stdout')
    p.add_argument('--provenance', action='store_true')
    p.add_argument('--aberrations', action='store_true',
                   help='Surface top micro-aberrations from amplification layer')
    p.add_argument('--surface',
                   choices=('A1_pub_internal', 'A2_ssp_internal',
                             'A3_xssp_coherence', 'A5_pair_template'),
                   help='Filter --aberrations by surface')
    p.add_argument('--templates', action='store_true',
                   help='Shortcut: show industrial template authors (A5 surface)')
    p.add_argument('--limit', type=int, default=20,
                   help='Row limit for --aberrations / --templates (default 20)')
    p.add_argument('--live', action='store_true',
                   help='Also fetch live ads.txt + sellers.json and produce a '
                        'fresh verdict alongside the receipts.db snapshot. '
                        'Bridges frozen receipt → current world.')
    p.add_argument('domain', nargs='?')
    args = p.parse_args()

    con = open_receipts(args.receipts)
    if args.report:      return cmd_report(con, args.report, args.out)
    if args.ssp:         return cmd_ssp(con, args.ssp)
    if args.signature:   return cmd_signature(con, args.signature)
    if args.premium:     return cmd_premium(con)
    if args.edgar:       return cmd_edgar(con)
    if args.templates:   return cmd_templates(con, args.limit)
    if args.aberrations: return cmd_aberrations(con, args.surface, args.limit)
    if args.findings:    return cmd_findings(con)
    if args.provenance:  return cmd_provenance(con, args.receipts)
    if args.live and args.domain:
        # --live + domain: skip the frozen path, do only live verification
        # (or pass live_too=True for both)
        return cmd_domain(con, args.domain, live_too=True)
    if args.live:
        print('FAIL: --live requires a domain', file=sys.stderr); return 2
    if args.domain:      return cmd_domain(con, args.domain)
    # Default action: show findings to make first impression high-value
    return cmd_findings(con)


if __name__ == '__main__':
    sys.exit(main())
