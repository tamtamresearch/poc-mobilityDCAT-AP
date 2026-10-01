# README and PROCEDURES review findings

Findings from a review of `README.md` and `PROCEDURES.md` against the workflows
in `.github/workflows/`, `.mise.toml` and `src/config.js`, ordered by severity.
Each item records its status; a fix updates the status in the same commit.

## Procedures that publish the wrong thing

### 1. Creating a release puts release metadata on the draft

`PROCEDURES.md`, Create a release, step 1 merges the release values in
`config.js` to `main` before branching. That merge triggers `build-main.yml`, so
`drafts/latest/` is published with a release `specStatus` and a `canonicalURI`
pointing at `releases/3.0.0/`, which is the draft/release mix the `config.js`
checklist warns against. No step resets `main` to draft values afterwards.

Status: fixed. The release values are now committed on the release branch
before its first push and never merged to `main`.

### 2. Publishing a draft snapshot has the same problem

`PROCEDURES.md`, Publish a named draft snapshot for review, step 2 merges the
snapshot values to `main` before tagging. `drafts/latest/` then advertises the
snapshot URL as its canonical URL, and nothing resets it.

Status: fixed. The snapshot values are now committed on a local branch that is
never pushed; only the tag pointing at that commit is pushed.

### 3. The hotfix version guidance contradicts itself

`PROCEDURES.md`, Hotfix without a pull request, step 3 says to bump the patch
version while keeping the branch at `release/3.0.0`, so `releases/3.0.0/` would
say 3.0.1. The next sentence says a new version number calls for
`release/3.0.1` instead. The same step lists `thisVersionURI` and
`canonicalURI` as entries to update, but they do not change for a hotfix on the
same branch.

Status: fixed. A hotfix now keeps the version number and changes only
`publishDate`; a change that needs a new version number is a new release branch
cut from the old one.

## Where the documents and the workflows disagree

### 4. A failed promotion still changes `LATEST_RELEASE`

`promote-latest.yml` commits `LATEST_RELEASE` to `main` before it checks whether
`releases/X.Y.Z/` exists. `PROCEDURES.md`, Promote a release, step 1 implies a
missing directory makes the workflow fail cleanly; in fact `main` is left
pointing at an unpublished version, and the next push to that release branch
would publish it to `releases/latest/`. The version input is not validated.

Status: fixed. `promote-latest.yml` now validates the version and checks the
directory before writing anything, and a repeated run for the same version no
longer fails on an empty commit.

### 5. Hotfixing the latest release can fail to update `releases/latest/`

In `build-release.yml`, the `publish` and `publish-latest` jobs run in parallel.
Each checks out `gh-pages`, commits and pushes, so the second push is likely
rejected as non-fast-forward. That breaks the "rebuilt in the same run" promise
in `PROCEDURES.md` and `README.md`. Nothing serialises the workflows that push
to `gh-pages`, so two of them running at once can collide the same way.

Status: fixed. Jobs writing the same `gh-pages` directory now share a
concurrency group, and a push rejected because `gh-pages` moved is rebased and
retried. Not yet exercised on GitHub.

### 6. Failed checks do not stop a publish, and neither document says so

`reusable-build.yml` runs `mise run check` with `continue-on-error`, so a broken
reference or a SHACL violation is still published, including on a merged hotfix
pull request. Hotfix without a pull request says the local build is the only
check; that is effectively true of every procedure.

Status: fixed. Both documents now say that checks are reported, not enforced,
and that `mise run lint` before a push is what catches a failure. Making the
checks blocking is a separate decision; `DEVELOPMENT.md` describes the current
behaviour as intended.

### 7. Two descriptions of the workflows are wrong

`README.md`, Workflows, says all workflows build through `reusable-build.yml`
and deploy through `reusable-publish-gh-pages.yml`; `promote-latest.yml` does
neither and `build-check.yml` does not deploy. `PROCEDURES.md`, Where things end
up, refers to "all five publishing workflows" sharing the build; only four
build, and only three of those publish through it.

Status: fixed. Both passages now name which workflows build, which publish
through `reusable-publish-gh-pages.yml`, and what `promote-latest.yml` does
instead.

### 8. "Manual" in the README Workflows table hides a catch

A manual run of `build-draft.yml` or `build-release.yml` fails unless the tag or
release branch is selected as the ref, because the version validation fails
otherwise.

Status: fixed. The table now says each manual run must start from the tag or
release branch, and a note below it explains why.

### 9. "Nothing re-triggers `build-draft.yml` for an existing tag" is too strong

`PROCEDURES.md`, Publish a named draft snapshot for review. A manual run from
that tag rebuilds and overwrites the snapshot.

Status: open

## Smaller inaccuracies in the README

### 10. The README command snippets leave out the preparation steps

The snippets under Publish a draft snapshot and Create a release skip
`git switch main` and `git pull`. Copied as they are, they tag or branch from
whatever is checked out.

Status: open

### 11. The README says the build checks the examples

`README.md`, Sources and build output, says the build checks the examples
against the SHACL shapes. `mise run check` does that, not `mise run build`.

Status: open

### 12. The `mise run serve` line does not say which URL to open

`serve.py` serves the repository root; the page is at
`http://localhost:<port>/src/index.html`.

Status: open

### 13. Installation may be missing `mise trust`

`.mise.toml` has an `[env]` section with a template, and mise normally refuses
to load such a file on a fresh clone until it is trusted. Neither `README.md` nor
`DEVELOPMENT.md` mentions it. Not yet confirmed on a fresh clone.

Status: open

### 14. Configuration covers only the `gh-pages` branch

The `https://w3id.org/mobilitydcat-ap/` redirect to GitHub Pages is maintained
outside this repository. `promote-latest.yml` pushes to `main`, so protecting
`main` against direct pushes would break promotion. Neither is mentioned.

Status: open

## Upkeep

### 15. The checklist will go out of date as `src/config.js` changes

The line numbers in the `config.js` checklist and the "current file is a useful
warning" paragraph describe today's file. They are correct now, but the next
upstream sync can silently invalidate them.

Status: open

### 16. The document map in `PROCEDURES.md` is out of date

It says the README covers only what is in the repository and which workflow
publishes where. The README now also summarises the procedures.

Status: open

### 17. The "open question for the meeting" text is meeting-specific

`PROCEDURES.md`, What CI could fill in, and what it cannot. It will read oddly
once the meeting has happened.

Status: open
