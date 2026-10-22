import functools
import random
import sys

import pygame

WIDTH, HEIGHT = 400, 600
FPS = 60
GROUND_H = 80
GRAVITY = 0.45
FLAP_V = -7.5
PIPE_W = 70
CAP_W = 82
CAP_H = 26
PIPE_GAP = 160
PIPE_SPEED = 3
PIPE_INTERVAL = 1500  # ms
BIRD_X = 90
PX = 4  # size of one "big pixel"

SKY = (112, 197, 206)
CLOUD = (240, 250, 250)
HILL = (140, 214, 150)
HILL_DARK = (110, 190, 125)
GREEN = (116, 191, 46)
GREEN_LIGHT = (184, 232, 92)
GREEN_DARK = (60, 120, 30)
GROUND_TOP = (140, 220, 70)
DIRT = (222, 216, 149)
DIRT_DARK = (200, 180, 110)
WHITE = (255, 255, 255)
BLACK = (30, 20, 20)
RED = (230, 70, 50)
YELLOW = (250, 215, 40)
ORANGE = (240, 130, 30)

# 17x12 bird traced from the reference image, one letter per pixel.
BIRD_PALETTE = {
    "K": (0, 0, 0),         # outline, pupil
    "Y": (255, 235, 60),    # yellow body
    "D": (254, 193, 7),     # darker belly
    "W": (255, 255, 255),   # eye and wing
    "O": (253, 87, 29),     # beak
}
BIRD_SPRITE = [
    "......KKKKKK.....",
    "....KKYYYYKWK....",
    "...KYYYYYKWWWK...",
    ".KKKKYYYYKWWKWK..",
    "KWWWWKYYYKWWKWK..",
    "KWWWWWKYYYKWWWK..",
    "KYWWWYKYYYYKKKKK.",
    ".KYYYKYYYYKOOOOOK",
    "..KKKDDDDKOKKKKK.",
    "....KDDDDDKOOOOK.",
    ".....KKDDDDKKKKK.",
    ".......KKKK......",
]
BIRD_SCALE = 4


def make_bird():
    w, h = len(BIRD_SPRITE[0]), len(BIRD_SPRITE)
    surf = pygame.Surface((w * BIRD_SCALE, h * BIRD_SCALE), pygame.SRCALPHA)
    for y, row in enumerate(BIRD_SPRITE):
        for x, ch in enumerate(row):
            if ch in BIRD_PALETTE:
                pygame.draw.rect(surf, BIRD_PALETTE[ch], (x * BIRD_SCALE, y * BIRD_SCALE, BIRD_SCALE, BIRD_SCALE))
    return surf


FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "J": ["..###", "....#", "....#", "....#", "....#", "#...#", ".###."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "!": ["#", "#", "#", "#", "#", ".", "#"],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}


