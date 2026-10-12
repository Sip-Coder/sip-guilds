# Sip Studies — Guild Crawler (Sipopedia academies)

A one-page WebGL atlas matching Sipopedia.com's structure: **5 guilds → 15 academies → 121 subgenres → 633 styles**. The crawler sits at the center of each subgenre (center label, e.g. "SPARKLING · Wine Academy · Cask Guild") and shoots one arm per style, then zooms out to all guilds. Full loop ≈ 13.5 min.

**Live:** https://sip-coder.github.io/sip-guilds/

- Controls: ⏮ / ⏸▶ / ⏭ buttons, keyboard ← → and Space; click a guild/academy in the GUILDS · ACADEMIES panel to jump there.
- Data: [`data/guilds.json`](data/guilds.json) (guild > academy > subgenre > styles) · outline [`data/guilds.pdf`](data/guilds.pdf) · generator `build/taxonomy.py`.
- Placement choices: sake, cider, perry and mead live in **Fermented Academy** (Culture Guild); NA beer/wine and zero-proof spirits sit inside the Beer/Wine/Spirits academies; club soda/tonic moved to Carbonated; yerba mate moved from Tea to Regional, guayusa to Energy.
- Static files; Three.js 0.160.0 (unpkg) + UnrealBloomPass; GPU-side per-subgenre lighting; respects `prefers-reduced-motion`. Preview helpers: `?stop=<index>&t=<sec>` or `?seek=<sec>`.

## Taxonomy sources
- Beer: BJCP 2021 Beer Style Guidelines, categories 1–34 — https://www.bjcp.org/style/2021/beer/
- Mead & cider/perry: BJCP 2015 Mead and 2025 Cider Guidelines — https://www.bjcp.org/
- Wine: WSET Level 2/3 specifications (styles, principal grapes, sparkling/fortified/sweet) — https://www.wsetglobal.com/
- Spirits: US TTB Standards of Identity, 27 CFR 5.22/5.143 — https://www.ecfr.gov/current/title-27/chapter-I/subchapter-A/part-5 ; Scotch Whisky Regulations 2009; Irish Whiskey Technical File; Japan Spirits & Liqueurs Makers Assn. labeling standard (2021); NOM-006-SCFI (tequila), NOM-070-SCFI (mezcal); BNIC (Cognac age statements)
- Sake: Japan National Tax Agency, tokutei meishoshu labeling standards — https://www.nta.go.jp/english/
- Coffee: Specialty Coffee Association (processing, brew methods) — https://sca.coffee/
- Tea: ISO 20715:2023 tea classification by manufacturing process (white, yellow, green, oolong, black, dark)
- Water: US FDA 21 CFR 165.110 bottled water standard of identity (spring, mineral, artesian, purified, sparkling)
- Non-alc: US TTB/FDA definitions for dealcoholized (<0.5% ABV) beverages; common market categories
- Juice: US FDA 21 CFR 101.30 (percentage juice declaration) and 21 CFR 120 (juice HACCP; unpasteurized warning)
- Milk: US FDA Grade "A" Pasteurized Milk Ordinance; 21 CFR 131 (milk fat levels)
- Health/medical drinks: WHO oral rehydration salts formula; IDDSI framework (thickened drinks)
- Protein/energy: US FDA dietary supplement & caffeine guidance; EFSA scientific opinion on caffeine safety (2015)
- Kombucha & fermented drinks: Kombucha Brewers International code of practice; BJCP 2025 cider and 2015 mead guidelines
