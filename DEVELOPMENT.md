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
mise run clean        # empty dist/ (run automatically at the start of mise run build)
mise run serialise    # convert src/*.rdf and src/examples/*.rdf -> dist/*.ttl + dist/*.jsonld
mise run build-spec   # copy assets to dist/ and build dist/index.html via ReSpec
```

## Linting

```sh
mise run lint         # full build + prints every broken local reference
```

ReSpec only reports the count of broken references in its CLI output. `mise run lint` runs the full build and then parses `dist/index.html` with `src/scripts/check-refs.py`, which cross-references all `id` attributes against all `href="#..."` links and prints each broken one.

## Live preview

To use ReSpec's interactive warnings panel in the browser:

```sh
mise run serve        # starts HTTP server on http://localhost:8080
```

Open `http://localhost:8080/src/index.html` in a browser. ReSpec runs live and shows a warnings badge at the top — click it to see all issues with locations. Stop with `Ctrl+C`.

## How it works

| Step | Script | What it does |
|------|--------|-------------|
| Serialise | `src/scripts/serialise.py` | Parses each `.rdf` with rdflib, writes `.ttl` and `.jsonld` to `dist/` |
| Copy assets | `src/scripts/copy-assets.py` | Copies ontology source, examples, figures, and SHACL shapes to `dist/` |
| Build spec | `src/scripts/build-spec.py` | Calls `respec --localhost`, which spins up its own HTTP server, builds `dist/index.html`, and shuts down |

`--localhost` is required because Chromium (used internally by ReSpec) blocks `file://` requests needed by `data-include`. All paths (`src/index.html` → `dist/index.html`) are defined in `build-spec.py`.

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
