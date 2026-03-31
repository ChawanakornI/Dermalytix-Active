import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_CSV = PROJECT_ROOT / "assets" / "HAM10000_metadata"
REQUIRED_COLUMNS = (
    "lesion_id",
    "image_id",
    "dx",
    "dx_type",
    "age",
    "sex",
    "localization",
    "dataset",
)
ALLOWED_LABELS = {"akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"}
ALLOWED_SEX = {"male", "female", "unknown"}
LEAKY_COLUMNS = {
    "target",
    "label",
    "dx",
    "future_label",
    "predicted_label",
    "ground_truth",
    "diagnosis_after_followup",
    "future_visit_result",
    "post_treatment_outcome",
}


def load_rows(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_row(row: Dict[str, str]) -> Dict[str, str]:
    return {key: (value or "").strip() for key, value in row.items()}


def validate_no_feature_leakage(feature_columns: Sequence[str], forbidden_columns: Sequence[str]) -> List[str]:
    forbidden = {col.strip().lower() for col in forbidden_columns}
    return [col for col in feature_columns if col.strip().lower() in forbidden]


def build_group_split(rows: Sequence[Dict[str, str]], train_ratio: float = 0.8) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
    grouped: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["lesion_id"]].append(row)

    lesion_ids = sorted(grouped)
    split_index = int(len(lesion_ids) * train_ratio)
    train_ids = set(lesion_ids[:split_index])
    train_rows: List[Dict[str, str]] = []
    val_rows: List[Dict[str, str]] = []

    for lesion_id, group_rows in grouped.items():
        if lesion_id in train_ids:
            train_rows.extend(group_rows)
        else:
            val_rows.extend(group_rows)

    return train_rows, val_rows


def find_overlap(values_a: Iterable[str], values_b: Iterable[str]) -> List[str]:
    overlap = sorted(set(values_a) & set(values_b))
    return overlap[:10]


@pytest.fixture(scope="module")
def ham_rows() -> List[Dict[str, str]]:
    assert DATASET_CSV.exists(), f"Missing dataset file: {DATASET_CSV}"
    rows = [normalize_row(row) for row in load_rows(DATASET_CSV)]
    assert rows, "Dataset is empty"
    return rows


def test_dataset_has_required_columns(ham_rows: List[Dict[str, str]]) -> None:
    columns = set(ham_rows[0].keys())
    missing = [column for column in REQUIRED_COLUMNS if column not in columns]
    assert not missing, f"Missing required columns: {missing}"


def test_core_columns_have_no_null_or_blank_values(ham_rows: List[Dict[str, str]]) -> None:
    core_columns = ("lesion_id", "image_id", "dx", "sex", "localization", "dataset")
    invalid_cells = []

    for index, row in enumerate(ham_rows, start=2):
        for column in core_columns:
            if row.get(column, "") == "":
                invalid_cells.append((index, column))
        if len(invalid_cells) >= 10:
            break

    assert not invalid_cells, f"Found blank/null core values: {invalid_cells}"


def test_image_ids_are_unique_across_rows(ham_rows: List[Dict[str, str]]) -> None:
    counts = Counter(row["image_id"] for row in ham_rows)
    duplicates = [image_id for image_id, count in counts.items() if count > 1]
    assert not duplicates, f"Duplicate image_ids found: {duplicates[:10]}"


def test_each_image_id_looks_like_isic_identifier(ham_rows: List[Dict[str, str]]) -> None:
    invalid_ids = [
        row["image_id"]
        for row in ham_rows
        if not row["image_id"].startswith("ISIC_") or not row["image_id"][5:].isdigit()
    ]
    assert not invalid_ids, f"Unexpected image_id format: {invalid_ids[:10]}"


