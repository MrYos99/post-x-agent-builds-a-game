#!/usr/bin/env bash
# Assemble the post-x video from the frames this session rendered.
#
#   Segment A  prompt cards    frames/cards/prompt-0..5.png
#   Segment B  agent working   frames/cards/work-1..7.png
#   Segment C  real gameplay   frames/game/g000..g106.png  (game.html?t=<ms>)
#   Segment D  call to action  frames/cards/cta-0.png
#   Segment E  make.fun referral end card (press pack, used as-is)
#              endcard-16x9.mp4 + referral code typed into its field
#
# Two passes: (1) concat the main clip at 30 fps; (2) append the end
# card (last frame held 1.5 s so the code stays readable) and draw the
# referral code into the card's field once it rests (1.433 s in).
# Run from anywhere:  bash scripts/build_video.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$SCRIPT_DIR/.."
WORK="$SCRIPT_DIR/../.."
FRAMES="$WORK/frames"
CARD="$WORK/endcard-16x9.mp4"
CODE="ge0by3j6"
MONO_B="/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
OUTDIR="$WORK/video"
mkdir -p "$OUTDIR"

LIST="$WORK/concat-inputs.txt"
: > "$LIST"
add() { # file duration
  printf "file '%s'\nduration %s\n" "$1" "$2" >> "$LIST"
}
# A: prompt, typed line by line
add "$FRAMES/cards/prompt-0.png" 0.7
add "$FRAMES/cards/prompt-1.png" 0.8
add "$FRAMES/cards/prompt-2.png" 0.8
add "$FRAMES/cards/prompt-3.png" 0.8
add "$FRAMES/cards/prompt-4.png" 0.8
add "$FRAMES/cards/prompt-5.png" 1.2
# B: agent working
for n in 1 2 3 4 5 6 7; do add "$FRAMES/cards/work-$n.png" 0.85; done
# C: gameplay, 150 ms of game time per frame
for f in "$FRAMES"/game/g*.png; do add "$f" 0.15; done
# D: call to action
add "$FRAMES/cards/cta-0.png" 3.0
# concat demuxer needs the last file repeated without a duration
printf "file '%s'\n" "$FRAMES/cards/cta-0.png" >> "$LIST"

MAIN="$OUTDIR/postx-main.mp4"
ffmpeg -y -v error -f concat -safe 0 -i "$LIST" \
  -vf "fps=30,format=yuv420p,fade=t=in:st=0:d=0.5" \
  -c:v libx264 -crf 20 -preset medium -movflags +faststart "$MAIN"

D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MAIN")
T=$(awk "BEGIN{print $D + 1.433}")
echo "main clip: ${D}s — code appears at ${T}s"

FINAL="$OUTDIR/postx-final.mp4"
ffmpeg -y -v error -i "$MAIN" -i "$CARD" -filter_complex \
  "[1:v]tpad=stop_mode=clone:stop_duration=1.5,format=yuv420p[v1]; \
   [0:v][v1]concat=n=2:v=1:a=0, \
   drawbox=x=430:y=692:w=9:h=81:color=white:t=fill:enable='gte(t,$T)', \
   drawtext=fontfile=$MONO_B:text=$CODE:fontsize=62:fontcolor=0x191419:x=432:y=712:enable='gte(t,$T)'[v]" \
  -map "[v]" -c:v libx264 -crf 22 -preset medium -pix_fmt yuv420p \
  -movflags +faststart "$FINAL"

ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$FINAL"
ls -la "$FINAL"
