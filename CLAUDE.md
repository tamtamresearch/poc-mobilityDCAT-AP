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
| `src/validationFiles/` | Granular SHACL shapes (one per class) |
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

## CI/CD workflows

All workflows live in `.github/workflows/` and publish to the `gh-pages` branch.

The build and deploy logic is split into two **reusable workflows** called by the three publishing workflows:

| File | Type | Purpose |
|------|------|---------|
| `reusable-build.yml` | reusable | Full build pipeline (serialise → copy-assets → build-spec → html-validate → check-refs); uploads `dist/` as artifact `spec-dist` |
| `reusable-publish-gh-pages.yml` | reusable | Downloads `dist/` artifact, pre-cleans the target directory on `gh-pages`, deploys via plain `git` |
| `build-main.yml` | caller | Triggered on push to `main` (path-filtered to `src/**`, `package.json`, `pyproject.toml`) or manually; publishes to `drafts/latest/` |
| `build-draft.yml` | caller | Triggered on push of a `draft/*` tag or manually; publishes to `drafts/<version>/` |
| `build-release.yml` | caller | Triggered on push to a `release/*` branch or manually; publishes to `releases/<version>/`; also publishes to `releases/latest/` if `LATEST_RELEASE` matches the branch version |
| `promote-latest.yml` | standalone | Manual only; updates `LATEST_RELEASE` on `main` + copies already-built `releases/<version>/` to `releases/latest/` on `gh-pages` directly |

**Version extraction** — `build-draft.yml` and `build-release.yml` strip the prefix from `GITHUB_REF_NAME` (`draft/` or `release/`) in a dedicated `extract-version` job. A fail-fast guard rejects the run early if the result does not look like a version number (e.g. when `workflow_dispatch` is triggered from a plain branch).

**Latest release marker** — `LATEST_RELEASE` in the repo root (on `main`) holds the version currently marked as latest. `build-release.yml` sparse-checks out this file from `main` and compares it to the current branch version; an `is_latest` output gates a second `publish-latest` job. `promote-latest.yml` does two things: updates `LATEST_RELEASE` on `main` (so future hotfixes to the promoted branch auto-update `releases/latest/`), then copies the already-built `releases/<version>/` to `releases/latest/` on `gh-pages` immediately. Release branches never carry this file.

**Artifact flow** — `reusable-build.yml` outputs `artifact_name` (default: `spec-dist`). Callers pass `needs.build.outputs.artifact_name` to `reusable-publish-gh-pages.yml`, so the artifact name is defined in one place.

---

## Key external links

- Published spec: https://w3id.org/mobilitydcat-ap/releases/
- Latest draft: https://w3id.org/mobilitydcat-ap/drafts/latest/
- Issues: https://github.com/mobilityDCAT-AP/mobilityDCAT-AP/issues
- Namespace: `http://w3id.org/mobilitydcat-ap#`
