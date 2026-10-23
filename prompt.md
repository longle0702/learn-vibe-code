Build a single-page web app prototype called "First Date Deck": a conversation card game that helps two people break the ice on a first date. Output ONE self-contained file, index.html, with inline CSS and vanilla JavaScript. No frameworks, no build step, no backend, no external requests except optionally one Google Font.

## Modes
Four modes, each with its own independent question pool:
- Level 1 – Perception (light): first impressions and guesses
- Level 2 – Connection (medium): values and experiences
- Level 3 – Reflection (deep): reflecting on the date and each other
- Mix: all questions from levels 1–3 combined in one pool

## Data
Define const QUESTIONS = [{ id, level, text }, ...] at the top of the script using the list at the end of this prompt. Ids are unique (L1-01 … L3-10). Build each pool from this array, so adding a question only means adding a line.

## State (in memory, mirrored to localStorage under key "fdd-state" inside try/catch; app must work if storage throws)
- currentMode: 1 | 2 | 3 | 'mix' | null
- remaining: { 1: [ids], 2: [ids], 3: [ids], mix: [ids] }
- history:   { 1: [ids], 2: [ids], 3: [ids], mix: [ids] }
- viewIndex: position in history[currentMode] being viewed

## Business rules
1. Start screen: title, one-line explanation, four mode cards showing "shown / total". Level 1 is visually suggested but any mode can be chosen.
2. Next question: pick uniformly at random from remaining[currentMode] (Math.random index into the remaining array), remove it, push to history, display it. Never pick from history, so no repeat can occur within a mode.
3. Show progress "7 / 10" for the current mode.
4. When remaining[currentMode] becomes empty, keep the last question on screen and replace the Next button with a "Level complete" panel:
   - Level 1 or 2: primary "Move to Level N+1", secondary "Replay this level" (refill + reshuffle only this pool), and "Back to levels".
   - Level 3: primary "Try Mix", secondary "Replay Level 3", "Back to levels".
   - Mix: "Reshuffle Mix", "Back to levels".
5. Users can switch mode anytime via a header control; each mode keeps its progress and resumes where it left off.
6. In Mix, each card shows a small badge with the question's original level.
7. "Previous" steps back through history for viewing only (never returns a question to the pool); "Next" from a past card first returns to the newest card, then draws.
8. "Restart all" in the header asks for confirmation, then refills every pool and clears history.
9. Edge cases: a mode with 0 questions is disabled ("No questions yet"); disable Next during the card transition to prevent double draws; drop duplicate ids with a console warning.

## UI
- Mobile-first, works at 360 px wide, centred card max ~480 px on desktop.
- One large question card in the centre, big readable type (~24–28 px) so both people can read it across a table.
- Each level has its own accent colour (e.g. warm red for L1, deep rose for L2, dark plum for L3, gradient for Mix); support prefers-color-scheme dark.
- Subtle card flip or slide animation on each draw; respect prefers-reduced-motion.
- Tap targets ≥ 44 px, buttons with visible focus states, aria-live="polite" on the question text.
- Keyboard: Space/Enter = next, Left arrow = previous.
- Do not use the name or branding of any existing card game.

## Code quality
Clear sections: data, state, pure functions (draw, reset, complete-check), rendering, event wiring. Add a small self-test function runSelfTest() (call from console) that draws every question in each mode and asserts each id appears exactly once.