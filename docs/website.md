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

## Before making the repo public

Public means *anyone* can read it, including search engines. Two things must
stay out:

**FIRST's copyrighted PDFs.** `.gitignore` excludes `docs/official-materials/*.pdf`,
so downloading them there keeps them on your computer and out of git. Confirm
nothing slipped in earlier:

```bash
git ls-files | grep -i '\.pdf$'      # should print nothing
```

If a PDF is already tracked, remove it from git while keeping your local copy:

```bash
git rm --cached docs/official-materials/whatever.pdf
git commit -m "Remove copyrighted PDF from version control"
```

**Students' personal details.** `docs/team-roster.md` has names, grades, and
contacts. It's excluded from the website in `mkdocs.yml` and stays repo-only.
Think carefully before adding photos of students, full names, or a school name
anywhere else.

The deploy workflow checks both of these on every build and **fails loudly**
rather than publishing them by accident. Don't disable that check.

## Editing

Three ways, in order of convenience:

**From the website.** Every page has a pencil ✏️ icon that opens it on GitHub
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
2. Add it to the `nav:` list in [`../mkdocs.yml`](../mkdocs.yml)
3. Commit and push

Skip step 2 and the page still builds, but nobody will find it in the menu.

## If the build fails

Check the **Actions** tab for the red ✗ and read the log. Common causes:

| Error | Cause | Fix |
| --- | --- | --- |
| `Guard against publishing private material` | A PDF got committed, or the roster exclusion was removed | See the safety section above |
| `is not found among documentation files` | A link points at a file that was renamed or deleted | Fix the link, or the path in `mkdocs.yml` |
| `Page exists in nav but not in docs` | `nav:` references a file that doesn't exist | Correct the path in `mkdocs.yml` |

The build uses `--strict`, which turns broken internal links into failures. That
is deliberate: better a red ✗ in Actions than a dead link found during judging
prep.

## Why MkDocs and not Notion or a wiki

The repo stays the single source of truth. A docs site that's a separate copy
drifts from reality within weeks, and then nobody trusts either version. Here,
the website *is* the repo — it cannot drift.
