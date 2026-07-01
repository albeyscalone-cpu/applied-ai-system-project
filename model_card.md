# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibePulse 1.0**

---

## 2. Intended Use  

This recommender is designed to generate classroom-style music suggestions based
on a small set of song features. It assumes the user can be described by a few
simple preferences such as favorite genre, favorite mood, target energy, target
valence, and whether they like acoustic songs. It is meant for learning how a
ranking system works, not for real production users.

---

## 3. How the Model Works  

The model looks at each song one at a time and compares it to the listener
profile. It checks whether the genre matches, whether the mood matches, how
close the song's energy is to the user's target energy, how close the valence
is to the user's target valence, and whether the song's acousticness fits the
user's acoustic preference. Each of those checks adds points to a total score.
After every song gets a score, the system sorts the list from highest to lowest
and returns the top results with plain-language reasons. Compared with the
starter code, I implemented the CSV loader, the scoring logic, the ranking
function, explanation strings, and a way to test alternative weights.

---

## 4. Data  

The catalog contains 18 songs. It includes genres like pop, lofi, rock,
ambient, jazz, synthwave, indie pop, latin, edm, folk, hip hop, rnb, indie,
and punk. I expanded the starter dataset so there would be more variety in mood
and genre testing. Even with that expansion, the data still leaves out a lot of
real musical taste, including lyrics, language, popularity, social context,
repeat listening behavior, and how taste changes over time.

---

## 5. Strengths  

The system works best when a listener's preferences line up clearly with the
catalog. The `Chill Lofi` profile produced results that felt very reasonable:
`Library Rain`, `Midnight Coding`, and `Focus Flow` all matched the expected
genre, calmer energy range, and acoustic feel. The `Deep Intense Rock` profile
also behaved well at the top of the list because `Storm Runner` strongly matched
genre, mood, and energy at the same time.

---

## 6. Limitations and Bias 

This recommender can over-reward numerical similarity even when the genre is not
especially close. For example, `Gym Hero` stayed near the top for both
`High-Energy Pop` and `Deep Intense Rock` because its energy and mood values fit
both profiles well enough to overcome the genre mismatch. The catalog is also
small and uneven, so lofi and pop songs have an advantage simply because there
are more close neighbors for those tastes. It does not consider lyrics, vocals,
language, listening history, or context, so it can miss why two songs with
similar numbers might feel completely different to a human listener.

---

## 7. Evaluation  

I tested three profiles: `High-Energy Pop`, `Chill Lofi`, and `Deep Intense
Rock`. I checked whether the top recommendations changed in a way that matched
the target vibe instead of returning the same few songs every time. The most
interesting result was that the top song usually made sense, but the second and
third recommendations sometimes crossed genre boundaries if their energy and
valence were close enough. I also ran a small experiment where I doubled the
energy weight and cut the genre weight in half. That changed the `High-Energy
Pop` ranking by moving `Rooftop Lights` above `Gym Hero`, which showed that the
system is quite sensitive to the weight choices.

---

## 8. Future Work  

If I kept building this, I would add more user preference fields such as tempo
range, favorite artists, and disliked genres. I would also add a diversity rule
so the top five recommendations do not cluster around one artist or one narrow
sound. Another improvement would be better explanations that compare one song
against another instead of only listing score reasons for a single track.

---

## 9. Personal Reflection  

My biggest takeaway was that a recommender can feel convincing even when the
logic behind it is pretty small. A few weighted comparisons were enough to make
the top result often feel plausible, which helped me understand why
recommendation apps can seem smart even when they are simplifying a lot. What
surprised me most was how sensitive the output was to weight changes. Small
adjustments to genre or energy could move songs around quickly, which made the
system feel less objective than it first appeared.

Working on this also changed how I think about real music apps. I now pay more
attention to the possibility that a platform is reinforcing one narrow version
of my taste because of the features it chose to measure. AI tools helped me move
faster when implementing and testing ideas, but I still had to verify the
results carefully and decide whether the rankings actually made sense.
