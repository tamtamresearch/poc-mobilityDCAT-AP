Here's a structured comparison you can present to the team. I'll first lay out the proposed strategy (draft on `main`, branch on release), then a brief overview of the main alternative, so the team has context.

---

**The proposed approach** is: `main` always holds the latest draft in progress. When a draft is approved, it's branched off as a `release/vX.Y` branch. Fixes and textual corrections to past versions happen on those release branches.

---

Now the pro/cons/risks breakdown:A few practical notes to add context for the team discussion:

**The cherry-pick problem is the central tradeoff in any multi-version doc strategy** — it's not specific to Strategy A. No Git branching model eliminates it; the question is how you want to manage it. A simple convention like a `backport-to:` label in PRs, checked during review, keeps it low-overhead.

**For "several parallel drafts"** — the proposed model handles this cleanly by creating `draft/feature-x` branches off `main` on demand, reviewing them via PRs, and merging when ready. This costs nothing structurally since `main` stays the integration target.

**Branch naming convention worth agreeing on upfront:** `release/v1.0`, `release/v1.1` (for textual corrections) and `draft/topic-name` for parallel work — keeps the branch list scannable and makes automation (e.g. building all `release/*` sites) trivial.