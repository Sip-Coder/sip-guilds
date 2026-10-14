# Sip Studies — Guild Crawler (Sipopedia academies)

A one-page WebGL atlas matching Sipopedia.com's structure: **5 guilds → 15 academies → 283 subgenres → 1,772 styles (optional sub-subgenre `parent`, e.g. Milk › Cream & Cream Products › Fluid Creams)**. The crawler sits at the center of each subgenre (center label, e.g. "SPARKLING · Wine Academy · Cask Guild") and shoots one arm per style, then zooms out to all guilds. Full loop ≈ 31 min at 1× (speed button: ½×/1×/2×/4×, key S).

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
- Production/cultivation/science depth (build/depth.py): SCA Coffee Value Assessment & cupping protocol, SCA Water Quality Handbook, World Coffee Research Arabica Variety Catalog & Sensory Lexicon (https://varieties.worldcoffeeresearch.org/); ISO 3720 (black tea) & ISO 11287 (green tea), Tea Research Association / Japan Tea Central Council processing guides; Kombucha Brewers International code of practice & TTB kombucha guidance; FDA Grade "A" PMO, USDA NOP pasture rule, Fox & McSweeney *Dairy Chemistry and Biochemistry*; Brewers Association hop variety and malt guides, BJCP; Japan Sake & Shochu Makers Association (brewing process, seimaibuai); US EPA SDWA, FDA 21 CFR 120 (juice HACCP); DSHEA (1994), FDA caffeine guidance, EFSA caffeine opinion (2015); FAO/WHO protein quality (DIAAS, 2013)
- Wine grapes, genetics & viticulture (Testable/Non-Testable varieties by country, non-vinifera species & hybrids, PIWI, clones, mutations, teinturiers, rootstocks, canopy, winemaking): Robinson, Harding & Vouillamoz, *Wine Grapes* (2012); Vitis International Variety Catalogue (VIVC, JKI) — https://www.vivc.de/ ; UC Davis Foundation Plant Services (clone/rootstock registry) — https://fps.ucdavis.edu/ ; PIWI International — https://piwi-international.de/ ; WSET Diploma D1 (viticulture & winemaking)
- Barrel Toasting & Aging (shared reference under Wine Academy; Spirits adds char levels, cask finishes, maturation systems, NOM-006 agave aging; Beer, Fermented and Coffee add barrel-aged styles and cross-reference the shared lists): Independent Stave Co. / ISC char & toast guides; Seguin Moreau and Tonnellerie François Frères cooperage references (forests, seasoning, toast); Scotch Whisky Association cask types; US 27 CFR 5.143 (bourbon new charred oak; bottled-in-bond); NOM-006-SCFI-2012 (tequila aging classes)
- Cocktails: International Bartenders Association official list (Unforgettables / Contemporary Classics / New Era) — https://iba-world.com/cocktails/all-cocktails/
- Decaffeination & coffee formats: SCA; Swiss Water Decaf Co. process notes
- Health/medical drinks: WHO oral rehydration salts formula; IDDSI framework (thickened drinks)
- Protein/energy: US FDA dietary supplement & caffeine guidance; EFSA scientific opinion on caffeine safety (2015)
- Kombucha & fermented drinks: Kombucha Brewers International code of practice; BJCP 2025 cider and 2015 mead guidelines

## Label layout & overlap check
The scene is a spiral nebula: one arm per guild (noisy log-like spiral, varied curvature/width), academies as knots along each arm, subgenres as knots within, plus color-blended dust, a bright core and soft gas haze that slowly swirl (disabled with reduced motion). The crawler travels along the arms (through the core between guilds). The dashboard counts STYLES EXPLORED (cumulative styles / total, recomputed on jump).

Tags are placed per stop by a deterministic screen-space solver (rings/angles around the crawler, greedy placement with 4px padding) that treats the header, step title, center label, crawler core, controls and dashboard as reserved zones; font steps down (min 10px) if needed. Layout is locked per stop and recomputed on resize. `build/check_overlaps.sh` visits all 121 stops at 390×844, 768×1024 and 1440×900 (exact iframe viewports via `build/check.html` + `?check=1`) and fails on any intersection or offscreen label.

## Cache-busting
`build/stamp.sh` writes a content hash into `index.html` (`VER`) and `version.json`. On load the page fetches `version.json` with `no-store`; if a phone has an older cached page it reloads once with `?v=<hash>`. Data is fetched as `data/guilds.json?v=<hash>`.

## Aging Requirements sources
`build/aging.py`: every entry's detail field names its regulation and is marked **[verified online 2026-10-12]**. Sources checked: DOCa Rioja pliego (2024), Ribera del Duero pliego (2023), Ley 24/2003 art. 3 (historical; repealed by Ley 6/2015) + DO pliegos now binding, DOP Cava, DOP Jerez (2024), Chianti Classico / Chianti DOCG Riserva / Brunello / Vino Nobile / Barolo / Barbaresco / Amarone / Taurasi / Franciacorta / Trento disciplinari, INAO cahiers (Champagne, Crémant d'Alsace/Bourgogne/Loire, Crémant du Jura, Côtes du Jura, Banyuls GC, Rivesaltes, Cognac, Calvados, Rhum de la Martinique), IVDP Special Categories (Port), IVBAM / Portaria 39/2015 (Madeira), Tokaj PDO, Sektbezeichnungsverordnung (Sekt Austria / Reserve / Große Reserve; Klassik retired), NOM-006-SCFI-2012, NOM-070-SCFI-2016, Scotch Whisky Regulations 2009, Irish Whiskey Act 1980, Canadian FDR B.02.023 / B.02.020, JSLMA standard, 27 CFR 5.74/5.88, BNIA Armagnac XO (10 yr from 2018), pliego IG Brandy de Jerez, Grappa IG disciplinare, Jamaica Rum GI (no age floor), Reglamento DO Pisco. Corrections this pass: Austrian Große Reserve 36 mo (not 30); Sekt Austria naming; Ley 24/2003 repealed note; Crémant 9 mo lees + often 12 mo to consumer.

