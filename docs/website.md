# The Team Website

Our notes are published as a searchable website at
**<https://amana4.github.io/FLL2026/>**

It's built from the exact same markdown files in this repo — there's no second
copy to keep in sync. Push a change to `main` and the site updates in about a
minute.

## One-time setup

Someone with admin on the repo does this once:

1. **Make the repo public.** GitHub Pages doesn't work on private repos on the
   free plan. Before you do — see the safety section below.
2. Go to **Settings → Pages**
3. Under **Source**, choose **GitHub Actions** (not "Deploy from a branch")
4. Push any commit to `main`. Watch it build in the **Actions** tab.
5. The site appears at `https://amana4.github.io/FLL2026/`

## What is public, and what is not

The repo is public, so anyone can read it and search engines index the site.
There are two different mechanisms at work, and confusing them has already caused
one leak, so it is worth being precise.

**`exclude_docs` in `mkdocs.yml` keeps a file off the website.** The file is still
in the repo and still readable by anyone browsing GitHub. It just does not become
a page.

**`.gitignore` keeps a file out of the repo entirely.** That is the only real
privacy mechanism.

**`not_in_nav` does neither.** It only silences the "this file is not in the nav"
build warning. The file is still built, published and indexed. `CLAUDE.md` sat in
`not_in_nav` for a day and was live at `/CLAUDE/` as a result.

### What is deliberately kept off the website

Listed in `exclude_docs`: `docs/team-roster.md` (children's names),
`docs/team-fund.md` and `.csv` (what each family paid), `docs/team-links.md` (the
Drive folder), and `CLAUDE.md`. All of these are still in the public repo — they
are off the *site*, not private. If any of them needs to be genuinely private,
gitignore it.

### FIRST's copyrighted materials are committed on purpose

The 15 PDFs and 13 slide decks in `docs/official-materials/` **are tracked**, by a
team decision on 9 August, so that a clone gets everything instead of each person
re-downloading. They are excluded from the site build only to keep the deploy
artifact small.

Do **not** run `git rm` on them. An earlier version of this page told you to,
which was wrong.

### What must never be committed

- **Purchase paperwork.** Sales orders and invoices carry a billing name, a
  residential address and payment details. `.gitignore` blocks
  `docs/official-materials/SalesOrd*` and anything matching invoice or receipt.
  Keep them outside the repo.
- **Photos of students.** Git history is permanent. Put these in the team Drive.
- **The 1.4 GB missions video.** It exceeds GitHub's 100 MB per-file limit and the
  push would be rejected. Stream it from the FIRST Season Resources page.

### The one automated check

The deploy workflow fails the build if `docs/team-roster.md` is tracked but no
longer excluded in `mkdocs.yml`. That is the only guard, and it exists because the
roster is the file most likely to be published by accident. There is no longer a
check on the PDFs, because committing them is now intentional.

## Editing

Three ways, in order of convenience:

**From the website.** Every page has a pencil icon that opens it on GitHub
ready to edit. Easiest for a quick fix from a phone.

**On GitHub.com.** Navigate to the file, click edit, commit. No git needed —
good for team members not comfortable with the command line.

**Locally with git.** See [`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Previewing locally

Optional, but useful before a big change:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000>. It reloads as you save.

## Adding a page

1. Create the `.md` file wherever it belongs
2. Add it to the `nav:` list in [`mkdocs.yml`](https://github.com/amana4/FLL2026/blob/main/mkdocs.yml)
3. Commit and push

Skip step 2 and the page still builds, but nobody will find it in the menu — and
`--strict` will warn unless you also add it to `not_in_nav`.

## If the build fails

Check the **Actions** tab for the red cross and read the log. Common causes:

| Error | Cause | Fix |
| --- | --- | --- |
| `Guard against publishing students' personal details` | `docs/team-roster.md` is tracked but no longer in `exclude_docs` | Restore the exclusion in `mkdocs.yml` |
| `is not found among documentation files` | A link points at a file that was renamed or deleted | Fix the link, or the path in `mkdocs.yml` |
| `Page exists in nav but not in docs` | `nav:` references a file that doesn't exist | Correct the path in `mkdocs.yml` |
| `contains an unrecognized relative link` | A link points at a directory with no `README.md`, or at a non-markdown file | Link the `README.md` explicitly, or use an absolute GitHub URL for non-pages |

The build uses `--strict`, which turns broken internal links into failures. That is
deliberate: better a red cross in Actions than a dead link found during judging
prep.

One thing `--strict` does **not** catch is a broken in-page anchor — a link of the
form `[see below](#a-heading-that-was-renamed)` where that heading no longer
exists. The `validation:` block in `mkdocs.yml` turns those into warnings too, and
`tools/check-links.py` catches them before you push.

## Why MkDocs and not Notion or a wiki

The repo stays the single source of truth. A docs site that's a separate copy
drifts from reality within weeks, and then nobody trusts either version. Here,
the website *is* the repo — it cannot drift.
