import json
OLD={g['name']:{s['name']:s['styles'] for s in g['subgenres']} for g in json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__),'base_v1.json')))['guilds']} if __import__('os').path.exists(__import__('os').path.join(__import__('os').path.dirname(__file__),'base_v1.json')) else None
def S(s): return [x.strip() for x in s.split(';')]
def old(g,drop=(),edit={}):
  out=[]
  for n,st in OLD[g].items():
    if n in drop: continue
    st=[x for x in st if x not in edit.get(n,[])]; out.append((n,'; '.join(st)))
  return out
W=old('WATER',edit={'Sparkling Water':['Club soda','Tonic water']})+[("Tap & Treated","Municipal tap water; Private well water; Carbon-filtered; Boiled (point-of-use); UV-treated")]
C=old('COFFEE')+[("Barrel-Aged Coffee","Green beans rested in bourbon barrels; Rum barrel-aged beans; Wine barrel-aged beans; Whiskey barrel-aged cold brew","Barrel Toasting & Aging"),("Decaffeination","Swiss Water Process; CO2 (supercritical) process; Ethyl acetate (sugarcane) process; Methylene chloride (direct/indirect) process"),
 ("Coffee Formats","Whole bean; Ground; Instant (freeze-dried); Instant (spray-dried); Single-serve pods/capsules; Coffee concentrate; Drip bags"),
 ("Iced & Blended Drinks","Iced coffee; Iced latte; Nitro cold brew; Frappé (Greek); Blended iced coffee (frappuccino-style); Espresso tonic; Dalgona coffee; Shakerato")]
T=old('TEA',edit={'Herbal Tisanes':['Yerba mate','Guayusa']})+[("Scented & Blended","Jasmine tea; Earl Grey (bergamot); Lychee black; Rose black; Osmanthus oolong; Chai spice blend"),
 ("Tea Drinks","Iced tea; Sweet tea (US South); Milk tea; Chai latte; Matcha latte; London fog; Arnold Palmer (tea + lemonade)"),
 ("Tea Formats","Loose leaf; Tea bags; Pyramid sachets; Compressed cakes/bricks; Powdered (matcha/instant); RTD bottled tea")]
