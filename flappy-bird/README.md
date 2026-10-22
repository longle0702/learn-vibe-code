# Flappy Bird (8-bit edition)

A Flappy Bird clone written in Python with [pygame-ce](https://pyga.me/). Fly the bird through the gaps in the pipes, and don't touch anything.

## How to play

| Action | Control |
| --- | --- |
| Flap / start the game | `Space`, `Up arrow`, or left mouse click |
| Restart after Game Over | `R`, `Space`, or left mouse click |
| Quit | `Esc` or close the window |

- Each pipe pair you pass is worth 1 point.
- You lose if you hit a pipe, the ground, or the top of the screen.
- A **Game Over** screen shows your score and your best score for this session.

## Run it

Requires Python 3. From inside this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

On macOS/Linux, use `.venv/bin/python` instead of `.\.venv\Scripts\python.exe`.

## Visual style

The game uses an 8-bit / pixel-art look. Everything is drawn in code, so there are no image or font files to download.

- **Bird:** a 12x9 pixel sprite stored as text maps, enlarged with hard edges. The wing changes position (up, middle, down) as the bird rises and falls, and the bird tilts in the direction it is moving.
- **Pipes:** flat green blocks with a light stripe, a dark stripe, a black outline, and a wider cap at the open end.
- **Background:** blocky clouds and stepped green hills, drawn once and reused every frame.
- **Ground:** a grass and dirt strip that scrolls while you play.
- **Text:** a hand-made 5x7 pixel font in the style of Minecraft's. Each letter is built from square blocks, with a dark offset drop shadow and a thin black outline so it stays readable on the bright sky.
  - Supported characters: `A-Z`, `0-9`, `/`, `!` and space. Any other character needs a new glyph added to `FONT` in `main.py` first.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | The whole game: sprites, pixel font, game loop |
| `requirements.txt` | Python dependency (`pygame-ce`) |

## Tweaking the game

The values at the top of `main.py` control how the game feels:

- `GRAVITY` and `FLAP_V`: how fast the bird falls and how hard it flaps
- `PIPE_GAP`: the size of the opening (bigger is easier)
- `PIPE_SPEED` and `PIPE_INTERVAL`: how fast pipes move and how often they appear
