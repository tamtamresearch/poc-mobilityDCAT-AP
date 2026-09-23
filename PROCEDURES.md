# Procedures

How to do the recurring things in this repository: edit the draft, publish a
draft snapshot for review, cut a release, promote it, and hotfix it.

The three documents divide as follows:

| Document | Answers |
|----------|---------|
| `README.md` | What is in the repository, which workflow publishes where |
| `DEVELOPMENT.md` | How to install the toolchain and build locally |
| `PROCEDURES.md` (this file) | How do I do X |

Each procedure below states when it applies, the steps, and what lands where on
the `gh-pages` branch. The refs used are the ones defined in the branching table
in [`README.md`](README.md#branching-and-naming-convention):

| Ref | Kind | Publishes to |
|-----|------|--------------|
| `main` | branch | `drafts/latest/` |
| `draft/X.Y.Z-draft.N[.C]` | tag | `drafts/X.Y.Z-draft.N[.C]/` |
| `release/X.Y.Z` | branch | `releases/X.Y.Z/` |

Everything published lives on the `gh-pages` branch and is served from
`https://w3id.org/mobilitydcat-ap/`.

---

## 1. Edit the current draft

**When:** any change to the specification that is not yet a release. This is the
normal, everyday case.

**Steps**

1. Branch from `main`. Any name that is not `main`, `release/*` or `gh-pages`
   works; something like `fix/distribution-table` keeps the intent visible.

   ```sh
   git switch main
   git pull
   git switch -c fix/distribution-table
   ```

2. Edit under `src/`, and build locally before pushing:

   ```sh
   mise run lint      # full build + HTML validation + broken reference check
   ```

   See `DEVELOPMENT.md` for the individual steps.

3. Push the branch. `build-check.yml` runs the full build pipeline and
   **publishes nothing**. The built `dist/` is uploaded as a run artifact, so the
   rendered page can be downloaded from the Actions tab and reviewed.

   ```sh
   git push -u origin fix/distribution-table
   ```

4. Open a pull request against `main`. `build-check.yml` runs again for the pull
   request; its concurrency group cancels the older run of the same branch.

5. Merge. `build-main.yml` then builds `main` and publishes it to
   `drafts/latest/`, replacing what was there.

**Result on `gh-pages`:** `drafts/latest/` is refreshed. Nothing else moves.

**Note:** `build-main.yml` and `build-check.yml` are path-filtered to `src/**`,
`package.json` and `pyproject.toml`. A pull request that only touches
documentation does not trigger a build, which is expected; `drafts/latest/` is
unaffected by it either way.

---

## 2. Publish a named draft snapshot for review

**When:** a version of the draft has to stay reachable at a stable URL, for
example to send to reviewers or to reference from a meeting agenda.
`drafts/latest/` is not suitable for that, because the next merge to `main`
overwrites it.

**Steps**

1. Decide the tag: `draft/X.Y.Z-draft.N`, where `X.Y.Z` is the version the draft
   is working towards and `N` is the review round, counting from 1. The first
   review round of the 3.0.0 draft is `draft/3.0.0-draft.1`, the second is
   `draft/3.0.0-draft.2`.

   `N` may carry an optional second number for a correction inside the same
   round: `draft/3.0.0-draft.1.1`. It sorts after `3.0.0-draft.1` and before
   `3.0.0-draft.2`. Use it when a snapshot has already gone out and needs a fix
   that does not amount to a new review round; otherwise use the plain
   `draft.N`.

2. Set the draft values in `src/config.js` — see the
   [checklist](#configjs-checklist-draft-vs-release) in procedure 3 — and merge
   that change to `main` through procedure 1.

3. Tag the commit on `main` and push the tag:

   ```sh
   git switch main
   git pull
   git tag draft/3.0.0-draft.1
   git push origin draft/3.0.0-draft.1
   ```

4. `build-draft.yml` extracts the version by stripping the `draft/` prefix,
   validates it against `^[0-9]+\.[0-9]+\.[0-9]+(-draft\.[0-9]+(\.[0-9]+)?)?$`,
   builds, and publishes.

**Result on `gh-pages`:** `drafts/3.0.0-draft.1/`. `drafts/latest/` is untouched;
it stays managed by `build-main.yml`.

**The snapshot is permanent and is never rebuilt.** Nothing re-triggers
`build-draft.yml` for an existing tag, so the published folder keeps showing the
state of the source at the moment the tag was pushed. If a snapshot turns out to
be wrong, publish a new tag rather than moving the existing one: `-draft.N.C` if
it is a correction within the round, `-draft.N+1` if it is the next round.

---

## 3. Create a release

**When:** a version of the specification is final and should be published under
`releases/`.

**Steps**

1. On a branch off `main`, set the release values in `src/config.js` (checklist
   below) and merge that change to `main` through procedure 1. Doing it on `main`
   first keeps the draft and the release branch from diverging immediately.

2. Create the release branch from `main` and push it:

   ```sh
   git switch main
   git pull
   git switch -c release/3.0.0
   git push -u origin release/3.0.0
   ```

3. `build-release.yml` extracts the version from the branch name, validates it
   against `^[0-9]+\.[0-9]+\.[0-9]+$` (no pre-release suffix is accepted on a
   release branch), builds, and publishes.

4. The same workflow reads `LATEST_RELEASE` from `main` with a sparse checkout
   and compares it to the branch version. If they match, a second `publish-latest`
   job also deploys to `releases/latest/`. For a brand new version they will not
   match yet; use procedure 4 to promote it.

**Result on `gh-pages`:** `releases/3.0.0/`, and `releases/latest/` as well if
`LATEST_RELEASE` on `main` already reads `3.0.0`.

**The release branch is long-lived.** It stays in the repository so hotfixes can
be made on it (procedure 5). Do not delete it after publishing.

### `config.js` checklist: draft vs release

All of these live in `src/config.js`. The current file is a useful warning: on
`main`, which is the living draft, it carries `specStatus: "unofficial"` and
`canonicalURI` pointing at `drafts/latest/`, but at the same time
`thisVersionURI` pointing at `releases/3.0.0/` and a `publishDate` of
`2026-10-01`. That is a mix of draft and release values, and it is what this
checklist exists to prevent.

| Field | Line | Draft (`main`, `draft/*`) | Release (`release/X.Y.Z`) |
|-------|------|---------------------------|---------------------------|
| `publishDate` | 17 | the date the draft snapshot is published, or omitted on `main` | the release date |
| `specStatus` | 59 | `"unofficial"` | the agreed published status (see [ReSpec specStatus](https://respec.org/docs/#specStatus)) |
| `latestVersion` | 61 | `https://w3id.org/mobilitydcat-ap/releases/` | unchanged |
| `canonicalURI` | 63 | `.../drafts/latest/`, or `.../drafts/X.Y.Z-draft.N/` for a tagged snapshot | `.../releases/X.Y.Z/` |
| `prevRecURI` | 64 | the last formally published release | the last formally published release |
| `thisVersionURI` | 66 | the draft's own URL, matching `canonicalURI` | `.../releases/X.Y.Z/` |
| `prevVersionURI` | 67 | the release this draft supersedes | the release this one supersedes |
| `latestVersionURI` | 68 | `https://w3id.org/mobilitydcat-ap/releases/` | unchanged |
| `edDraftURI` | 70 | `.../drafts/latest/` | `.../drafts/latest/` (the editor's draft is always `main`) |

Two more entries carry version numbers by hand and are easy to miss, because they
are hard-coded `otherLinks` rows rather than ReSpec fields:

| Entry | Line | What to set |
|-------|------|-------------|
| `otherLinks` → "Document version" | 132-137 | the version number being published |
| `otherLinks` → "Previous version:" | 140-141 | `value` and `href`, both the previous release URL |
| `otherLinks` → "This version:" | 144-145 | `value` and `href`, both this version's URL |

Note that the `otherLinks` rows use `https://mobilitydcat-ap.github.io/mobilityDCAT-AP/...`
while the ReSpec fields above use `https://w3id.org/mobilitydcat-ap/...`. The two
forms resolve to the same pages; keeping each entry consistent with its
neighbours matters more than unifying them.

Do not fix any of this by editing the built HTML in `dist/`. The next automated
build overwrites `dist/` entirely. Anything that cannot be expressed in
`config.js` belongs in `src/index.html`.

### What CI could fill in, and what it cannot

Four of the fields above are a pure function of the ref that triggered the build,
and a workflow step could write them into `config.js` before the ReSpec build:

- `thisVersionURI` and `canonicalURI` — derivable from the branch or tag name,
  which the `extract-version` job already parses.
- `publishDate` — the build date.
- `specStatus` — determined by which workflow is running.

Two cannot be derived and need a human decision:

- `prevVersionURI` — which release this one supersedes.
- `prevRecURI` — which release counts as the last formally published one.

Whether to automate the first group is **an open question for the meeting**, not
something implemented here. The trade-off: it removes four manual steps from this
checklist, but it makes a local build and a CI build produce different metadata
from the same source, which is a real cost when debugging a published page.

---

## 4. Promote a release to `releases/latest/`

**When:** a published release should become the one that
`https://w3id.org/mobilitydcat-ap/releases/latest/` points at. This is always a
deliberate step; no version becomes latest on its own.

**Steps**

1. Confirm `releases/X.Y.Z/` already exists on `gh-pages`. `promote-latest.yml`
   copies what is published; it does not build. It fails with an explicit error
   if the directory is not there.

2. Actions tab → **Promote release to releases/latest** → Run workflow → enter
   the version, for example `3.0.0`.

3. The workflow does two things:
   - writes the version into `LATEST_RELEASE` on `main` and commits it;
   - copies `releases/X.Y.Z/` to `releases/latest/` on `gh-pages` directly.

4. Confirm both landed, because they are two separate commits on two branches:

   ```sh
   git fetch origin
   git show origin/main:LATEST_RELEASE          # must read X.Y.Z
   git log -1 --oneline origin/gh-pages         # promote commit for releases/latest
   ```

   Then open `https://w3id.org/mobilitydcat-ap/releases/latest/` and check the
   version shown on the page.

**Result on `gh-pages`:** `releases/latest/` becomes a copy of `releases/X.Y.Z/`.
On `main`, `LATEST_RELEASE` now reads `X.Y.Z`.

**Why `LATEST_RELEASE` matters afterwards.** It is the marker
`build-release.yml` checks on every push to a `release/*` branch. Once it reads
`3.0.0`, any later hotfix pushed to `release/3.0.0` refreshes both
`releases/3.0.0/` and `releases/latest/` in the same run, with no second manual
step. Before promotion, a push to that branch would only refresh the versioned
directory.

`LATEST_RELEASE` lives on `main` only. Release branches never carry it, so a
hotfix branch cannot accidentally promote itself.

---

## 5. Hotfix a published release

**When:** a correction has to reach an already published release without waiting
for the next version.

**Steps**

1. Check out the existing release branch:

   ```sh
   git switch release/3.0.0
   git pull
   ```

2. Make the fix under `src/`, and bump the patch version. The branch name stays
   `release/3.0.0` — the branch is the release line, and `config.js` records the
   published version. If the correction is substantive enough to warrant a new
   version number, create `release/3.0.1` from `release/3.0.0` through procedure
   3 instead; the two approaches differ in whether `releases/3.0.0/` is rewritten
   or left standing.

3. Update the version-bearing entries in `config.js` from the checklist in
   procedure 3: `publishDate`, `thisVersionURI`, `canonicalURI`, and the
   `otherLinks` rows.

4. Push. `build-release.yml` runs exactly as it does for a new release branch.

**Result on `gh-pages`:** `releases/3.0.0/` is rebuilt. If `LATEST_RELEASE` on
`main` reads `3.0.0`, `releases/latest/` is rebuilt in the same run.

**A hotfix to a branch that is not the latest leaves `releases/latest/`
untouched.** That is the intended behaviour: correcting an old release must not
change what current readers see. If the fix does belong in the latest release
too, apply it to that branch as well.

Pull requests targeting a `release/*` branch are covered by `build-check.yml`, so
a hotfix can go through review the same way a draft change does.

---

## Where things end up

| Ref you push | Workflow | `gh-pages` directory |
|--------------|----------|----------------------|
| any other branch, or a PR | `build-check.yml` | nothing; `dist/` as a run artifact |
| `main` | `build-main.yml` | `drafts/latest/` |
| `draft/X.Y.Z-draft.N[.C]` tag | `build-draft.yml` | `drafts/X.Y.Z-draft.N[.C]/` |
| `release/X.Y.Z` branch | `build-release.yml` | `releases/X.Y.Z/`, plus `releases/latest/` if marked |
| (manual run) | `promote-latest.yml` | `releases/latest/`, and `LATEST_RELEASE` on `main` |

All five publishing workflows share the same build through
`reusable-build.yml`, and all deployment goes through
`reusable-publish-gh-pages.yml`, which pre-cleans the target directory before
writing. A published directory therefore never keeps a file that has been
removed from the source.
