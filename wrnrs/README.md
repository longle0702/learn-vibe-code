# First Date Deck

A small conversation card game for two people who want to break the ice, built as a single self-contained web page. Draw a card, answer out loud, and let the conversation wander.

> **Just for fun.** This is a hobby and learning project. It is not affiliated with, endorsed by, or a substitute for the original game, and it is not for sale.

## Credit

The idea and the questions come from **We're Not Really Strangers**, the card game by its original creators. All credit for the concept, the levels (Perception, Connection, Reflection) and the wildcards belongs to them. If you enjoy this, please buy the real deck.

The question lists were taken from this article: <https://ahaslides.com/blog/we-are-not-really-strangers-questions/>

I edited the lists for a first date: I removed near-duplicates, dropped questions that assume you already know each other, and rewrote a few. The question text is not my own work. If you are a rights holder and want it removed, please open an issue.

## How to play

1. Open `index.html` in any browser. There is no build step or server.
2. Pick a mode:
   - **Level 1 – Perception:** first impressions and guesses
   - **Level 2 – Connection:** values and experiences
   - **Level 3 – Reflection:** reflecting on the date and each other
   - **Mix:** every question from all levels
3. Each level also includes the shared **wildcard** challenges.
4. Tap **Next** (or press Space/Enter) to draw a card, and **Previous** (or the left arrow) to look back. A question never repeats within a mode.

Progress is saved in your browser, and **Restart all** reshuffles every deck.

## Files

- `index.html`: the whole app (data, state, rendering and a self-test). Run `runSelfTest()` in the browser console to check that every question is drawn exactly once.
- `question-sets/`: the source CSV files the questions came from.
