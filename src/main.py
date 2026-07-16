"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import DEFAULT_WEIGHTS, load_songs, recommend_with_reliability


BASE_PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.6,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "valence": 0.45,
        "likes_acoustic": False,
    },
}

EXPERIMENT_WEIGHTS = {
    "genre": 1.0,
    "energy": 2.0,
}


def print_recommendations(profile_name: str, recommendations: list[tuple], label: str) -> None:
    """Print a readable recommendation block for one profile."""
    print(f"\n{profile_name} ({label})")
    print("-" * (len(profile_name) + len(label) + 3))
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


def print_reliability(reliability: dict) -> None:
    """Print confidence as a guardrail, not as a claim of listener enjoyment."""
    print(f"Ranking confidence: {reliability['score']:.2f} ({reliability['level']})")
    for warning in reliability["warnings"]:
        print(f"Guardrail: {warning}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    print(f"Loaded songs: {len(songs)}")
    print(f"Default weights: {DEFAULT_WEIGHTS}")

    for profile_name, user_prefs in BASE_PROFILES.items():
        print(f"\nUser profile: {profile_name} -> {user_prefs}")
        result = recommend_with_reliability(user_prefs, songs, k=5)
        print_recommendations(profile_name, result["recommendations"], "base weights")
        print_reliability(result["reliability"])

    experiment_profile_name = "High-Energy Pop"
    experiment_profile = BASE_PROFILES[experiment_profile_name]
    experiment_result = recommend_with_reliability(
        experiment_profile,
        songs,
        k=5,
        weights=EXPERIMENT_WEIGHTS,
    )
    print(
        "\nExperiment: doubled energy weight and halved genre weight "
        f"for {experiment_profile_name}"
    )
    print(f"Experiment weights: {EXPERIMENT_WEIGHTS}")
    print_recommendations(
        experiment_profile_name,
        experiment_result["recommendations"],
        "energy-first experiment",
    )
    print_reliability(experiment_result["reliability"])


if __name__ == "__main__":
    main()
