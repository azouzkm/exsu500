import numpy as np

from src.eval.metrics import calibration_metrics, discrimination_metrics


def test_perfect_separation_gives_auroc_and_auprc_of_one():
    y_true = [0, 0, 0, 1, 1, 1]
    y_prob = [0.01, 0.02, 0.1, 0.9, 0.95, 0.99]
    disc = discrimination_metrics(y_true, y_prob, threshold=0.5)
    assert disc.auroc == 1.0
    assert disc.auprc == 1.0
    assert disc.sensitivity == 1.0
    assert disc.specificity == 1.0


def test_discrimination_metrics_respect_threshold():
    y_true = [0, 0, 1, 1]
    y_prob = [0.3, 0.6, 0.4, 0.7]
    low = discrimination_metrics(y_true, y_prob, threshold=0.2)
    high = discrimination_metrics(y_true, y_prob, threshold=0.8)
    assert low.sensitivity == 1.0
    assert low.specificity == 0.0
    assert high.sensitivity == 0.0
    assert high.specificity == 1.0


def test_well_calibrated_predictions_have_low_ece_and_brier():
    rng = np.random.default_rng(0)
    y_prob = rng.uniform(0, 1, size=5000)
    y_true = (rng.uniform(0, 1, size=5000) < y_prob).astype(int)

    calib = calibration_metrics(y_true, y_prob, n_bins=10)
    assert calib.ece < 0.05
    assert calib.brier_score < 0.3
    assert 0.5 < calib.calibration_slope < 1.5
    assert abs(calib.calibration_intercept) < 0.3


def test_overconfident_predictions_have_high_ece():
    # Always predicts near-certainty in the wrong direction half the time.
    y_true = [0, 0, 0, 0, 1, 1, 1, 1]
    y_prob = [0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]
    calib = calibration_metrics(y_true, y_prob, n_bins=10)
    assert calib.ece > 0.4
