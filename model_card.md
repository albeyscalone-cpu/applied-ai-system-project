# Model Card: VibePulse 2.0

## 1. Model Name and Purpose

**VibePulse 2.0: Reliable Music Recommendation Assistant** extends my Module 3
Music Recommender Simulation. It is a classroom-scale, content-based
recommender that ranks songs from a small catalog using genre, mood, energy,
valence, and acousticness. Project 4 adds input validation, a confidence
assessment, guardrail warnings, and a reproducible evaluation harness.

## 2. Intended Use

The system is intended to demonstrate how a transparent recommendation system
can make and explain ranking decisions. A user provides a simple taste profile,
and the app returns songs from its local catalog with score explanations. It is
appropriate for learning, prototyping, and inspecting recommendation trade-offs.
It is not intended to make claims about a person's identity, emotional health,
or long-term music preferences.

## 3. How the System Works

For each song, VibePulse awards weighted points for matching genre and mood,
then adds points for closeness to target energy and valence and for matching the
acoustic preference. It ranks the resulting scores and shows the reasons behind
each result. Before ranking, the system rejects missing or invalid profile
values, including numeric values outside the catalog's 0.0 to 1.0 scale.

After ranking, the reliability layer calculates a confidence score from two
signals: how much of the available scoring evidence supports the top result and
how far the top score is from the next result. It also displays warnings for a
small catalog, close scores, or a top result without an exact genre or mood
match. This confidence score measures support inside this rule-based model; it
does not measure whether a human will enjoy the recommendation.

## 4. Data

The local CSV catalog contains 18 example songs with structured fields for
title, artist, genre, mood, energy, tempo, valence, danceability, and
acousticness. The catalog includes pop, lofi, rock, ambient, jazz, synthwave,
indie pop, latin, EDM, folk, hip hop, R&B, indie, and punk. It does not include
lyrics, language, popularity, cultural context, listening history, skip rates,
or feedback from real users.

## 5. Strengths

The ranking rule is inspectable: every recommendation includes the exact
matching factors that produced its score. The validation guardrail prevents
invalid feature values from producing plausible-looking output, and the
evaluation harness can repeatedly verify the expected top results for three
test profiles. In the current catalog, `Library Rain` is a strong result for the
Chill Lofi profile, while `Storm Runner` is a strong result for Deep Intense
Rock because the relevant features align closely.

## 6. Limitations and Biases

The catalog is very small and uneven, so a few tracks can dominate the top
results. The system overvalues what it can measure: numerical similarity can
outweigh genre, and the model cannot understand lyrics, vocals, culture,
language, memory, or the changing context in which someone listens to music.
For example, `Gym Hero` can rank highly for multiple profiles because its energy
and mood values are close, even where the genre does not match.

The confidence score also has an important limitation. It can be high when a
song fits the model's narrow features, even though the catalog lacks a song the
listener would prefer. Confidence therefore describes the consistency of the
scoring rule, not objective quality or personal satisfaction.

## 7. Misuse Prevention and Guardrails

The app does not collect personal listening history or infer sensitive personal
traits. It accepts only the limited, explicit preference fields used by the
local scoring rule. Invalid or out-of-range energy and valence values are
rejected with clear error messages instead of being silently adjusted.

Users should treat the output as a suggestion from a tiny sample, not as an
authoritative statement about their taste. The interface makes this visible by
displaying small-catalog and close-score warnings. A production version would
need opt-in data collection, broader catalog auditing, controls for excluding
artists or genres, and human review of potential feedback-loop effects.

## 8. Reliability Testing and Surprises

The `python -m src.evaluate` harness checks three fixed listener profiles and
one invalid-energy input. The current run passes all four checks: the expected
top songs are `Sunrise City`, `Library Rain`, and `Storm Runner`, and an energy
value of `1.4` is rejected.

The main surprise was that a high confidence score did not always mean the
ranking felt uniquely determined. The Chill Lofi profile has a high confidence
score of `0.71`, but its first two songs are close enough to trigger the
close-score warning. This showed why the confidence number needs a written
warning alongside it rather than being treated as a final answer.

## 9. AI Collaboration Reflection

I used an AI coding assistant to help structure the reliability layer, write
tests, and review the command-line output. One helpful suggestion was to reject
out-of-range profile values before scoring. That was correct because the song
features use a 0.0 to 1.0 range, and rejecting `energy=1.4` makes the failure
obvious instead of returning a misleading ranking.

One flawed suggestion was to describe a high confidence score as proof that a
listener would enjoy the top song. That interpretation was incorrect: the score
only reflects the match and margin inside this small rule-based catalog. I
corrected the wording and added guardrail messages so the app explicitly says
that confidence is about ranking support, not personal enjoyment. This project
reinforced that AI-generated code and explanations still need human checking,
especially when a number can sound more certain than it really is.

## 10. Future Work

Future versions could add a larger and more diverse catalog, artist and tempo
preferences, disliked genres, diversity constraints, and opt-in human feedback.
I would also evaluate whether explanations help users decide when to trust a
recommendation, rather than only measuring whether the expected title ranks
first.
