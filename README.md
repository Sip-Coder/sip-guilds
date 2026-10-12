# Sip Studies — Guild Crawler (Sipopedia academies)

A one-page WebGL atlas matching Sipopedia.com's structure: **5 guilds → 15 academies → 155 subgenres → 861 styles (optional sub-subgenre `parent`, e.g. Milk › Cream & Cream Products › Fluid Creams)**. The crawler sits at the center of each subgenre (center label, e.g. "SPARKLING · Wine Academy · Cask Guild") and shoots one arm per style, then zooms out to all guilds. Full loop ≈ 16 min.

**Live:** https://sip-coder.github.io/sip-guilds/

- Controls: ⏪ previous academy (first press = start of current academy) / ⏮ previous stop / ⏯ / ⏭ next stop / ⏩ next academy; keyboard ← → (stop), Shift+← → or PageUp/PageDown (academy), Space; click a guild/academy in the GUILDS · ACADEMIES panel to jump there.
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
- Milk & cream: US FDA 21 CFR Part 131 standards of identity — milk §131.110, acidified §131.111, cultured §131.112, concentrated §131.115, sweetened condensed §131.120, nonfat dry §131.125, evaporated §131.130, dry whole §131.147, dry cream §131.149, heavy cream §131.150, light cream §131.155, light whipping §131.157, sour cream §131.160/.162, eggnog §131.170, half-and-half §131.180, sour half-and-half §131.185/.187, yogurt §131.200 — https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-131 ; reduced/low/fat-free naming per 21 CFR 101.62 & 130.10; Grade "A" Pasteurized Milk Ordinance; UK cream fat minimums per UK Dairy industry/Food Standards Agency guidance; USDA National Organic Program (organic)
- Barrel Toasting & Aging (shared reference under Wine Academy; Spirits adds char levels, cask finishes, maturation systems, NOM-006 agave aging; Beer, Fermented and Coffee add barrel-aged styles and cross-reference the shared lists): Independent Stave Co. / ISC char & toast guides; Seguin Moreau and Tonnellerie François Frères cooperage references (forests, seasoning, toast); Scotch Whisky Association cask types; US 27 CFR 5.143 (bourbon new charred oak; bottled-in-bond); NOM-006-SCFI-2012 (tequila aging classes)
- Cocktails: International Bartenders Association official list (Unforgettables / Contemporary Classics / New Era) — https://iba-world.com/cocktails/all-cocktails/
- Decaffeination & coffee formats: SCA; Swiss Water Decaf Co. process notes
- Health/medical drinks: WHO oral rehydration salts formula; IDDSI framework (thickened drinks)
- Protein/energy: US FDA dietary supplement & caffeine guidance; EFSA scientific opinion on caffeine safety (2015)
- Kombucha & fermented drinks: Kombucha Brewers International code of practice; BJCP 2025 cider and 2015 mead guidelines

## Label layout & overlap check
The scene is a spiral nebula: one arm per guild (noisy log-like spiral, varied curvature/width), academies as knots along each arm, subgenres as knots within, plus color-blended dust, a bright core and soft gas haze that slowly swirl (disabled with reduced motion). The crawler travels along the arms (through the core between guilds). The dashboard counts STYLES EXPLORED (cumulative styles / total, recomputed on jump).

Tags are placed per stop by a deterministic screen-space solver (rings/angles around the crawler, greedy placement with 4px padding) that treats the header, step title, center label, crawler core, controls and dashboard as reserved zones; font steps down (min 10px) if needed. Layout is locked per stop and recomputed on resize. `build/check_overlaps.sh` visits all 121 stops at 390×844, 768×1024 and 1440×900 (exact iframe viewports via `build/check.html` + `?check=1`) and fails on any intersection or offscreen label.
