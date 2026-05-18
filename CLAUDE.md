# CLAUDE.md — how to work in this repo

This is the LTF AI ad-creative pipeline. If the user (Mark) asks to
**add, change, disable, or remove an image style**, follow this exactly.

## The one rule: styles live in `styles.yaml`

`styles.yaml` is the single source of truth. Never hardcode prompts
anywhere else. When the user asks for a new/changed style:

1. **Edit `styles.yaml`** — add or modify a style block (schema below).
2. **Run:** `python3 build_styles.py` (regenerates `gallery/styles.json`,
   which the Lovable app reads — the YAML alone does nothing).
3. **Commit & push:**
   `git add -A && git commit -m "..." && git push origin main`
4. Tell the user it will appear as a selectable option in the app
   within a few minutes (GitHub cache).

Do all four every time. Skipping step 2 or 3 means it won't show up.

## Style block schema

```yaml
  - key: short-unique-id          # lowercase, hyphens, used in filenames
    title: "Human Label"
    category: head-to-head        # head-to-head | club-spotlight | stadium-atmosphere
    enabled: true                 # false = keep on file but hide it
    has_players: false            # true only if it shows invented players
    needs: [home, away]           # [] none | [home] | [home, away]
    prompt: |
      <the full image prompt>
```

Placeholders the pipeline fills per match (use these, not real names):
`{home_primary}` `{home_secondary}` `{away_primary}` `{away_secondary}`

Categories:
- **head-to-head** — both teams (rival supporters in the two colours)
- **club-spotlight** — one team's colours (its fans / atmosphere)
- **stadium-atmosphere** — generic, no team

## Non-negotiable creative rules

- **No fake/invented players for VS** — Mark's direction: supporters
  connect, fake players don't (and real players are copyrighted).
  Prefer rival-supporter scenes for head-to-head.
- **Every prompt MUST end with an IP-safety clause**, e.g.:
  "CRITICAL IP SAFETY: plain clothing only, no kits, club crests or
  badges, no sponsor/maker/apparel-brand logos (no swoosh, stripes or
  double-diamond), no text or emblems on scarves, no national flags,
  no advertising boards, no real venue, no real player likenesses,
  no readable text anywhere."
- Generic invented stadium only — never name or depict a real venue.
- The matchup is signalled by the two team colours, never by logos.

## Testing a style before locking it (optional)

Add it to `experiments/compare_directions.py` and run
`python3 experiments/compare_directions.py <key>` to preview one image
in `experiments/output/` before enabling it in `styles.yaml`.
Needs a FAL key in `.env` (copy `.env.example`).

## What NOT to touch unless asked

`src/`, `main.py`, `config.yaml`, `team_colours.yaml` — the pipeline
engine. Style changes only need `styles.yaml` + `build_styles.py`.
