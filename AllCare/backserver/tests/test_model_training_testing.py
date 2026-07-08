import random
from typing import Dict, List, Tuple

import numpy as np
import pytest

torch = pytest.importorskip("torch")
nn = pytest.importorskip("torch.nn")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def build_toy_dataset() -> Tuple[torch.Tensor, torch.Tensor]:
    features = torch.tensor(
        [
            [-2.0, -1.0],
            [-1.8, -1.2],
            [-1.5, -0.9],
            [-1.2, -0.7],
            [1.0, 1.1],
            [1.3, 1.0],
            [1.7, 1.4],
            [2.1, 2.0],
        ],
        dtype=torch.float32,
    )
    labels = torch.tensor([0, 0, 0, 0, 1, 1, 1, 1], dtype=torch.long)
    return features, labels


def train_linear_classifier(seed: int, epochs: int = 150, learning_rate: float = 0.1) -> Dict[str, object]:
    set_seed(seed)
    model = nn.Linear(2, 2)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    features, labels = build_toy_dataset()
    losses: List[float] = []
    gradient_norms: List[float] = []

    initial_state = {name: tensor.detach().clone() for name, tensor in model.state_dict().items()}

    for _ in range(epochs):
        optimizer.zero_grad()
        logits = model(features)
        loss = loss_fn(logits, labels)
        loss.backward()

        total_norm_sq = 0.0
        for parameter in model.parameters():
            if parameter.grad is not None:
                grad_norm = float(parameter.grad.detach().norm().item())
                total_norm_sq += grad_norm ** 2
        gradient_norms.append(total_norm_sq ** 0.5)

        optimizer.step()
        losses.append(float(loss.item()))

    with torch.no_grad():
        final_logits = model(features)
        predictions = final_logits.argmax(dim=1)
        accuracy = float((predictions == labels).float().mean().item())

    return {
        "model": model,
        "losses": losses,
        "accuracy": accuracy,
        "features": features,
        "labels": labels,
        "initial_state": initial_state,
        "gradient_norms": gradient_norms,
    }


def test_training_loss_decreases_materially() -> None:
    result = train_linear_classifier(seed=7, epochs=100)
    losses = result["losses"]
    assert losses[-1] < losses[0], f"Expected loss to decrease, got {losses[0]} -> {losses[-1]}"
    assert min(losses[-10:]) <= min(losses[:10]), "Loss should improve by the end of training"


def test_model_can_overfit_a_tiny_dataset() -> None:
    result = train_linear_classifier(seed=11, epochs=200)
    assert result["accuracy"] >= 0.99, f"Sanity check failed, tiny-set accuracy={result['accuracy']:.3f}"


def test_training_is_reproducible_with_fixed_seed() -> None:
    result_a = train_linear_classifier(seed=123, epochs=100)
    result_b = train_linear_classifier(seed=123, epochs=100)

    for params_a, params_b in zip(result_a["model"].parameters(), result_b["model"].parameters()):
        assert torch.allclose(params_a, params_b), "Model weights differ with the same seed"

    assert result_a["losses"] == pytest.approx(result_b["losses"])
    assert result_a["accuracy"] == pytest.approx(result_b["accuracy"])


def test_different_seed_changes_learned_weights() -> None:
    result_a = train_linear_classifier(seed=1, epochs=50)
    result_b = train_linear_classifier(seed=2, epochs=50)

    parameter_equalities = [
        torch.allclose(params_a, params_b)
        for params_a, params_b in zip(result_a["model"].parameters(), result_b["model"].parameters())
    ]
    assert not all(parameter_equalities), "Different seeds should not end with identical weights"


def test_weights_are_updated_from_initial_state() -> None:
    result = train_linear_classifier(seed=33, epochs=80)
    model = result["model"]
    initial_state = result["initial_state"]

    updated = False
    for name, tensor in model.state_dict().items():
        if not torch.allclose(tensor, initial_state[name]):
            updated = True
            break

    assert updated, "Training should update at least one parameter tensor"


def test_gradients_remain_finite_during_training() -> None:
    result = train_linear_classifier(seed=21, epochs=120)
    gradient_norms = result["gradient_norms"]

    assert gradient_norms, "Expected recorded gradient norms"
    assert all(np.isfinite(norm) for norm in gradient_norms), f"Non-finite gradient norms found: {gradient_norms}"
    assert max(gradient_norms) > 0, "All gradients are zero; model may not be learning"


def test_final_predictions_match_expected_classes() -> None:
    result = train_linear_classifier(seed=44, epochs=150)
    model = result["model"]
    features = result["features"]
    labels = result["labels"]

    with torch.no_grad():
        predictions = model(features).argmax(dim=1)

    assert torch.equal(predictions, labels), "Tiny sanity dataset should be perfectly memorized"