WI=[(('Testable '+n) if n in ('Red','White') else n,st) for n,st in old('WINE')]+[("France","Tannat; Petit Verdot; Carignan; Cinsault; Pinot Meunier; Négrette; Mondeuse; Poulsard; Trousseau; Fer Servadou","Non-Testable Red"),
 ("Italy","Aglianico; Nero d'Avola; Montepulciano; Dolcetto; Corvina; Lagrein; Sagrantino; Nerello Mascalese; Teroldego; Schiava","Non-Testable Red"),
 ("Spain & Portugal","Mencía; Bobal; Graciano; Prieto Picudo; Touriga Nacional; Touriga Franca; Baga; Castelão","Non-Testable Red"),
 ("Central & Eastern Europe","Blaufränkisch; Zweigelt; St. Laurent; Kadarka; Plavac Mali; Xinomavro; Agiorgitiko; Fetească Neagră; Mavrud","Non-Testable Red"),
 ("New World","Carménère (Chile); País (Chile); Pinotage (South Africa); Bonarda (Argentina)","Non-Testable Red"),
 ("France","Marsanne; Roussanne; Melon de Bourgogne; Aligoté; Petit Manseng; Gros Manseng; Savagnin; Picpoul; Clairette; Mauzac","Non-Testable White"),
 ("Italy","Garganega; Vermentino; Fiano; Greco; Falanghina; Cortese; Arneis; Trebbiano; Verdicchio; Friulano","Non-Testable White"),
 ("Spain & Portugal","Verdejo; Godello; Macabeo (Viura); Xarel·lo; Parellada; Palomino; Loureiro; Arinto; Encruzado","Non-Testable White"),
 ("Central & Eastern Europe","Furmint; Hárslevelű; Welschriesling; Silvaner; Müller-Thurgau; Kerner; Rkatsiteli; Moschofilero; Malagousia","Non-Testable White"),
 ("Other","Muscat of Alexandria; Colombard; Chasselas; Petite Arvine","Non-Testable White"),
 ("Vitis labrusca","Concord; Catawba; Niagara; Isabella; Ives","Non-Vitis vinifera"),
 ("Vitis riparia & rupestris","Vitis riparia (riverbank grape); Vitis rupestris (rock grape); Vitis berlandieri; Mainly rootstock parents — see Rootstocks","Non-Vitis vinifera"),
 ("Vitis rotundifolia (Muscadine)","Scuppernong; Carlos; Noble; Magnolia","Non-Vitis vinifera"),
 ("Vitis aestivalis","Norton (Cynthiana)","Non-Vitis vinifera"),
 ("Interspecific Hybrids","Seyval Blanc; Vidal Blanc; Chambourcin; Baco Noir; Maréchal Foch; Traminette; Marquette; Frontenac; La Crescent","Non-Vitis vinifera"),
 ("PIWI (Fungus-Resistant)","Regent; Solaris; Johanniter; Souvignier Gris; Cabernet Cortis; Muscaris; Divico","Non-Vitis vinifera"),
 ("Clones","Pinot Noir Dijon 115; Pinot Noir Dijon 667; Pinot Noir Dijon 777; Pinot Noir Pommard (UCD 4); Pinot Noir Wädenswil (UCD 1A); Chardonnay Dijon 76; Chardonnay Dijon 96; Chardonnay Wente; Cabernet Sauvignon 337; Sangiovese Grosso (Brunello)","Vine Genetics"),
 ("Mutations (Bud Sports)","Pinot Gris (from Pinot Noir); Pinot Blanc; Pinot Meunier (chimera); Grenache Blanc; Grenache Gris; Gewürztraminer (aromatic Savagnin Rose); Chardonnay Musqué; Sauvignon Gris","Vine Genetics"),
 ("Teinturiers (Red-Fleshed)","Alicante Bouschet; Saperavi; Petit Bouschet; Grand Noir de la Calmette; Gamay de Bouze; Rubired","Vine Genetics"),
 ("Riparia & Rupestris Types","Riparia Gloire de Montpellier; Rupestris du Lot (St. George); 3309 Couderc; 101-14 Millardet et de Grasset; Schwarzmann","Rootstocks"),
 ("Berlandieri × Riparia","5BB Kober; SO4; 5C Teleki; 420A Millardet et de Grasset","Rootstocks"),
 ("Berlandieri × Rupestris","110 Richter; 1103 Paulsen; 140 Ruggeri; 99 Richter","Rootstocks"),
 ("Nematode-Resistant & Other","Freedom; Harmony; Dog Ridge; Ramsey (Salt Creek); 1616 Couderc; Own-rooted (ungrafted)","Rootstocks"),
 ("Training Systems","Single Guyot; Double Guyot; Bilateral cordon (spur-pruned); Vertical shoot positioning (VSP); Gobelet (bush vine); Pergola; Lyre; Scott Henry; Smart-Dyson; Geneva Double Curtain; Sprawl","Canopy Management"),
 ("Canopy Practices","Cane pruning; Spur pruning; Shoot thinning; Shoot positioning; Leaf removal; Hedging (topping); Green harvest (crop thinning); Cover crops","Canopy Management"),
 ("Red Winemaking","Destemming; Whole-cluster fermentation; Cold soak; Carbonic maceration; Pump-over (remontage); Punch-down (pigeage); Délestage (rack & return); Extended maceration; Saignée; Malolactic conversion","Winemaking Techniques"),
 ("White & Rosé Winemaking","Whole-bunch pressing; Skin contact; Cold settling (débourbage); Cool fermentation; Lees aging (sur lie); Bâtonnage; Direct-press rosé; Blocked malolactic","Winemaking Techniques"),
 ("Sparkling Methods","Traditional method; Tank (Charmat) method; Ancestral method; Transfer method; Riddling (remuage); Disgorgement; Dosage; Carbonation","Winemaking Techniques"),
 ("Fortified & Oxidative","Mutage (fortification during fermentation); Post-fermentation fortification; Flor (biological aging); Oxidative aging; Estufagem (Madeira)","Winemaking Techniques"),
 ("Finishing","Fining; Filtration; Cold stabilization; Blending","Winemaking Techniques"),("Oak & Other Woods","American white oak (Quercus alba); French sessile oak (Q. petraea); French pedunculate oak (Q. robur); Hungarian oak (Q. petraea); Oregon oak (Q. garryana); Mizunara (Q. mongolica, Japan); Acacia (black locust); Chestnut (Castanea sativa); Cherry (Prunus avium); Amburana (Brazil)","Barrel Toasting & Aging"),
 ("French Oak Forests","Allier; Tronçais (Allier); Nevers; Bertranges; Vosges; Limousin (wide grain, Cognac); Jupilles","Barrel Toasting & Aging"),
 ("Seasoning","Open-air seasoning (typically 24–36 months); Kiln-dried staves; Rain & sun leaching of harsh tannins","Barrel Toasting & Aging"),
 ("Toast Levels","Light toast; Medium toast; Medium-plus toast; Heavy toast; Toasted heads; Untoasted heads; See Spirits Academy: char levels","Barrel Toasting & Aging"),
 ("Barrel Sizes","Blood tub (~40 L); Quarter cask (~125 L); American standard barrel (200 L / 53 gal); Bordeaux barrique (225 L); Burgundy pièce (228 L); Hogshead (~250 L); Puncheon (~450–500 L); Sherry butt (~500 L); Port pipe (~550–650 L); Foudre / foeder (1,000 L+)","Barrel Toasting & Aging"),
 ("New vs Used","New oak; First fill; Refill (second fill+); Neutral oak (3+ uses); Rejuvenated (re-toasted/re-charred); Percentage new oak (wine élevage)","Barrel Toasting & Aging"),("Wine-Based Drinks","Sangria; Spritzer; Wine cooler; Mulled wine; Kalimotxo (wine + cola)"),("Dealcoholized Wine (≤0.5% ABV)","Dealcoholized red; Dealcoholized white; Dealcoholized sparkling; Dealcoholized rosé")]
