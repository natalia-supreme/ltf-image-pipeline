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
    "d1hh-drummer-vs": (
        f"A split-screen diptych key visual made of TWO separate "
        f"ultra-photorealistic matchday photographs joined side by side, "
        f"divided ONLY by a clean thin vertical glowing light seam down "
        f"the exact centre (NO fence, NO barrier, NO stewards) — clearly "
        f"two shots taken from different corners of the same stadium. "
        f"LEFT photo, drummer CENTERED in the left half: a passionate "
        f"anonymous fan mid-beat on a large plain unbranded drum, behind "
        f"him a dense floodlit crowd in plain solid {HOME_PRIMARY} and "
        f"{HOME_SECONDARY} casual clothing with plain "
        f"{HOME_PRIMARY}-and-{HOME_SECONDARY} scarves and flags raised, "
        f"mouths open chanting, night, haze. RIGHT photo, drummer "
        f"CENTERED in the right half: a mirrored opposing fan mid-beat on "
        f"a plain unbranded drum, behind him a dense floodlit crowd in "
        f"plain solid {AWAY_PRIMARY} and {AWAY_SECONDARY} casual clothing "
        f"with plain {AWAY_PRIMARY}-and-{AWAY_SECONDARY} scarves and "
        f"flags raised. Both halves the same energetic composition and "
        f"lighting, each drummer prominent and centred in its own half, "
        f"bright central light burst on the seam. Gritty documentary "
        f"realism, cinematic, 8K, Nikon Z9 35mm, diverse anonymous "
        f"faces. CRITICAL IP SAFETY: plain clothing and plain drums "
        f"only, no kits, club crests, sponsor/maker logos, no text or "
        f"emblems on scarves, drums or flags, no real venue, no real "
        f"player likeness, no readable text anywhere."
    ),
    "d1-drummer": (
        f"Ultra-photorealistic editorial sports photograph: a passionate "
        f"anonymous supporter mid-beat on a large plain unbranded drum at "
        f"the front of a packed singing section, behind him a dense crowd "
        f"in plain solid {HOME_PRIMARY} and {HOME_SECONDARY} casual "
        f"clothing with plain {HOME_PRIMARY}-and-{HOME_SECONDARY} scarves "
        f"raised, mouths open chanting, floodlit night, haze. Gritty "
        f"documentary realism, 8K, Nikon Z9 35mm. CRITICAL IP SAFETY: "
        f"plain clothing and plain drum only, no kits, club crests, "
        f"sponsor/maker logos, text or emblems on scarves or drum, no "
        f"real venue, no real player likeness, no readable text."
    ),
    "d2-smoke-wall": (
        f"Ultra-photorealistic editorial sports photograph: a packed "
        f"stand engulfed in thick celebratory coloured smoke in "
        f"{HOME_PRIMARY}, {HOME_SECONDARY}, {AWAY_PRIMARY} and "
        f"{AWAY_SECONDARY}, silhouetted fans with arms and scarves raised "
        f"emerging through the haze, floodlight beams cutting the smoke, "
        f"euphoric celebratory mood (festive smoke, NOT fire or danger). "
        f"Epic, atmospheric, cinematic, 8K, Nikon Z9 35mm. CRITICAL IP "
        f"SAFETY: plain clothing only, no kits, club crests, sponsor or "
        f"maker logos, text or emblems on scarves, no real venue, no "
        f"real player likeness, no readable text anywhere."
    ),
    "d3-pub": (
        f"Ultra-photorealistic editorial photograph inside a packed cosy "
        f"traditional pub before a match: anonymous fans in plain solid "
        f"{HOME_PRIMARY} and {HOME_SECONDARY} casual clothing singing "
        f"with arms around shoulders and pints raised, warm tungsten "
        f"light, condensation on the windows, joyful pre-match "
        f"anticipation. Gritty documentary realism, 8K, Nikon Z9 35mm. "
        f"CRITICAL IP SAFETY: generic pub, no brewery or drink brands, no "
        f"readable signage or labels, plain clothing only, no kits, club "
        f"crests, sponsor or maker logos, no real venue, no real player "
        f"likeness, no readable text anywhere."
    ),
    "d4-away-day": (
        f"Ultra-photorealistic editorial photograph at dawn: anonymous "
        f"football fans in plain solid {HOME_PRIMARY} and "
        f"{HOME_SECONDARY} casual clothing on a supporters' coach or "
        f"train, faces lit by soft window light, a plain "
        f"{HOME_PRIMARY}-and-{HOME_SECONDARY} scarf and a thermos, quiet "
        f"anticipation of the away-day journey, condensation on the "
        f"glass. Intimate documentary realism, 8K, Nikon Z9 35mm. "
        f"CRITICAL IP SAFETY: generic vehicle interior, no transport or "
        f"other brands, plain clothing only, no kits, club crests, "
        f"sponsor or maker logos, text on scarves, no real venue, no "
        f"real player likeness, no readable text anywhere."
    ),
    "d5-retro-terrace": (
        f"Authentic 1970s-80s vintage film photograph, heavy 35mm grain, "
        f"faded warm retro colour, slight light leak: a dense standing "
        f"terrace of anonymous fans in plain period casual clothing in "
        f"{HOME_PRIMARY}, {HOME_SECONDARY}, {AWAY_PRIMARY} and "
        f"{AWAY_SECONDARY}, plain scarves aloft, packed old-school "
        f"concrete terrace, nostalgic atmosphere. Analogue documentary "
        f"aesthetic. CRITICAL IP SAFETY: plain period clothing only, no "
        f"retro kits, club crests, sponsor or maker logos, no text or "
        f"emblems on scarves, no real venue, no real player likeness, no "
        f"readable text anywhere."
    ),
    "d6-kinetic-type": (
        f"Bold modern kinetic typographic key visual: the single huge "
        f"sliced word \"MATCHDAY\" in massive condensed type cutting "
        f"across the frame, set over a dynamic field split into "
        f"{HOME_PRIMARY} and {AWAY_PRIMARY} colour blocks with "
        f"{HOME_SECONDARY} and {AWAY_SECONDARY} accents, a small abstract "
        f"football and stadium-stand silhouette, energetic motion shapes, "
        f"high contrast, premium poster design, 8K. CRITICAL: the ONLY "
        f"word allowed is MATCHDAY — no club or competition names, no "
        f"logos, crests, sponsor text, real venue or real player "
        f"likeness, no other text anywhere."
    ),
    "d7-3d-ball": (
        f"Surreal premium 3D CGI render: a glossy football exploding "
        f"apart into sleek geometric shards and ribbons of energy in "
        f"{HOME_PRIMARY}, {HOME_SECONDARY}, {AWAY_PRIMARY} and "
        f"{AWAY_SECONDARY}, floating on a clean studio gradient "
        f"background with soft shadows and rim light, hyper-detailed, "
        f"modern, 8K octane render. CRITICAL IP SAFETY: completely plain "
        f"unbranded ball, no maker mark or logo, no club crests, sponsor "
        f"text, real venue, real player likeness, or readable text."
    ),
    "d8-street-cage": (
        f"Ultra-photorealistic gritty photograph at dusk: anonymous "
        f"youths playing football on a floodlit urban street cage pitch "
        f"between apartment blocks, silhouettes and motion, plain solid "
        f"{HOME_PRIMARY} and {HOME_SECONDARY} tops, a plain unbranded "
        f"ball, raw authentic energy, long shadows, city haze. "
        f"Documentary realism, 8K, Nikon Z9 35mm. CRITICAL IP SAFETY: "
        f"generic anonymous urban setting, no shop or other brand "
        f"signage, plain clothing only, no kits, club crests, sponsor or "
        f"maker logos, no real venue, no real player likeness, no "
        f"readable text anywhere."
    ),
    "d9-countdown": (
        f"Cinematic photograph of a giant generic stadium scoreboard "
        f"clock glowing in the dark, large digital numerals reading "
        f"\"00:00\", a thin {HOME_PRIMARY} bar on the left and "
        f"{AWAY_PRIMARY} bar on the right, a silhouetted packed stand "
        f"below in haze, dramatic anticipation and urgency. 8K, Nikon Z9 "
        f"85mm. CRITICAL: the ONLY characters shown are the time 00:00 — "
        f"no club or competition names, no scores, no logos, crests, "
        f"sponsor text, real venue, real player likeness, or any other "
        f"readable text anywhere."
    ),
    "d10-ritual-hands": (
        f"Ultra-photorealistic premium macro close-up sequence feel: "
        f"weathered hands gripping a plain {HOME_PRIMARY}-and-"
        f"{HOME_SECONDARY} scarf stretched taut, shallow depth of field, "
        f"warm soft directional light, intimate emotional matchday-ritual "
        f"mood, blurred floodlit stand bokeh behind. 8K, Nikon Z9 100mm "
        f"macro. CRITICAL IP SAFETY: plain scarf only — no text, words, "
        f"club name, crest, logo or emblem; no sponsor or maker marks, "
        f"no real venue, no real player likeness, no readable text."
    ),
    "c1-ticket-hero": (
        f"Ultra-photorealistic cinematic product photograph: a single "
        f"generic unbranded paper match ticket with a tear-off stub held "
        f"up between fingers, sharp in the foreground, against a vast "
        f"blurred floodlit stadium at dusk dissolved into glowing bokeh. "
        f"The ticket is split into a {HOME_PRIMARY} colour block and an "
        f"{AWAY_PRIMARY} colour block with the only printed words "
        f"'MATCH TICKET' and a generic seat/row number; a plain "
        f"perforation line. Warm rim light, shallow depth of field, "
        f"premium 8K, Nikon Z9 100mm. CRITICAL IP SAFETY: NO club or "
        f"competition names, NO team names, NO logos, crests, sponsor or "
        f"maker marks, NO real barcode, NO real venue; the only text "
        f"anywhere is the generic 'MATCH TICKET' and a seat number."
    ),
    "c2-half-and-half": (
        f"Bold graphic key visual, ultra-high-contrast cinematic poster "
        f"style: the frame split exactly down the middle into two halves "
        f"— the LEFT half saturated in {HOME_PRIMARY} with a "
        f"{HOME_SECONDARY} accent, the RIGHT half saturated in "
        f"{AWAY_PRIMARY} with an {AWAY_SECONDARY} accent. On the centre "
        f"divide, a single plain unbranded white-and-black football and a "
        f"clean stadium-stand silhouette, dramatic light burst behind. "
        f"Stylised, minimal, energetic, 8K. CRITICAL IP SAFETY: no club "
        f"or competition names, no logos, crests, sponsor text, real "
        f"venue, real player likeness, or any readable text anywhere."
    ),
    "c3-tifo": (
        f"Ultra-photorealistic editorial sports photograph of a single "
        f"vast packed grandstand at night where the entire crowd holds up "
        f"coloured cards forming a huge bold ABSTRACT GEOMETRIC mosaic "
        f"(blocks, chevrons, diagonal bands) in {HOME_PRIMARY}, "
        f"{HOME_SECONDARY}, {AWAY_PRIMARY} and {AWAY_SECONDARY}, plus a "
        f"few large hand-held flags and banners in the same plain "
        f"colours. Floodlit, smoke haze, epic scale, cinematic, 8K, "
        f"Nikon Z9 24mm. CRITICAL: the mosaic is PURELY ABSTRACT colour "
        f"geometry — it must NOT spell any word, letter, club name or "
        f"form any crest, logo or recognisable real tifo. No sponsor "
        f"text, no real venue, no real player likeness, no readable text."
    ),
    "c4-scarf-wall": (
        f"Ultra-photorealistic editorial close-up: a dense wall of plain "
        f"football scarves held aloft and stretched taut by unseen hands, "
        f"filling the entire frame — a sea of plain {HOME_PRIMARY}-and-"
        f"{HOME_SECONDARY} and {AWAY_PRIMARY}-and-{AWAY_SECONDARY} "
        f"scarves, knitted texture, slight motion, floodlight glow and "
        f"haze behind. Abstract, textural, emotional, 8K, Nikon Z9 50mm, "
        f"shallow depth of field. CRITICAL IP SAFETY: completely plain "
        f"scarves — NO text, words, club names, crests, logos or emblems "
        f"on any scarf; no sponsor text, no real venue, no readable text."
    ),
    "c5-city-pilgrimage": (
        f"Ultra-photorealistic cinematic photograph at dusk: a stream of "
        f"anonymous football supporters in plain solid {HOME_PRIMARY} and "
        f"{HOME_SECONDARY} casual clothing walking away from camera down "
        f"a generic ordinary city street toward a distant stadium glowing "
        f"with floodlights on the horizon, warm street lights, long "
        f"shadows, anticipation. Documentary feel, 8K, Nikon Z9 35mm. "
        f"CRITICAL IP SAFETY: generic anonymous city (no real skyline or "
        f"landmark), plain clothing only, no kits, club crests, sponsor "
        f"or maker logos, no shop-brand signage, no real venue, no real "
        f"player likeness, no readable text anywhere."
    ),
    "c6-floodlight-pylons": (
        "Ultra-photorealistic cinematic photograph, minimal and iconic: "
        "tall stadium floodlight pylons blazing with intense white light "
        "against a deep dark blue night sky, dramatic lens flare and "
        "light beams, faint haze, just a sliver of a glowing packed stand "
        "at the bottom edge. Moody, atmospheric, anticipatory, 8K, "
        "Nikon Z9 85mm. CRITICAL IP SAFETY: invented generic stadium, no "
        "real venue, no club logos, crests, sponsor text, advertising, "
        "signage, team names, real player likeness, or readable text."
    ),
    "c7-empty-dawn": (
        "Ultra-photorealistic cinematic photograph: a vast empty modern "
        "stadium at first light, pristine perfectly mown green pitch with "
        "mist drifting low, soft golden dawn rays raking across thousands "
        "of empty seats, total stillness and quiet anticipation before a "
        "big match. Wide, epic, serene, 8K, Nikon Z9 24mm. CRITICAL IP "
        "SAFETY: invented generic stadium, no real venue, no club logos, "
        "crests, sponsor text, advertising boards, scoreboard text, "
        "signage, team names, real player likeness, or readable text."
    ),
    "c8-ball-trail": (
        f"Ultra-photorealistic high-energy sports visual: a plain "
        f"unbranded white-and-black football streaking across a dark "
        f"dramatic background, frozen mid-flight with an explosive "
        f"dynamic motion trail of light and energy in {HOME_PRIMARY} and "
        f"{AWAY_PRIMARY} sweeping behind it, sparks and particles, sharp "
        f"ball, intense rim light. Betting-ad punchy, 8K, Nikon Z9 "
        f"200mm. CRITICAL IP SAFETY: plain ball with no brand or maker "
        f"mark, no logos, crests, sponsor text, real venue, real player "
        f"likeness, or readable text anywhere."
    ),
    "c9-matchday-stilllife": (
        f"Ultra-photorealistic premium still-life photograph on a worn "
        f"wooden changing-room bench: a pair of plain unbranded black "
        f"football boots, a plain unbranded white-and-black ball, and a "
        f"neatly folded plain {HOME_PRIMARY}-and-{HOME_SECONDARY} scarf, "
        f"soft directional window light, shallow depth of field, calm "
        f"matchday-ritual mood, 8K, Nikon Z9 50mm. CRITICAL IP SAFETY: "
        f"everything plain and unbranded — no maker marks, logos, crests, "
        f"sponsor or text on boots, ball or scarf; no real venue, no "
        f"readable text anywhere."
    ),
    "svs1-rival-split": (
        f"Ultra-photorealistic editorial sports photograph of two rival "
        f"supporter blocks in a COMPLETELY PACKED stadium at night, every "
        f"single seat and tier filled to the rafters with a massive dense "
        f"crowd, brilliant blazing floodlights and dramatic light beams "
        f"cutting through thick atmospheric smoke and haze. The two "
        f"blocks are in the SAME tiered grandstand at the SAME height, "
        f"TURNED SIDEWAYS TO FACE EACH OTHER across a narrow central "
        f"stairway aisle, in a fierce, heated, explosive face-off — "
        f"snarling intense expressions, veins bulging, mouths wide "
        f"mid-roar, fists and forearms thrust toward the rival end, "
        f"furious passionate aggression (intense rivalry energy, NOT "
        f"physical fighting or violence). LEFT block faces RIGHT: home "
        f"fans in plain solid {HOME_PRIMARY} and {HOME_SECONDARY} casual "
        f"clothing (plain tops/hoodies, no logos) with plain "
        f"{HOME_PRIMARY}-and-{HOME_SECONDARY} scarves stretched taut "
        f"overhead. RIGHT block faces LEFT: away fans mirrored at the "
        f"same height, plain solid {AWAY_PRIMARY} and {AWAY_SECONDARY} "
        f"clothing with plain {AWAY_PRIMARY}-and-{AWAY_SECONDARY} "
        f"scarves, roaring back. Both groups IN THE STANDS only — nobody "
        f"on the pitch or floor, no players or grass. Key visual: two "
        f"walls of fans turned inward facing each other, raw electric "
        f"hostility, deep high-contrast lighting, embers and smoke in "
        f"the air, epic scale, cinematic, hyper-detailed, 8K, Nikon Z9 "
        f"35mm. Diverse anonymous faces of all ages, gritty documentary "
        f"realism. CRITICAL IP SAFETY: plain clothing only, no kits, no "
        f"club crests or badges, no sponsor, maker or apparel-brand "
        f"logos (no swoosh, stripes or double-diamond marks), no text or "
        f"emblems on scarves, no national flags, no advertising boards, "
        f"no real venue, no real player likenesses, no readable text "
        f"anywhere."
    ),
    "svs2-rival-clash": (
        f"Ultra-photorealistic editorial sports photograph, tight "
        f"eye-level close-up of two rival supporter groups pressed "
        f"together in the stands at peak emotion. In the foreground a "
        f"passionate home fan in plain solid {HOME_PRIMARY} clothing "
        f"mid-roar, surrounded by a blur of {HOME_PRIMARY} and "
        f"{HOME_SECONDARY} supporters; sharply beside them an away fan in "
        f"plain solid {AWAY_PRIMARY} clothing reacting, backed by "
        f"{AWAY_PRIMARY} and {AWAY_SECONDARY} supporters. Plain scarves in "
        f"each team's two colours raised overhead, subtle face paint in "
        f"plain team colours (no emblems), intense contrast of elation "
        f"and tension. Shallow depth of field, floodlit night, diverse "
        f"anonymous faces, documentary realism, cinematic, 8K, Nikon Z9 "
        f"50mm. CRITICAL IP SAFETY: plain clothing only, no kits, no club "
        f"crests or badges, no sponsor or maker logos, no text or emblems "
        f"on scarves or flags, no advertising boards, no real venue, no "
        f"real player likenesses, no readable text anywhere."
    ),
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

    # ---- Crowd / fan-culture atmosphere (single team colour) ----
    "crowd-night": (
        f"Ultra-photorealistic editorial sports photograph from inside a "
        f"packed stand at eye level among the home supporters at dusk, "
        f"floodlights on, deep blue evening sky. A dense, joyous crowd of "
        f"diverse anonymous fans of all ages in plain solid {HOME_PRIMARY} "
        f"casual clothing — plain {HOME_PRIMARY} t-shirts, hoodies and "
        f"jackets, no logos — holding plain {HOME_PRIMARY}-and-"
        f"{HOME_SECONDARY} scarves stretched overhead with both hands, "
        f"arms raised, singing, a child on shoulders. The green pitch just "
        f"visible far below at the edge of frame. Warm stadium light, "
        f"electric celebratory emotion, gritty documentary realism, "
        f"shallow depth, cinematic, 8K, Nikon Z9 35mm. CRITICAL IP SAFETY: "
        f"plain clothing only — no kits, no club crests or badges, no "
        f"sponsor or maker logos (no Nike/Adidas/Puma marks), no text or "
        f"emblems on scarves, no advertising boards, no naming-rights "
        f"signage, no real venue, no real player likenesses."
    ),
    "crowd-goldenhour": (
        f"Ultra-photorealistic editorial sports photograph from inside a "
        f"packed traditional stand at golden hour, warm low sun, older "
        f"covered terrace with steel roof girders. A dense crowd of diverse "
        f"anonymous fans across generations — an older man, a teenager, "
        f"families — in plain solid {AWAY_PRIMARY} and {AWAY_SECONDARY} "
        f"casual clothing (plain tops, hoodies, no logos), holding plain "
        f"{AWAY_PRIMARY}-and-{AWAY_SECONDARY} scarves overhead, clapping, "
        f"singing, fists raised, glowing backlit by the sunset. The pitch "
        f"edge visible far left. Nostalgic, emotional, warm cinematic "
        f"colour, gritty documentary feel, 8K, Nikon Z9 35mm. CRITICAL IP "
        f"SAFETY: plain clothing only — no kits, no club crests or badges, "
        f"no sponsor or maker logos, no text or emblems on scarves, no "
        f"advertising boards, no naming-rights signage, no real venue, no "
        f"real player likenesses."
    ),
    "fan-hero-day": (
        f"Ultra-photorealistic cinematic sports photograph, dramatic low "
        f"angle looking slightly up at two or three jubilant anonymous "
        f"supporters in the stand on a bright sunny day, vivid blue sky "
        f"with sun flare, a vast modern stadium bowl behind them blurred "
        f"into glowing bokeh. The fans wear plain solid {HOME_PRIMARY} "
        f"casual clothing (plain {HOME_PRIMARY} t-shirts/polos, no logos) "
        f"and one holds a plain {HOME_PRIMARY}-and-{HOME_SECONDARY} scarf "
        f"stretched high overhead with both arms, mouth open mid-roar, pure "
        f"elation. Heroic, premium, high-contrast composite look, shallow "
        f"depth of field, 8K, Nikon Z9 35mm. CRITICAL IP SAFETY: plain "
        f"clothing only — no kits, no club crests or badges, no sponsor or "
        f"maker logos, no text or emblems on the scarf, no advertising "
        f"boards, no naming-rights signage, no real venue, no real player "
        f"likenesses."
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
