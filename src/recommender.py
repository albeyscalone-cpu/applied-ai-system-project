import csv
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Tuple

NUMERIC_FIELDS = {
    "energy",
    "tempo_bpm",
    "valence",
    "danceability",
    "acousticness",
}

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.5
ENERGY_WEIGHT = 1.0
VALENCE_WEIGHT = 0.75
ACOUSTIC_WEIGHT = 0.5

DEFAULT_WEIGHTS = {
    "genre": GENRE_WEIGHT,
    "mood": MOOD_WEIGHT,
    "energy": ENERGY_WEIGHT,
    "valence": VALENCE_WEIGHT,
    "acoustic": ACOUSTIC_WEIGHT,
}

MAX_SCORE = sum(DEFAULT_WEIGHTS.values())

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def validate_user_preferences(user_prefs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and normalize a profile before using it to rank songs.

    The recommender is intentionally limited to values that can be compared to
    the 0.0-1.0 song features in the catalog. Raising a clear error prevents a
    plausible-looking recommendation from being produced from invalid input.
    """
    if not isinstance(user_prefs, dict):
        raise ValueError("User preferences must be provided as a dictionary.")

    normalized = user_prefs.copy()
    for field in ("genre", "mood"):
        value = normalized.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"'{field}' must be a non-empty string.")
        normalized[field] = value.strip().lower()

    for field, default in (("energy", None), ("valence", 0.5)):
        value = normalized.get(field, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"'{field}' must be a number from 0.0 to 1.0.")
        if not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"'{field}' must be a number from 0.0 to 1.0.")
        normalized[field] = float(value)

    likes_acoustic = normalized.get("likes_acoustic", False)
    if not isinstance(likes_acoustic, bool):
        raise ValueError("'likes_acoustic' must be true or false.")
    normalized["likes_acoustic"] = likes_acoustic
    return normalized


def assess_reliability(
    recommendations: List[Tuple[Dict, float, str]],
    catalog_size: int,
) -> Dict[str, Any]:
    """Estimate recommendation confidence and return review warnings.

    Confidence is based on the top score's coverage of the available scoring
    signals and its margin over the next result. It describes ranking certainty,
    not whether a listener will personally enjoy the song.
    """
    if not recommendations:
        return {
            "score": 0.0,
            "level": "low",
            "warnings": ["No recommendations were available from the catalog."],
        }

    top_score = recommendations[0][1]
    next_score = recommendations[1][1] if len(recommendations) > 1 else 0.0
    score_coverage = top_score / MAX_SCORE
    score_margin = max(0.0, top_score - next_score) / MAX_SCORE
    confidence = round(min(1.0, 0.7 * score_coverage + 0.3 * score_margin), 2)
    level = "high" if confidence >= 0.7 else "medium" if confidence >= 0.45 else "low"

    warnings = []
    if catalog_size < 25:
        warnings.append("Small catalog: results may not represent the listener's full taste.")
    if score_margin < 0.05:
        warnings.append("Close scores: the top ranking could change with small preference updates.")
    if "genre match" not in recommendations[0][2] and "mood match" not in recommendations[0][2]:
        warnings.append("Top result has no exact genre or mood match; review before relying on it.")

    return {"score": confidence, "level": level, "warnings": warnings}

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top songs for a user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "valence": 0.8,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            score, _ = score_song(user_prefs, asdict(song))
            scored.append((song, score))
        return [song for song, _ in sorted(scored, key=lambda item: item[1], reverse=True)[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain how one song scored for a user profile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "valence": 0.8,
            "likes_acoustic": user.likes_acoustic,
        }
        score, reasons = score_song(user_prefs, asdict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            row["id"] = int(row["id"])
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(
    user_prefs: Dict,
    song: Dict,
    weights: Dict[str, float] | None = None,
) -> Tuple[float, List[str]]:
    """Score one song against user preferences and explain the score."""
    user_prefs = validate_user_preferences(user_prefs)
    active_weights = DEFAULT_WEIGHTS.copy()
    if weights:
        active_weights.update(weights)

    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs["genre"].lower():
        score += active_weights["genre"]
        reasons.append(f"genre match (+{active_weights['genre']:.2f})")

    if song["mood"].lower() == user_prefs["mood"].lower():
        score += active_weights["mood"]
        reasons.append(f"mood match (+{active_weights['mood']:.2f})")

    energy_score = max(0.0, 1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_score * active_weights["energy"]
    reasons.append(f"energy closeness (+{energy_score * active_weights['energy']:.2f})")

    target_valence = user_prefs.get("valence", 0.5)
    valence_score = max(0.0, 1 - abs(song["valence"] - target_valence))
    score += valence_score * active_weights["valence"]
    reasons.append(f"valence closeness (+{valence_score * active_weights['valence']:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_match = song["acousticness"] >= 0.5 if likes_acoustic else song["acousticness"] < 0.5
    if acoustic_match:
        score += active_weights["acoustic"]
        reasons.append(f"acoustic preference match (+{active_weights['acoustic']:.2f})")

    return round(score, 2), reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Dict[str, float] | None = None,
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k ranked recommendations."""
    user_prefs = validate_user_preferences(user_prefs)
    if not isinstance(k, int) or k < 1:
        raise ValueError("'k' must be a positive integer.")

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        scored.append((song, score, "; ".join(reasons)))

    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


def recommend_with_reliability(
    user_prefs: Dict[str, Any],
    songs: List[Dict],
    k: int = 5,
    weights: Dict[str, float] | None = None,
) -> Dict[str, Any]:
    """Return recommendations together with a guardrail-based assessment."""
    recommendations = recommend_songs(user_prefs, songs, k=k, weights=weights)
    return {
        "recommendations": recommendations,
        "reliability": assess_reliability(recommendations, catalog_size=len(songs)),
    }