## Intro overview
On load and at each loop restart the crawler holds on the All Guilds overview (stop 0, styles counter 0 / total) for about 4 s, then flies to Wine / Testable Red. While paused it stays put. ⏮ or ⏪ from the first Wine stop goes back to the intro; ⏩ and ⏭ from the finale skip it. `?stop=-1` freezes on the intro.

## Definition cards
Every tag and the center label is a button (click/tap, or Tab + Enter). It opens a definition card (a dialog on desktop, a bottom sheet on mobile) showing the term, its path, a plain-language definition, key facts and the source. Opening a card pauses playback. Close it with ✕, Esc, Close or a tap outside; **Resume ▶** closes the card and resumes playback. Data: `data/definitions.json` (keyed by id: subgenre `g.a.s`, style `g.a.s.n`), generated by `build/definitions.py` from `build/defs_curated.py`. Entries without a hand-written definition get a cautious, context-only definition flagged `needs_review: true`. The PDF glossary lists only reviewed entries. `?stop=k&def=ID` opens a card for screenshots.

## Definition infographics
Every definition card ends with a small data-driven infographic (`js/infographic.js`, HTML + inline SVG, no images). It uses only fields that exist in `data/guilds.json` and `data/definitions.json`:
- **All entries:** guild icon in the academy colour, path breadcrumb (Guild › Academy › parent › subgenre › style).
- **Styles:** position strip ("3 of 8 in Rioja") and related-style chips (tap to open that card).
- **Groups:** size bar against the largest group in the academy, member chips and neighbouring groups.
- **Aging:** total / wood / bottle / lees bars when the term name states them (e.g. "Reserva · 3 yr (1 oak, 6 mo btl)"), scaled to the longest requirement in that group; ranges are skipped.
- **ABV:** a 0–20% (or 0–100%) gauge when the term or definition states an ABV.
`build/check_infographics.sh` opens all 2,197 cards at 390×844, 768×1024 and 1440×900 and fails if any card lacks an infographic (path, icon, chips) or overflows horizontally.

## Illustrated cards
Each definition's infographic opens with an illustrated card (`cards/generated/<id>.svg`, about 10 KB each, lazy-loaded) above the data panel. `build/oneliners.py` writes `data/oneliners.json`: one sentence of 140 characters or less per term. It is built only from our definitions and guilds data. BJCP beer styles use paraphrased BJCP overall impressions from `build/beer_lines.py`, and a few long entries are shortened by hand. `build/cards.py --all` draws every card in about 2 s. Each card is a procedural flat-line scene (vessel, ingredients, setting, time of day) chosen from the term's data and seeded by its id. Its text is the clean term name in a serif title, a tag chip (region, age, parenthetical), the one-liner and a guild/academy label. Every card uses the same fixed sizes: title 66, one-liner 38, chip 22, label 21. Long titles wrap to at most 3 lines. A one-liner that is too long is cut at a clause boundary rather than shrunk. `build/check_cards.py` asserts uniform font sizes, no text overflow and a card for every term. Run it with `build/check_infographics.sh` and `build/check_overlaps.sh` before each push.
