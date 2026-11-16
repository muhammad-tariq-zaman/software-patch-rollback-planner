import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import plan

def row(patch_id, system, installed, snapshot, risk, reboot="no"):
    return {"patch_id": patch_id, "system": system, "installed_date": installed,
            "has_snapshot": snapshot, "risk": risk, "reboot_required": reboot}

class TestRollbackPlanner(unittest.TestCase):
    def test_high_risk_first(self):
        can, _ = plan([row("KB1", "WS-01", "2026-11-08", "yes", "low"),
                       row("KB2", "WS-02", "2026-11-08", "yes", "high")])
        self.assertEqual(can[0][0], "KB2")

    def test_newest_first_within_risk(self):
        can, _ = plan([row("KB1", "WS-01", "2026-11-07", "yes", "high"),
                       row("KB2", "WS-02", "2026-11-10", "yes", "high")])
        self.assertEqual([c[0] for c in can], ["KB2", "KB1"])

    def test_no_snapshot_is_blocked(self):
        can, blocked = plan([row("KB1", "WS-01", "2026-11-09", "no", "high"),
                             row("KB2", "WS-02", "2026-11-09", "yes", "high")])
        self.assertEqual([c[0] for c in can], ["KB2"])
        self.assertEqual([b[0] for b in blocked], ["KB1"])

    def test_empty_input(self):
        self.assertEqual(plan([]), ([], []))
