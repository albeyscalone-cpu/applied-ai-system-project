from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_with_reliability,
    recommend_songs,
    score_song,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_converts_csv_numbers():
    songs = load_songs("data/songs.csv")

    assert len(songs) == 18
    assert isinstance(songs[0]["id"], int)
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)


def test_score_song_returns_score_and_reasons():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "likes_acoustic": False,
    }
    song = load_songs("data/songs.csv")[0]

    score, reasons = score_song(user_prefs, song)
    recommendations = recommend_songs(user_prefs, [song], k=1)

    assert score > 0
    assert "genre match" in "; ".join(reasons)
    assert recommendations[0][0]["title"] == "Sunrise City"


def test_custom_weights_shift_high_energy_pop_order():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "likes_acoustic": False,
    }
    songs = load_songs("data/songs.csv")

    baseline = recommend_songs(user_prefs, songs, k=3)
    experiment = recommend_songs(
        user_prefs,
        songs,
        k=3,
        weights={"genre": 1.0, "energy": 2.0},
    )

    assert baseline[1][0]["title"] == "Gym Hero"
    assert experiment[1][0]["title"] == "Rooftop Lights"


def test_invalid_preference_energy_is_rejected():
    songs = load_songs("data/songs.csv")
    invalid_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 1.4,
        "likes_acoustic": False,
    }

    try:
        recommend_songs(invalid_prefs, songs)
    except ValueError as error:
        assert "energy" in str(error)
    else:
        raise AssertionError("Invalid energy values should be rejected.")


def test_reliability_result_includes_confidence_and_guardrails():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "likes_acoustic": False,
    }
    result = recommend_with_reliability(user_prefs, load_songs("data/songs.csv"), k=3)

    assert len(result["recommendations"]) == 3
    assert 0.0 <= result["reliability"]["score"] <= 1.0
    assert result["reliability"]["level"] in {"low", "medium", "high"}
    assert result["reliability"]["warnings"]
