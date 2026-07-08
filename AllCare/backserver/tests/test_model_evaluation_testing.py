from collections import Counter
from typing import Dict, List

import pytest


def accuracy_score(y_true: List[int], y_pred: List[int]) -> float:
    correct = sum(int(a == b) for a, b in zip(y_true, y_pred))
    return correct / len(y_true)


def precision_recall_f1_for_positive_class(y_true: List[int], y_pred: List[int], positive_label: int = 1):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == positive_label and yp == positive_label)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != positive_label and yp == positive_label)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == positive_label and yp != positive_label)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return precision, recall, f1


def binary_auc(y_true: List[int], y_score: List[float]) -> float:
    positives = [score for truth, score in zip(y_true, y_score) if truth == 1]
    negatives = [score for truth, score in zip(y_true, y_score) if truth == 0]
    wins = 0.0

    for positive in positives:
        for negative in negatives:
            if positive > negative:
                wins += 1.0
            elif positive == negative:
                wins += 0.5

    return wins / (len(positives) * len(negatives))


def confusion_matrix(y_true: List[int], y_pred: List[int], labels: List[int]) -> List[List[int]]:
    label_to_index = {label: idx for idx, label in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]
    for truth, pred in zip(y_true, y_pred):
        matrix[label_to_index[truth]][label_to_index[pred]] += 1
    return matrix


def slice_accuracy(y_true: List[int], y_pred: List[int]) -> Dict[int, float]:
    per_class_counts: Dict[int, List[int]] = {}
    for truth, pred in zip(y_true, y_pred):
        per_class_counts.setdefault(truth, []).append(int(truth == pred))
    return {label: sum(values) / len(values) for label, values in per_class_counts.items()}


def macro_average(values: Dict[int, float]) -> float:
    return sum(values.values()) / len(values)


def test_evaluation_metrics_are_computed_correctly() -> None:
    y_true = [0, 1, 1, 0, 1, 0]
    y_pred = [0, 1, 0, 0, 1, 1]
    y_score = [0.10, 0.95, 0.45, 0.30, 0.90, 0.70]

    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1 = precision_recall_f1_for_positive_class(y_true, y_pred)
    auc = binary_auc(y_true, y_score)

    assert accuracy == pytest.approx(4 / 6)
    assert precision == pytest.approx(2 / 3)
    assert recall == pytest.approx(2 / 3)
    assert f1 == pytest.approx(2 / 3)
    assert auc == pytest.approx(8 / 9)


def test_candidate_model_beats_multiple_baselines() -> None:
    candidate_metrics = {"accuracy": 0.83, "precision": 0.79, "recall": 0.81, "auc": 0.90}
    baseline_metrics = {"accuracy": 0.50, "precision": 0.45, "recall": 0.44, "auc": 0.61}

    assert candidate_metrics["accuracy"] > baseline_metrics["accuracy"]
    assert candidate_metrics["precision"] > baseline_metrics["precision"]
    assert candidate_metrics["recall"] > baseline_metrics["recall"]
    assert candidate_metrics["auc"] > baseline_metrics["auc"]


def test_confusion_matrix_shape_and_counts_are_consistent() -> None:
    y_true = [0, 0, 1, 1, 2, 2]
    y_pred = [0, 1, 1, 1, 2, 0]
    labels = [0, 1, 2]
    matrix = confusion_matrix(y_true, y_pred, labels)

    assert len(matrix) == 3
    assert all(len(row) == 3 for row in matrix)
    assert sum(sum(row) for row in matrix) == len(y_true)
    assert matrix == [[1, 1, 0], [0, 2, 0], [1, 0, 1]]


def test_metrics_are_reported_per_data_slice() -> None:
    y_true = [0, 0, 1, 1, 2, 2]
    y_pred = [0, 1, 1, 1, 2, 0]
    per_class = slice_accuracy(y_true, y_pred)

    assert per_class[0] == pytest.approx(0.5)
    assert per_class[1] == pytest.approx(1.0)
    assert per_class[2] == pytest.approx(0.5)
    assert set(per_class.keys()) == {0, 1, 2}


def test_macro_average_catches_slice_regressions() -> None:
    per_class_scores = {0: 0.95, 1: 0.96, 2: 0.40}
    macro_score = macro_average(per_class_scores)
    assert macro_score == pytest.approx((0.95 + 0.96 + 0.40) / 3)
    assert macro_score < 0.8, "Macro score should expose poor minority-class performance"


def test_prediction_and_ground_truth_lengths_must_match() -> None:
    y_true = [0, 1, 1]
    y_pred = [0, 1]
    assert len(y_true) != len(y_pred)


def test_slice_support_is_visible_for_each_class() -> None:
    y_true = [0, 0, 1, 1, 2, 2, 2]
    support = Counter(y_true)
    assert support == {0: 2, 1: 2, 2: 3}
