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
.....                                                                    [100%]
5 passed in 0.03s
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

I tested three listener profiles and one weight-shift experiment:

- `High-Energy Pop`: looked for bright, upbeat, non-acoustic songs.
- `Chill Lofi`: looked for calm, acoustic, low-energy songs.
- `Deep Intense Rock`: looked for intense, high-energy songs with darker valence.
- `Energy-first experiment`: doubled energy weight and cut genre weight in half.

```text
High-Energy Pop (base weights)
1. Sunrise City by Neon Echo - Score: 5.70
2. Gym Hero by Max Pulse - Score: 4.10
3. Rooftop Lights by Indigo Parade - Score: 3.70
4. Desert Bloom by Maya Sol - Score: 2.08
5. Thunder Arcade by Pixel Riot - Score: 2.07
```

```text
Chill Lofi (base weights)
1. Library Rain by Paper Lanterns - Score: 5.75
2. Midnight Coding by LoRoom - Score: 5.65
3. Focus Flow by LoRoom - Score: 4.19
4. Spacewalk Thoughts by Orbit Bloom - Score: 3.64
5. Quiet Pines by North Window - Score: 2.17
```

```text
Deep Intense Rock (base weights)
1. Storm Runner by Voltline - Score: 5.72
2. Gym Hero by Max Pulse - Score: 3.48
3. Garage Sparks by Voltline - Score: 2.17
4. Subway Static by Concrete Verse - Score: 2.09
5. Night Drive Loop by Neon Echo - Score: 2.07
```

```text
High-Energy Pop (energy-first experiment)
1. Sunrise City by Neon Echo - Score: 5.68
2. Rooftop Lights by Indigo Parade - Score: 4.66
3. Gym Hero by Max Pulse - Score: 3.97
4. Subway Static by Concrete Verse - Score: 3.00
5. Desert Bloom by Maya Sol - Score: 2.96
```

The experiment made the system care more about raw energy than exact genre. That
shift pushed `Rooftop Lights` above `Gym Hero`, which felt reasonable because it
has almost the same energy and valence as the target profile even without the
same genre label.

---

## Limitations and Risks

This recommender still has a tiny catalog, so one or two strong matches can
dominate the results. It also only understands structured features like genre,
mood, energy, valence, and acousticness, not lyrics, context, or the listener's
real behavior over time. During testing, I also noticed that a song like `Gym
Hero` can rank high for very different profiles because energy and mood can
outweigh genre when the numbers line up well.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project helped me see how recommendation systems turn a small set of
features into something that feels like a prediction. Even with a tiny dataset,
the scoring rules were enough to make the top recommendation often feel
reasonable, especially when the profile had a clear genre and mood target. It
also made the connection between feature design and output much more obvious to
me than when I use a polished real app.

The biggest lesson about bias was how easy it is for the system to overvalue the
features it can measure. My recommender does not know anything about lyrics,
memory, cultural context, or why a user likes a song, so it can over-rank
tracks that merely share similar energy and valence. Building and testing the
weight-shift experiment made that limitation feel very concrete.

