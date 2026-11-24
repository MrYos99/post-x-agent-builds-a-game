# post-x-agent-builds-a-game

[![make.fun · post-x-the-agent-builds-a-game-from-20261122-1709](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)
[![rank](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/MrYos99/post-x-agent-builds-a-game/rank.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)
[![reward](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/MrYos99/post-x-agent-builds-a-game/reward.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)

One prompt, one game, one short video. An AI coding agent built the tiny
browser game in `game.html` — NEON DODGE, a neon ship dodging falling
meteors — from a single prompt, while the camera watched. The video shows
the prompt, the agent working, and the finished game running, and ends on
make.fun's referral end card. It was posted natively on X; the post is the
entry.

## The one prompt

> Build a tiny browser game: NEON DODGE. A little neon ship dodges falling
> meteors — steer with arrow keys, each dodge scores a point, one hit ends
> the run, Space restarts. Dark space, glowing ship, score top-left.

## Play the game

Open `game.html` in a browser. Steer with ← → (or ↑ ↓), dodge the meteors,
press Space to restart after a game over. `game.html?t=<ms>` renders the
exact frame at that game-time — that is how the video filmed it.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22) copies `POST.json` — `{"url":
"https://x.com/<handle>/status/<id>"}` — to `/output/POST.json`, where the
house reads the post and its counts from X.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ge0by3j6&utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)</sub>
