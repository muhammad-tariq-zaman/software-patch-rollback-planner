"""Plan patch rollbacks: what can be rolled back, in what order.

Usage: python3 main.py patches.csv
CSV columns: patch_id,system,installed_date,has_snapshot,risk,
reboot_required. Risk is high, medium or low; has_snapshot and
reboot_required are yes or no. Patches with a snapshot can be
rolled back, newest first within the same risk (roll back the
newest patch first), highest risk first. Patches without a
snapshot cannot be rolled back safely and are listed separately.
"""
import argparse, csv, sys

RISK_ORDER = {"high": 0, "medium": 1, "low": 2}

def plan(rows):
    can = []
    blocked = []
    for row in rows:
        entry = (row["patch_id"].strip(), row["system"].strip(),
                 row["installed_date"].strip(),
                 row["has_snapshot"].strip().lower() == "yes",
                 row["risk"].strip().lower(),
                 row["reboot_required"].strip().lower() == "yes")
        (can if entry[3] else blocked).append(entry)
    key = lambda e: (RISK_ORDER.get(e[4], 3), _reverse_date(e[2]))
    can.sort(key=key)
    blocked.sort(key=key)
    return can, blocked

def _reverse_date(value):
    return tuple(-int(part) for part in value.split("-"))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        can, blocked = plan(list(csv.DictReader(f)))
    print("Rollback plan:")
    for index, (patch_id, system, installed, _, risk, reboot) in enumerate(can, 1):
        line = (f"{index}. {patch_id} on {system} (installed {installed}, "
                f"{risk.upper()} risk, snapshot ready")
        if reboot:
            line += ", reboot required"
        print(line + ")")
    if blocked:
        print("Cannot roll back safely (no snapshot):")
        for patch_id, system, installed, _, risk, _ in blocked:
            print(f"  {patch_id} on {system} (installed {installed}, "
                  f"{risk.upper()} risk)")
    print(f"{len(can)} patch(es) can be rolled back, {len(blocked)} cannot "
          f"(no snapshot).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
