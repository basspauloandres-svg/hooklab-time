import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mie_core.measurement_calibration_engine import (  # noqa: E402
    beat_f_measure,
    categorical_agreement,
    execute,
    numeric_agreement,
)


perfect = categorical_agreement([
    {"ratings": ["PRESENT", "PRESENT"]},
    {"ratings": ["ABSENT", "ABSENT"]},
    {"ratings": ["PRESENT", "PRESENT"]},
    {"ratings": ["UNRESOLVED", "UNRESOLVED"]},
])
assert perfect["raw_agreement"] == 1
assert perfect["krippendorff_alpha_nominal"] == 1

imperfect = categorical_agreement([
    {"ratings": ["PRESENT", "ABSENT"]},
    {"ratings": ["ABSENT", "ABSENT"]},
    {"ratings": ["PRESENT", "PRESENT"]},
])
assert 0 <= imperfect["raw_agreement"] < 1
assert imperfect["krippendorff_alpha_nominal"] < 1

numeric = numeric_agreement([
    {"reference": 1, "estimate": 1.1},
    {"reference": 2, "estimate": 2.1},
    {"reference": 3, "estimate": 3.1},
    {"reference": 4, "estimate": 4.1},
])
assert math.isclose(numeric["spearman_rho"], 1.0)
assert math.isclose(numeric["median_absolute_error"], 0.1, abs_tol=1e-9)
assert math.isclose(numeric["p90_absolute_error"], 0.1, abs_tol=1e-9)

beat = beat_f_measure([0, 1, 2, 3], [0.01, 0.99, 2.03, 3.02])
assert beat["f_measure"] == 1
assert beat["tolerance_seconds"] == 0.07

report = execute({"mode": "NUMERIC_REFERENCE_COMPARISON", "pairs": [{"reference": 1, "estimate": 1}]})
assert report["calibration_executed"] is True
assert report["association_test_executed"] is False
assert report["conditioned_deduction_created"] is False
assert report["scientific_d_unlocked"] is False

blocked = execute({"mode": "INFER_SUCCESS_FROM_LITERATURE"})
assert blocked["status"] == "AUDIT_UNSUPPORTED_CALIBRATION_MODE"
assert blocked["calibration_executed"] is False
assert blocked["scientific_d_unlocked"] is False

print("MEASUREMENT_CALIBRATION_ENGINE_PASS")
