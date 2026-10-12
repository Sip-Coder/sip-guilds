import json
OLD={g['name']:{s['name']:s['styles'] for s in g['subgenres']} for g in json.load(open('/tmp/guilds_v1.json'))['guilds']} if __import__('os').path.exists('/tmp/guilds_v1.json') else None
def S(s): return [x.strip() for x in s.split(';')]
def old(g,drop=(),edit={}):
  out=[]
  for n,st in OLD[g].items():
    if n in drop: continue
    st=[x for x in st if x not in edit.get(n,[])]; out.append((n,'; '.join(st)))
  return out
W=old('WATER',edit={'Sparkling Water':['Club soda','Tonic water']})
C=old('COFFEE')
T=old('TEA',edit={'Herbal Tisanes':['Yerba mate','Guayusa']})
WI=old('WINE')+[("Dealcoholized Wine (≤0.5% ABV)","Dealcoholized red; Dealcoholized white; Dealcoholized sparkling; Dealcoholized rosé")]
B=[(n,st) for n,st in old('BEER')]+[("NA & Low-Alcohol Beer (outside BJCP)","Non-alcoholic lager (≤0.5% ABV); Non-alcoholic IPA; Non-alcoholic stout; Radler/shandy")]
SP=old('SPIRITS')+[("Zero-Proof","Virgin cocktails (mocktails); Non-alcoholic gin alternatives; Non-alcoholic whiskey alternatives; Non-alcoholic aperitif/bitter alternatives; Shrub-based drinks")]
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
  ("Product Types (FDA)","100% juice; Juice from concentrate; Nectar; Juice drink/cocktail; Smoothie"),
  ("Processing","Not-from-concentrate (NFC); Fresh-squeezed (unpasteurized, warning label); Flash-pasteurized; Cold-pressed (HPP); Frozen concentrate"),
  ("Citrus","Orange; Grapefruit; Lemon; Lime; Tangerine/mandarin; Blood orange"),
  ("Pome & Stone Fruit","Apple (cloudy/clear); Pear; Tart cherry; Peach nectar; Apricot nectar"),
  ("Berry & Grape","Concord grape; Cranberry; Pomegranate; Blueberry; Açaí; Elderberry"),
  ("Tropical","Pineapple; Mango; Passion fruit; Guava; Papaya; Coconut water"),
  ("Vegetable","Tomato; Carrot; Beet; Celery; Green juice (kale/spinach/cucumber); Mixed vegetable juice")]),
 ("Milk Academy","#e8f4ff",[
  ("By Species","Cow; Goat; Sheep; Water buffalo; Camel"),
  ("Fat Level (US)","Whole (3.25%); Reduced-fat (2%); Low-fat (1%); Fat-free (skim)"),
  ("Processing","Raw (unpasteurized); Pasteurized (HTST); Ultra-pasteurized; UHT (shelf-stable); Homogenized; Non-homogenized (cream-top); Lactose-free; Ultra-filtered; A2 milk"),
  ("Milk Drinks","Chocolate milk; Strawberry milk; Eggnog; Milkshake; Cultured buttermilk"),
  ("Plant Milks","Oat; Almond; Soy; Coconut; Rice; Pea; Cashew; Hemp; Macadamia")])]),
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
  ("Carbonation Methods","Forced carbonation (CO2); Natural carbonation (bottle-conditioned); Nitrogenation (nitro); Post-mix (fountain); Pre-mix (bottle/can)")]),
 ("Fermented Academy","#ff6af0",SC+[
  ("Fermented Milks","Milk kefir; Kumis (mare's milk); Drinkable yogurt; Lactobacillus fermented milk drink"),
  ("Grain & Rice Ferments","Kvass; Boza; Amazake; Makgeolli; Chicha de jora"),
  ("Plant & Fruit Ferments","Water kefir (tibicos); Tepache; Pulque; Ginger beer (ginger bug); Palm wine")]),
 ("Regional Academy","#ff9ad5",[
  ("Latin America","Horchata (Mexican rice); Agua fresca; Chicha morada; Yerba mate; Tereré; Champurrado; Atole; Tejate; Aguapanela"),
  ("Asia","Bubble tea (boba); Masala chai; Lassi; Thai iced tea; Vietnamese iced coffee (cà phê sữa đá); Hong Kong milk tea; Teh tarik; Sikhye; Barley tea (mugicha/boricha)"),
  ("Middle East & Africa","Ayran; Doogh; Jallab; Sahlab; Moroccan mint tea; Qahwa (Arabic coffee); Bissap/karkadé (hibiscus); Sobia; Tamarind drink"),
  ("Europe","Horchata de chufa (Valencia); Kompot; Sbiten; Elderflower cordial; Mulled wine (Glühwein)"),
  ("Caribbean & Pacific","Sorrel (Jamaica); Mauby; Sea moss drink; Peanut punch; Kava (Fiji/Vanuatu/Tonga)")])])]
out={"title":"Sip Studies × Sipopedia Beverage Taxonomy","version":"2.0","structure":"guild > academy > subgenre > styles","guilds":[]}
for gi,(gn,tag,grp,gc,acs) in enumerate(G):
  g={"id":gi+1,"name":gn,"tagline":tag,"grouping":grp,"color":gc,"academies":[]}
  for ai,(an,ac,subs) in enumerate(acs):
    g["academies"].append({"id":f"{gi+1}.{ai+1}","name":an,"color":ac,"subgenres":[{"id":f"{gi+1}.{ai+1}.{j+1}","name":n,"styles":S(st)} for j,(n,st) in enumerate(subs)]})
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
    for s in a['subgenres']: h.append(f"<h4>{s['id']} {s['name']}</h4><p>{' · '.join(s['styles'])}</p>")
  tot[0]+=3;tot[1]+=ns;tot[2]+=nt
print(tot)
open('build/guilds.html','w').write(''.join(h)+'</body></html>')
