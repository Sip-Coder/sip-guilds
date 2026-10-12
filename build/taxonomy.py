import json
def S(s): return [x.strip() for x in s.split(';')]
G=[
("WATER","#2ee6ff",[
 ("Spring Water","Natural spring; Artesian spring; Glacier/icecap water"),
 ("Mineral Water","Low-mineral (<500 mg/L TDS); Medium-mineral; High-mineral (>1500 mg/L TDS); Naturally carbonated mineral"),
 ("Sparkling Water","Carbonated (added CO2); Seltzer; Club soda; Tonic water"),
 ("Purified Water","Distilled; Reverse osmosis; Deionized"),
 ("Functional Water","Alkaline (ionized); Electrolyte-enhanced; Flavored/infused; Hydrogen water")]),
("COFFEE","#ff9a3c",[
 ("Species","Arabica (Coffea arabica); Robusta (Coffea canephora); Liberica; Excelsa"),
 ("Processing","Washed (wet); Natural (dry); Honey (pulped natural); Wet-hulled (Giling Basah); Anaerobic fermentation; Carbonic maceration"),
 ("Roast Level","Light (cinnamon/New England); Medium (City/American); Medium-dark (Full City); Dark (Vienna/French/Italian)"),
 ("Espresso Drinks","Espresso; Ristretto; Lungo; Americano; Macchiato; Cortado; Flat white; Cappuccino; Latte; Mocha; Affogato"),
 ("Brew Methods","Pour-over (V60/Chemex/Kalita); French press; AeroPress; Moka pot; Siphon; Drip (batch brew); Turkish (cezve); Cold brew; Cold drip (Kyoto); Phin (Vietnamese)")]),
("TEA","#7dff6a",[
 ("White Tea","Silver Needle (Bai Hao Yin Zhen); White Peony (Bai Mu Dan); Shou Mei; Darjeeling white"),
 ("Yellow Tea","Junshan Yinzhen; Meng Ding Huang Ya; Huoshan Huang Ya"),
 ("Green Tea","Longjing (Dragon Well); Bi Luo Chun; Gunpowder; Sencha; Gyokuro; Matcha; Hojicha; Genmaicha; Bancha"),
 ("Oolong Tea","Tieguanyin; Da Hong Pao (Wuyi rock); Dong Ding; Alishan high-mountain; Oriental Beauty; Dan Cong"),
 ("Black Tea","Assam; Darjeeling; Ceylon; Keemun; Dian Hong (Yunnan); Lapsang Souchong; English Breakfast blend; Earl Grey"),
 ("Dark Tea","Sheng (raw) pu-erh; Shou (ripe) pu-erh; Liu Bao; Fu Zhuan (Anhua brick)"),
 ("Herbal Tisanes","Rooibos; Honeybush; Chamomile; Peppermint; Hibiscus; Yerba mate; Guayusa; Ginger; Lemongrass")]),
("WINE","#ff3b7a",[
 ("Red","Cabernet Sauvignon; Merlot; Pinot Noir; Syrah/Shiraz; Grenache/Garnacha; Tempranillo; Sangiovese; Nebbiolo; Malbec; Zinfandel/Primitivo; Cabernet Franc; Gamay; Barbera; Mourvèdre/Monastrell"),
 ("White","Chardonnay; Sauvignon Blanc; Riesling; Pinot Grigio/Gris; Chenin Blanc; Gewürztraminer; Viognier; Albariño; Grüner Veltliner; Sémillon; Torrontés; Assyrtiko"),
 ("Rosé","Provence rosé; Tavel; Rosado (Navarra); Rosato; White Zinfandel"),
 ("Sparkling","Champagne; Crémant; Cava; Prosecco; Franciacorta; Sekt; Pét-nat (ancestral method); Lambrusco; Moscato d'Asti"),
 ("Orange (Skin-Contact)","Georgian qvevri (Rkatsiteli); Friulian Ribolla Gialla; Slovenian (Brda) skin-contact"),
 ("Fortified","Port (Ruby/Tawny/Vintage); Sherry (Fino/Manzanilla/Amontillado/Oloroso/PX); Madeira; Marsala; Vermouth; Vin doux naturel"),
 ("Dessert","Sauternes; Tokaji Aszú; Icewine/Eiswein; Beerenauslese/TBA; Vin Santo; Recioto; Late harvest")]),
("BEER","#ffd23c",[
 ("1 Standard American Beer","American Light Lager; American Lager; Cream Ale; American Wheat Beer"),
 ("2 International Lager","International Pale Lager; International Amber Lager; International Dark Lager"),
 ("3 Czech Lager","Czech Pale Lager; Czech Premium Pale Lager; Czech Amber Lager; Czech Dark Lager"),
 ("4 Pale Malty European Lager","Munich Helles; Festbier; Helles Bock"),
 ("5 Pale Bitter European Beer","German Leichtbier; Kölsch; German Helles Exportbier; German Pils"),
 ("6 Amber Malty European Lager","Märzen; Rauchbier; Dunkles Bock"),
 ("7 Amber Bitter European Beer","Vienna Lager; Altbier"),
 ("8 Dark European Lager","Munich Dunkel; Schwarzbier"),
 ("9 Strong European Beer","Doppelbock; Eisbock; Baltic Porter"),
 ("10 German Wheat Beer","Weissbier; Dunkles Weissbier; Weizenbock"),
 ("11 British Bitter","Ordinary Bitter; Best Bitter; Strong Bitter"),
 ("12 Pale Commonwealth Beer","British Golden Ale; Australian Sparkling Ale; English IPA"),
 ("13 Brown British Beer","Dark Mild; British Brown Ale; English Porter"),
 ("14 Scottish Ale","Scottish Light; Scottish Heavy; Scottish Export"),
 ("15 Irish Beer","Irish Red Ale; Irish Stout; Irish Extra Stout"),
 ("16 Dark British Beer","Sweet Stout; Oatmeal Stout; Tropical Stout; Foreign Extra Stout"),
 ("17 Strong British Ale","British Strong Ale; Old Ale; Wee Heavy; English Barley Wine"),
 ("18 Pale American Ale","Blonde Ale; American Pale Ale"),
 ("19 Amber and Brown American Beer","American Amber Ale; California Common; American Brown Ale"),
 ("20 American Porter and Stout","American Porter; American Stout; Imperial Stout"),
 ("21 IPA","American IPA; Specialty IPA: Belgian IPA; Specialty IPA: Black IPA; Specialty IPA: Brown IPA; Specialty IPA: Red IPA; Specialty IPA: Rye IPA; Specialty IPA: White IPA; Specialty IPA: Brut IPA; Hazy IPA"),
 ("22 Strong American Ale","Double IPA; American Strong Ale; American Barleywine; Wheatwine"),
 ("23 European Sour Ale","Berliner Weisse; Flanders Red Ale; Oud Bruin; Lambic; Gueuze; Fruit Lambic; Gose"),
 ("24 Belgian Ale","Witbier; Belgian Pale Ale; Bière de Garde"),
 ("25 Strong Belgian Ale","Belgian Blond Ale; Saison; Belgian Golden Strong Ale"),
 ("26 Monastic Ale","Trappist Single; Belgian Dubbel; Belgian Tripel; Belgian Dark Strong Ale"),
 ("27 Historical Beer","Kellerbier; Kentucky Common; Lichtenhainer; London Brown Ale; Piwo Grodziskie; Pre-Prohibition Lager; Pre-Prohibition Porter; Roggenbier; Sahti"),
 ("28 American Wild Ale","Brett Beer; Mixed-Fermentation Sour Beer; Wild Specialty Beer; Straight Sour Beer"),
 ("29 Fruit Beer","Fruit Beer; Fruit and Spice Beer; Specialty Fruit Beer; Grape Ale"),
 ("30 Spiced Beer","Spice, Herb, or Vegetable Beer; Autumn Seasonal Beer; Winter Seasonal Beer; Specialty Spice Beer"),
 ("31 Alternative Fermentables Beer","Alternative Grain Beer; Alternative Sugar Beer"),
 ("32 Smoked Beer","Classic Style Smoked Beer; Specialty Smoked Beer"),
 ("33 Wood Beer","Wood-Aged Beer; Specialty Wood-Aged Beer"),
 ("34 Specialty Beer","Commercial Specialty Beer; Mixed-Style Beer; Experimental Beer")]),
("SPIRITS","#b06bff",[
 ("American Whiskey","Bourbon; Straight Bourbon; Bottled-in-Bond; Tennessee Whiskey; Rye Whiskey; Wheat Whiskey; Corn Whiskey; American Single Malt"),
 ("Scotch Whisky","Speyside; Highland; Lowland; Islay; Campbeltown; Islands (Highland sub-region); Single Malt; Blended Malt; Single Grain; Blended Scotch"),
 ("Irish Whiskey","Single Pot Still; Single Malt; Single Grain; Blended"),
 ("Japanese Whisky","Single Malt; Blended; Grain"),
 ("Other Whisk(e)y","Canadian Whisky; Indian Single Malt; Taiwanese Single Malt; Welsh Whisky"),
 ("Gin","London Dry; Plymouth; Old Tom; Genever (Jenever); Navy Strength; Contemporary/New Western; Sloe Gin (liqueur)"),
 ("Rum","Light/White; Gold; Dark; Overproof; Spiced; Rhum Agricole (AOC Martinique); Cachaça; Jamaican pot-still; Demerara (Guyana)"),
 ("Agave","Tequila Blanco; Tequila Joven; Tequila Reposado; Tequila Añejo; Tequila Extra Añejo; Mezcal (Joven/Reposado/Añejo); Mezcal Ancestral; Mezcal Artesanal; Raicilla; Sotol (Dasylirion); Bacanora"),
 ("Brandy","Cognac VS; Cognac VSOP; Cognac XO; Armagnac; Brandy de Jerez; Pisco (Peru/Chile); Calvados; Grappa; Eau-de-vie (Kirsch/Poire Williams); American brandy"),
 ("Vodka","Grain vodka; Potato vodka; Grape vodka; Flavored vodka"),
 ("Liqueurs","Amaro; Orange liqueur (Triple sec/Curaçao); Herbal (Chartreuse/Bénédictine); Anise (Pastis/Ouzo/Sambuca/Absinthe); Coffee liqueur; Cream liqueur; Nut liqueur (Amaretto/Frangelico); Fruit liqueur (Limoncello/Crème de cassis)"),
 ("Asian Spirits","Baijiu: Strong aroma (nongxiang); Baijiu: Light aroma (qingxiang); Baijiu: Sauce aroma (jiangxiang); Baijiu: Rice aroma (mixiang); Shochu (honkaku); Awamori; Soju; Arrack")]),
("SAKE · CIDER · MEAD","#ff6af0",[
 ("Sake Grades (Tokutei Meishoshu)","Junmai Daiginjo; Daiginjo; Junmai Ginjo; Ginjo; Tokubetsu Junmai; Tokubetsu Honjozo; Junmai; Honjozo"),
 ("Sake Styles","Futsushu (table sake); Nigori; Namazake; Genshu; Koshu (aged); Taruzake; Sparkling sake; Kimoto; Yamahai"),
 ("Cider","Modern/standard cider; Heritage cider; English cider; French cidre (Normandy/Brittany); Spanish sidra (Asturias/Basque); Ice cider (cidre de glace); Hopped cider"),
 ("Perry","Modern perry; Traditional perry (perry-pear varieties)"),
 ("Mead","Traditional mead (dry/semi-sweet/sweet); Melomel (fruit); Cyser (apple); Pyment (grape); Metheglin (spice); Braggot (malt); Sack mead; Hydromel (session)")]),
("NON-ALC","#3cffc8",[
 ("Mocktails","Virgin Mojito; Virgin Mary; Shirley Temple; Arnold Palmer; Nojito/spritz-style zero-proof; Shrub-based cocktails"),
 ("NA Beer","NA lager (dealcoholized); NA IPA; NA stout; Radler (low-alc shandy)"),
 ("NA Wine","Dealcoholized red; Dealcoholized white; Dealcoholized sparkling"),
 ("NA Spirits","Gin alternatives; Whiskey alternatives; Aperitif/bitter alternatives; Agave alternatives"),
 ("Fermented","Kombucha; Water kefir; Kvass; Jun; Tepache"),
 ("Juices","Not-from-concentrate juice; From-concentrate juice; Cold-pressed (HPP) juice; Nectar; Smoothie"),
 ("Sodas","Cola; Lemon-lime; Root beer; Ginger ale; Ginger beer; Cream soda; Prebiotic soda"),
 ("Energy & Functional","Energy drinks; Sports drinks; Coconut water; Protein shakes; Adaptogenic drinks"),
 ("Dairy & Plant Milks","Milk; Kefir; Lassi; Oat milk; Almond milk; Soy milk; Horchata")])]
