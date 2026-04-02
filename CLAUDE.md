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
| `src/tables/` | HTML property tables included by `index.html` |
| `src/examples/` | Worked examples (Turtle, JSON-LD, XML) |
| `src/figures/` | UML diagrams |
| `src/enterpriseArchitectFiles/` | Enterprise Architect model (`.qea`) |
| `src/js/` | Custom JavaScript |
| `src/appendices/` | Appendix content (placeholder) |
| `src/scripts/` | Build tooling |
| `dist/` | Generated artefacts — do not edit by hand |

---

## The builder

**Run from repo root:**
```bash
bash src/scripts/run-all.sh
```

| Script | Purpose |
|--------|---------|
| `run-all.sh` | Top-level entry point — calls `build-all.sh` + `serialise-all.sh` |
| `build-class-tables.php` | Generates class/property HTML tables from ontology RDF |
| `build-summary-tables.php` | Generates summary tables |
| `build-example-index.php` | Indexes examples |
| `serialise-vocabulary.sh` | Converts ontology to Turtle/JSON-LD via `rdfpipe` |
| `serialise-examples.sh` | Serialises example files |

**Prerequisites:** PHP CLI, `rdfpipe` (`pip install rdflib`), `pyshacl` (optional, for validation).

---

## Key external links

- Published spec: https://w3id.org/mobilitydcat-ap/releases/
- Latest draft: https://w3id.org/mobilitydcat-ap/drafts/latest/
- Issues: https://github.com/mobilityDCAT-AP/mobilityDCAT-AP/issues
- Namespace: `http://w3id.org/mobilitydcat-ap#`
