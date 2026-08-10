# Runs

A **run** is one trip out of Base and back, usually completing several missions
before returning.

One file per run. Copy [`_TEMPLATE.md`](_TEMPLATE.md) and name it `RX-name.md`
(e.g. `R2-cargo-line.md`), matching the SPIKE project in
[`../../code/spike-projects/`](../../code/spike-projects/README.md).

## How runs get built

1. Group missions by **field location** in [`../strategy.md`](../strategy.md) —
   the robot shouldn't cross the mat twice for the same area
2. Create a run file from the template
3. Build the attachment → [`../../robot-design/attachments/`](../../robot-design/attachments/README.md)
4. Program it, and log every test in the run file's reliability table
5. It ships when it clears **80% over 10 consecutive attempts**

## Run index

| Run | Missions | Points | Time | Attachment | Success rate | Ready? |
| --- | --- | --- | --- | --- | --- | --- |
| _TODO_ | | | | | | ☐ |

**Total run time must fit in 150 seconds**, including ~5s per attachment swap.
If it doesn't, cut the run with the worst points-per-second.

--8<-- "includes/abbreviations.md"
