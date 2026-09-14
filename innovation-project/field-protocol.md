# Field Protocol — counting bees in your garden

Print this. Take it outside with you.

Or use the [**Bee Field Log**](field-log.html) on a phone, which does the same job
with a timer built in and exports a spreadsheet at the end. Paper still works when
the battery does not, so take both the first few times.

The whole project depends on every count being done **the same way**. If one
person watches for ten minutes on a hot morning and someone else watches for five
minutes on a cool evening, the two numbers cannot be compared and the experiment
is wasted. The rules below are the experiment.

## Before you start: mark your patch

Pick one patch of flowers, about **50 cm by 50 cm**, and mark the corners so you
find exactly the same patch every time. Photograph it on day one.

You count bees **visiting this patch**, and nothing else. A bee flying past does
not count. A bee on a flower outside the markers does not count.

## The count

| Rule | Why |
| --- | --- |
| **10 minutes**, timed | Same effort every time |
| Between **10:00 and 15:00** | When most bees are active |
| Only if it is **warm, bright and not windy** | Cold, dull or windy days give near-zero counts whatever you did to the garden |
| Same patch, same markers | You are comparing like with like |
| Record the date, start time, temperature and weather | Without these the number means nothing |

Photograph every bee that lands on a flower in the patch. Take more photos than
you think you need — most will be blurry, and you only need one usable shot per
type.

**Do not catch, trap or kill anything.** The standard scientific method uses bowls
of soapy water that drown the bees. We are not doing that, on purpose, and it is
worth being able to say why.

## Sorting what you photographed

Here is the honest part: **you will not be able to name most of these to species.**
Many native bees can only be told apart under a microscope by a specialist. That
is normal and it does not spoil the experiment.

Instead, sort your photos into **types that look different**. Scientists call these
morphospecies and it is a real, published method.

Sort on things you can actually see:

- **Size** — smaller than a grain of rice, honeybee-sized, bigger than a honeybee
- **Colour** — black, brown, metallic green, striped, orange
- **Hairiness** — furry all over, shiny and almost bald
- **Stripes** — where they are and how many
- **Where it carries pollen** — back legs, under the belly, nowhere visible

Two photos go in the same pile only if you cannot see a difference. Give each pile
a number and a nickname, keep one clear photo as the reference, and use the same
piles every week.

**Your headline number is how many piles you have.** That is the diversity
measure.

### Is it even a bee?

Hoverflies are very good at looking like bees. Two quick checks:

- **Wings:** bees have four, flies have two
- **Antennae:** bees have long obvious ones, hoverflies have tiny stubby ones
- **Eyes:** hoverfly eyes are huge and take up most of the head

Keep a "not sure" pile. Do not force it.

### Honeybees go in their own pile, and are not part of the score

Honeybees are kept livestock and are not what we are trying to help. Count them,
write the number down, but keep them **out** of the diversity total. A garden that
gained six honeybees and no new wild types has not succeeded.

## Free tools worth using

- **iNaturalist** — upload a photo and the community plus its AI suggest an
  identification. Often gets you to a group rather than a species, which is fine.
  It also puts your record into a real database that scientists use.
- **Seek** (same people) — identifies from your phone camera without posting.

Use these to *label* your piles where you can. Do not let a wrong confident
label overwrite what you actually saw.

## Recording sheet

Copy this per count.

| Field | Value |
| --- | --- |
| Who counted | Kid _ |
| Date | |
| Start time | |
| Temperature | |
| Weather (sun / cloud / wind) | |
| Garden and patch | |
| Before or after the change? | |

| Pile # | Nickname | How many seen | Photo reference |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

| Total | Value |
| --- | --- |
| **Number of different piles (wild bees only)** | |
| Honeybees seen (recorded separately) | |
| Not-sure photos | |

## The Bee Field Log app

[**Open the field log**](field-log.html) — works on a phone, and works with no
signal once the page has loaded.

