# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version will simulate a small content-based music recommender. Instead of
using millions of real user actions like a streaming app, it will compare a
listener's taste profile to each song's stored features and rank the closest
matches with a clear explanation.

---

## How The System Works

Real recommendation platforms combine many signals. Collaborative filtering
looks for patterns in what similar users liked, skipped, replayed, saved, or
added to playlists. Content-based filtering looks at the item itself, such as a
song's genre, mood, tempo, energy, or acousticness. This project will focus on a
simple content-based version so the scoring rule is easy to inspect.

Each `Song` will use these features from `data/songs.csv`: title, artist, genre,
mood, energy, tempo_bpm, valence, danceability, and acousticness. The
`UserProfile` will store a favorite genre, favorite mood, target energy, and
whether the listener likes acoustic songs.

My starting algorithm recipe is:

- Add 2.0 points when the song genre matches the user's favorite genre.
- Add 1.5 points when the song mood matches the user's favorite mood.
- Add up to 1.0 point when the song's energy is close to the user's target
  energy, using `1 - abs(song_energy - target_energy)`.
- Add up to 0.75 point for valence closeness so "happy" profiles prefer brighter
  songs and moodier profiles can prefer lower-valence songs.
- Add 0.5 point when the acousticness level matches whether the user likes
  acoustic songs.
- Rank all songs from highest score to lowest score and return the top results
  with human-readable reasons.

Default taste profile for the first implementation:

```python
user_prefs = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,
    "valence": 0.8,
    "likes_acoustic": False,
}
```

Data flow sketch:

```text
CSV song catalog -> load each row -> compare every song to user_prefs
-> calculate score and reasons -> sort by score -> print top recommendations
```

Expected bias: because this is a small catalog, the system may over-favor genres
or moods that appear more often. It also cannot understand lyrics, culture,
listening context, or the way a person's taste changes over time.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

Current result:

```text
$ python -B -m pytest -q -p no:cacheprovider
....                                                                     [100%]
4 passed in 0.03s
```

---

## Sample Recommendation Output

```text
$ python -B -m src.main
Loaded songs: 18
User profile: genre=pop, mood=happy, energy=0.8, valence=0.8, likes_acoustic=False

Top recommendations:

1. Sunrise City by Neon Echo - Score: 5.70
Because: genre match (+2.00); mood match (+1.50); energy closeness (+0.98); valence closeness (+0.72); acoustic preference match (+0.50)

2. Gym Hero by Max Pulse - Score: 4.10
Because: genre match (+2.00); energy closeness (+0.87); valence closeness (+0.73); acoustic preference match (+0.50)

3. Rooftop Lights by Indigo Parade - Score: 3.70
Because: mood match (+1.50); energy closeness (+0.96); valence closeness (+0.74); acoustic preference match (+0.50)

4. Desert Bloom by Maya Sol - Score: 2.08
Because: energy closeness (+0.88); valence closeness (+0.70); acoustic preference match (+0.50)

5. Thunder Arcade by Pixel Riot - Score: 2.07
Because: energy closeness (+0.84); valence closeness (+0.73); acoustic preference match (+0.50)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



