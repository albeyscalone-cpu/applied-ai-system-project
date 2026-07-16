# Applied AI System Project: Reliable Music Recommendation Assistant

## Project Summary

This project extends my **Module 3 Music Recommender Simulation** into a more
complete applied AI system. The original project focused on a content-based
music recommender that scored songs using features like genre, mood, energy,
valence, and acousticness. It could rank songs for a user profile, explain why
they matched, and show how weight changes affected recommendation results.

For Project 4, I am using that earlier recommender as the base system and
turning it into a more professional AI assistant with stronger documentation,
architecture, evaluation, and reliability features. The applied-AI addition is
a reliability layer that validates listener profiles before scoring and reports
a confidence estimate plus clear guardrail warnings with each ranked result.

The original Module 3 goals were to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This new version will keep the original scoring and recommendation workflow, but
it will be expanded step by step into an applied AI system that is easier to
trust, test, and explain.

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
User profile -> validation guardrail -> CSV song catalog -> scoring and ranking
-> confidence assessment -> recommendations and review warnings
```

### Architecture Overview

The system first checks that profile values are valid for the catalog's 0.0 to
1.0 numeric features. It then scores each song, ranks the results, and measures
how strongly the top result is supported by the scoring signals and how far it
is from the next result. The confidence score is a ranking-quality signal, not
a claim that a person will definitely enjoy a song. Small catalogs and very
close rankings produce warnings for the user to review.

The editable Mermaid source is available in
[`diagrams/architecture.mmd`](diagrams/architecture.mmd).

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
.......                                                                  [100%]
7 passed in 0.04s
```

---

## Reproducible Execution Evidence

```text
$ python -B -m src.main
Loaded songs: 18

Input: High-Energy Pop profile
Top output: Sunrise City by Neon Echo - Score: 5.70
Ranking confidence: 0.78 (high)
Guardrail: Small catalog: results may not represent the listener's full taste.

Input: Chill Lofi profile
Top output: Library Rain by Paper Lanterns - Score: 5.75
Ranking confidence: 0.71 (high)
Guardrail: Small catalog: results may not represent the listener's full taste.
Guardrail: Close scores: the top ranking could change with small preference updates.

Input: Deep Intense Rock profile
Top output: Storm Runner by Voltline - Score: 5.72
Ranking confidence: 0.81 (high)
Guardrail: Small catalog: results may not represent the listener's full taste.

Invalid input check
Input: energy=1.4
Output: ValueError: 'energy' must be a number from 0.0 to 1.0.
```

The application also runs an energy-first experiment for the High-Energy Pop
profile. Its second-ranked result changes from `Gym Hero` to `Rooftop Lights`,
which makes the weight trade-off visible instead of hidden.

### Design Decisions

- I kept the original content-based scoring model because every score and
  explanation remains inspectable.
- I added validation at the recommendation boundary so invalid values cannot
  silently create misleading rankings.
- I used a lightweight confidence calculation based on match coverage and the
  gap between the first two results. This is easy to test and explain, but it
  intentionally does not pretend to predict a listener's real enjoyment.
- I display warnings rather than blocking valid low-confidence results, because
  a human listener should be able to review a recommendation with its limits.

### Testing Summary

The automated suite checks CSV parsing, scoring, ranking, explanations, a
weight-shift experiment, invalid input rejection, and the structure of the
reliability result. All 7 tests pass. Manual command-line runs also confirmed
that each of the three built-in profiles produces recommendations, confidence,
and at least one guardrail message without crashing.

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
outweigh genre when the numbers line up well. The confidence score only measures
support from this small scoring system; it cannot measure personal enjoyment,
data quality, or cultural fit.

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