It walks through the same five steps as this sheet: session details, weather
check, one card per observation, the running tally, and quick ID help. There is a
ten-minute timer so nobody has to watch a clock.

| Thing | How it behaves |
| --- | --- |
| Where the data lives | In the browser on that phone, until you send it |
| Names | **First name only**, for observer and recorder |
| Getting the data out | **Download CSV**, or **Send to team sheet** |
| Photos | Shrunk to about 100 KB, kept with the record, and sent to a private Drive folder |
| Clearing it | **Clear all**, which warns you about anything not yet sent |

Precisely, it is browser **localStorage**, under two keys: `op_recs` for the
observations and `op_sess` for the session details. That storage belongs to one
website address on one browser on one phone. So:

- A different phone has a different log.
- Safari and Chrome on the same phone have different logs.
- The copy you test at `127.0.0.1` is not the copy on the real website.
- Private or incognito browsing throws it away when you close the tab.

There is about 5 MB of room in total. Photos are shrunk on the way in to protect
that, and if it ever does fill up the log says so and tells you to export, rather
than quietly failing to save.

### Sending it to the team sheet

**Send to team sheet** puts every record into one Google Sheet the coach owns, so
five phones in five gardens end up as one table.

It is deliberately a button, not automatic. The log works with no signal, and
uploading is what you do when you get back to wifi. Records that have gone up are
marked `sent`, so pressing it twice does not duplicate anything.

**Photos go too.** Each one lands in a Drive folder and the sheet's photo column
gets a link to it. Click the link to see the bee.

That folder is **private on purpose**. A garden photo can catch somebody in the
background, and pictures of children stay off anything public. Share the folder by
hand with whoever needs it. Making it public would let the sheet show thumbnails
in the cells, which is nicer to look at and not worth it.

Records go up four at a time. A phone on weak wifi drops one big request but
usually manages small ones, and if it stops halfway the records that arrived are
marked sent. Press it again and it picks up where it left off.

This follows the same idea as the
[after-class notes](../docs/after-class-notes.md): the coach owns the data, the
kids need no login, and the setup lives in the repo as a script rather than as
clicks somebody has to remember.

**It needs setting up once**, by a grown-up, before the button does anything. The
instructions are at the top of
[`tools/create-field-log-sheet.gs`](https://github.com/amana4/FLL2026/blob/main/tools/create-field-log-sheet.gs).
Roughly: run the script to make the sheet and the photo folder, deploy it as a web
app, paste the address into `field-log.html`. Until that is done the button says so
and points you at Download CSV.

**Export before you clear, and export the same day.** Browser storage is not a
backup, and neither is a button you have not pressed yet. The CSV is the copy that
is definitely yours.

Two people, two jobs: one watches and calls it out, one types. The log has a field
for each, because the Robot Design and Core Values rubrics both reward being able
to say who did what.

### Two things to know before you rely on it

**Open the page before you leave the house.** Once loaded it runs with no signal,
but it cannot load itself from nothing. The only thing it fetches is the fonts, so
on a weak signal it will look plain and work fine.

**Each phone keeps its own separate log.** There is no shared pile. If three people
count in three gardens, that is three CSV files, and somebody has to put them
together. Decide who, before the first count.

Once the CSVs are out, the numbers go into [`research.md`](research.md).

## The schedule that makes this an experiment

1. **Count before you change anything.** At least three counts on different days,
   so you know what a normal day looks like. One count is not a baseline.
2. **Make one change**, and only one. Write down exactly what and when.
3. **Keep counting**, same rules, same patch.
4. **Compare.** Did the number of piles go up?

Three counts before and three after, per garden, is the minimum worth presenting.
Five is better.

## Where the numbers go

Into [`research.md`](research.md) as the data record, and the story of what
changed into [`solution.md`](solution.md). Photograph your patch on day one and
again at the end — a before-and-after pair of the *garden* is as convincing to
judges as the bee count itself.

--8<-- "includes/abbreviations.md"
