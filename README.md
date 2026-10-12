# Sip Studies — Guild Crawler

A one-page WebGL demo: a crawler travels through 8 beverage guilds and **84 subgenres** (440 styles), visiting each subgenre sub-cluster and shooting tendrils to its style tags, then zooms out to show every guild lit. Loop ≈ 4.5 min.

**Live:** https://sip-coder.github.io/sip-guilds/

- Taxonomy data: [`data/guilds.json`](data/guilds.json) (guild > subgenre > styles) · readable outline: [`data/guilds.pdf`](data/guilds.pdf) · generator: `build/taxonomy.py`
- Static files only. Three.js 0.160.0 (unpkg) with EffectComposer + UnrealBloomPass; particle lighting is GPU-side (per-subgenre data texture sampled in the vertex shader).
- Autoplays; respects `prefers-reduced-motion`; dashboard collapses on mobile. `?seek=<seconds>` freezes at a timestamp (used for `previews/`).

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
