#!/usr/bin/env python3
"""
The APPROVED creative directions (signed off 2026-05-17).

Only directions Natalia accepted are kept here — rejected/superseded
experiments have been removed to keep this simple.

Run from the repo root:
    python3 experiments/compare_directions.py                # all 12
    python3 experiments/compare_directions.py F,foot-v1      # a subset

Two-colour kits: Arsenal (home) = red/white, Burnley (away) =
claret/sky-blue. In production these come from team_colours.yaml.
"""

import sys
from pathlib import Path

import requests
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.generate import _call_fal, _crop_to_spec  # noqa: E402
from main import _load_env  # noqa: E402

_load_env()

# Invented two-colour kit colours (primary + secondary), NOT official
HOME_PRIMARY, HOME_SECONDARY = "bright red", "white"                  # Arsenal
AWAY_PRIMARY, AWAY_SECONDARY = "deep claret / burgundy", "sky blue"   # Burnley

_KIT = (
    "wearing an INVENTED non-official football kit with a bold 50/50 "
    "vertical halved shirt — the left half solid {primary}, the right "
    "half solid {secondary}, split straight down the centre — with one "
    "large plain white squad number across it; solid {primary} shorts "
    "with a single bold {secondary} vertical stripe down each side; "
    "solid {primary} socks with a wide {secondary} band near the top. "
    "This halved design must look clearly different from any real "
    "Premier League club's official kit"
)