B=[(n,st) for n,st in old('BEER')]+[("Barrel-Aged & Wood Beers","Bourbon barrel-aged imperial stout; Barrel-aged barleywine; Foeder-fermented beer; Wine-barrel sour; Brettanomyces aged in oak; Lambic in oak foudres; See Wine Academy: oak, toast, sizes","Barrel Toasting & Aging"),("Flavored Malt & Hard Seltzer (outside BJCP)","Hard seltzer; Flavored malt beverage; Malt liquor; Hard root beer/soda; Hard tea"),("NA & Low-Alcohol Beer (outside BJCP)","Non-alcoholic lager (≤0.5% ABV); Non-alcoholic IPA; Non-alcoholic stout; Radler/shandy")]
SP=old('SPIRITS')+[("Char Levels","#1 char (light); #2 char; #3 char (common for bourbon); #4 char (alligator); Toast + char (two-step); See Wine Academy: oak, forests, sizes","Barrel Toasting & Aging"),
 ("Cask Finishes","Ex-bourbon; Oloroso sherry; Pedro Ximénez (PX) sherry; Fino/Amontillado sherry; Port (ruby/tawny); Madeira; Sauternes; Red wine; Rum cask; Cognac cask; Beer/stout cask","Barrel Toasting & Aging"),
 ("Maturation Systems","Solera (criaderas y solera); Angel's share (evaporation); Dunnage warehouse; Rickhouse (rackhouse); Palletized warehouse; Tropical maturation; Bottled-in-Bond (≥4 years, US)","Barrel Toasting & Aging"),
 ("Agave Aging (NOM-006)","Tequila Reposado (≥2 months in oak); Tequila Añejo (≥1 year, ≤600 L oak); Tequila Extra Añejo (≥3 years, ≤600 L oak); Cristalino (aged, then filtered)","Barrel Toasting & Aging"),("Other Regional Spirits","Aquavit (akvavit); Rakı; Arak; Pálinka; Slivovitz (šljivovica); Singani; Feni"),
 ("The Unforgettables","Old Fashioned; Manhattan; Dry Martini; Negroni; Daiquiri; Whiskey Sour; Sidecar; Sazerac; Boulevardier; Martinez","Cocktails (IBA)"),
 ("Contemporary Classics","Margarita; Mojito; Cosmopolitan; Moscow Mule; Mai Tai; Piña Colada; Bloody Mary; Caipirinha; Mimosa; French 75","Cocktails (IBA)"),
 ("New Era Drinks","Espresso Martini; Spritz Veneziano; Penicillin; Paper Plane; Tommy's Margarita; Naked and Famous","Cocktails (IBA)"),("Zero-Proof","Virgin cocktails (mocktails); Non-alcoholic gin alternatives; Non-alcoholic whiskey alternatives; Non-alcoholic aperitif/bitter alternatives; Shrub-based drinks")]