@functools.lru_cache(maxsize=None)
def pixel_text(text, scale, color=WHITE, shadow=(60, 60, 60), outline=BLACK):
    """Minecraft-style blocky text: 5x7 pixel letters, 1px gap, drop shadow."""
    glyphs = [FONT[ch] for ch in text.upper()]
    w = sum(len(g[0]) for g in glyphs) + len(glyphs) - 1
    mask = pygame.Surface((w, 7), pygame.SRCALPHA)
    x = 0
    for g in glyphs:
        for y, row in enumerate(g):
            for gx, c in enumerate(row):
                if c == "#":
                    mask.set_at((x + gx, y), (255, 255, 255, 255))
        x += len(g[0]) + 1
    big = pygame.transform.scale(mask, (w * scale, 7 * scale))
    m = pygame.mask.from_surface(big)
    face = m.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
    dark = m.to_surface(setcolor=shadow, unsetcolor=(0, 0, 0, 0))
    edge = m.to_surface(setcolor=outline, unsetcolor=(0, 0, 0, 0))
    pad = scale * 2
    out = pygame.Surface((big.get_width() + pad * 2, big.get_height() + pad * 2), pygame.SRCALPHA)
    o = max(1, scale // 2)
    # outline around face + shadow, then shadow, then face
    for dx in range(-o, o + 1, o):
        for dy in range(-o, o + 1, o):
            out.blit(edge, (pad + dx, pad + dy))
            out.blit(edge, (pad + scale + dx, pad + scale + dy))
    out.blit(dark, (pad + scale, pad + scale))
    out.blit(face, (pad, pad))
    return out


def make_background():
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(SKY)
    # blocky clouds
    for cx, cy in [(40, 90), (250, 60), (330, 170), (120, 230)]:
        for bx, by, bw, bh in [(0, 8, 64, 16), (12, 0, 40, 28), (24, -8, 20, 12)]:
            pygame.draw.rect(bg, CLOUD, (cx + bx, cy + by, bw, bh))
    # stepped hills
    base = HEIGHT - GROUND_H
    for i, h in enumerate([60, 90, 120, 90, 70, 100, 130, 80, 60, 90]):
        x = i * 40
        pygame.draw.rect(bg, HILL_DARK, (x, base - h - 8, 40, h + 8))
        pygame.draw.rect(bg, HILL, (x, base - h, 40, h))
    return bg


@functools.lru_cache(maxsize=None)
def make_pipe_surface(w, h, cap=False):
    """Shaded pixel pipe piece with vertical stripes."""
    s = pygame.Surface((w, h))
    s.fill(GREEN)
    pygame.draw.rect(s, GREEN_LIGHT, (PX * 2, 0, PX * 2, h))
    pygame.draw.rect(s, GREEN_DARK, (w - PX * 4, 0, PX * 3, h))
    pygame.draw.rect(s, BLACK, (0, 0, w, h), PX // 2 + 1)
    return s


class Bird:
    def __init__(self):
        self.image = make_bird()
        self.reset()

    def reset(self):
        self.y = HEIGHT / 2
        self.vel = 0.0

    def flap(self):
        self.vel = FLAP_V

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    @property
    def rect(self):
        return pygame.Rect(BIRD_X - 22, int(self.y) - 15, 44, 30)

    def draw(self, surf, now):
        angle = max(-25, min(60, -self.vel * 4))
        rotated = pygame.transform.rotate(self.image, angle)
        surf.blit(rotated, rotated.get_rect(center=(BIRD_X, int(self.y))))


class Pipe:
    def __init__(self):
        self.x = WIDTH + 10
        self.gap_y = random.randint(120, HEIGHT - GROUND_H - 120)
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED

    @property
    def rects(self):
        """(top body, top cap, bottom cap, bottom body)"""
        cap_x = self.x - (CAP_W - PIPE_W) // 2
        top_end = self.gap_y - PIPE_GAP // 2
        bot_start = self.gap_y + PIPE_GAP // 2
        floor = HEIGHT - GROUND_H
        return (
            pygame.Rect(self.x, 0, PIPE_W, top_end - CAP_H),
            pygame.Rect(cap_x, top_end - CAP_H, CAP_W, CAP_H),
            pygame.Rect(cap_x, bot_start, CAP_W, CAP_H),
            pygame.Rect(self.x, bot_start + CAP_H, PIPE_W, floor - bot_start - CAP_H),
        )

    def draw(self, surf):
        for i, r in enumerate(self.rects):
            if r.height > 0:
                surf.blit(make_pipe_surface(r.width, r.height), r)


def draw_ground(surf, offset):
    top = HEIGHT - GROUND_H
    pygame.draw.rect(surf, DIRT, (0, top, WIDTH, GROUND_H))
    pygame.draw.rect(surf, BLACK, (0, top, WIDTH, PX))
    pygame.draw.rect(surf, GROUND_TOP, (0, top + PX, WIDTH, PX * 3))
    # moving diagonal-ish stripes on the grass, as blocky steps
    for gx in range(-32, WIDTH + 32, 32):
        x = gx + offset
        pygame.draw.rect(surf, GREEN, (x, top + PX, PX * 4, PX * 3))
        pygame.draw.rect(surf, GREEN_DARK, (x + PX * 4, top + PX * 2, PX * 2, PX))
    pygame.draw.rect(surf, DIRT_DARK, (0, top + PX * 4, WIDTH, PX))
    for gx in range(-32, WIDTH + 32, 32):
        x = gx + offset
        pygame.draw.rect(surf, DIRT_DARK, (x + 8, top + PX * 8, PX * 2, PX * 2))
        pygame.draw.rect(surf, DIRT_DARK, (x + 24, top + PX * 13, PX * 2, PX * 2))


def blit_center(surf, img, center):
    surf.blit(img, img.get_rect(center=center))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    background = make_background()
    bird = Bird()

    title_flappy = pixel_text("FLAPPY", 8, YELLOW, shadow=(120, 80, 0))
    title_bird = pixel_text("BIRD", 8, (255, 170, 50), shadow=(130, 50, 0))
    t_ready = pixel_text("GET READY", 4)
    t_hint = pixel_text("SPACE / UP / CLICK", 3)
    t_over = pixel_text("GAME OVER", 6, RED, shadow=(70, 10, 10))
    t_restart = pixel_text("R / SPACE / CLICK", 3)
    t_restart2 = pixel_text("TO RESTART", 3)

    pipes = []
    score = 0
    best = 0
    state = "ready"  # ready | playing | over
    last_pipe = 0
    ground_x = 0

    def restart():
        nonlocal pipes, score, state, ground_x
        bird.reset()
        pipes = []
        score = 0
        ground_x = 0
        state = "ready"

    while True:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            action = (
                (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP))
                or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and state == "over":
                restart()
            elif action:
                if state == "ready":
                    state = "playing"
                    last_pipe = now
                    bird.flap()
                elif state == "playing":
                    bird.flap()
                elif state == "over":
                    restart()

        if state == "ready":
            bird.y = HEIGHT / 2 + 8 * pygame.math.Vector2(0, 1).rotate(now / 5).y
            ground_x = (ground_x - 1) % 32 - 32
        elif state == "playing":
            bird.update()
            if now - last_pipe > PIPE_INTERVAL:
                pipes.append(Pipe())
                last_pipe = now
            for p in pipes:
                p.update()
                if not p.scored and p.x + PIPE_W < BIRD_X - 14:
                    p.scored = True
                    score += 1
            pipes = [p for p in pipes if p.x + CAP_W > 0]
            ground_x = (ground_x - PIPE_SPEED) % 32 - 32

            brect = bird.rect
            hit_pipe = any(brect.colliderect(r) for p in pipes for r in p.rects)
            if hit_pipe or brect.bottom >= HEIGHT - GROUND_H or brect.top <= 0:
                state = "over"
                best = max(best, score)

        # draw
        screen.blit(background, (0, 0))
        for p in pipes:
            p.draw(screen)
        draw_ground(screen, ground_x)
        bird.draw(screen, now)

        if state == "ready":
            blit_center(screen, title_flappy, (WIDTH // 2, 100))
            blit_center(screen, title_bird, (WIDTH // 2, 165))
            blit_center(screen, t_ready, (WIDTH // 2, 300))
            blit_center(screen, t_hint, (WIDTH // 2, 350))
        else:
            blit_center(screen, pixel_text(str(score), 6), (WIDTH // 2, 60))

        if state == "over":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 110))
            screen.blit(overlay, (0, 0))
            blit_center(screen, t_over, (WIDTH // 2, 210))
            blit_center(screen, pixel_text(f"SCORE {score}", 4), (WIDTH // 2, 290))
            blit_center(screen, pixel_text(f"BEST {best}", 4, YELLOW, shadow=(90, 70, 0)), (WIDTH // 2, 335))
            blit_center(screen, t_restart, (WIDTH // 2, 395))
            blit_center(screen, t_restart2, (WIDTH // 2, 420))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
