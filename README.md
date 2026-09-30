# Skin Lesion Triage from Dermoscopy Images

**EXSU 500: Fundamentals of AI in Medicine, McGill University, Fall 2026**

## Problem

We classify dermoscopic images of skin lesions as **malignant or pre-malignant** (melanoma, basal cell carcinoma, actinic keratosis / intraepithelial carcinoma) or **benign** (melanocytic nevus, benign keratosis, dermatofibroma, vascular lesion). The intended use is to support triage of lesions for dermatology referral.

**Why it matters:** skin cancer is the most common cancer, and outcomes depend heavily on catching malignant lesions early. Most lesions seen in practice are benign, so a tool that flags the minority needing specialist review could reduce both missed cancers and unnecessary referrals.

**Task type:** binary image classification (supervised).

## Dataset

**HAM10000** (Human Against Machine with 10,000 training images): 10,015 dermoscopic images of 7,470 unique pigmented skin lesions, with diagnosis, age, sex and body site.

- **Source:** Harvard Dataverse, [doi:10.7910/DVN/DBW86T](https://doi.org/10.7910/DVN/DBW86T)
- **Licence:** CC BY-NC 4.0 (non-commercial use)
- **Citation:** Tschandl P, Rosendahl C, Kittler H. The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions. *Scientific Data* 5, 180161 (2018).

**Planned splits:**
- **Train / validation:** HAM10000, split at the lesion level so that images of the same lesion never appear in more than one set.
- **Held-out test:** the official ISIC 2018 Task 3 test set (1,512 images of 1,223 lesions), included in the same download. It is evaluated once, after model selection.
- **Human benchmark:** reader data from Tschandl et al. (*Nature Medicine*, 2020), also included in the download. It is used only for comparison, never for training.

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