SC=old('SAKE · CIDER · MEAD')
G=[
("CASK GUILD","Fermentation, transformation, and time","Grouped by maturation, cellar craft, and cellar-to-service.","#ff3b7a",[
 ("Wine Academy","#ff3b7a",WI),("Beer Academy","#ffd23c",B),("Spirits Academy","#b06bff",SP)]),
("STEEP GUILD","Leaf, seed, culture, and extraction","Grouped by extraction, infusion, sensory calibration, and ritual.","#7dff6a",[
 ("Coffee Academy","#ff9a3c",C),("Tea Academy","#7dff6a",T),
 ("Kombucha Academy","#c8ff3c",[
  ("Culture & Fermentation","SCOBY (bacterial cellulose pellicle); Starter liquid (backslopping); Primary fermentation (F1); Secondary fermentation (F2, bottle conditioning)"),
  ("Base Teas","Black tea kombucha; Green tea kombucha; Oolong kombucha; White tea kombucha; Herbal/rooibos-base kombucha"),
  ("Kombucha Styles","Original/plain; Fruit-flavored; Ginger; Botanical/herbal; Hard kombucha (>0.5% ABV)"),
  ("Related Cultures","Jun (green tea and honey); Kombucha vinegar")])]),
("SOURCE GUILD","Origin, nourishment, and custody","Grouped by foundational ingredients, safe processing, freshness, and custody.","#2ee6ff",[
 ("Water Academy","#2ee6ff",W),
 ("Juice Academy","#ffb03c",[
  ("Product Types (FDA)","100% juice; Juice from concentrate; Nectar; Juice drink/cocktail; Smoothie; Lemonade; Limeade; Fruit punch"),
  ("Processing","Not-from-concentrate (NFC); Fresh-squeezed (unpasteurized, warning label); Flash-pasteurized; Cold-pressed (HPP); Frozen concentrate"),
  ("Citrus","Orange; Grapefruit; Lemon; Lime; Tangerine/mandarin; Blood orange"),
  ("Pome & Stone Fruit","Apple (cloudy/clear); Pear; Tart cherry; Peach nectar; Apricot nectar"),
  ("Berry & Grape","Concord grape; Cranberry; Pomegranate; Blueberry; Açaí; Elderberry"),
  ("Tropical","Pineapple; Mango; Passion fruit; Guava; Papaya; Coconut water"),
  ("Vegetable","Tomato; Carrot; Beet; Celery; Green juice (kale/spinach/cucumber); Mixed vegetable juice")]),
 ("Milk Academy","#e8f4ff",[
  ("Fat Level: Whole, 2%, 1%, Skim","Whole milk (≥3.25% milkfat); Reduced-fat milk (2%); Low-fat milk (1%); Fat-free/skim milk (<0.5%)",None,"Whole milk: 21 CFR 131.110"),
  ("Fluid Creams","Half-and-half (10.5–18% fat); Light (coffee) cream (18–30%); Light whipping cream (30–36%); Heavy cream (≥36%); Whipping cream (30–36%, not std.); Whipped cream (aerosol)","Cream & Cream Products","Half-and-half: §131.180; Light (coffee) cream: §131.155; Light whipping cream: §131.157; Heavy cream: §131.150"),
  ("Cultured Creams","Sour cream; Acidified sour cream; Sour half-and-half; Acidified sour half-and-half; Crème fraîche","Cream & Cream Products","Sour cream: §131.160; Acidified sour cream: §131.162; Sour half-and-half: §131.185; Acidified sour half-and-half: §131.187"),
  ("International & Dry Creams","Single cream (UK, ≥18%); Double cream (UK, ≥48%); Clotted cream (UK, ≥55%); Dry cream","Cream & Cream Products","Dry cream: §131.149"),
  ("Concentrated & Dry","Evaporated milk; Sweetened condensed milk; Concentrated milk; Nonfat dry milk; Dry whole milk",None,"Evaporated milk: §131.130; Sweetened condensed milk: §131.120; Concentrated milk: §131.115; Nonfat dry milk: §131.125; Dry whole milk: §131.147"),
  ("Cultured & Acidified Milks","Cultured buttermilk; Acidified milk; Drinkable yogurt (yogurt base); See Fermented Academy: kefir, kumis; See Regional Academy: lassi, ayran, doogh",None,"Cultured buttermilk: §131.112; Acidified milk: §131.111; Drinkable yogurt: §131.200"),
  ("Flavored Milks","Chocolate milk; Strawberry milk; Vanilla milk; Banana milk; Coffee milk; Eggnog; Milkshake",None,"Eggnog: §131.170"),
  ("Processing","Raw (unpasteurized); Pasteurized (HTST); Vat (low-temperature) pasteurized; Ultra-pasteurized; UHT (aseptic, shelf-stable); Homogenized; Non-homogenized (cream-top); Lactose-free; A2 milk; Ultra-filtered (high-protein); Organic (USDA NOP); Grass-fed; Vitamin A & D fortified",None),
  ("By Species","Cow; Goat; Sheep; Water buffalo; Camel; Yak; Donkey; Mare",None),
  ("Plant Milks","Oat; Almond; Soy; Rice; Coconut; Cashew; Pea; Hemp; Macadamia; Flax; Hazelnut; Pistachio",None),
  ("Creamers","Dairy coffee creamer (half-and-half based); Non-dairy creamer (liquid); Non-dairy creamer (powder); Oat creamer; Almond creamer; Coconut creamer",None)])]),
("ENERGY GUILD","Evidence, function, and stewardship","Grouped by health, supplements, protein systems, and energy formulations.","#ffd23c",[
 ("Health Academy","#3cffc8",[
  ("Hydration & Electrolytes","Oral rehydration solution (WHO ORS); Isotonic sports drinks; Hypotonic electrolyte drinks; Electrolyte powders/tablets"),
  ("Gut Health","Probiotic shots; Prebiotic/fiber drinks; Apple cider vinegar drinks"),
  ("Functional Wellness","Vitamin-enhanced water; Collagen drinks; Ginger/turmeric shots; Golden milk (turmeric latte); Mushroom elixirs (reishi/chaga)"),
  ("Relaxation & Sleep","Magnesium drinks; L-theanine drinks; Melatonin drinks; Adaptogenic drinks (ashwagandha)"),
  ("Medical Nutrition","Oral nutritional supplements; Diabetes-specific formulas; Infant formula; Thickened liquids (IDDSI levels 1–4)")]),
 ("Protein Academy","#ff6a6a",[
  ("Dairy Proteins","Whey protein concentrate; Whey protein isolate; Hydrolyzed whey; Micellar casein; Milk protein isolate"),
  ("Plant Proteins","Pea; Soy isolate; Brown rice; Hemp; Pumpkin seed; Blended plant protein"),
  ("Other Proteins","Egg white protein; Collagen peptides; Beef protein isolate"),
  ("Formats","Powder (mix-in); Ready-to-drink (RTD) shake; Clear whey isolate drinks; Protein coffee; High-protein ultra-filtered milk; Meal replacement shake"),
  ("Use Cases","Post-workout recovery; Mass gainer; Weight management; Overnight (casein)")]),
 ("Energy Academy","#ffd23c",[
  ("Energy Drinks","Standard energy drink; Sugar-free/zero; Energy shots; Fitness/performance energy; Natural/organic energy"),
  ("Caffeine Sources","Caffeine anhydrous; Guarana; Green coffee extract; Green tea extract; Guayusa; Kola nut"),
  ("Pre-Workout","Stimulant pre-workout; Stim-free (pump) pre-workout; Beta-alanine; Creatine monohydrate; L-citrulline"),
  ("RTD Caffeinated","Canned cold brew; Nitro coffee; RTD tea; Caffeinated sparkling water"),
  ("Focus & Nootropic","Caffeine + L-theanine; Citicoline/Alpha-GPC drinks; Lion's mane drinks")])]),
("CULTURE GUILD","Carbonation, living systems, and what comes next","Grouped by living systems, carbonation, place, and shared traditions.","#ff6af0",[
 ("Carbonated Academy","#6ab8ff",[
  ("Classic Soda Styles","Cola; Lemon-lime; Root beer; Ginger ale (dry/golden); Cream soda; Orange soda; Grape soda; Pepper-style soda; Birch beer; Sarsaparilla"),
  ("Mixers & Tonics","Tonic water; Club soda; Bitter lemon; Ginger beer (soft)"),
  ("Modern Sodas","Prebiotic soda; Probiotic soda; Craft cane-sugar soda; Diet/zero-sugar soda; Italian soda; Sparkling juice"),
  ("Cordials & Squashes","Squash (UK fruit concentrate); Cordial; Drinking vinegar (shrub syrup); Soda syrup"),
  ("Carbonation Methods","Forced carbonation (CO2); Natural carbonation (bottle-conditioned); Nitrogenation (nitro); Post-mix (fountain); Pre-mix (bottle/can)")]),
 ("Fermented Academy","#ff6af0",SC+[
  ("Barrel & Wood Aging","Taruzake (Japanese cedar, sugi); Barrel-aged cider (ex-bourbon/rum); Normandy/Asturian cider in oak vats; Barrel-aged mead; See Wine Academy: oak, toast, sizes","Barrel Toasting & Aging"),
  ("Fermented Milks","Milk kefir; Kumis (mare's milk); Drinkable yogurt; Lactobacillus fermented milk drink"),
  ("Grain & Rice Ferments","Kvass; Boza; Amazake; Makgeolli; Chicha de jora"),
  ("Plant & Fruit Ferments","Water kefir (tibicos); Tepache; Pulque; Ginger beer (ginger bug); Palm wine")]),
 ("Regional Academy","#ff9ad5",[
  ("Latin America","Horchata (Mexican rice); Agua fresca; Chicha morada; Yerba mate; Tereré; Champurrado; Atole; Tejate; Aguapanela"),
  ("Asia","Bubble tea (boba); Masala chai; Lassi; Thai iced tea; Vietnamese iced coffee (cà phê sữa đá); Hong Kong milk tea; Teh tarik; Sikhye; Barley tea (mugicha/boricha)"),
  ("Middle East & Africa","Ayran; Doogh; Jallab; Sahlab; Moroccan mint tea; Qahwa (Arabic coffee); Bissap/karkadé (hibiscus); Sobia; Tamarind drink"),
  ("Europe","Horchata de chufa (Valencia); Kompot; Sbiten; Elderflower cordial; Mulled wine (Glühwein)"),
  ("North America","Egg cream (New York); Switchel (New England); Sweet apple cider (unfiltered); Root beer float; Hot chocolate"),
  ("Caribbean & Pacific","Sorrel (Jamaica); Mauby; Sea moss drink; Peanut punch; Kava (Fiji/Vanuatu/Tonga)")])])]
