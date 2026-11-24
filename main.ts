// Entry program for "The agent builds a game from one prompt"
// (post-x-the-agent-builds-a-game-from-20261122-1709, Node 22).
//
// The entry is the X post itself: a short video of an AI coding agent
// building the tiny browser game in game.html from one prompt, ending
// with make.fun's referral end card. This program only hands the post
// in: it copies POST.json ({"url": "https://x.com/<handle>/status/<id>"})
// from the repository root to /output/POST.json, where the house reads
// it and fetches the post's counts from X. Nothing written here about
// the post is scored.
//
// Local check:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(BOT_DIR, 'POST.json');
const target = join(OUTPUT_DIR, 'POST.json');

if (!existsSync(source)) {
  console.error(`POST.json not found in ${BOT_DIR} — write the X post URL there first.`);
  process.exit(1);
}

let post;
try {
  post = JSON.parse(readFileSync(source, 'utf8'));
} catch (err) {
  console.error(`POST.json does not parse: ${(err).message}`);
  process.exit(1);
}

if (typeof post.url !== 'string' || !/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\//.test(post.url)) {
  console.error('POST.json must hold {"url": "https://x.com/<handle>/status/<id>"}.');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(source, target);
console.log(`POST.json copied to ${target}`);
