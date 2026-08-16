# Team Links

Shared places that live outside this repo.

Important: this file is excluded from the published website, but **the repository
itself is public**, so anyone who browses it on GitHub can read this page. That is
fine if the Drive folder is shared with specific people, because a stranger
clicking the link just gets a permission error. It is **not** fine if the folder
is set to "anyone with the link", because then publishing the link publishes the
contents. Check which it is:

Open the folder, click **Share**, and look at **General access**. If it says
"Anyone with the link", either change it to "Restricted" and invite the parents
individually, or tell me and I will gitignore this file so the link stays only on
your machine.

## Google Drive

Team folder:
<https://drive.google.com/drive/folders/1TAPErgAN9CTvfzRXEwAXNV8DCEpO98Jq>

Use Drive for anything too big or too awkward for git:

- **Video.** Match footage, run recordings, the 1.4 GB official missions video.
  `.gitignore` deliberately blocks video files, because committing them makes the
  repo painful to clone.
- **Photos of the team.** Keep these out of the repo entirely. Git history is
  permanent and the repo is public.
- **The team fund spreadsheet**, once the CSV is imported to Google Sheets. See
  [`team-fund.md`](team-fund.md).
- **Scans and receipts.**

A suggested folder layout, so things stay findable in November:

```
FLL BIOGLOW 2026/
  Official materials/      the FIRST PDFs and the missions video
  Robot/                   photos and video of the robot and attachments
  Innovation project/      research, interview notes, prototype photos
  Notebook/                drafts and the final Engineering Notebook
  Admin/                   fund spreadsheet, receipts, registration
  Competition day/         photos and video from the event
```

## Other team links

Fill these in as they exist.

| What | Link |
| --- | --- |
| After-class notes form (what the kids fill in) | <https://docs.google.com/forms/d/e/1FAIpQLSdZLffhEKDjB5kv6IGmUgxbquTiqsvH47d2jKIVPAcYK1TXQg/viewform> |
| After-class notes form — edit the questions | <https://docs.google.com/forms/d/1FrGEAl5az6Peacy8POCYNkS58cCG2dghD_3KPgBLSX8/edit> |
| After-class notes responses (Google Sheets) | _paste once created_ |
| Team fund spreadsheet (Google Sheets) | _paste once imported_ |
| WhatsApp group | _optional_ |
| Team website (public) | <https://amana4.github.io/FLL2026/> |
| This repository | <https://github.com/amana4/FLL2026> |

The notes responses sheet is the running record of what happened each session,
ordered by date. It does not exist yet — create it from the form's **Responses**
tab and paste the link in above.

The **form** link is not a secret; it is embedded on the public website by design.
The **edit** link and the **responses sheet** are different. A stranger clicking
the edit link gets a permission error as long as the form's sharing stays
restricted, which is the same caveat as the Drive folder above — worth
re-checking if you ever widen it. The responses sheet holds a session-by-session
account of what the children did, so keep that one restricted to coaches and
parents.

## Official FIRST links

These are public and safe to share anywhere.

| What | Link |
| --- | --- |
| Season materials | <https://www.firstinspires.org/resources/library/fll/season-materials> |
| FLL Challenge home | <https://www.firstinspires.org/robotics/fll> |

## What goes where

| Kind of thing | Where |
| --- | --- |
| Notes, plans, mission analysis, code | This repo |
| Robot programs (`.llsp3`) and screenshots | This repo, in `code/` |
| Video of any kind | Drive |
| Photos of students | Drive |
| Photos of the robot | Either, but resize before committing |
| Money and receipts | Drive, plus the summary in `team-fund.md` |
| Anything with a student's full name | Not the repo, not the website |
