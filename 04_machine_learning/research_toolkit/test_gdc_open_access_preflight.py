"""Offline tests: no network and no patient identifiers."""
import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).with_name("gdc_open_access_preflight.py")
spec = importlib.util.spec_from_file_location("gdc_gate", SOURCE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
A = "00000000-0000-4000-8000-000000000001"
B = "00000000-0000-4000-8000-000000000002"

def record(file_id=A, access="open", project="TCGA-BRCA",
           data_type="Gene Expression Quantification"):
    return {"file_id": file_id, "access": access, "data_type": data_type,
            "file_size": 120, "md5sum": "a" * 32,
            "cases": [{"project": {"project_id": project}}]}

class GdcPreflightTests(unittest.TestCase):
    def test_open_access_metadata_only(self):
        report = gate.preflight([A, B], fetch=lambda fid: record(fid))
        self.assertEqual(report["file_count"], 2)
        self.assertFalse(report["download_performed"])
        self.assertNotIn(A, str(report))
        self.assertNotIn(B, str(report))

    def test_fail_closed_on_controlled_or_wrong_source(self):
        for variant in ({"access": "controlled"}, {"access": None},
                        {"project": "TCGA-LUAD"}, {"project": None},
                        {"data_type": "Aligned Reads"}, {"file_id": B}):
            with self.subTest(variant=variant), self.assertRaises(ValueError):
                gate.validate_metadata(record(**variant), A)

    def test_strict_identity_and_hash(self):
        for invalid in ("TCGA-AB-0001", "../GDC", "not-a-uuid", ""):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                gate.checked_uuid(invalid)
        with self.assertRaises(ValueError):
            gate.preflight([A, A], fetch=lambda fid: record(fid))
        broken = record()
        del broken["md5sum"]
        with self.assertRaises(ValueError):
            gate.validate_metadata(broken, A)

if __name__ == "__main__":
    unittest.main()
