"""Run reproducible reliability checks for the music recommender."""

from typing import Any, Dict, List

from src.recommender import load_songs, recommend_with_reliability


EVALUATION_CASES = (
    {
        "name": "High-Energy Pop",
        "profile": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "valence": 0.8,
            "likes_acoustic": False,
        },
        "expected_top_title": "Sunrise City",
    },
    {
        "name": "Chill Lofi",
        "profile": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.6,
            "likes_acoustic": True,
        },
        "expected_top_title": "Library Rain",
    },
    {
        "name": "Deep Intense Rock",
        "profile": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "valence": 0.45,
            "likes_acoustic": False,
        },
        "expected_top_title": "Storm Runner",
    },
)


def run_evaluation(csv_path: str = "data/songs.csv") -> List[Dict[str, Any]]:
    """Evaluate expected recommendations and one invalid-input guardrail."""
    songs = load_songs(csv_path)
    results = []

    for case in EVALUATION_CASES:
        output = recommend_with_reliability(case["profile"], songs, k=3)
        top_title = output["recommendations"][0][0]["title"]
        results.append(
            {
                "name": case["name"],
                "passed": top_title == case["expected_top_title"],
                "details": (
                    f"expected {case['expected_top_title']}; received {top_title}; "
                    f"confidence {output['reliability']['score']:.2f}"
                ),
            }
        )

    invalid_profile = {
        "genre": "pop",
        "mood": "happy",
        "energy": 1.4,
        "likes_acoustic": False,
    }
    try:
        recommend_with_reliability(invalid_profile, songs)
    except ValueError as error:
        results.append(
            {
                "name": "Invalid energy guardrail",
                "passed": "energy" in str(error),
                "details": f"rejected invalid input: {error}",
            }
        )
    else:
        results.append(
            {
                "name": "Invalid energy guardrail",
                "passed": False,
                "details": "invalid input was not rejected",
            }
        )

    return results


def main() -> None:
    """Print a compact evaluation report for reproducible project evidence."""
    results = run_evaluation()
    passed_count = sum(result["passed"] for result in results)

    print("Music Recommender Reliability Evaluation")
    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"{status}: {result['name']} - {result['details']}")
    print(f"Summary: {passed_count}/{len(results)} checks passed")


if __name__ == "__main__":
    main()