import sys,os;sys.path.insert(0,os.path.dirname(__file__));from depth import DEPTH;from aging import AGING
G=[(gn,tag,grp,gc,[(an,ac,list(subs)+DEPTH.get(an,[])+AGING.get(an,[])) for an,ac,subs in acs]) for gn,tag,grp,gc,acs in G]
out={"title":"Sip Studies × Sipopedia Beverage Taxonomy","version":"2.0","structure":"guild > academy > subgenre > styles","guilds":[]}
for gi,(gn,tag,grp,gc,acs) in enumerate(G):
  g={"id":gi+1,"name":gn,"tagline":tag,"grouping":grp,"color":gc,"academies":[]}
  for ai,(an,ac,subs) in enumerate(acs):
    g["academies"].append({"id":f"{gi+1}.{ai+1}","name":an,"color":ac,"subgenres":[dict({"id":f"{gi+1}.{ai+1}.{j+1}","name":t[0],"styles":S(t[1])},**({"parent":t[2]} if len(t)>2 and t[2] else {}),**({"standards":t[3]} if len(t)>3 else {})) for j,t in enumerate(subs)]})
  out["guilds"].append(g)
json.dump(out,open('data/guilds.json','w'),ensure_ascii=False,indent=1)
h=['<html><head><meta charset=utf-8><style>body{font-family:Georgia,serif;font-size:10.5pt;color:#112;margin:28px}h1{font-size:20pt;color:#0b2a33}h2{border-bottom:2px solid #c6a15b;margin-top:20px;font-size:15pt;color:#0b2a33}h3{font-size:12pt;margin:10px 0 2px;color:#7a5a1e}h4{font-size:10.5pt;margin:6px 0 1px;font-family:Helvetica}p{margin:0 0 3px;color:#333;font-family:Helvetica;font-size:9.5pt}.s{font-size:9pt;color:#666;font-family:Helvetica}</style></head><body><h1>Sip Studies × Sipopedia Beverage Taxonomy</h1><p class=s>Guild &gt; academy &gt; subgenre &gt; styles. Source data: data/guilds.json. Beer follows BJCP 2021 categories 1–34.</p>']
tot=[0,0,0]
for g in out['guilds']:
  ns=sum(len(a['subgenres']) for a in g['academies']);nt=sum(len(s['styles']) for a in g['academies'] for s in a['subgenres'])
  h.append(f"<h2>{g['id']}. {g['name'].title()} <span class=s>— {g['tagline']} ({ns} subgenres, {nt} styles)</span></h2><p class=s>{g['grouping']}</p>")
  for a in g['academies']:
    an=sum(len(s['styles']) for s in a['subgenres']);print(f"{g['name']:13} {a['name']:20} {len(a['subgenres']):3} {an:4}")
    h.append(f"<h3>{a['id']} {a['name']} <span class=s>({len(a['subgenres'])} subgenres, {an} styles)</span></h3>")
    for s in a['subgenres']: h.append(f"<h4>{s['id']} {(s['parent']+' › ') if s.get('parent') else ''}{s['name']}</h4><p>{' · '.join(s['styles'])}</p>"+(f"<p class=s>Standards: {s['standards']}</p>" if s.get('standards') else ''))
  tot[0]+=3;tot[1]+=ns;tot[2]+=nt
print(tot)
open('build/guilds.html','w').write(''.join(h)+'</body></html>')
