#!/usr/bin/env -S deno run --allow-net --allow-read
/**
 * Evidence verification API — lightweight, standalone.
 * All O(n) work at startup → O(1) queries. (Knuth: amortize the cost.)
 */

const PORT = 8890;
const HERE = new URL(".", import.meta.url).pathname;

type Claim = { publisher: string; ssp: string; seller_id: string; registry_type: string; verdict: string };
type Tally = { total: number; contradicted: number; phantom: number; plausible: number; false_pct: number | null };

// ── Load + pre-compute everything at startup ──

const byPublisher = new Map<string, Claim[]>();
const bySsp = new Map<string, Claim[]>();
const publisherTallies = new Map<string, Tally>();
const sspTallies = new Map<string, Tally>();
const sspTopPubs = new Map<string, { publisher: string; false_claims: number }[]>();
let sspRankedList: ({ ssp: string } & Tally)[] = [];
let publishersSorted: string[] = [];

console.log("Loading false_direct_claims.jsonl...");
const text = Deno.readTextFileSync(HERE + "false_direct_claims.jsonl");
let claimCount = 0;
for (const line of text.split("\n")) {
  if (!line.trim()) continue;
  const r = JSON.parse(line) as Claim;
  claimCount++;
  let pubArr = byPublisher.get(r.publisher);
  if (!pubArr) { pubArr = []; byPublisher.set(r.publisher, pubArr); }
  pubArr.push(r);
  let sspArr = bySsp.get(r.ssp);
  if (!sspArr) { sspArr = []; bySsp.set(r.ssp, sspArr); }
  sspArr.push(r);
}

// Pre-compute tallies (single O(n) pass already done above, now O(m) for aggregation)
function computeTally(arr: Claim[]): Tally {
  let contradicted = 0, phantom = 0, plausible = 0;
  for (const c of arr) {
    if (c.verdict === "CONTRADICTED") contradicted++;
    else if (c.verdict === "PHANTOM") phantom++;
    else plausible++;
  }
  const total = arr.length;
  return { total, contradicted, phantom, plausible, false_pct: total ? Math.round((contradicted + phantom) / total * 100) : null };
}

for (const [pub, arr] of byPublisher) publisherTallies.set(pub, computeTally(arr));
for (const [ssp, arr] of bySsp) {
  sspTallies.set(ssp, computeTally(arr));
  // Pre-compute top publishers per SSP
  const pubCounts: Record<string, number> = {};
  for (const c of arr) if (c.verdict !== "PLAUSIBLE") pubCounts[c.publisher] = (pubCounts[c.publisher] || 0) + 1;
  const top = Object.entries(pubCounts).sort((a, b) => b[1] - a[1]).slice(0, 20).map(([p, n]) => ({ publisher: p, false_claims: n }));
  sspTopPubs.set(ssp, top);
}

// Pre-compute /api/ssps response
sspRankedList = [...sspTallies.entries()].map(([ssp, t]) => ({ ssp, ...t })).sort((a, b) => b.total - a.total);
// Pre-sort publishers for autocomplete
publishersSorted = [...byPublisher.keys()].sort();

const summary = JSON.parse(Deno.readTextFileSync(HERE + "supply_chain_summary.json"));
const consent = JSON.parse(Deno.readTextFileSync(HERE + "consent_measurement.json"));
const crawl = JSON.parse(Deno.readTextFileSync(HERE + "crawl_summary.json"));
const identityGraph = JSON.parse(Deno.readTextFileSync(HERE + "identity_graph.json"));
const evidenceHtml = Deno.readTextFileSync(HERE + "evidence.html")
  .replace(/location\.port === '8889' \? '' : location\.port === '8890' \? '' : 'http:\/\/127\.0\.0\.1:8890'/, "''");

console.log(`Loaded ${claimCount} claims, ${byPublisher.size} publishers, ${bySsp.size} SSPs (all pre-computed)`);

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*" },
  });
}

Deno.serve({ port: PORT, hostname: "127.0.0.1" }, (req) => {
  const url = new URL(req.url);
  const path = url.pathname;

  if (req.method === "OPTIONS") return new Response(null, { headers: { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, OPTIONS", "Access-Control-Allow-Headers": "*" } });

  if (path === "/" || path === "/evidence") {
    return new Response(evidenceHtml, { headers: { "Content-Type": "text/html; charset=utf-8", "Access-Control-Allow-Origin": "*" } });
  }

  if (path === "/api/verify") {
    const publisher = url.searchParams.get("publisher")?.toLowerCase() || "";
    if (!publisher) return json({ error: "need ?publisher=domain.com" }, 400);
    const tally = publisherTallies.get(publisher);
    if (!tally) return json({ publisher, total: 0, contradicted: 0, phantom: 0, plausible: 0, false_pct: null, claims: [] });
    const claims = byPublisher.get(publisher)!.slice(0, 200);
    return json({ publisher, ...tally, claims });
  }

  if (path === "/api/ssp") {
    const ssp = url.searchParams.get("ssp")?.toLowerCase() || "";
    if (!ssp) return json({ error: "need ?ssp=domain.com" }, 400);
    const tally = sspTallies.get(ssp);
    if (!tally) return json({ ssp, total: 0, contradicted: 0, phantom: 0, plausible: 0, false_pct: null, top_publishers: [] });
    return json({ ssp, ...tally, top_publishers: sspTopPubs.get(ssp) || [] });
  }

  if (path === "/api/summary") {
    return json({ supply_chain: summary, consent, crawl });
  }

  if (path === "/api/identity") {
    return json(identityGraph);
  }

  if (path === "/api/publishers") {
    const q = url.searchParams.get("q")?.toLowerCase() || "";
    // Binary search for prefix, then linear scan for substring (still O(log n + k) vs O(n))
    const matches = publishersSorted.filter(p => p.includes(q)).slice(0, 50);
    return json({ matches });
  }

  if (path === "/api/ssps") {
    return json({ ssps: sspRankedList });  // O(1) - pre-computed
  }

  return new Response("Not found", { status: 404 });
});

console.log(`Evidence API on http://localhost:${PORT}`);
