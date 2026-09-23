# Development guide

This guide covers the toolchain: prerequisites, setup, building and linting
locally. For the editing and publishing procedures that use it - edit the draft,
tag a draft snapshot, create a release, promote it, hotfix it - see
[`PROCEDURES.md`](PROCEDURES.md).

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
mise run build        # full build: serialise Turtle + build ReSpec spec
```

All output is written to **`dist/`**. Open `dist/index.html` in a browser to preview the built specification.

Individual steps:

```sh
mise run clean        # empty dist/ (run automatically at the start of mise run build)
mise run serialise    # convert src/*.ttl and src/examples/*.ttl -> dist/*.rdf + dist/*.jsonld
mise run build-spec   # copy assets to dist/ and build dist/index.html via ReSpec
```

## Linting

```sh
mise run lint         # full build + HTML validation + broken local references
mise run validate     # HTML markup validation only (requires a prior build)
```

`mise run lint` runs the full build, then:
1. Validates `dist/index.html` markup with `html-validate` (rules defined in `.htmlvalidate.json`)
2. Parses `dist/index.html` with `src/scripts/check-refs.py`, which cross-references all `id` attributes against all `href="#..."` links and prints each broken one

ReSpec only reports a count of broken references in its CLI output — `check-refs.py` gives the actual list.

## Live preview

To use ReSpec's interactive warnings panel in the browser:

```sh
mise run serve        # starts HTTP server on http://localhost:8080
```

Open `http://localhost:8080/src/index.html` in a browser. ReSpec runs live and shows a warnings badge at the top — click it to see all issues with locations. Stop with `Ctrl+C`.

## How it works

| Step | Script | What it does |
|------|--------|-------------|
| Serialise | `src/scripts/serialise.py` | Parses each `.ttl` with rdflib, writes `.rdf` and `.jsonld` to `dist/` |
| Copy assets | `src/scripts/copy-assets.py` | Copies the Turtle sources, examples, figures, and SHACL shapes to `dist/` |
| Build spec | `src/scripts/build-spec.py` | Calls `respec --localhost`, which spins up its own HTTP server, builds `dist/index.html`, and shuts down |

`--localhost` is required because Chromium (used internally by ReSpec) blocks `file://` requests needed by `data-include`. All paths (`src/index.html` → `dist/index.html`) are defined in `build-spec.py`.

## Source layout

All hand-authored files live under `src/`. Never edit files in `dist/` — they are generated.

Turtle is the source format for the ontology and the examples. The `.rdf` and `.jsonld` serialisations are generated on every build and are never committed.

| Path | Purpose |
|------|---------|
| `src/mobilitydcat-ap.ttl` | Ontology — primary source of truth (Turtle) |
| `src/index.html` | ReSpec specification document |
| `src/config.js` | ReSpec configuration (version, editors, dates, bibliography) |
| `src/tables/` | HTML property tables included by `index.html` via `data-include` |
| `src/examples/` | Worked examples (Turtle) |
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

Every publishing workflow runs the same pipeline as `mise run lint`, through the
reusable workflow `.github/workflows/reusable-build.yml`. Which ref publishes
where is listed in `README.md`; the step-by-step procedures are in
[`PROCEDURES.md`](PROCEDURES.md).
