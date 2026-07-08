import statistics
import time
from typing import Dict, Iterable, List

import pytest


LABELS = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]


def fake_predict(probabilities: List[float]) -> Dict[str, object]:
    ranked = sorted(
        (
            {"label": label, "confidence": float(confidence)}
            for label, confidence in zip(LABELS, probabilities)
        ),
        key=lambda item: item["confidence"],
        reverse=True,
    )
    return {"predictions": ranked}


def average(values: Iterable[float]) -> float:
    values = list(values)
    return sum(values) / len(values)


def simple_mean_drift(train_values: List[float], production_values: List[float]) -> float:
    return abs(average(train_values) - average(production_values))


def std_drift(train_values: List[float], production_values: List[float]) -> float:
    return abs(statistics.pstdev(train_values) - statistics.pstdev(production_values))


def top_k_labels(predictions: List[Dict[str, float]], k: int) -> List[str]:
    return [item["label"] for item in predictions[:k]]


def test_inference_latency_stays_under_threshold() -> None:
    started_at = time.perf_counter()
    fake_predict([0.01, 0.03, 0.06, 0.05, 0.70, 0.10, 0.05])
    latency_ms = (time.perf_counter() - started_at) * 1000
    assert latency_ms < 100, f"Inference is too slow: {latency_ms:.2f} ms"


def test_prediction_output_shape_and_probability_budget_are_valid() -> None:
    result = fake_predict([0.01, 0.03, 0.06, 0.05, 0.70, 0.10, 0.05])
    predictions = result["predictions"]

    assert len(predictions) == 7
    assert [item["label"] for item in predictions] == ["mel", "nv", "bkl", "df", "vasc", "bcc", "akiec"]
    assert sum(item["confidence"] for item in predictions) == pytest.approx(1.0)
    assert all(0.0 <= item["confidence"] <= 1.0 for item in predictions)


def test_prediction_output_is_sorted_by_confidence_descending() -> None:
    result = fake_predict([0.15, 0.10, 0.05, 0.25, 0.20, 0.15, 0.10])
    confidences = [item["confidence"] for item in result["predictions"]]
    assert confidences == sorted(confidences, reverse=True)


def test_top_k_predictions_are_stable() -> None:
    result = fake_predict([0.01, 0.03, 0.06, 0.05, 0.70, 0.10, 0.05])
    assert top_k_labels(result["predictions"], 3) == ["mel", "nv", "bkl"]


def test_output_payload_size_matches_number_of_classes() -> None:
    result = fake_predict([0.20, 0.10, 0.15, 0.05, 0.30, 0.10, 0.10])
    payload = result["predictions"]
    assert len(payload) == len(LABELS)
    assert {item["label"] for item in payload} == set(LABELS)


def test_data_drift_is_flagged_when_mean_distribution_moves() -> None:
    training_confidences = [0.12, 0.15, 0.14, 0.18, 0.16]
    production_confidences = [0.70, 0.72, 0.69, 0.75, 0.73]
    drift_score = simple_mean_drift(training_confidences, production_confidences)
    assert drift_score > 0.20


def test_data_drift_is_small_when_production_matches_training_profile() -> None:
    training_confidences = [0.12, 0.15, 0.14, 0.18, 0.16]
    production_confidences = [0.13, 0.16, 0.14, 0.17, 0.15]
    drift_score = simple_mean_drift(training_confidences, production_confidences)
    assert drift_score < 0.05


def test_variance_shift_is_detected_in_production_scores() -> None:
    training_confidences = [0.40, 0.41, 0.39, 0.42, 0.40]
    production_confidences = [0.10, 0.90, 0.15, 0.85, 0.50]
    assert std_drift(training_confidences, production_confidences) > 0.15
