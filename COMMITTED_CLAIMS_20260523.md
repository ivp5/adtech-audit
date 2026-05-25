# Committed claims — 2026-05-23

Each claim names: the operator, the specific identifier, the live source
that confirms or refutes, and the date of confirmation. Verifiable in
under 60 seconds with `curl`.

---

**1.** `appnexus.com, 1908, RESELLER` appears in 19,516 publisher ads.txt
files including `aarp.org`, `appleinsider.com`, `foxla.com`. AppNexus's
authoritative registry — fetched 2026-05-23 from
`https://www.appnexus.com/sellers.json`, 1,586 sellers, contact
`sellers-json@microsoft.com` — does not contain seller_id 1908. Verified
absent: 1908, 4071, 6849, 7158, 9057, 4012, 2928, 7664.

```
curl -sL https://www.appnexus.com/sellers.json | jq '.sellers[] | select(.seller_id=="1908")'
# → no output
```

**2.** `lijit.com, 246013-eb, DIRECT` appears in 1,859 publisher ads.txt
files. Sovrn's registry — fetched 2026-05-23 from
`https://lijit.com/sellers.json`, 7,284 sellers, contact
`support@sovrn.com` — does not contain seller_id `246013-eb`. The base
`246013` is present as `THE MONEYTIZER` INTERMEDIARY at `us.themoneytizer.com`.
The same absence holds across 18 Wayback snapshots from 2019-09-30 to
2022-07-13. Themoneytizer's own ads.txt at `themoneytizer.com/ads.txt`
contained `lijit.com, 246013, RESELLER` on 2019-07-21 (Wayback) and
contained both `lijit.com, 246013, DIRECT` and `lijit.com, 246013-eb,
DIRECT` by 2021-10-20 (Wayback).

**3.** 82 distinct `<base>-eb` seller_ids appear in publisher ads.txt as
DIRECT claims at `lijit.com`. All 82 base IDs present in Sovrn's live
registry as INTERMEDIARY (100%). All 82 suffixed forms absent. Named
owners include THE MONEYTIZER (246013), Adpone SL (257429), Domain
Development Corp (240817), Sortable, walletcircle.co, luponmedia.

**4.** Criteo's live sellers.json at `https://www.criteo.com/sellers.json`
and TheMediaGrid's at `https://themediagrid.com/sellers.json` both return
the same 1,725-seller registry with contact `commerce-grid@criteo.com`
(2026-05-23). Publisher ads.txt files contain 60,450 B-prefix-format
criteo.com seller_ids (`B-060278`, etc.) and 11,831 numeric criteo.com
seller_ids (`7822`, `155036`, etc.). Zero of these match the current
1,725-seller alphanum-6-char registry. 100% of 76,038 publisher
criteo.com DIRECT claims fail cross-validation against the post-
acquisition registry.

**5.** TheMediaGrid registry does not contain seller_id `Q19AKF`. The
seller_id `Q19AKF` appears in 813 of 907 publisher ads.txt files
managed by Ezoic via AdsTxtManager.com. Format mimics TheMediaGrid's
legitimate 6-character alphanumeric pattern (`2RT75Y`, `GODNC4`,
`DQ6AMB` all present in registry).

**6.** Google's live sellers.json at
`https://realtimebidding.google.com/sellers.json` (986,194 sellers,
contact `sellers_json@google.com`, fetched 2026-05-23) does not contain
`pub-8622186303703569`. That pub-ID appears in 4,033 publisher ads.txt
files as `google.com, pub-8622186303703569, DIRECT, f08c47fec0942fa0`.
704,235 of 986,194 (71.41%) entries in Google's registry have
`is_confidential: true` with name and domain redacted.

**7.** The literal placeholder `pub-1234567890123456` (sequential digits)
appears in 4 publisher ads.txt files (`blog.jp`, `listindiario.com`,
`acheiusa.com`, `samcash21.com`) declared as `google.com,
pub-1234567890123456, DIRECT, f08c47fec0942fa0`. Independently, 4
different publishers (`korearace.com`, `portaldozacarias.com.br`,
`drawingtutorials101.com`, `oeffentlicher-dienst.info`) embed
`client=ca-pub-1234567890123456` in their HTML AdSense scripts. Google's
endpoint accepts the placeholder request without rejection: HTTP 200 on
both `pagead2.googlesyndication.com/pagead/js/adsbygoogle.js` and
`googleads.g.doubleclick.net/pagead/ads`. The response body for
`/pagead/ads` in both direct-curl and full browser-context Playwright
tests on korearace.com (2026-05-23) is the 603-byte no-fill stub
`<html><body style="background-color:transparent"></body></html>`. The
same 603-byte response is returned for a registered publisher's pub-ID
under identical unauthenticated context. Google's URL-parameter layer
does not validate the pub-ID; the no-fill stub on the placeholder
indicates the auction layer (downstream of URL acceptance) does not
match any real AdSense account for serving. The fault is accepted but
not monetized — at least under unauthenticated direct fetch.

**8.** IAB ads.txt v1.1 specification §5.2.1 states that SSPs/exchanges
"should also consider crawling publishers' domains and notifying
publishers...of the absence of an ads.txt file or the absence of
appropriate declarations in the file." DoubleVerify, Integral Ad
Science, and Pixalate public product pages (fetched 2026-05-23 from
`doubleverify.com/products/`, `integralads.com/products/`,
`pixalate.com/products`) contain 17 + 20 + 17 substring hits for "spo"
respectively and zero substring hits for "sellers.json", "ads.txt", or
"authorized seller" across all three.

**9.** Publisher ads.txt files contain 2,223,658 phantom DIRECT claims
(seller_id absent from declared SSP's registry). Decomposition by
mechanism: 1,522,659 (68.5%) carry template-injection signature
(seller_id-SSP pair shared across ≥50 publishers); 467,795 (21.0%)
long-tail; 146,984 (6.6%) defunct/acquired SSPs; 76,037 (3.4%) Criteo
schema migration; 15,422 (0.7%) Yandex non-IAB framework.

**10.** Playwright capture of OpenRTB POST bodies on `worldcrunch.com`
(2026-05-23) shows the in-band supply chain object
`source.ext.schain.nodes[0] = {asi: "themoneytizer.com", sid: "122815",
hp: 1, complete: 1}`. Themoneytizer's live sellers.json
(`https://www.themoneytizer.com/sellers.json`, 4,322 sellers, fetched
2026-05-23) contains `{"seller_id": "122815", "name": "wORLDCRUNCH",
"domain": "worldcrunch.com", "seller_type": "PUBLISHER"}`. The schain
validates. The same publisher's ads.txt contains `lijit.com, 246013-eb,
DIRECT` which does not. ads.txt cross-validation and OpenRTB schain
validation check different identifier namespaces.

---

Each numeric claim above is reproducible from the public registries with
two `curl` calls and a `jq` filter. The corpus claims (count of
publishers carrying line X) are reproducible against
`release/false_direct_claims.jsonl.gz`.
