# mobilityDCAT-AP - Repository Structure POC

> **This is a proof of concept** demonstrating a proposed repository layout and GitHub Actions publishing workflow for mobilityDCAT-AP. It is not the authoritative specification repository.
>
> The goal is to validate the branch-based versioning strategy before applying it to the main repo.

## Source files

All hand-authored source files live in `src/`. Generated artefacts go in `dist/` and must not be edited by hand.

Turtle is the source format for the ontology and the examples. The RDF/XML and JSON-LD serialisations are produced by the build and are never committed.

## Structure

```
src/
├── index.html                 # ReSpec specification document (entry point)
├── config.js                  # ReSpec configuration
├── mobilitydcat-ap.ttl        # Ontology - primary source of truth (Turtle)
├── tables/                    # HTML property tables included by index.html
├── examples/                  # Worked examples (Turtle)
├── figures/                   # UML diagrams and logo
├── shaclShapes/               # SHACL validation constraints
├── js/                        # Custom JavaScript
├── scripts/                   # Build scripts (Python); see DEVELOPMENT.md
├── enterpriseArchitectFiles/  # EA model (.qea)
└── appendices/                # Appendix content (placeholder)
```

## Branching and naming convention

| Ref | Kind | Goes to folder in gh-pages | Example |
|-----|------|----------------------------|---------|
| `main` | branch | `drafts/latest/` | - |
| `draft/X.Y.Z-draft.N[.C]` | tag | `drafts/X.Y.Z-draft.N[.C]/` | `draft/3.0.0-draft.1`, `draft/3.0.0-draft.1.1` |
| `release/X.Y.Z` | branch | `releases/X.Y.Z/` | `release/3.0.0` |

The rule in one sentence: a draft snapshot is tagged `draft/X.Y.Z-draft.N`, where
`X.Y.Z` is the version the draft is working towards and `N` is the review round
counting from 1, and a release is a `release/X.Y.Z` branch with no suffix.

`N` may carry an optional second number, `draft.N.C`, for a correction published
within the same review round - a typo found right after the snapshot went out,
where opening a new review round would misrepresent what happened. Use it
sparingly; the plain `draft.N` is the normal form.

`X.Y.Z-draft.N` is a valid SemVer pre-release, so version ordering follows from
the SemVer rules rather than from a local convention. Pre-release identifiers are
compared left to right, `draft` equals `draft`, and the numeric ones compare
numerically instead of as text. A longer set of identifiers sorts above a shorter
one when everything before it is equal, which is what places a correction after
the snapshot it corrects:

```
3.0.0-draft.1  <  3.0.0-draft.1.1  <  3.0.0-draft.2  <  3.0.0-draft.10  <  3.0.0
```

The convention also matches how DCAT-AP labels its own drafts by target version.

Both patterns are enforced in CI: `build-draft.yml` rejects a tag that does not
match `^[0-9]+\.[0-9]+\.[0-9]+(-draft\.[0-9]+(\.[0-9]+)?)?$` and
`build-release.yml` rejects a branch that does not match
`^[0-9]+\.[0-9]+\.[0-9]+$`.

Step-by-step procedures that use these refs are in [`PROCEDURES.md`](PROCEDURES.md).

## GitHub Actions workflows

Workflows live in `.github/workflows/` and publish to the `gh-pages` branch.

| Workflow | Trigger | Publishes to |
|----------|---------|-------------|
| `build-main.yml` | push to `main` (src changes), manual | `drafts/latest/` |
| `build-release.yml` | push to `release/*`, manual | `releases/X.Y.Z/` and `releases/latest/` if marked |
| `build-draft.yml` | push of `draft/*` tag, manual | `drafts/X.Y.Z-draft.N[.C]/` |
| `promote-latest.yml` | manual only | updates `LATEST_RELEASE` on `main` + copies already-built `releases/X.Y.Z/` to `releases/latest/` on `gh-pages` |
| `build-check.yml` | push to any other branch, pull request to `main` or `release/*` (src changes), manual | nothing; `dist/` is uploaded as a run artifact only |

The build and deploy steps are split into two reusable workflows called by the above:

| Reusable workflow | Purpose |
|-------------------|---------|
| `reusable-build.yml` | Full build pipeline through the mise tasks - `mise run build`, then `mise run check` (HTML validation, references, SHACL validation of the examples); uploads `dist/` as an artifact |
| `reusable-publish-gh-pages.yml` | Pre-clean target directory on `gh-pages`, then deploy the artifact via plain `git` |

### Promoting a release to `releases/latest/`

`LATEST_RELEASE` in the repo root (on `main`) holds the version number currently marked as latest (e.g. `1.0.0`). On every push to a `release/*` branch, `build-release.yml` reads this file from `main` - if the version matches the branch, it also deploys to `releases/latest/` automatically.

This means:
- Hotfixes to the current latest release branch update `releases/latest/` automatically, just like they update the versioned directory.
- Hotfixes to older release branches only update their versioned directory - `releases/latest/` is untouched.

To promote a different version to latest:

- Run `promote-latest.yml` from the Actions tab and enter the version number.
- It updates `LATEST_RELEASE` on `main` (so future hotfixes to that branch also update `releases/latest/`).
- It also copies the already-built `releases/X.Y.Z/` to `releases/latest/` on `gh-pages` immediately - no rebuild needed.
- Promotion is an explicit, deliberate step - no version silently becomes latest without a human decision.

## Building locally

See `DEVELOPMENT.md` for prerequisites, setup, and build instructions.

## Editing and publishing

See [`PROCEDURES.md`](PROCEDURES.md) for step-by-step procedures: editing the
current draft, publishing a named draft snapshot for review, creating a release,
promoting a release to latest, and hotfixing a published release. It also carries
the `src/config.js` checklist for drafts and releases.
