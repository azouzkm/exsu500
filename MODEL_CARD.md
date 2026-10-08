# Model Card

**Status:** draft, covers the best model built so far (model 2 of 3). Will
be updated once the CNN (model 3) is built and the three are compared on
the held-out test set.

## Model details

- **Name:** `classical_ml` (`src/models/classical_ml.py`)
- **Type:** `HistGradientBoostingClassifier` (scikit-learn gradient-boosted
  trees) over 20 hand-crafted dermoscopic image features (shape, color,
  texture; see `src/features/handcrafted.py`).
- **Version:** trained from `data/features/{train,val}.csv`, commit
  `d84cebc` on branch `modelling/mourad`.

## Intended use

Research/educational prototype for the EXSU 500 course project. Intended
to illustrate and compare triage-support approaches for flagging
dermoscopic images of skin lesions as malignant/pre-malignant vs. benign,
**not** to make or support real clinical decisions.

**This is not a medical device and must not be used for clinical care.**

## Training data

HAM10000 training split: 8,488 images of 6,349 lesions (lesion-level
split, see `data/splits/train.csv`), sourced from the Harvard Dataverse
record [doi:10.7910/DVN/DBW86T](https://doi.org/10.7910/DVN/DBW86T).
Labels are binarized from the 7-class `dx` diagnosis (malignant/
pre-malignant: melanoma, basal cell carcinoma, actinic keratosis;
benign: nevus, benign keratosis, dermatofibroma, vascular lesion; see
`src/data/labels.py`). Features are extracted automatically (no manual
lesion annotation used) per image, from a lesion region found by Otsu
thresholding rather than ground-truth segmentation.

## Evaluation data

HAM10000 validation split: 1,527 images of 1,121 lesions
(`data/splits/val.csv`), disjoint from training at the lesion level. The
official ISIC 2018 Task 3 test set (1,512 images) is held out and has not
been used for any decision about this model yet.

## Metrics (validation set, 95% bootstrap CI, threshold 0.5)

| Metric | Value |
|---|---|
| AUROC | 0.840 [0.818, 0.862] |
| AUPRC | 0.555 [0.502, 0.616] |
| Sensitivity | 0.747 [0.697, 0.799] |
| Specificity | 0.730 [0.708, 0.756] |
| Brier score | 0.160 [calibration not yet recalibrated] |
| Expected calibration error | 0.163 |

Full metrics, including per-feature permutation importance, are in
`reports/classical_ml/metrics.json`.

## Known limitations

- **Calibration is poor out of the box.** The reliability diagram
  (`reports/classical_ml/reliability_diagram.png`) shows systematic
  overconfidence: predicted probabilities run well above the observed
  malignancy rate. This traces to `class_weight="balanced"` shifting
  predictions away from the true base rate. Post-hoc recalibration
  (planned, not yet implemented) is needed before any probability output
  should be trusted at face value.
- **Lesion segmentation is automatic and approximate** (~0.64 mean IoU
  against the real HAM10000 masks on a small validation sample, not
  pixel-accurate). Feature quality, and therefore predictions, will
  degrade on images where this simple Otsu-threshold segmentation finds
  the wrong region (e.g. very low-contrast lesions, heavy hair/ruler
  artifacts).
- **Dataset provenance and population.** HAM10000 draws from a limited
  set of academic dermatology clinics in Austria and Australia. Skin tone
  distribution, imaging equipment, and patient demographics are not
  representative of the general population; performance on populations
  or imaging conditions outside this distribution is unknown and not
  validated here.
- **Threshold is not clinically derived.** 0.5 is the default operating
  point for reporting; it has not been chosen to optimise any specific
  clinical trade-off (e.g. minimum acceptable sensitivity for a referral
  pathway).
- **Not yet evaluated against the held-out test set**, so these numbers
  may not generalise; they are a validation-set estimate only.

## Populations this model should not be used on

Any real patient, in any clinical or non-clinical setting. As a research
prototype it has not been validated on populations outside HAM10000's
source clinics, on skin tones underrepresented in that dataset, on
pediatric patients, or on images taken with equipment/protocols
different from HAM10000's.
