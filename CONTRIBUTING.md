# How we work in this repo

Written for team members who may be new to git. Ask if anything here is unclear —
that's not a silly question, it's a gap in this document.

## The short version

1. Make a branch
2. Do your work
3. Commit with a clear message
4. Open a pull request
5. Someone else looks at it, then it gets merged

## Branches

Never commit straight to `main`. `main` should always be the version that works.

Name branches `area/short-description`:

```
robot/gripper-attachment
code/r2-line-following
project/interview-notes
docs/update-strategy
```

```bash
git checkout main
git pull
git checkout -b code/r2-line-following
```

## Commits

A good message says **what changed and why**. Future-you has no memory.

```
✅ R2: slow approach to 30% — was overshooting the drop zone
✅ Add interview notes from the recycling centre visit
✅ Gripper v3: wider fork so it doesn't miss the loop

❌ update
❌ fixed stuff
❌ asdf
```

```bash
git add .
git commit -m "R2: slow approach to 30% — was overshooting the drop zone"
git push -u origin code/r2-line-following
```

## Pull requests

Open a PR on GitHub. Say what you changed and what you tested. If it's a robot
program, **include the screenshot** — nobody can review a `.llsp3` file.

Someone else on the team reviews it. Reviewing is not criticising; it's how
everyone stays aware of what the robot does.

## Special rules for robot code

`.llsp3` files are binary — git can't merge them, and two people editing the same
program will conflict painfully.

**So:** one person at a time per program. Say in the team chat which program
you're taking. When you're done, push and say you're done.

Always commit the `.llsp3` **and** its screenshot together.

## Photos and video

- Photos: commit them, but resize to something sensible first
- Video: **don't commit it.** Put it in the team's shared drive and link to it.
  A repo full of match footage takes forever to clone.

## If something goes wrong

Nothing here is unfixable — git keeps history. Ask a coach before running any
command you found online that has `--force` in it.

```bash
git status                  # what's going on right now
git diff                    # what have I changed
git checkout -- <file>      # throw away my changes to one file
git log --oneline           # recent history
```

## Writing docs

Markdown. Keep the templates' structure so files stay comparable. Fill in `TODO`
placeholders rather than deleting them — a visible `TODO` is information; a
missing section looks finished when it isn't.
