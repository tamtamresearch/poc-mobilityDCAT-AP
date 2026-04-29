# mobilityDCAT-AP — Claude Code Context

## What this project is

**mobilityDCAT-AP** is a European standard: an RDF/OWL application profile of DCAT-AP for describing mobility datasets, dataset services, and services across National Access Points (NAPs) in Europe. Maintained by [NAPCORE](https://napcore.eu/).

This is a **proof-of-concept repository** for a proposed new repository structure. See `PLAN.md` for the branching strategy (`main` = draft, `release/vX.Y` branches, `draft/topic-name` for parallel work).

---

## Repository layout

All hand-authored source files live under `src/`. Generated artefacts go in `dist/` (do not edit by hand).

| Path | Purpose |
|------|---------|
| `src/mobilitydcat-ap.rdf` | Ontology — primary source of truth (RDF/XML) |
| `src/index.html` | ReSpec specification document (entry point) |
| `src/config.js` | ReSpec configuration (version, editors, dates, bibliography) |
| `src/shaclShapes/` | SHACL validation constraints |
| `src/tables/` | HTML property tables included by `index.html` via `data-include` |
| `src/examples/` | Worked examples (RDF/XML, Turtle, JSON-LD) |
| `src/figures/` | UML diagrams |
| `src/enterpriseArchitectFiles/` | Enterprise Architect model (`.qea`) |
| `src/js/` | Custom JavaScript |
| `src/appendices/` | Appendix content (placeholder) |
| `src/scripts/` | Build scripts (Python) |
| `dist/` | Generated artefacts — do not edit by hand |

---

## The builder

**Run from repo root:**
```sh
mise run build
```

| Script | Purpose |
|--------|---------|
| `src/scripts/clean.py` | Empties `dist/` before a fresh build |
| `src/scripts/serialise.py` | Converts `src/*.rdf` and `src/examples/*.rdf` to Turtle and JSON-LD using rdflib |
| `src/scripts/copy-assets.py` | Copies ontology files, examples, figures, and SHACL shapes to `dist/` |
| `src/scripts/build-spec.py` | Starts a local HTTP server and builds `dist/index.html` via `respec` |

**Why a local HTTP server?** ReSpec uses a headless Chromium browser internally. Chromium blocks `file://` fetches needed by `data-include`, so the build script serves the repo over HTTP on a random local port.

**Prerequisites:** [mise](https://mise.jdx.dev/) — see `DEVELOPMENT.md` for full setup instructions.

**Tool versions:**
- Node.js 24, respec 36.0.0 — managed via mise + `package.json`
- Python 3.12, rdflib 7.6.0, pyshacl 0.31.0 — managed via mise + uv + `pyproject.toml`

---

## Key external links

- Published spec: https://w3id.org/mobilitydcat-ap/releases/
- Latest draft: https://w3id.org/mobilitydcat-ap/drafts/latest/
- Issues: https://github.com/mobilityDCAT-AP/mobilityDCAT-AP/issues
- Namespace: `http://w3id.org/mobilitydcat-ap#`