out={"title":"Sip Studies Beverage Guild Taxonomy","version":"1.0","guilds":[{"id":i+1,"name":n,"color":c,"subgenres":[{"id":f"{i+1:02d}.{j+1}","name":sn,"styles":S(st)} for j,(sn,st) in enumerate(subs)]} for i,(n,c,subs) in enumerate(G)]}
json.dump(out,open('data/guilds.json','w'),ensure_ascii=False,indent=1)
h=['<html><head><meta charset=utf-8><style>body{font-family:Helvetica,Arial;font-size:10.5pt;color:#111;margin:28px}h1{font-size:20pt}h2{border-bottom:2px solid;margin-top:18px;font-size:14pt}h3{font-size:11pt;margin:8px 0 2px}p{margin:0 0 4px;color:#333}.s{font-size:9pt;color:#555}</style></head><body><h1>Sip Studies Beverage Guild Taxonomy</h1><p class=s>Guild &gt; subgenre &gt; styles. Source data: data/guilds.json. Beer follows BJCP 2021 categories.</p>']
for g in out['guilds']:
  h.append(f"<h2 style='border-color:{g['color']}'>{g['id']:02d} {g['name']} <span class=s>({len(g['subgenres'])} subgenres, {sum(len(s['styles']) for s in g['subgenres'])} styles)</span></h2>")
  for s in g['subgenres']: h.append(f"<h3>{s['id']} {s['name']}</h3><p>{' · '.join(s['styles'])}</p>")
open('build/guilds.html','w').write(''.join(h)+'</body></html>')
for g in out['guilds']: print(g['name'],len(g['subgenres']),sum(len(s['styles']) for s in g['subgenres']))
