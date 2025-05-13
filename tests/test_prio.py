from buggy_tasks.priority import train_priority_model, compute_priority


def test_prio():
    """Test the priority model training and prediction with a concrete example."""
    train_priority_model()

    result = compute_priority(["python", "work"])
    assert result == 1, f"Expected priority 1, got {result}"
