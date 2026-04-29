# Development guide

## Prerequisites

- [mise](https://mise.jdx.dev/) — manages Node.js and uv versions locally

All build scripts are written in Python and work identically on Windows and Linux. No bash required on either platform.

### Installing mise

**Linux / macOS**
```sh
curl https://mise.run | sh
```

**Windows** (PowerShell or cmd)
```powershell
winget install jdx.mise
# or
scoop install mise
```

## First-time setup

```sh
mise install          # installs Node 24 and uv (uv installs Python 3.12 automatically)
mise run install      # npm install + uv sync (creates .venv with all Python dependencies)
```

## Build

```sh
mise run build        # full build: serialise RDF + build ReSpec spec
```

All output is written to **`dist/`**. Open `dist/index.html` in a browser to preview the built specification.

Individual steps:

```sh
mise run serialise    # convert src/*.rdf and src/examples/*.rdf -> dist/*.ttl + dist/*.jsonld
mise run build-spec   # copy assets to dist/ and build dist/index.html via ReSpec
```

## How it works

| Step | Script | What it does |
|------|--------|-------------|
| Serialise | `src/scripts/serialise.py` | Parses each `.rdf` with rdflib, writes sibling `.ttl` and `.jsonld` |
| Copy assets | `src/scripts/copy-assets.py` | Copies ontology files, examples, figures, and SHACL shapes to `dist/` |
| Build spec | `src/scripts/build-spec.py` | Starts a local HTTP server, runs `respec` against it, writes `dist/index.html` |

A local HTTP server is used for the ReSpec build because Chromium (used internally by ReSpec) blocks `file://` requests required by `data-include`.

## Source layout

All hand-authored files live under `src/`. Never edit files in `dist/` — they are generated.

| Path | Purpose |
|------|---------|
| `src/mobilitydcat-ap.rdf` | Ontology — primary source of truth (RDF/XML) |
| `src/index.html` | ReSpec specification document |
| `src/config.js` | ReSpec configuration (version, editors, dates, bibliography) |
| `src/tables/` | HTML property tables included by `index.html` via `data-include` |
| `src/examples/` | Worked examples (RDF/XML, Turtle, JSON-LD) |
| `src/shaclShapes/` | SHACL validation constraints |
| `src/figures/` | UML diagrams |
| `src/enterpriseArchitectFiles/` | Enterprise Architect model (`.qea`) |
| `src/js/` | Custom JavaScript |
| `src/appendices/` | Appendix content (placeholder) |
| `src/scripts/` | Build scripts (Python) |

## Dependencies

| Tool | Version | Managed by | Purpose |
|------|---------|-----------|---------|
| Node.js | 24 | mise | Runtime for ReSpec |
| respec | 36.0.0 | npm / `package.json` | Builds the HTML specification |
| uv | latest | mise | Python package manager |
| Python | 3.12 | uv | Runtime for build scripts |
| rdflib | 7.6.0 | uv / `pyproject.toml` | RDF serialisation |
| pyshacl | 0.31.0 | uv / `pyproject.toml` | SHACL validation (optional) |

- `.mise.toml` — pins Node and uv versions
- `package.json` — pins respec
- `pyproject.toml` — declares Python dependencies
- `uv.lock` — exact locked versions; commit this file for reproducible installs

## CI

The GitHub Actions workflow (`.github/workflows/build-main.yml`) mirrors the local build and publishes to `gh-pages` under `drafts/latest/` on every push to `main`.
