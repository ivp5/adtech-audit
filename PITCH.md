# Evidence Pitch — Ad Supply Chain Fraud

## One-liner

68% of supply chain authorization claims in digital advertising are false. We have 915K cross-verified records proving it.

## The hook (for Google antitrust angle)

Magnite and PubMatic just filed antitrust lawsuits against Google. Our data shows:
- **Magnite**: 65.5% of their "DIRECT" claims are provably false
- **PubMatic**: 54.4% provably false
- **Google**: 0% provably false (but 71% hidden behind confidentiality)

The plaintiffs have worse disclosure records than the defendant.

## The broader story

The ads.txt/sellers.json system was created to prevent ad fraud. Nine years later:
- **68% of DIRECT claims are false** (34% contradicted, 34% phantom)
- **0.012% of identity-sharing carries valid consent**
- **~4% of ad-tech activity is properly authorized**

This isn't broken. It's working as designed — a system that provides the appearance of authorization while enabling opacity.

## What we have

- **915,460 cross-verified claims** across 11,990 publishers and 87 SSPs
- **Per-company fraud rates** for every major SSP
- **Interactive verification tool** (type any publisher, see their false claims)
- **Methodology documented** with reproducible commands
- **Self-audit with corrections** (we caught and fixed our own errors)

## The angles

| Outlet | Angle |
|--------|-------|
| **AdExchanger** | Industry insider: "Your SSP is lying to you" |
| **The Markup** | Data journalism: "We verified 915K claims" |
| **Platformer** | Policy: "Why Google's opacity might be legal" |
| **Ars Technica** | Technical: "How template injection works" |
| **Reuters/WSJ** | Antitrust: "Plaintiffs' own records" |

## Contact

Evidence package: https://github.com/ivp5/adtech-audit
Interactive tool: evidence.html (runs locally, no server needed)
Raw data: 915K JSONL records with verdicts

## Pre-verified examples (no server needed)

| Publisher | Total Claims | Contradicted | Phantom | Plausible | False Rate |
|-----------|--------------|--------------|---------|-----------|------------|
| cnn.com | 167 | 50 | 18 | 99 | 40.7% |
| reuters.com | 104 | 46 | 21 | 37 | 64.4% |
| bbc.com | 26 | 5 | 0 | 21 | 19.2% |

Manual verification (no code):
```bash
# Download and grep — works on any machine
curl -sL https://github.com/ivp5/adtech-audit/raw/main/false_direct_claims.jsonl.gz | gunzip | grep '"cnn.com"' | head -5
```

## Ready to send

```
Subject: Data on Google antitrust — the plaintiffs are worse

The companies suing Google for ad-tech monopoly have demonstrably
worse supply chain disclosure than Google itself.

Our analysis: 915,460 cross-verified claims.
- Magnite: 65.5% false
- PubMatic: 54.4% false
- Google: 0% false (but 71% hidden)

We have the data, methodology, and interactive audit tool.
Interested in an exclusive before this goes wider?
```
