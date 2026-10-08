# Skin Lesion Triage: Comparing Models and Their Calibration

**EXSU 500: Fundamentals of AI in Medicine, McGill University, Fall 2026**

## Problem

We classify dermoscopic images of skin lesions as **malignant or pre-malignant** (melanoma, basal cell carcinoma, actinic keratosis / intraepithelial carcinoma) or **benign** (melanocytic nevus, benign keratosis, dermatofibroma, vascular lesion). The intended use is to support triage of lesions for dermatology referral.

We compare three types of model:

1. A baseline using patient metadata only (age, sex, body site).
2. A classical machine learning model using hand-crafted image features.
3. A fine-tuned convolutional neural network (CNN).

The models are compared on two questions:

- **Discrimination:** how well does each model separate malignant from benign lesions? Measured with AUROC, AUPRC, and sensitivity/specificity at a stated threshold.
- **Calibration:** can its predicted probabilities be trusted? For example, do lesions given an "80% risk" turn out to be malignant about 80% of the time? Measured with reliability diagrams, Brier score, expected calibration error, and calibration slope and intercept, both before and after post-hoc recalibration.

**Why it matters:** skin cancer is the most common cancer, and outcomes depend on catching malignant lesions early. A triage tool is only useful if clinicians can act on its output. A model that ranks lesions well but reports overconfident probabilities can still push referral decisions in the wrong direction.

**Task type:** binary image classification (supervised), with calibration analysis.

## Dataset

**HAM10000** (Human Against Machine with 10,000 training images): 10,015 dermoscopic images of 7,470 unique pigmented skin lesions, with diagnosis, age, sex and body site.

- **Source:** Harvard Dataverse, [doi:10.7910/DVN/DBW86T](https://doi.org/10.7910/DVN/DBW86T)
- **Licence:** CC BY-NC 4.0 (non-commercial use)
- **Citation:** Tschandl P, Rosendahl C, Kittler H. The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions. *Scientific Data* 5, 180161 (2018).

**Planned splits:**

- **Train / validation:** HAM10000, split at the lesion level so that images of the same lesion never appear in more than one set. All tuning and recalibration use the validation set only.
- **Held-out test:** the official ISIC 2018 Task 3 test set (1,512 images of 1,223 lesions), included in the same download. It is evaluated once, after model selection.
- **Reference comparison:** reader and CNN data from Tschandl et al., *Nature Medicine* 26, 1229–1234 (2020), included in the download. These data are used only for comparison and never for training.

The data are **not** committed to this repository. Download instructions and a download script will be added here.

## Team roles

| Role | Member |
|---|---|
| Data lead | Giuliana Curcio |
| Modelling lead | Abdul Aziz Mourad |
| Interface lead | Sophie Lee |
| Writing lead | Ariel Subekti |

## Licence

Code: MIT (see `LICENSE`). Data: CC BY-NC 4.0, owned by the dataset authors and not redistributed here.

*Course prototype for research and educational purposes. Not a medical device and not for clinical use.*
