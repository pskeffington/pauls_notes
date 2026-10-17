"""G4 protocol negative controls: stage remains synthetic and unexecuted."""
import copy
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "check_survival_protocol.py"
spec = importlib.util.spec_from_file_location("g4_protocol_checker", SOURCE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class SurvivalProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = checker.load_contract()
        cls.protocol = checker.PROTOCOL.read_text(encoding="utf-8")
        cls.dictionary = checker.DICTIONARY.read_text(encoding="utf-8")

    def inspect(self, contract=None, protocol=None, dictionary=None):
        return checker.validate(
            self.contract if contract is None else contract,
            self.protocol if protocol is None else protocol,
            self.dictionary if dictionary is None else dictionary,
        )

    def test_clean_frozen_contract_and_zero_execution_claims(self):
        self.assertEqual(self.inspect(), [])
        self.assertEqual(self.contract["lifecycle"], "protocol_only_not_executed")
        self.assertTrue(self.contract["synthetic_only"])
        self.assertFalse(self.contract["real_cancer_data_admitted"])

    def test_rejects_patient_or_clinical_admission(self):
        item = copy.deepcopy(self.contract)
        item["data_source"] = "actual_patient_records"
        item["clinical_use_authorized"] = True
        item["real_cancer_data_admitted"] = True
        self.assertTrue(any("research-only" in x for x in self.inspect(item)))

    def test_survival_event_cannot_become_specimen_label(self):
        item = copy.deepcopy(self.contract)
        item["endpoint"]["event_code"] = 0
        item["endpoint"]["horizon_months"] = 12
        item["endpoint"]["fictional_event"] = "verified clinical recurrence"
        problems = self.inspect(item)
        self.assertTrue(any("endpoint changed" in x for x in problems))
        self.assertTrue(any("verified recurrence" in x for x in problems))

    def test_held_out_reserve_and_disjoint_people_are_frozen(self):
        item = copy.deepcopy(self.contract)
        item["partition"]["reserved_people"] = 0
        item["partition"]["outer_folds"] = 5
        item["partition"]["reserved_policy"] = "scan reserved endpoints"
        problems = self.inspect(item)
        self.assertTrue(any("allocation changed" in x for x in problems))
        self.assertTrue(any("reserve protection changed" in x for x in problems))

    def test_censoring_and_brier_cannot_be_labeled_naive_accuracy(self):
        item = copy.deepcopy(self.contract)
        item["estimators"]["censor"]["train_only"] = False
        item["estimators"]["censor"]["positivity_threshold_at_horizon"] = 0
        item["evaluation"]["censored_early"] = "treat as event free"
        item["evaluation"]["event_term"] = "ordinary binary Brier"
        problems = self.inspect(item)
        self.assertTrue(any("censoring model changed" in x for x in problems))
        self.assertTrue(any("Brier assessment" in x for x in problems))

    def test_cox_score_is_not_an_absolute_survival_probability(self):
        item = copy.deepcopy(self.contract)
        item["estimators"]["cox"]["prediction"] = "predict(fit, type='lp')"
        item["estimators"]["cox"]["formula"] = "Surv(time_months, event) ~ marker"
        self.assertTrue(any("Cox training-only" in x for x in self.inspect(item)))

    def test_rejects_extra_data_column_and_missing_features(self):
        item = copy.deepcopy(self.contract)
        item["observation_schema"].append(
            {"name": "patient_barcode", "type": "synthetic_unique_id",
             "missing": "prohibited", "validation": "do not allow"}
        )
        item["generator"]["missingness"] = "mean imputed"
        problems = self.inspect(item)
        self.assertTrue(any("exactly five" in x for x in problems))
        self.assertTrue(any("generator field changed" in x for x in problems))

    def test_negative_calibration_and_failure_record_gates(self):
        item = copy.deepcopy(self.contract)
        item["evaluation"]["calibration"]["bin_edges"] = [0, .5, 1]
        item["quality_gates"]["negative_cases"].remove(
            "censored-before-horizon mislabeled as event-free"
        )
        problems = self.inspect(item)
        self.assertTrue(any("calibration bins" in x for x in problems))
        self.assertTrue(any("Adversarial survival" in x for x in problems))

    def test_text_evidence_and_lifecycle_cannot_overclaim_execution(self):
        item = copy.deepcopy(self.contract)
        item["lifecycle"] = "accepted_clinical_survival_fits"
        self.assertTrue(any("Unexecuted protocol" in x for x in self.inspect(item)))
        changed = self.protocol.replace("IPCW_Brier(24)", "accuracy_score")
        self.assertTrue(any("Protocol narrative absent" in x for x in self.inspect(protocol=changed)))
        changed = self.dictionary.replace("S001...S240", "real patient barcodes")
        self.assertTrue(any("dictionary incomplete" in x for x in self.inspect(dictionary=changed)))


if __name__ == "__main__":
    unittest.main()
