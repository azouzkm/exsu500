"""Build the train/validation/test splits for the HAM10000 binary
malignancy task, declared once before any model is trained.

- Train/validation come from HAM10000_metadata.csv, split at the LESION
  level (GroupShuffleSplit on lesion_id) so images of the same lesion never
  appear in more than one split.
- Test is the official ISIC 2018 Task 3 test set, read from its
  ground-truth CSV and touched only at final evaluation.

Usage:
    python -m src.data.make_splits \\
        --metadata data/raw/HAM10000_metadata.csv \\
        --test-ground-truth data/raw/ISIC2018_Task3_Test_GroundTruth.csv \\
        --out data/splits --val-size 0.15 --seed 42
"""
import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

from src.data.labels import ALL_CLASSES, dx_to_binary

OUTPUT_COLUMNS = ["image_id", "lesion_id", "dx", "label", "split"]


def load_train_val_metadata(metadata_path: Path) -> pd.DataFrame:
    df = pd.read_csv(metadata_path)
    required = {"lesion_id", "image_id", "dx"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{metadata_path} is missing expected columns: {missing}")
    df["label"] = df["dx"].map(dx_to_binary)
    return df


def split_train_val(df: pd.DataFrame, val_size: float, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    splitter = GroupShuffleSplit(n_splits=1, test_size=val_size, random_state=seed)
    train_idx, val_idx = next(splitter.split(df, groups=df["lesion_id"]))
    train_df = df.iloc[train_idx].copy()
    val_df = df.iloc[val_idx].copy()

    overlap = set(train_df["lesion_id"]) & set(val_df["lesion_id"])
    assert not overlap, f"Lesion-level leakage between train and val: {overlap}"

    train_df["split"] = "train"
    val_df["split"] = "val"
    return train_df, val_df


def load_test_ground_truth(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    class_cols = [c for c in df.columns if c.lower() in ALL_CLASSES]
    if not class_cols:
        raise ValueError(
            f"{path}: expected one-hot diagnosis columns (one per class in "
            f"{sorted(ALL_CLASSES)}), found columns {list(df.columns)}"
        )
    image_col = "image" if "image" in df.columns else df.columns[0]
    df = df.rename(columns={image_col: "image_id"})
    df["dx"] = df[class_cols].idxmax(axis=1).str.lower()
    df["label"] = df["dx"].map(dx_to_binary)
    df["lesion_id"] = pd.NA  # not provided for the official test set
    df["split"] = "test"
    return df[OUTPUT_COLUMNS]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--test-ground-truth", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=Path("data/splits"))
    parser.add_argument("--val-size", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    df = load_train_val_metadata(args.metadata)
    train_df, val_df = split_train_val(df, args.val_size, args.seed)

    train_df[OUTPUT_COLUMNS].to_csv(args.out / "train.csv", index=False)
    val_df[OUTPUT_COLUMNS].to_csv(args.out / "val.csv", index=False)
    print(f"train: {len(train_df):5d} images, {train_df['lesion_id'].nunique():5d} lesions")
    print(f"val:   {len(val_df):5d} images, {val_df['lesion_id'].nunique():5d} lesions")

    if args.test_ground_truth is not None:
        test_df = load_test_ground_truth(args.test_ground_truth)
        test_df.to_csv(args.out / "test.csv", index=False)
        print(f"test:  {len(test_df):5d} images (official ISIC 2018 Task 3 test set)")
    else:
        print("No --test-ground-truth given; test.csv not written.")


if __name__ == "__main__":
    main()
