from src.evaluate import run_evaluation


def test_evaluation_harness_passes_all_defined_checks():
    results = run_evaluation()

    assert len(results) == 4
    assert all(result["passed"] for result in results)
    assert results[-1]["name"] == "Invalid energy guardrail"
