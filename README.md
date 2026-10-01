# mobilityDCAT-AP repository structure POC

[mobilityDCAT-AP](https://w3id.org/mobilitydcat-ap/releases/) is the
[NAPCORE](https://napcore.eu/) application profile of DCAT-AP for describing
mobility datasets, data services and services in the European National Access
Points. This repository is a proof of concept, not the authoritative
specification repository: it validates a proposed source layout, versioning
convention and GitHub Actions publishing workflow before they are applied to
[mobilityDCAT-AP/mobilityDCAT-AP](https://github.com/mobilityDCAT-AP/mobilityDCAT-AP).

# Concepts

## Sources and build output

The specification document is a [ReSpec](https://respec.org/) page,
`src/index.html`, configured by `src/config.js`. ReSpec renders it into a static
HTML page at build time.

The ontology, `src/mobilitydcat-ap.ttl`, and the worked examples in
`src/examples/` are written in Turtle, which is the source format. The RDF/XML
and JSON-LD serialisations are produced by the build and never committed.

The SHACL shapes in `src/shaclShapes/` are the validation constraints of the
profile. The build checks the examples against them.

Everything hand-authored lives in `src/`. The build writes everything it
produces to `dist/`, which is emptied at the start of each build and must not be
edited by hand.

```
src/
├── index.html                 # ReSpec specification document (entry point)
├── config.js                  # ReSpec configuration: version, editors, dates, links
├── mobilitydcat-ap.ttl        # Ontology, primary source of truth
├── tables/                    # HTML property tables included by index.html
├── examples/                  # Worked examples
├── figures/                   # UML diagrams and logo
├── shaclShapes/               # SHACL validation constraints
├── js/                        # Custom JavaScript
├── scripts/                   # Build scripts (Python), owned by this repository
├── enterpriseArchitectFiles/  # Enterprise Architect model (.qea)
└── appendices/                # Appendix content (placeholder)
```

Apart from `src/scripts/`, the content of `src/` mirrors the upstream
`drafts/latest`. It is kept identical so the proposed structure can be compared
with upstream; specification changes are made upstream, not here.

## Published versions

Every built version is a directory on the `gh-pages` branch, served under
`https://w3id.org/mobilitydcat-ap/`.

The editor's draft, `drafts/latest/`, is always the current `main`.

A draft snapshot, `drafts/X.Y.Z-draft.N/`, freezes the draft at a stable URL for
a review round.

A release, `releases/X.Y.Z/`, is a published version of the standard. It is
built from a long-lived `release/X.Y.Z` branch, so it can be hotfixed later.

The latest release, `releases/latest/`, is a copy of one release chosen by a
person. The file `LATEST_RELEASE` on `main` records which version that is.

## Branching and naming convention

| Ref | Kind | Goes to folder in gh-pages | Example |
|-----|------|----------------------------|---------|
| `main` | branch | `drafts/latest/` | |
| `draft/X.Y.Z-draft.N[.C]` | tag | `drafts/X.Y.Z-draft.N[.C]/` | `draft/3.0.0-draft.1`, `draft/3.0.0-draft.1.1` |
| `release/X.Y.Z` | branch | `releases/X.Y.Z/` | `release/3.0.0` |

A draft snapshot is tagged `draft/X.Y.Z-draft.N`, where `X.Y.Z` is the version
the draft is working towards and `N` is the review round counting from 1. A
release is a `release/X.Y.Z` branch with no suffix. This matches how DCAT-AP
labels its own drafts by target version.

The optional `.C` in `draft.N.C` is a correction published within the same
review round, such as a typo found right after the snapshot went out. Use it
sparingly; the plain `draft.N` is the normal form.

`X.Y.Z-draft.N` is a valid SemVer pre-release, so versions order by the SemVer
rules: numeric identifiers compare as numbers, and a longer identifier list
sorts above a shorter one with the same prefix, which places a correction after
the snapshot it corrects.

```
3.0.0-draft.1  <  3.0.0-draft.1.1  <  3.0.0-draft.2  <  3.0.0-draft.10  <  3.0.0
```

CI enforces both patterns: `build-draft.yml` rejects a tag that does not match
`^[0-9]+\.[0-9]+\.[0-9]+(-draft\.[0-9]+(\.[0-9]+)?)?$`, and `build-release.yml`
rejects a branch that does not match `^[0-9]+\.[0-9]+\.[0-9]+$`.

## mise tasks

[mise](https://mise.jdx.dev/) pins the tool versions (Node.js and uv) and
defines the build as named tasks in `.mise.toml`. CI runs the same tasks as a
local build, so the two produce the same result.

# Installation

Install [mise](https://mise.jdx.dev/getting-started.html), then in the project
folder:

```sh
mise install        # Node.js and uv at the pinned versions
mise run install    # npm install + uv sync
```

`DEVELOPMENT.md` covers installing mise on Windows and Linux.

# Configuration

A local build needs no settings, credentials or environment variables.

| What | Where |
|------|-------|
| Tool versions and task definitions | `.mise.toml` |
| ReSpec version | `package.json` |
| Python dependencies | `pyproject.toml`, locked in `uv.lock` |
| HTML validation rules | `.htmlvalidate.json` |
| Version, dates and URLs shown in the specification | `src/config.js`; the values differ between a draft and a release, see `PROCEDURES.md`, section [`config.js` checklist: draft vs release](PROCEDURES.md#configjs-checklist-draft-vs-release) |
| Which release `releases/latest/` points at | `LATEST_RELEASE` on `main`, changed through `promote-latest.yml` |

Publishing needs a `gh-pages` branch in the GitHub repository, with GitHub Pages
serving from it. The publish workflow checks that branch out and fails if it
does not exist.

# Usage

## Building locally

```sh
mise run build      # serialise the Turtle and build the ReSpec page into dist/
mise run lint       # build, then HTML validation, broken reference check and SHACL validation
mise run serve      # serve the repository for a live ReSpec preview
```

Open `dist/index.html` to see the built specification. The individual steps and
the expected output of the checks are in [`DEVELOPMENT.md`](DEVELOPMENT.md).

## Procedures

Every change to what is published follows one of five procedures. Each is
summarised here; the full steps, checks and edge cases are in
[`PROCEDURES.md`](PROCEDURES.md). Publishing a draft snapshot, creating a
release and hotfixing one also involve setting the snapshot or release values in
`src/config.js`, following `PROCEDURES.md`, section
[`config.js` checklist: draft vs release](PROCEDURES.md#configjs-checklist-draft-vs-release).

### Edit the current draft

For any change that is not yet a release; the everyday case. Branch from
`main`, edit under `src/`, run `mise run lint`, and open a pull request.
`build-check.yml` builds the branch without publishing it and attaches `dist/`
to the run for review. Merging to `main` refreshes `drafts/latest/`.
Full procedure: `PROCEDURES.md`, section [Edit the current draft](PROCEDURES.md#edit-the-current-draft).

### Publish a draft snapshot for review

When a version of the draft has to stay at a stable URL, for reviewers or a
meeting agenda. On a local branch from `main`, commit the snapshot values in
`config.js`, tag that commit and push only the tag:

```sh
git switch main
git pull
git switch -c snapshot/3.0.0-draft.1
# set the snapshot values in src/config.js and commit
git tag draft/3.0.0-draft.1
git push origin draft/3.0.0-draft.1
```

The snapshot values never go to `main`, which keeps its draft values.

`build-draft.yml` publishes `drafts/3.0.0-draft.1/`. A snapshot is never rebuilt
or moved; if it is wrong, publish `draft.1.1` or `draft.2` instead.
Full procedure: `PROCEDURES.md`, section [Publish a named draft snapshot for review](PROCEDURES.md#publish-a-named-draft-snapshot-for-review).

### Create a release

When a version is final. Create the release branch from `main`, set the
release values in `config.js` on that branch only, and push it:

```sh
git switch main
git pull
git switch -c release/3.0.0
# set the release values in src/config.js and commit
git push -u origin release/3.0.0
```

The release values never go to `main`, which keeps its draft values.

`build-release.yml` publishes `releases/3.0.0/`. The branch is long-lived and
must not be deleted, because hotfixes are made on it.
Full procedure: `PROCEDURES.md`, section [Create a release](PROCEDURES.md#create-a-release).

### Promote a release to latest

When a published release should become the one behind `releases/latest/`. This
is always a manual decision: run `promote-latest.yml` from the Actions tab with
the version number. It writes the version to `LATEST_RELEASE` on `main` and
copies the already-built `releases/X.Y.Z/` to `releases/latest/` without
rebuilding.
Full procedure: `PROCEDURES.md`, section [Promote a release to `releases/latest/`](PROCEDURES.md#promote-a-release-to-releaseslatest).

### Hotfix a published release

When a correction has to reach a published release before the next version.
There are two options. A small urgent fix can be committed straight to
`release/X.Y.Z` and pushed, which publishes it without review; see
`PROCEDURES.md`, section
[Hotfix without a pull request](PROCEDURES.md#hotfix-without-a-pull-request).
Otherwise, branch from `origin/release/X.Y.Z` and open a pull request against
`release/X.Y.Z`; see `PROCEDURES.md`, section
[Hotfix with a pull request](PROCEDURES.md#hotfix-with-a-pull-request).

Either way, the version number stays the same and only `publishDate` changes in
`config.js`; keep the fix in a commit separate from that change. A correction
that needs a new version number is a new release branch, such as
`release/3.0.1`, instead. Publishing rebuilds `releases/X.Y.Z/`, and also `releases/latest/`
if `LATEST_RELEASE` names that version; a hotfix to an older release leaves
`releases/latest/` alone. Cherry-pick the fix commit to `main` too, or the next
release ships the defect again.
Full procedure: `PROCEDURES.md`, section [Hotfix a published release](PROCEDURES.md#hotfix-a-published-release).

## Workflows

The procedures above trigger these workflows in `.github/workflows/`, which
build the ref and write the result to `gh-pages`.

| Workflow | Trigger | Publishes to |
|----------|---------|-------------|
| `build-main.yml` | push to `main` changing the build inputs, manual | `drafts/latest/` |
| `build-draft.yml` | push of a `draft/*` tag, manual | `drafts/X.Y.Z-draft.N[.C]/` |
| `build-release.yml` | push to `release/*`, manual | `releases/X.Y.Z/`, and `releases/latest/` if `LATEST_RELEASE` names this version |
| `promote-latest.yml` | manual only | sets `LATEST_RELEASE` on `main` and copies the already-built `releases/X.Y.Z/` to `releases/latest/` |
| `build-check.yml` | push to any other branch, pull request to `main` or `release/*`, manual | nothing; `dist/` is uploaded as a run artifact |

All of them build through `reusable-build.yml`, which runs `mise run build` and
then `mise run check`, and deploy through `reusable-publish-gh-pages.yml`, which
empties the target directory before writing so no removed file survives.
