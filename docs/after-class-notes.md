# After-Class Notes

Five minutes at the end of a session, or on the way home. What you write here is
what you will have to talk about in the judging room in November, and it is much
easier to remember now than in October.

Everything goes into **one shared list, ordered by date**, so the whole team can
see it and nothing depends on one person's phone.

## Add today's note

<iframe
  src="https://docs.google.com/forms/d/e/1FAIpQLSdZLffhEKDjB5kv6IGmUgxbquTiqsvH47d2jKIVPAcYK1TXQg/viewform?embedded=true"
  width="100%"
  height="900"
  style="border:0;max-width:100%"
  title="After-class notes form">Loading the form…</iframe>

If the form does not load, open it in a new tab instead — the link is in
`docs/team-links.md` in the repo, which is kept off this website.

## What to write

You do not have to fill in every box. One good sentence beats five blank fields.

**What changed on the robot.** Even a small change counts. If you took something
apart and put it back differently, that is an iteration.

**What broke.** This is worth more to judges than what worked. "This is version
four, and versions one to three did not work because…" is the single strongest
thing you can say about your robot. Write the reason down while you still
remember it.

**Numbers from testing.** Numbers matter more than adjectives. "It got more
reliable" is weak; "it went from four out of ten to nine out of ten after we
added gyro correction" is strong. Nobody remembers the numbers a week later, so
write them at the table.

**Anyone you talked to about the project, and what they said.** Especially
anything that surprised you or changed your mind. The rubric asks for evidence
that feedback actually *changed* something, so write down both halves: what they
said, and what you did differently because of it.

**A Core Values moment.** Something small is fine. Somebody helped somebody.
Something was funny. Somebody stuck with something hard.

**Any disagreement, and how you sorted it out.** Judges ask about this almost
every year, and "we never disagree" is a worse answer than a real story. Two
honest examples by November is the goal.

**What you personally did.** Answer for yourself, not the team. Judges pick who
they ask, so each of you needs to be able to say what *you* built, coded, or
worked out. This feeds [`who-did-what.md`](who-did-what.md).

**What needs photographing.** Photos are the highest-value thing you can bring to
judging and the easiest to lose the chance at. **You can only photograph version
one before you take it apart.** Once it is dismantled it is gone, and "we had an
earlier version but no picture" scores nothing.

Two rules on what not to write. Use **Kid 1** to **Kid 5** rather than real
names, because notes get copied into the repo and the repo is public. And no
photos of people's faces on the website — robot, field, attachments, sketches
and prototype photos are all fine.

## Reading the notes back

The responses live in one spreadsheet, newest at the bottom, with a timestamp on
every row. The link is in `docs/team-links.md` in the repo, which is kept off
this website.

Two things worth knowing when you read it:

There are **two dates** on every row. The automatic *Timestamp* is when the form
was submitted; *Session date* is the meeting the note is about. They are usually
the same day, but not if somebody fills the form in the next morning. **Sort by
Session date**, not Timestamp, or your timeline will be subtly wrong.

Sort newest-first with **Data**, then **Sort range**, then Session date
descending. Filter by the *Area* column to pull out just the robot notes or just
the project notes when filling in a prep sheet.

## Where these notes end up

The spreadsheet is the running record. These files are what gets printed and
carried into the judging room, and they are assembled *from* the spreadsheet.

| What you wrote | Where it belongs |
| --- | --- |
| Robot changes, things that broke | [`robot-design/design-log.md`](../robot-design/design-log.md) |
| Code changes and test numbers | [`code/README.md`](../code/README.md) and the mission's own page |
| Test results | [`robot-game/scoring-tracker.md`](../robot-game/scoring-tracker.md) |
| Innovation Project progress | [`innovation-project/README.md`](../innovation-project/README.md) |
| Feedback, and what changed because of it | [`innovation-project/sharing.md`](../innovation-project/sharing.md) |
| Core Values moments, disagreements | [`core-values/evidence-log.md`](../core-values/evidence-log.md) |
| Who did what | [`who-did-what.md`](who-did-what.md) |

Copying across does not need doing weekly. Once a fortnight is fine, and the
notebook checkpoint at Meeting 18 is the natural moment to catch up. The
spreadsheet means nothing is lost in the meantime, which is the part that used to
go wrong.

## What else to record for judging day

Beyond the form, these are the things teams most often wish they had written
down. All of them come straight off the two official rubrics.

**Why you rejected things.** Which missions you decided *not* to attempt and why,
and which Innovation Project ideas you dropped. Judges ask "why not that one?"
and a reasoned answer — points per second, too risky, no time — shows strategy.
"We just didn't" does not. Missions go in
[`robot-game/strategy.md`](../robot-game/strategy.md), rejected project ideas in
[`innovation-project/brainstorm.md`](../innovation-project/brainstorm.md).

