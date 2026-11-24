#!/usr/bin/env python3
"""Render the title cards of the post-x video (segments A, B, D).

Every frame is drawn fresh here with PIL — no stock footage, no
hand-made video. The gameplay frames come from the real game
(game.html?t=<ms> screenshots); the end card is make.fun's own file
from the press pack, used as-is. Run from the repo root:

    python3 scripts/make_frames.py

Writes PNGs to frames/cards/.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG = (5, 5, 16)
CYAN = (57, 213, 255)
MAGENTA = (196, 28, 131)
WHITE = (255, 255, 255)
DIM = (160, 165, 190)
GREEN = (86, 220, 130)

SANS = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
SANS_B = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
MONO = '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf'
MONO_B = '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'

OUT = os.path.join(os.path.dirname(__file__), '..', '..', 'frames', 'cards')
os.makedirs(OUT, exist_ok=True)


def canvas():
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    # faint starfield, fixed pattern
    for i, (x, y) in enumerate([(137, 91), (411, 203), (1660, 120), (1801, 640),
                                (95, 880), (1500, 950), (720, 60), (980, 1000),
                                (1850, 300), (300, 500), (1200, 200), (60, 300)]):
        r = 2 if i % 3 else 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=(120, 140, 180))
    return im, d


def label(d, text, x, y, size=34, color=MAGENTA, font=SANS_B):
    d.text((x, y), text, font=ImageFont.truetype(font, size), fill=color)


def prompt_frames():
    """Segment A — the one prompt, typed word by word."""
    lines = [
        'Build a tiny browser game: NEON DODGE.',
        'A little neon ship dodges falling meteors —',
        'steer with arrow keys, each dodge scores a point,',
        'one hit ends the run, Space restarts.',
        'Dark space, glowing ship, score top-left.',
    ]
    for step in range(len(lines) + 1):
        im, d = canvas()
        label(d, 'THE PROMPT  ·  one prompt, that is all', 120, 90)
        d.text((120, 170), 'make.fun', font=ImageFont.truetype(SANS_B, 40), fill=CYAN)
        for i in range(step):
            d.text((120, 260 + i * 92), lines[i],
                   font=ImageFont.truetype(MONO, 46), fill=WHITE)
        if step < len(lines):
            # blinking block cursor after the last shown line
            cx = 120
            cy = 260 + step * 92
            d.rectangle([cx, cy + 8, cx + 26, cy + 52], fill=CYAN)
        else:
            d.text((120, 260 + 5 * 92 + 40), '>>  sent to the agent',
                   font=ImageFont.truetype(SANS_B, 40), fill=GREEN)
        im.save(os.path.join(OUT, f'prompt-{step}.png'))


def working_frames():
    """Segment B — the agent working, terminal lines appearing."""
    lines = [
        ('$ agent — one prompt received', WHITE),
        ('+ writing game.html ...', WHITE),
        ('+ canvas · meteors · ship · score · autopilot', WHITE),
        ('+ verifying in a headless browser ...', WHITE),
        ('OK  game runs — score 025 at 18 seconds', GREEN),
        ('OK  video rendered — 1920×1080, 30 fps', GREEN),
        ('→ ready to post on X', CYAN),
    ]
    for step in range(1, len(lines) + 1):
        im, d = canvas()
        label(d, 'THE AGENT  ·  working, while you watch', 120, 90)
        # terminal window
        d.rounded_rectangle([110, 170, 1810, 900], radius=28,
                            outline=(70, 80, 120), width=3)
        d.rounded_rectangle([110, 170, 1810, 240], radius=28, fill=(20, 22, 44))
        d.ellipse([150, 194, 178, 222], fill=(255, 95, 86))
        d.ellipse([196, 194, 224, 222], fill=(255, 189, 46))
        d.ellipse([242, 194, 270, 222], fill=(39, 201, 63))
        d.text((300, 192), 'agent — building your game', font=ImageFont.truetype(SANS_B, 30), fill=DIM)
        for i in range(step):
            text, color = lines[i]
            d.text((150, 280 + i * 78), text,
                   font=ImageFont.truetype(MONO, 40), fill=color)
        im.save(os.path.join(OUT, f'work-{step}.png'))


def cta_frame():
    """Segment D — the call to come build on make.fun."""
    im, d = canvas()
    d.text((120, 330), 'The game is live.', font=ImageFont.truetype(SANS_B, 110), fill=WHITE)
    d.text((120, 470), 'Your turn — come build on make.fun',
           font=ImageFont.truetype(SANS_B, 72), fill=CYAN)
    d.text((120, 600), 'One prompt is all it takes.',
           font=ImageFont.truetype(SANS, 44), fill=DIM)
    im.save(os.path.join(OUT, 'cta-0.png'))


if __name__ == '__main__':
    prompt_frames()
    working_frames()
    cta_frame()
    print('cards written to', OUT)
