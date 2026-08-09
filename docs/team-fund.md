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
| Spent so far | **$440.23** |
| Remaining, once all contributions are in | **$559.77** |
| Received so far | _fill in_ |

The $440.23 covers team registration and the robot kit together. That is 44% of
the budget gone on the two unavoidable startup costs, which is normal and leaves
a reasonable amount for everything else.

Per family, the spend so far works out at $88.05 each.

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
| Aug 2026 | Team registration and robot kit | $440.23 | _fill in_ | |
| | **Total** | **$440.23** | | |

Worth splitting that into two lines once the receipts are to hand. If a school or
PTA ever reimburses any of it, they will ask which was which.

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

Whoever holds the money updates the Sheet. If you want the repo copy to stay
accurate too, download the Sheet as CSV occasionally (**File**, **Download**,
**Comma-separated values**) and replace `team-fund.csv`. That is optional. The
Sheet can be the live version and this file the starting point.