**Where your information came from.** Websites, videos, books, the SPIKE app
tutorials, other teams, and every real conversation. The Innovation Project
rubric names "a variety of sources" explicitly, so a list of only websites caps
your score. Log them in
[`innovation-project/research.md`](../innovation-project/research.md) as you go —
reconstructing a source list in October is miserable.

**The numbers you will be asked for.** Wheel circumference, typical success rate,
best practice score, attachment swap time, how many missions you attempt, how
many motors you use. The table is already waiting in
[`robot-design-prep.md`](judging/robot-design-prep.md); it only gets filled in by
someone measuring and writing it down.

**Who can explain what.** Both rubrics ask for evidence that *all* members have
building and coding skills, not just one expert. That is what
[`who-did-what.md`](who-did-what.md) is for, and it doubles as your answer to
"how did you divide the work?"

**What you would do with more time.** Asked almost every year. A real answer
means noticing during the season what you are leaving unfinished, rather than
inventing something in the room.

**What another team did that you liked.** Gracious Professionalism is scored at
the table by referees, and having actually learned something from another team is
strong evidence. Write it down the same day.

**Anything you promised somebody.** If an expert asked for a follow-up, or you
said you would send them the result, that goes in
[`innovation-project/sharing.md`](../innovation-project/sharing.md). Judges are
impressed by teams who closed the loop.

## Setting this up

??? note "Coach: creating the form (about ten minutes, once)"

## How this was set up

The form already exists and is wired into this page. This section is here so it
can be rebuilt — if the form gets deleted, or next season's team wants a fresh
one without re-inventing the questions.

??? note "Rebuilding the form"

    **The quick way.** `tools/create-notes-form.gs` in this repo is a Google Apps
    Script that builds the whole form in one run. Paste it into a new project at
    <https://script.google.com>, run `createNotesForm`, and copy the embed URL it
    prints from the execution log. That script is also the authoritative record of
    the question list.

    **By hand.** Start a blank form at <https://forms.google.com>, call it
    "FLL BIOGLOW — After-class notes", and add these questions in order. Only the
    first three are required; leaving the rest optional is what keeps kids
    actually filling it in.

    | # | Question | Type | Required |
    | --- | --- | --- | --- |
    | 1 | Session date | Date | Yes |
    | 2 | Who is writing this? | Dropdown: Kid 1, Kid 2, Kid 3, Kid 4, Kid 5, Coach | Yes |
    | 3 | Area | Checkboxes: Robot, Programming, Innovation Project, Core Values, Other | Yes |
    | 4 | What we did, built, or changed | Paragraph | No |
    | 5 | What broke or did not work, and why we think so | Paragraph | No |
    | 6 | Numbers from testing | Short answer | No |
    | 7 | Anyone we talked to, and what they told us | Paragraph | No |
    | 8 | A Core Values moment | Paragraph | No |
    | 9 | Any disagreement, and how we sorted it out | Paragraph | No |
    | 10 | What I personally did today | Paragraph | No |
    | 11 | What needs photographing before it changes | Short answer | No |
    | 12 | Anything else | Paragraph | No |

    Question 2 uses **Kid 1 to Kid 5, not real names.** The roster is the key and
    is kept off the website. Question 1 exists because the automatic timestamp is
    when the form was *submitted*, which is not always the session it describes.

    **Settings that matter.** Under **Settings**:

    - **Collect email addresses**: **off**. You do not want children's email
      addresses in a spreadsheet, and it means no login is needed, which is what
      lets the younger kids use it at all.
    - **Allow response editing**: on, so a kid can fix a typo.
    - **Limit to 1 response**: **off** — several kids submit per session, and one
      kid may add a second note later.
    - **Responder access**: "Anyone with the link", and the form must be
      **published**. Google changed this in late 2024, and a form can look
      finished while silently refusing responses.

    **Connecting it here.** Take the published form URL, add `?embedded=true`,
    and put it in the `src` of the iframe near the top of this file.

    **The responses sheet.** On the **Responses** tab, click the Sheets icon to
    create the linked spreadsheet. Put it in the team Drive folder under `Admin/`
    and paste its link into `docs/team-links.md`, which is kept off the published
    website.

    **One thing to know about embedding it here.** This website is public, so the
    form is reachable by anyone who finds the page. For a small team site that is
    very low risk, but it does mean a stranger could submit a junk response. They
    would land as obvious rubbish in the sheet and you can delete the row. If you
    would rather not have it public at all, the form can move behind the private
    `team-links.md` page instead — the trade is one extra tap for the kids.

--8<-- "includes/abbreviations.md"
