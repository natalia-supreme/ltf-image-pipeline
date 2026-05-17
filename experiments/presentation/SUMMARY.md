# LTF AI Ad-Creative Engine — Summary for Mark

**From:** Natalia · **Date:** 2026-05-17

---

## TL;DR
A working pipeline that pulls the live LFT feed and auto-generates
**copyright-clean** ad creatives — no team logos, kits, players or real
venues — for **~$0.08 an image**. 12 creative directions approved and
ready. A full Premier League season costs a few dollars (images are
reused per team, not regenerated per match).

---

## What works today
- Pulls `livefootballtickets.com/feeds/all-glad.xml`, filters to a league
- Builds the prompt from feed fields, calls FAL `nano-banana-2`
- Crops to exact Google asset specs (1200×1200 + 1200×628)
- Tags each image by team → reused across all that team's matches
- Exports a CSV mapping (event → image) for Channable
- Verified end-to-end on real matches (Arsenal v Burnley etc.)

## The IP problem — solved
1. Never name the real team/venue in the prompt (model copied real
   stadiums/logos when we did) → generic stadium; the matchup is carried
   by the ad headline from the feed.
2. We research each club's official kit, then deliberately **invent a
   non-official two-colour kit** (bold halved shirt in the club's
   primary + secondary). Recognisable by colour, legally distinct.
3. Result: no crests, sponsors, maker logos, player likenesses, real
   venues, or readable signage anywhere.

## Approved creative library (15, in 3 categories)
- **Head-to-head (7)** — two teams' colours: halved-kit duel (hero),
  golden duel, night duel, explosive duel, + 3 foot-vs-foot close-ups
- **Club Spotlight (4)** — one team's colours: single player hero,
  home crowd dusk, home crowd golden hour, fan hero daytime
- **Stadium atmosphere (4)** — fully generic, no team: fan POV, ball
  in motion, pitch/tunnel, epic stadium bowl

## How you own it (no coding)
Two plain files control everything:
- `config.yaml` — feed, image sizes, model, reuse rules
- `prompts/football.txt` — the image style
Plus `team_colours.yaml` — the 20 EPL club colours (hand-verified;
unknown teams auto-looked-up once and cached). All human-editable.
Repo is Claude-Code-friendly — change behaviour in plain English.

## Cost
~$0.08/image. Reuse model = pay once per team, not per match →
full PL season ≈ a few dollars, near-zero ongoing.

## Decisions I need from you
1. Which style(s) should the full feed run produce? (or all, tagged)
2. OK to productionise: wire colour map + approved prompt into the
   pipeline for automatic per-match generation?
3. Repo name/owner for GitHub (suggested `Markvdeng/ltf-image-pipeline`)?

## What's left (small)
- Wire the table-first/search-on-miss colour lookup into the pipeline
- Bake the chosen approved prompt(s) in with colour placeholders
- Push to GitHub + connect the Lovable UI on top
