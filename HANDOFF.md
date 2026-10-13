# Sip Guilds Guild Crawler: Handoff to To-Do Teddy and the Sipopedia team

Prepared 2026-10-13 by SipChief. Every fact below was checked against the repo at commit `ccbeca5` (2026-10-12 18:49 PT).

## 1. What it is
- A one-page WebGL atlas (Three.js 0.160.0 + UnrealBloomPass, static files) that follows Sipopedia.com's structure: **5 guilds, 15 academies, 283 subgenres and 1,772 styles**.
  - Cask: Wine, Beer, Spirits
  - Steep: Coffee, Tea, Kombucha
  - Source: Water, Juice, Milk
  - Energy: Health, Protein, Energy
  - Culture: Carbonated, Fermented, Regional
- A crawler sits at the center of each subgenre and shoots one arm per style. The layout is a **spiral nebula** with one arm per guild and academies as knots along each arm. It has swirling dust and haze, which turn off when the viewer prefers reduced motion.
- The crawler starts with about a 4 s hold on the All Guilds overview, then crawls the stops, then zooms out to all guilds at the finale. A full loop takes about 31 min at 1×.
- The **STYLES EXPLORED** counter shows cumulative styles out of the total. It is recomputed whenever you jump.
- Controls:
  - ⏪ previous academy / ⏮ previous stop / ⏯ / ⏭ next stop / ⏩ next academy.
  - Keyboard: ← → move by stop, **Shift+← →** or PageUp/PageDown move by academy, and Space plays or pauses.
  - Speed button: **½× / 1× / 2× / 4×** (key S). The code also has 4×, so it's more than just ½/1/2.
  - Clicking a guild or academy in the panel jumps there.
- **Wine** is split into Testable and Non-Testable grapes by country, plus non-vinifera, PIWI, clones, mutations, teinturiers, rootstocks, canopy and winemaking.
- **Definition cards**: every tag is clickable. `data/definitions.json` is built by `build/definitions.py` from `build/defs_curated.py`, and the commit log reports 0 entries needing review.

## 2. Where it lives
- Repo: https://github.com/Sip-Coder/sip-guilds (branch `main`)
- Live: https://sip-coder.github.io/sip-guilds/ (GitHub Pages, `.nojekyll`; it returned HTTP 200 on 2026-10-13)
- Key files:
  - `index.html`: the whole app
  - `data/guilds.json`: guild > academy > subgenre > styles
  - `data/guilds.pdf`: outline
  - `data/definitions.json`
  - `build/taxonomy.py`, `build/depth.py`, `build/aging.py`, `build/definitions.py`, `build/defs_curated.py`: data generators
  - `build/stamp.sh`: cache-busting
  - `build/check_overlaps.sh` + `build/check.html`: QA
  - `previews/`: screenshots
  - `version.json`
  - `README.md`: the full list of sources

## 3. Run, QA and deploy
1. Run it locally with `python3 -m http.server` in the repo root and open `/`. Preview helpers: `?stop=<i>&t=<sec>`, `?seek=<sec>`, `?stop=-1` (intro) and `?stop=k&def=ID` (definition card).
2. After editing data, rerun the matching `build/*.py` generator.
3. **QA, no overlapping labels:** `build/check_overlaps.sh` uses headless Chrome to visit all **121 stops** at 390×844, 768×1024 and 1440×900. It must print `PASS`, meaning zero label or zone intersections and no offscreen labels.
4. Run `build/stamp.sh` before each commit. It writes the content hash into `index.html` (`VER`) and `version.json` so phones reload stale caches.
5. To deploy, commit and push to `main`. GitHub Pages serves it from there.

## 4. Open work and status
- **The site is PARKED.** Don't do any new feature work unless Jonathan restarts it.
- **Legal aging minimums:** the Aging Requirements groups are already in the taxonomy (`build/aging.py`, commits `99ecf30`, `4dfa38b`, `095747e`). Every entry names its regulation and is marked "verified online 2026-10-12". Tequila (NOM-006) and Mezcal (NOM-070) are now separate. The remaining work is extending or maintaining this list as regulations change.
- No `TODO` or `FIXME` markers are in the source.
- No direct references to this repo were found under `/workspace/Sipopedia`. The crawler is standalone, and its guild and academy names mirror Sipopedia.
- **Never touch sipopedia.com (deploys, DNS, content) without Jonathan's explicit OK.**

## 5. Jonathan's rules
- Every `.md`, `.csv`, `.docx` or `.pptx` needs a PDF beside it (for example, this file has `HANDOFF.pdf`).
- Sipopedia's look is **teal and gold**. Keep the crawler's teal/gold theme.
