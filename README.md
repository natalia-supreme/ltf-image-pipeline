# LTF Image Pipeline

Pulls the LiveFootballTickets event feed, generates a copyright-clean
AI image per event with FAL AI, reuses good images across matching
events, and exports a CSV mapping for Channable.

```
FETCH  ->  DEDUPE/REUSE  ->  PROMPT  ->  GENERATE  ->  STORE  ->  EXPORT
```

---

## Quick start

```bash
# 1. install dependencies (one time)
pip3 install -r requirements.txt

# 2. add your FAL key
cp .env.example .env
#    then open .env and paste the real key

# 3. test the flow WITHOUT spending anything
python3 main.py --dry-run --limit 3

# 4. real run
python3 main.py
```

Output lands in:

- `data/images/` — the generated images
- `data/output.csv` — event → image mapping (for Channable)
- `data/library.json` — every image, its tag, reusable flag, usages

---

## How to change things (no coding needed)

Almost everything is controlled by two files:

### `config.yaml` — behaviour
- **`feed.url`** — which feed to pull
- **`feed.only_categories`** — limit to certain leagues (e.g. just Premier
  League). Empty list = all.
- **`fal.model`** — which FAL model to use
- **`fal.sizes`** — image sizes produced per event
- **`reuse`** — how images get reused (see below)

### `prompts/football.txt` — how the images look
This is the actual prompt sent to FAL. Edit the wording to change the
visual style, then re-run `python3 main.py`. Any `{field}` in the file
is replaced with that field from the feed (e.g. `{name}`, `{category}`,
`{venue_name}`, `{venue_city}`).

---

## The reuse model (important)

Images are **not** one-per-match. Each image is tagged by an entity —
by default the **home team**, derived from the feed `name`
("Arsenal vs Burnley" → tag `Arsenal`).

1. First run generates a fresh image for each event and stores it in
   `data/library.json` with `"reusable": false`.
2. **You review the images** and set `"reusable": true` on the good ones
   (edit `data/library.json`, or do it from the Lovable UI later).
3. Future runs **reuse** a marked-reusable image whenever a new event
   shares the same tag — no new FAL call, no cost.

Tune this in `config.yaml` under `reuse:` (e.g. tag by away team
instead, or reuse even unmarked images).

---

## Cost

~$0.04 per image (FAL `nano-banana-2`). The reuse model means you pay
once per team, not once per fixture — a full Premier League season is a
few dollars, not hundreds. `--dry-run` costs nothing.

---

## File map (for whoever maintains this)

| File | What it does |
|---|---|
| `main.py` | Orchestrates the whole flow |
| `config.yaml` | All settings |
| `prompts/football.txt` | The image prompt |
| `src/fetch_feed.py` | Download + parse the XML feed |
| `src/build_prompt.py` | Fill the prompt + derive the reuse tag |
| `src/library.py` | Dedupe / store / reuse logic |
| `src/generate.py` | Call FAL, save the image |
| `src/export.py` | Write the CSV |

Open this folder in Claude Code and ask in plain English to change
behaviour (e.g. "tag images by away team instead", "add a 16:9 size").