def test_age_and_label_values_are_in_expected_range(ham_rows: List[Dict[str, str]]) -> None:
    invalid_ages = []
    invalid_labels = []

    for index, row in enumerate(ham_rows, start=2):
        label = row["dx"].lower()
        if label not in ALLOWED_LABELS:
            invalid_labels.append((index, label))

        age_raw = row["age"]
        if not age_raw:
            continue

        try:
            age_value = float(age_raw)
        except ValueError:
            invalid_ages.append((index, age_raw))
            continue

        if not 0 <= age_value <= 120:
            invalid_ages.append((index, age_value))

    assert not invalid_labels, f"Unexpected labels found: {invalid_labels[:10]}"
    assert not invalid_ages, f"Age values out of range or invalid: {invalid_ages[:10]}"


def test_categorical_columns_are_within_expected_domain(ham_rows: List[Dict[str, str]]) -> None:
    invalid_sex = sorted({row["sex"].lower() for row in ham_rows if row["sex"].lower() not in ALLOWED_SEX})
    empty_localizations = [row["image_id"] for row in ham_rows if not row["localization"]]
    invalid_dx_type = [row["image_id"] for row in ham_rows if not row["dx_type"]]

    assert not invalid_sex, f"Unexpected sex values: {invalid_sex}"
    assert not empty_localizations, f"Missing localization for rows: {empty_localizations[:10]}"
    assert not invalid_dx_type, f"Missing dx_type for rows: {invalid_dx_type[:10]}"


def test_all_supported_classes_are_present_in_dataset(ham_rows: List[Dict[str, str]]) -> None:
    present_labels = {row["dx"].lower() for row in ham_rows}
    missing_labels = sorted(ALLOWED_LABELS - present_labels)
    assert not missing_labels, f"Dataset is missing classes: {missing_labels}"


def test_label_distribution_is_not_single_class_collapsed(ham_rows: List[Dict[str, str]]) -> None:
    counts = Counter(row["dx"].lower() for row in ham_rows)
    total = sum(counts.values())
    dominant_label, dominant_count = counts.most_common(1)[0]
    dominant_ratio = dominant_count / total
    assert dominant_ratio < 0.9, f"Dataset is too collapsed into one class: {dominant_label}={dominant_ratio:.3f}"


def test_group_based_split_prevents_lesion_leakage(ham_rows: List[Dict[str, str]]) -> None:
    train_rows, val_rows = build_group_split(ham_rows, train_ratio=0.8)
    overlapping_lesions = find_overlap(
        (row["lesion_id"] for row in train_rows),
        (row["lesion_id"] for row in val_rows),
    )
    overlapping_images = find_overlap(
        (row["image_id"] for row in train_rows),
        (row["image_id"] for row in val_rows),
    )

    assert train_rows and val_rows, "Split should produce non-empty train and validation partitions"
    assert not overlapping_lesions, f"Lesion leakage across split: {overlapping_lesions}"
    assert not overlapping_images, f"Image leakage across split: {overlapping_images}"


def test_group_split_preserves_all_rows_without_loss(ham_rows: List[Dict[str, str]]) -> None:
    train_rows, val_rows = build_group_split(ham_rows, train_ratio=0.8)
    original_images = sorted(row["image_id"] for row in ham_rows)
    split_images = sorted(row["image_id"] for row in train_rows + val_rows)
    assert split_images == original_images


def test_selected_feature_columns_do_not_include_target_or_future_information() -> None:
    selected_feature_columns = ["age", "sex", "localization", "dataset"]
    leaked = validate_no_feature_leakage(selected_feature_columns, LEAKY_COLUMNS)
    assert not leaked, f"Feature leakage detected in selected columns: {leaked}"


def test_leakage_rule_catches_direct_and_future_columns() -> None:
    bad_feature_columns = ["age", "sex", "dx", "future_label", "post_treatment_outcome"]
    leaked = validate_no_feature_leakage(bad_feature_columns, LEAKY_COLUMNS)
    assert leaked == ["dx", "future_label", "post_treatment_outcome"]
