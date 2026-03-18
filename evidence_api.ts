#!/usr/bin/env -S deno run --allow-net --allow-read
/**
 * Evidence verification API — lightweight, standalone.
 * Loads 177,897 false_direct_claims into memory, serves queries.
 */

const PORT = 8890;
const HERE = new URL(".", import.meta.url).pathname;
const EXPORTS = HERE;

// ── Load all data into memory at startup ──

type Claim = { publisher: string; ssp: string; seller_id: string; registry_type: string; verdict: string };

const claims: Claim[] = [];
const byPublisher: Record<string, Claim[]> = {};
const bySsp: Record<string, Claim[]> = {};

console.log("Loading false_direct_claims.jsonl...");
const text = Deno.readTextFileSync(EXPORTS + "false_direct_claims.jsonl");
for (const line of text.split("\n")) {
  if (!line.trim()) continue;
  const r = JSON.parse(line) as Claim;
  claims.push(r);
  (byPublisher[r.publisher] ??= []).push(r);
  (bySsp[r.ssp] ??= []).push(r);
}
console.log(`Loaded ${claims.length} claims, ${Object.keys(byPublisher).length} publishers, ${Object.keys(bySsp).length} SSPs`);

const summary = JSON.parse(Deno.readTextFileSync(EXPORTS + "supply_chain_summary.json"));
const consent = JSON.parse(Deno.readTextFileSync(EXPORTS + "consent_measurement.json"));
const crawl = JSON.parse(Deno.readTextFileSync(EXPORTS + "crawl_summary.json"));
const identityGraph = JSON.parse(Deno.readTextFileSync(EXPORTS + "identity_graph.json"));
const evidenceHtml = Deno.readTextFileSync(HERE + "evidence.html")
  .replace(/location\.port === '8889' \? '' : location\.port === '8890' \? '' : 'http:\/\/127\.0\.0\.1:8890'/, "''");
console.log("All data loaded.");

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*" },
  });
}

function countVerdicts(arr: Claim[]) {
  let contradicted = 0, phantom = 0, plausible = 0;
  for (const c of arr) {
    if (c.verdict === "CONTRADICTED") contradicted++;
    else if (c.verdict === "PHANTOM") phantom++;
    else plausible++;
  }
  const total = arr.length;
  return { total, contradicted, phantom, plausible, false_pct: total ? Math.round((contradicted + phantom) / total * 100) : null };
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
    const matches = byPublisher[publisher] || [];
    const stats = countVerdicts(matches);
    return json({ publisher, ...stats, claims: matches.slice(0, 200) });
  }

  if (path === "/api/ssp") {
    const ssp = url.searchParams.get("ssp")?.toLowerCase() || "";
    if (!ssp) return json({ error: "need ?ssp=domain.com" }, 400);
    const matches = bySsp[ssp] || [];
    const stats = countVerdicts(matches);
    const pubCounts: Record<string, number> = {};
    for (const c of matches) if (c.verdict !== "PLAUSIBLE") pubCounts[c.publisher] = (pubCounts[c.publisher] || 0) + 1;
    const topPubs = Object.entries(pubCounts).sort((a, b) => b[1] - a[1]).slice(0, 20).map(([pub, n]) => ({ publisher: pub, false_claims: n }));
    return json({ ssp, ...stats, top_publishers: topPubs });
  }

  if (path === "/api/summary") {
    return json({ supply_chain: summary, consent, crawl });
  }

  if (path === "/api/identity") {
    return json(identityGraph);
  }

  if (path === "/api/publishers") {
    const q = url.searchParams.get("q")?.toLowerCase() || "";
    const matches = Object.keys(byPublisher).filter(p => p.includes(q)).sort().slice(0, 50);
    return json({ matches });
  }

  if (path === "/api/ssps") {
    const ranked = Object.entries(bySsp).map(([ssp, arr]) => {
      const s = countVerdicts(arr);
      return { ssp, ...s };
    }).sort((a, b) => b.total - a.total);
    return json({ ssps: ranked });
  }

  return new Response("Not found", { status: 404 });
});

console.log(`Evidence API on http://localhost:${PORT}`);
