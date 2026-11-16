# software-patch-rollback-planner

Plan patch rollbacks: what can be rolled back, in what order — the input CSV lists patch_id, system, installed_date, has_snapshot (yes/no), risk (high/medium/low) and reboot_required (yes/no). Patches with a snapshot can be rolled back, highest risk first and newest first within the same risk (roll back the newest patch first); patches without a snapshot cannot be rolled back safely and are listed separately.

Sample input is included (sample.csv with five patches).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
Rollback plan:
1. KB5034441 on WS-01 (installed 2026-11-10, HIGH risk, snapshot ready, reboot required)
2. KB5034437 on WS-04 (installed 2026-11-07, HIGH risk, snapshot ready)
3. KB5034439 on SRV-DB01 (installed 2026-11-08, MEDIUM risk, snapshot ready)
4. KB5034438 on WS-03 (installed 2026-11-11, LOW risk, snapshot ready, reboot required)
Cannot roll back safely (no snapshot):
  KB5034440 on WS-02 (installed 2026-11-09, HIGH risk)
4 patch(es) can be rolled back, 1 cannot (no snapshot).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
