# Team Fund

Working record of money in and money out. The spreadsheet version is
[`team-fund.csv`](team-fund.csv), which imports straight into Google Sheets with
the formulas intact. See below for how.

Note: this file and the CSV are **not published** to the team website. They track
what each family has paid, which is not something to put on a public page. Both
are excluded in `mkdocs.yml`.

## Where things stand

| | |
| --- | --- |
| Expected total, 5 families at $200 | **$1,000.00** |
| Recorded spend so far | **$440.23** |
| Remaining on paper, once all contributions are in | **$559.77** |
| Received so far | _fill in_ |

## Open question: the robot kits are not on this receipt

Sales order SO164149, dated 30 July 2026, itemises exactly three things:

| Line | Amount |
| --- | --- |
| `F27-Team-FLLCH-REG` — team registration | $285.00 |
| `F27-FLL-CHLNG-SET` — BIOGLOW Challenge Set | $105.00 |
| Shipping $20.00 and tax $30.23 | $50.23 |
| **Total** | **$440.23** |

There is **no SPIKE Prime set on that order.** The Challenge Set is the mat and the
mission models; it is not the robot.

The kits reportedly arrived on 8 August, so one of two things is true. Either they
were bought on a second order whose receipt has not been recorded here — in which
case the real spend is higher than $440.23 and **$200 per family may be
under-set** — or they came from a school, a sponsor or a loan and cost the team
nothing.

Worth resolving before more money is collected, because the answer changes whether
$1,000 is enough. A SPIKE Prime set is a few hundred dollars, so this is not a
rounding error.

Until it is settled, treat $440.23 as the *recorded* spend rather than the total
spend.

## Contributions

Families are listed by slot rather than name. The mapping is in
[`team-roster.md`](team-roster.md).

| Family | Slot | Expected | Received | Date | Method |
| --- | --- | --- | --- | --- | --- |
| Family 1 | Kid 1 | $200.00 | | | |
| Family 2 | Kid 2 | $200.00 | | | |
| Family 3 | Kid 3 | $200.00 | | | |
| Family 4 | Kid 4 | $200.00 | | | |
| Family 5 | Kid 5 | $200.00 | | | |
| **Total** | | **$1,000.00** | | | |

## Expenses so far

| Date | Item | Amount | Paid by | Receipt |
| --- | --- | --- | --- | --- |
| 30 Jul 2026 | Team registration (`F27-Team-FLLCH-REG`) | $285.00 | | Sales order SO164149 |
| 30 Jul 2026 | BIOGLOW Challenge Set (`F27-FLL-CHLNG-SET`) | $105.00 | | same order |
| 30 Jul 2026 | Shipping and tax | $50.23 | | $20.00 + $30.23 |
| | **Total** | **$440.23** | | |
| ? | **SPIKE Prime sets — receipt missing** | **unknown** | | See the open question below |

The three lines above are the itemised order. Keep the receipt outside the repo —
it carries a billing address, so `.gitignore` blocks it. A copy is in
`~/Documents/FLL2026-private/`.

## Still to come

Rough list, no figures yet. Fill in estimates as you price them.

| Item | How necessary | Note |
| --- | --- | --- |
| Printing the Engineering Notebook | Essential | Colour printing adds up |
| Travel to the competition | Essential | Early November |
| Competition table and border walls | Recommended | Timber, per the official Table Building Instructions. You can practise on the floor, but matches are on tables and robots behave differently. |
| Spare motors | Recommended | Medium angular motors fail most often |
| Spare LEGO parts | Recommended | Beams, pins, axles |
| Storage boxes | Recommended | Sorted parts save real time every session |
| Spare hub | Optional | A dead hub on competition day ends the season |
| Team shirts | Optional | |
| Judge handouts | Optional | A few printed copies |
| Snacks across 26 meetings | Optional | Adds up more than you would think |

If contributions fall short, the table and the spare hub are the two things to
drop first. Neither stops you competing.

## Turning the CSV into a Google Sheet

1. Go to <https://drive.google.com> and click **New**, then **File upload**.
2. Choose `docs/team-fund.csv`.
3. Right-click the uploaded file and pick **Open with**, then **Google Sheets**.
4. **File**, then **Save as Google Sheets** so it becomes editable.
5. Share it with the other parents.

The `=SUM(...)` formulas become live formulas on import, so the totals and the
summary update themselves as you fill rows in.

Two things worth doing once it is open: format the money columns as currency
(**Format**, **Number**, **Currency**), and rename the tab to something clearer
than "team-fund".

## Keeping it up to date

Whoever holds the money updates the Sheet. Keep it in the team Google Drive
folder alongside the receipts, under `Admin/`. The folder link is in
[`team-links.md`](team-links.md).

If you want the repo copy to stay accurate too, download the Sheet as CSV
occasionally (**File**, **Download**, **Comma-separated values**) and replace
`team-fund.csv`. That is optional. The Sheet can be the live version and this
file the starting point.