# ===========================================================
#  APPROVED — Head-to-head match (7)
# ===========================================================
DIRECTIONS = {
    "F-twocolour-duel": (
        f"Ultra-photorealistic cinematic sports photograph, dramatic low "
        f"pitch-level angle looking slightly upward. Two dynamic anonymous "
        f"footballers competing hard for a plain unbranded white-and-black "
        f"football in an explosive mid-action moment. The first player is "
        f"{_KIT.format(primary=HOME_PRIMARY, secondary=HOME_SECONDARY)}. "
        f"The second player is "
        f"{_KIT.format(primary=AWAY_PRIMARY, secondary=AWAY_SECONDARY)}. "
        f"The ball is prominent in the foreground, frozen with motion blur, "
        f"turf and water spraying up, muscles straining, intense focus. "
        f"Behind them a vast modern stadium bowl packed with a blurred "
        f"glowing crowd, completely out of focus. Brilliant golden-hour sun "
        f"flaring low directly behind the stadium rim, warm light rays, "
        f"atmospheric haze, drifting light particles and orange sparks, "
        f"lush green pitch catching the light. Heroic, premium, "
        f"high-contrast composite look, 8K, Nikon Z9 35mm, shallow depth "
        f"of field. The two kits are clearly different invented designs, "
        f"each combining its two colours so the teams are easy to tell "
        f"apart. CRITICAL IP SAFETY: do NOT reproduce any real team's "
        f"official kit; no club logos, crests, badges, sponsor text, "
        f"manufacturer marks, team names, advertising hoardings, "
        f"naming-rights signage, or real player likenesses. Only a plain "
        f"squad number is allowed, nothing else written anywhere."
    ),
    "2-golden-duel-2col": (
        f"Ultra-photorealistic cinematic sports photograph, tight dynamic "
        f"lower-body action crop, low pitch-level angle. Two anonymous "
        f"footballers competing hard for a plain unbranded white-and-black "
        f"football, frozen mid-action with motion blur, turf and water "
        f"spraying up. The first player is "
        f"{_KIT.format(primary=HOME_PRIMARY, secondary=HOME_SECONDARY)}. "
        f"The second player is "
        f"{_KIT.format(primary=AWAY_PRIMARY, secondary=AWAY_SECONDARY)}. "
        f"Brilliant golden-hour sun flaring low behind a vast modern "
        f"stadium bowl packed with a blurred glowing crowd, warm light "
        f"rays, atmospheric haze, drifting sparks, lush green pitch. "
        f"Premium high-contrast composite look, 8K, Nikon Z9 35mm, shallow "
        f"depth of field. The two kits are clearly different invented "
        f"designs. CRITICAL IP SAFETY: do NOT reproduce any real team's "
        f"official kit; no club logos, crests, badges, sponsor text, "
        f"manufacturer marks, team names, advertising hoardings, or real "
        f"player likenesses. Only a plain squad number is allowed."
    ),
    "3-night-duel-2col": (
        f"Ultra-photorealistic cinematic sports photograph, dramatic moody "
        f"NIGHT match under powerful white floodlights (not golden hour). "
        f"Two anonymous footballers competing hard for a plain unbranded "
        f"white-and-black football, explosive mid-action moment, motion "
        f"blur, turf and water spraying up, volumetric light shafts, faint "
        f"fog, orange spark particles. The first player is "
        f"{_KIT.format(primary=HOME_PRIMARY, secondary=HOME_SECONDARY)}. "
        f"The second player is "
        f"{_KIT.format(primary=AWAY_PRIMARY, secondary=AWAY_SECONDARY)}. "
        f"Behind them a vast dark modern stadium bowl, blurred roaring "
        f"crowd, deep blue night sky. Heroic high-contrast composite look, "
        f"8K, Nikon Z9 35mm, shallow depth of field. The two kits are "
        f"clearly different invented designs. CRITICAL IP SAFETY: do NOT "
        f"reproduce any real team's official kit; no club logos, crests, "
        f"badges, sponsor text, manufacturer marks, team names, "
        f"advertising hoardings, or real player likenesses. Only a plain "
        f"squad number is allowed."
    ),
    "4-explosive-duel-2col": (
        f"Ultra-photorealistic cinematic sports photograph, dramatic very "
        f"low ground-level angle, the most explosive 1v1 duel: two "
        f"anonymous footballers lunging for a plain unbranded "
        f"white-and-black ball low between them, huge spray of turf and "
        f"water kicked up, intense strain, strong motion blur. The first "
        f"player is "
        f"{_KIT.format(primary=HOME_PRIMARY, secondary=HOME_SECONDARY)}. "
        f"The second player is "
        f"{_KIT.format(primary=AWAY_PRIMARY, secondary=AWAY_SECONDARY)}. "
        f"Behind them a vast modern stadium at night, blurred roaring "
        f"crowd, powerful floodlights, orange sparks. Heroic dynamic "
        f"composition, 8K, Nikon Z9 35mm, shallow depth of field. The two "
        f"kits are clearly different invented designs. CRITICAL IP SAFETY: "
        f"do NOT reproduce any real team's official kit; no club logos, "
        f"crests, badges, sponsor text, manufacturer marks, team names, "
        f"advertising hoardings, or real player likenesses. Only a plain "
        f"squad number is allowed."
    ),
    "foot-v1-flare": (
        f"Ultra-photorealistic cinematic sports photograph, extreme "
        f"close-up at grass level: two opposing players' boots meeting "
        f"over a plain unbranded white-and-black football on lush dewy "
        f"green grass, the ball large and razor-sharp in the centre "
        f"foreground, one boot pressing the top of the ball. Left player's "
        f"sock solid {HOME_PRIMARY} with a bold {HOME_SECONDARY} band; "
        f"right player's sock solid {AWAY_PRIMARY} with a bold "
        f"{AWAY_SECONDARY} band. A vast modern stadium completely blurred "
        f"into glowing bokeh behind, brilliant white floodlights and a "
        f"bright central sun/light flare bursting between the legs, warm "
        f"backlight rim, water droplets and light particles in the air, "
        f"shallow depth of field. Premium high-contrast composite look, "
        f"8K, Nikon Z9 100mm macro. CRITICAL IP SAFETY: ball and boots "
        f"completely plain, NO brand, NO logos, NO sponsor text, no club "
        f"crests, no advertising, no team names, no real player "
        f"likenesses, no trademarks."
    ),
    "foot-v3-strike": (
        f"Ultra-photorealistic cinematic sports photograph, dynamic "
        f"close-up low angle: the instant two opposing players' boots "
        f"clash at a plain unbranded white-and-black football on dewy "
        f"grass, slight motion blur, turf and water exploding off the "
        f"ball, the ball prominent and sharp in the foreground. Left "
        f"player's sock solid {HOME_PRIMARY} with a bold {HOME_SECONDARY} "
        f"band; right player's sock solid {AWAY_PRIMARY} with a bold "
        f"{AWAY_SECONDARY} band. Warm golden-hour sun flaring low behind "
        f"a vast stadium blurred into glowing bokeh, drifting sparks, "
        f"atmospheric haze, shallow depth of field. Premium high-contrast "
        f"composite look, 8K, Nikon Z9 100mm. CRITICAL IP SAFETY: ball "
        f"and boots completely plain, NO brand, NO logos, NO sponsor "
        f"text, no club crests, no advertising, no team names, no real "
        f"player likenesses, no trademarks."
    ),
    "foot-v4-groundlevel": (
        f"Ultra-photorealistic cinematic sports photograph, ultra-low "
        f"camera right on the turf: a plain unbranded white-and-black "
        f"football huge in the immediate foreground with two pairs of "
        f"players' lower legs and boots framing it either side, blades of "
        f"grass and dew in sharp focus. Left legs in solid {HOME_PRIMARY} "
        f"socks with a bold {HOME_SECONDARY} band; right legs in solid "
        f"{AWAY_PRIMARY} socks with a bold {AWAY_SECONDARY} band. Behind, "
        f"a vast packed modern stadium at dusk dissolved into glowing "
        f"bokeh, floodlights bursting into starbursts, warm sky, light "
        f"particles, very shallow depth of field. Premium high-contrast "
        f"cinematic look, 8K, Nikon Z9 24mm low macro. CRITICAL IP "
        f"SAFETY: ball and boots completely plain, NO brand, NO logos, "
        f"NO sponsor text, no club crests, no advertising, no team "
        f"names, no real player likenesses, no trademarks."
    ),

    # =======================================================
    #  APPROVED — Stadium atmosphere (5)
    # =======================================================
    "B-fan-pov": (
        "Ultra-photorealistic editorial sports photograph shot from deep in "
        "the stands of a large modern football stadium at night, looking "
        "over the dark silhouetted backs, heads and raised arms of a dense "
        "crowd of standing supporters down onto a brilliant green floodlit "
        "pitch far below where tiny distant anonymous players are mid-game. "
        "Plain scarves and plain flags held overhead with NO text or "
        "emblems, hands and phones raised, electric celebratory atmosphere, "
        "haze in the floodlight beams. Foreground fans fully in shadow as "
        "silhouettes, the bright pitch as the focal point, strong depth, "
        "gritty documentary feel, cinematic, 8K, Nikon Z9 24mm. CRITICAL IP "
        "SAFETY: no club logos, crests or badges, no text or emblems on "
        "scarves or flags, no sponsor text, no advertising boards, no "
        "naming-rights signage, no real player likenesses, no trademarks."
    ),
    "A-ball-motion": (
        "Ultra-photorealistic cinematic sports photograph: extreme close-up "
        "of a plain unbranded white-and-black football frozen in mid-air a "
        "split second after being struck, sharp motion blur streaking behind "
        "it, droplets of water and tiny turf particles spraying off it. "
        "Behind it a huge modern football stadium at night, completely out "
        "of focus into creamy bokeh — thousands of blurred crowd lights, "
        "intense white floodlights flaring, warm orange spark particles "
        "drifting. Shallow depth of field, dramatic backlight and lens "
        "flare, low pitch-level angle, hyper-detailed, 8K, shot on Nikon Z9 "
        "200mm f/2. CRITICAL IP SAFETY: the ball is completely plain with no "
        "brand, no manufacturer mark, no logo; no club crests, no sponsor "
        "text, no advertising boards, no readable signage anywhere, no "
        "people in focus, no real player likenesses, no trademarks."
    ),
    "3-pitch-tunnel": (
        "Ultra-photorealistic editorial photograph from pitch level inside "
        "a large modern generic football stadium before kickoff. View "
        "looking out from the dark players' tunnel toward a perfectly mown "
        "empty green pitch under intense white floodlights. Tiered stands "
        "fill with blurred distant supporters, dramatic shafts of light, "
        "lens flare, faint mist in the floodlight beams, a sense of quiet "
        "anticipation before kickoff. Shot on Nikon Z9, 24mm wide lens, "
        "shallow dark foreground, cinematic, 8K, documentary style. "
        "CRITICAL IP SAFETY: invented generic stadium that does not "
        "resemble any real venue; no club logos, crests, badges, sponsor "
        "text, advertising boards, branded kits, naming-rights signage, "
        "team names, or real player likenesses; no readable text anywhere."
    ),
    "4b-hero-2col": (
        f"Ultra-photorealistic cinematic sports photograph, dramatic low "
        f"pitch-level angle looking slightly upward. A single dynamic "
        f"anonymous footballer caught mid-strike kicking a plain unbranded "
        f"white-and-black football, the ball prominent in the foreground "
        f"frozen with motion blur, turf and water spraying up, muscles "
        f"straining. The player is "
        f"{_KIT.format(primary=HOME_PRIMARY, secondary=HOME_SECONDARY)}. "
        f"Behind the player a vast modern stadium bowl packed with a "
        f"blurred glowing crowd, completely out of focus. Brilliant "
        f"golden-hour sun flaring low directly behind the stadium rim, "
        f"warm light rays, atmospheric haze, drifting light particles and "
        f"orange sparks, lush green pitch catching the light. Heroic, "
        f"premium, high-contrast composite look, 8K, Nikon Z9 35mm, "
        f"shallow depth of field. CRITICAL IP SAFETY: do NOT reproduce any "
        f"real team's official kit; no club logos, crests, badges, sponsor "
        f"text, manufacturer marks, team names, advertising hoardings, or "
        f"real player likenesses. Only a plain squad number is allowed. "
        f"Football must be completely plain with no brand."
    ),
    "5b-epic-bowl": (
        "Ultra-photorealistic cinematic sports photograph, wide elevated "
        "high-angle view of the inside of a vast generic modern football "
        "stadium at night, completely packed with a roaring crowd, every "
        "tier full, brilliant white floodlights blazing, the lush green "
        "pitch glowing far below, scattered flashes from phone cameras "
        "across the stands like sparkling stars, faint haze and "
        "atmospheric depth, deep blue night sky above the open roof. "
        "Electric, epic, awe-inspiring scale and energy. Premium "
        "high-contrast cinematic look, 8K, shot on Nikon Z9 24mm wide "
        "lens, slight tilt-shift depth. CRITICAL IP SAFETY: invented "
        "fictional stadium that does not resemble any real venue; no club "
        "logos, crests, badges, sponsor text, advertising boards, "
        "scoreboard text, naming-rights signage, team names, or real "
        "player likenesses; no readable text anywhere."
    ),
}

SIZE = {"label": "square", "width": 1200, "height": 1200}


def main() -> None:
    config = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
    out_dir = Path("experiments/output")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Optional: comma-separated substrings to run only matching directions
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    items = {k: v for k, v in DIRECTIONS.items()
             if not only or any(o in k for o in only)}

    for key, prompt in items.items():
        print(f"-> generating direction {key} ...")
        url = _call_fal(prompt, SIZE, config)
        raw = requests.get(url, timeout=120).content
        final = _crop_to_spec(raw, SIZE["width"], SIZE["height"])
        path = out_dir / f"arsenal-burnley-{key}.png"
        path.write_bytes(final)
        print(f"   saved -> {path}")

    print(f"\nDone. {len(items)} image(s) in experiments/output/")


if __name__ == "__main__":
    main()
