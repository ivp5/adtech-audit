# DOJ Antitrust Evidence — Google Ad-Tech Dominance (SUPERSEDED 2026-05-22)

> **⚠ THIS DOCUMENT IS SUPERSEDED for the ads.txt-framework portion.** The Google-dominance measurements (10:1 Google:Meta presence ratio, 41,742 syncs across 9,699 sites, etc.) remain numerically valid. However, the framing that linked Google's dominance to the "false DIRECT" rate as fraud evidence is mis-targeted: cycle 468 structural decomposition shows 97.5% of phantom volume is framework brittleness, and Google's 178,871 phantom claims are dominantly attributable to the IAB-spec-legal `is_confidential: true` flag (8.1% of total phantom). The DOJ antitrust angle now properly applies only to (1) observed identity-graph dominance, (2) the 24% of companies operating outside any authorization framework, (3) Google's confidentiality-flag usage at 71% vs other SSPs at 0% — but NOT to the headline phantom-rate framing. See `ERRATA.md` entries E-2026-05-22-a through E-2026-05-22-m.

> **Snapshot pin.** Numbers below are at the **2026-03-25 crawl** (332,356 page scans). Live crawler state has continued to grow; ratios (10:1 Google:Meta) are stable; raw counts will exceed those quoted here.

## Market Position (from 332,356 page scans)

| Company | Page Appearances | Share |
|---------|-----------------|-------|
| Google (combined) | 511,994 | **91%** |
| Meta | 51,481 | 9% |
| Microsoft Ads | 19,518 | 3% |

**10:1 dominance ratio** over nearest competitor.

## Bundling / Tying Evidence

Sites running multiple Google services together:

| Bundle | Sites | % of Scans |
|--------|-------|------------|
| GTM + Analytics | 93,162 | 28% |
| GTM + GAM (ad server) | 58,520 | 17.6% |
| GAM + Google Ads | 54,470 | 16.4% |
| **Full stack** (GTM + GAM + Analytics + Ads) | 28,543 | 8.6% |

When publishers adopt one Google tool, they tend to adopt others. 28,543 sites run the complete Google advertising stack.

## Control Points

| Layer | Google Product | Reach |
|-------|---------------|-------|
| Tag deployment | GTM | 167,952 appearances |
| Measurement | Analytics | 97,080 appearances |
| Ad serving | GAM | 63,455 appearances |
| Demand | Google Ads | 92,336 appearances |
| Exchange | AdSense/AdX | 39,346+ appearances |

Google controls measurement, deployment, serving, and demand — vertically integrated across the entire transaction.

## Relevance to DOJ v. Google

The DOJ's ad-tech antitrust case alleges Google leveraged its position across the ad-tech stack. This data provides:

1. **Quantified dominance**: 10:1 over Meta in page presence
2. **Bundling pattern**: 28K sites with full Google stack
3. **Vertical integration**: Control at every layer of the transaction

## Data Source

- 332,356 page scans via Playwright browser automation
- Entity detection via request URL pattern matching
- Period: March 2026
- Methodology: Same as supply chain analysis
