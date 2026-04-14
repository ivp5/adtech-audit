#!/usr/bin/env python3
# ads.txt × sellers.json verifier · CC0 · stdlib · py3.9+
# Usage: python3 verify.py example.com   (domain only, https:// and /ads.txt appended)
#   good:  appnexus.com, 7529, DIRECT       → PLAUSIBLE
#   bad:   smartadserver.com, 4073, DIRECT  → PHANTOM (CAS SDK template line)
import csv, json, sys
from functools import cache
from urllib.request import urlopen
from collections import Counter


def fetch(url):
    return urlopen(url, timeout=20).read().decode()


@cache
def load_registry(ssp):
    try:
        sellers = json.loads(fetch(f'https://{ssp}/sellers.json')).get('sellers') or []
    except Exception:
        return None
    publishers, intermediaries = set(), set()
    for seller in sellers:
        seller_id = str(seller.get('seller_id', '')).lower()
        (intermediaries if (seller.get('seller_type') or '').upper() == 'INTERMEDIARY' else publishers).add(seller_id)
    return publishers, intermediaries


tally = Counter()
for fields in csv.reader(line.split('#', 1)[0] for line in fetch(f'https://{sys.argv[1]}/ads.txt').lstrip('\ufeff').splitlines()):
    if len(fields) < 3 or fields[2].strip().upper() != 'DIRECT':
        continue
    ssp, seller_id = fields[0].strip().lower(), fields[1].strip().lower()
    registry = load_registry(ssp)
    verdict = ('UNCOVERED' if registry is None
               else 'PLAUSIBLE' if seller_id in registry[0]
               else 'CONTRADICTED' if seller_id in registry[1]
               else 'PHANTOM')
    tally[verdict] += 1
    print(f'{verdict:12} {ssp}, {seller_id}')

for verdict, count in sorted(tally.items()):
    print(f'{verdict}: {count}')
