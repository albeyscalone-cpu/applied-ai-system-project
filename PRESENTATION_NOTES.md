# Project 4 Presentation Notes

Use this file as a 5-7 minute presentation guide. It is written to be read
directly, so no slides or video are required for the project evidence.

## Before Presenting

Open a terminal in this repository and run these commands if you want a live
text-only demonstration:

```bash
python -B -m pytest -q -p no:cacheprovider
python -B -m src.evaluate
python -B -m src.main
```

Expected checks: `8 passed` from pytest and `4/4 checks passed` from the
evaluation script.

## Speaking Script

### 0:00-0:45 - Introduction

My Project 4 system is VibePulse 2.0, a reliable music recommendation
assistant. It extends my earlier Module 3 Music Recommender Simulation. The
original project used a small content-based algorithm to rank songs based on a
listener's genre, mood, energy, valence, and acoustic preferences.

For this final project, I focused on making that original recommender easier to
trust and easier to test. I added validation, confidence information, guardrail
warnings, automated evaluation, and professional documentation.

### 0:45-1:45 - What the System Does

The user provides a taste profile. The system loads 18 songs from a local CSV
catalog and compares every song to that profile. Genre and mood matches add
points, while energy and valence contribute based on how close they are to the
target. The system ranks the songs and explains why each song received its
score.

The key Project 4 addition is the reliability layer. It checks that the input
is valid before a ranking is created. For example, an energy value must be a
number from 0.0 to 1.0. After ranking, the app reports confidence and warnings
when the catalog is small or the top scores are close together.

### 1:45-2:30 - Architecture

The architecture is documented in `diagrams/architecture.mmd`. The user profile
passes through input validation while the CSV catalog feeds the scorer. The
system then ranks songs, assesses confidence and warnings, and produces output
for human review. The diagram also shows the separate evaluation harness using
predefined profiles and producing a pass-or-fail report. Invalid input goes to a
clear error message instead of producing a misleading recommendation.

### 2:30-3:45 - Live Text Demo

Run `python -B -m src.main`.

For the High-Energy Pop profile, the top result is `Sunrise City` with a score
of 5.70 and confidence 0.78. The app also says that the catalog is small, so the
recommendation should be treated as a suggestion rather than a complete picture
of the listener's taste.

For the Chill Lofi profile, `Library Rain` is the top result. It has high
confidence, but the app still warns that the first two scores are close. This is
important because a confidence number should not hide uncertainty.

For the Deep Intense Rock profile, `Storm Runner` is the top result. The output
shows exactly which features matched, so the user can inspect the decision.

### 3:45-4:45 - Reliability Evaluation

Run `python -B -m src.evaluate`.

This evaluation checks that the three fixed profiles return their expected top
song: `Sunrise City`, `Library Rain`, and `Storm Runner`. It also sends an
invalid profile with `energy=1.4`. The system rejects that value with a clear
error. The current evaluation result is 4 out of 4 checks passed.

Then mention that `pytest` runs 8 automated tests. Those tests cover CSV
loading, scoring, ranking, explanations, the weight-shift experiment, invalid
input handling, reliability data, and the evaluation harness.

### 4:45-5:45 - Limitations and Responsible AI

This system is transparent, but it has major limits. Its catalog has only 18
songs and the system only sees a few numeric features. It cannot understand
lyrics, cultural context, real listening history, or why a person connects with
a song.

The confidence score is also limited. It measures how strongly the rule-based
model supports the ranking, not whether a person will enjoy the song. That is
why the interface includes warnings and why I documented the limitations and
misuse prevention in `model_card.md`.

### 5:45-6:30 - Conclusion

The main lesson from this project was that an AI system needs more than an
answer. It needs clear inputs, understandable reasons, testing, and honest
limits. This project shows that I can take a simple prototype and improve it
into a more reliable, documented, and testable applied AI system.

## Quick File Guide

- `README.md`: project overview, setup, architecture, sample outputs, and test evidence.
- `src/recommender.py`: ranking, input validation, confidence, and guardrails.
- `src/evaluate.py`: reproducible 4-check reliability evaluation.
- `tests/`: automated tests.
- `diagrams/architecture.mmd`: editable Mermaid architecture diagram.
- `model_card.md`: responsible-AI limitations, safeguards, and reflection.

## Portfolio Artifact

GitHub repository: https://github.com/albeyscalone-cpu/applied-ai-system-project

Portfolio reflection: This project shows that I can build an understandable
applied AI system, test its behavior with repeatable checks, and communicate its
limits instead of treating a confident-looking output as unquestionable.
