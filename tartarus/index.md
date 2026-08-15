# Tartarus - codebase diagnostic

> ZeroHype Lab / tools / tartarus
> Built on top of GRAFT, the open-source MIT-licensed context graph engine.

Tartarus is a heuristic scan that estimates how ready a codebase is for AI agents. It produces a **Context Readiness Score** from 0 to 100 across code structure, dependency clarity, documentation coverage, and AI-readiness. It is **not** a senior review. It is a starting point.

Your repo URL is scanned once and never stored. No backend. No server-side processing.

- **URL:** https://zerohypelab.com/tartarus/
- **Author:** ZeroHype Lab (anonymous software diagnostics brand)
- **Contact:** zerohype@proton.me
- **Underlying engine:** GRAFT (open-source, MIT-licensed context graph engine, originally developed at Nanonets)

---

## What the tool does

Inputs:

1. GitHub repo URL (validated against github.com)
2. Primary tech stack (JavaScript/TypeScript, Python, Go, Rust, Java/Kotlin, Ruby, PHP, or multi-language)
3. Email (results only, optional persistence)
4. Required terms checkbox acknowledging the scan is heuristic, not a full audit

After submission, Tartarus runs a short sequence:

- Parsing ASTs...
- Building dependency graph...
- Analyzing hotspots...
- Generating report...

and produces a **Context Readiness Score** from 0 to 100 with four subscores:

| Dimension | Weight |
|---|---|
| Code Structure | 28% |
| Dependency Clarity | 27% |
| Documentation Coverage | 22% |
| AI-Readiness | 23% |

The output shows the overall score, the four subscores, and the top three issues detected with severity badges (high / medium / low).

Important honesty note: this is a heuristic estimate generated from the URL and metadata you provide. Tartarus does not clone your repo or run static analysis on its contents. It is a triage, not a diagnosis.

---

## Full report (paid)

The free scan estimates. The full report delivers a written, structure-by-structure analysis with actionable recommendations.

- **Price:** $49 one-time
- Includes: annotated code structure map, dependency graph with problem nodes, documentation gap analysis with priorities, AI-agent readiness checklist, written recommendations.
- **Stripe:** https://buy.stripe.com/eVq6oJgE88nC2IJg5UaR20b

## Custom integration

- **Price:** from $2,500
- Includes: tailored diagnostic for your specific stack, custom AI-readiness criteria, CI/CD integration, ongoing monitoring setup, dedicated report with your team.
- **Contact:** mailto:zerohype@proton.me

---

## What this is not

- **Not a real audit.** It is a heuristic scan based on your repo URL and metadata. No repo cloning, no full file parsing, no static analysis.
- **Not stored.** Your repo URL is scanned once. Not stored, cached, or shared.
- **Not affiliated with your code.** Output is an estimate generated from the inputs you provide.
- **Built on GRAFT.** Tartarus is built on top of GRAFT, the open-source MIT-licensed context graph engine from Nanonets.

---

## FAQ

**How is the score computed?**
The score combines four dimensions: Code Structure (module organization, file size distribution), Dependency Clarity (explicit vs implicit dependencies), Documentation Coverage (README, inline docs, API docs), and AI-Readiness (context boundaries, prompt-friendly structure). Each is weighted heuristically. The exact formula changes as we learn from real repos.

**Is my repo stored?**
No. Your repo URL is submitted once for the scan. We do not store, cache, or log it. The scan runs client-side with no backend persistence. Your email is used only to optionally receive your results.

**Who built this?**
Tartarus was built by ZeroHype Lab on top of GRAFT, the open-source MIT-licensed context graph engine originally developed at Nanonets. ZeroHype Lab is an anonymous diagnostics brand. No named founders. The work speaks.

---

*Tartarus is a tool by ZeroHype Lab. (c) 2026. Contact: zerohype@proton.me.*
