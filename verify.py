#!/usr/bin/env python3
# ads.txt × sellers.json verifier · CC0 · stdlib · py3.9+
# Usage: python3 verify.py example.com   (domain only, https:// and /ads.txt appended)
#   good:  appnexus.com, 7529, DIRECT       → PLAUSIBLE
#   bad:   smartadserver.com, 4073, DIRECT  → PHANTOM (CAS SDK template line)
#
# This file is ALSO the canonical SSP_URL_OVERRIDES + load_registry source
# inside verify_kit.zip. release/verify_claim.py imports from this module
# (rather than carrying its own copy) so the kit ships one source of truth
# instead of two. cycle 440.
import csv, json, sys
from functools import cache
from urllib.request import Request, urlopen
from collections import Counter


# Cycle 434/440: SSPs that publish sellers.json at a non-canonical URL.
# Without these, verify.py silently mis-verdicts google/sovrn/etc. claims
# as UNCOVERED (registry fetch 404s → registry is None → UNCOVERED).
# Mirrored in scripts/ssp_fetch.py — cross-checked by tests/test_overrides_sync.py.
SSP_URL_OVERRIDES = {
    'google.com':       'https://realtimebidding.google.com/sellers.json',
    'doubleclick.net':  'https://realtimebidding.google.com/sellers.json',
    'sovrn.com':        'https://lijit.com/sellers.json',
    'genieesspv.jp':    'https://r.genieesspv.jp/sellers.json',
}


def fetch(url):
    # Some publishers/SSPs 403 the default Python User-Agent. Set one explicitly.
    # 'replace' on decode tolerates malformed bytes seen in the wild.
    return urlopen(Request(url, headers={'User-Agent': 'verifier/1'}), timeout=20).read().decode('utf-8', 'replace')


@cache
def load_registry(ssp):
    url = SSP_URL_OVERRIDES.get(ssp, f'https://{ssp}/sellers.json')
    try:
        sellers = json.loads(fetch(url)).get('sellers') or []
    except Exception:
        return None
    publishers, intermediaries = set(), set()
    for seller in sellers:
        seller_id = str(seller.get('seller_id', '')).lower()
        (intermediaries if (seller.get('seller_type') or '').upper() == 'INTERMEDIARY' else publishers).add(seller_id)
    return publishers, intermediaries


def classify(ssp: str, seller_id: str) -> str:
    """Live-fetch the SSP's sellers.json and classify (ssp, seller_id).
    Returns one of: PLAUSIBLE, CONTRADICTED, PHANTOM, UNCOVERED.
    Imported by release/verify_claim.py — single source of truth."""
    registry = load_registry(ssp)
    if registry is None:
        return 'UNCOVERED'
    if seller_id in registry[0]:
        return 'PLAUSIBLE'
    if seller_id in registry[1]:
        return 'CONTRADICTED'
    return 'PHANTOM'


def verify_publisher(domain: str) -> Counter:
    """Live-verify one publisher's ads.txt. Returns Counter of verdicts.
    Imported by release/verify_claim.py — single source of truth."""
    tally = Counter()
    body = fetch(f'https://{domain}/ads.txt').lstrip('﻿')
    for fields in csv.reader(line.split('#', 1)[0] for line in body.splitlines()):
        if len(fields) < 3 or fields[2].strip().upper() != 'DIRECT':
            continue
        ssp = fields[0].strip().lower()
        seller_id = fields[1].strip().lower()
        verdict = classify(ssp, seller_id)
        tally[verdict] += 1
    return tally


if __name__ == '__main__':
    tally = verify_publisher(sys.argv[1])
    for verdict, count in sorted(tally.items()):
        print(f'{verdict}: {count}')
