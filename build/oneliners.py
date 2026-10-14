# Builds data/oneliners.json: one friendly sentence (<=140 chars) per term, derived only from our definitions/guilds data
# (+ build/beer_lines.py paraphrases of BJCP overall impressions for BJCP beer styles).
import json,re,sys
sys.path.insert(0,'build');from beer_lines import B
D=json.load(open('data/definitions.json'))['definitions'];G=json.load(open('data/guilds.json'))['guilds']
SUB={};ACAD={}
for g in G:
  for a in g['academies']:
    for s in a['subgenres']:SUB[s['id']]=s;ACAD[s['id']]=a['name']
U={'yr':'year','mo':'month'}
def dur(n,u):
  n=float(n);n=int(n) if n==int(n) else n;w=U.get(u,u);return f"{n} {w}{'s' if n!=1 else ''}"
def aging(term,parent):
  name=term.split(' · ')[0];spec=term.split(' · ',1)[1] if ' · ' in term else ''
  m=re.match(r'(\d+(?:\.\d+)?)\+?\s*(yr|mo)\b',spec);
  if not m:return None
  tot=dur(m.group(1),m.group(2));extra=[]
  rest=spec[m.end():]
  for n,u,kind in re.findall(r'(\d+(?:\.\d+)?)\s*(yr|mo)?\s*(oak|wood|btl|lees|under voile|from tirage)',rest+' '+spec[:0]):
    tu=u or (m.group(2) if not(m.group(2)=='yr' and float(n)>float(m.group(1))) else 'mo')
    extra.append(dur(n,tu)+{'oak':' in oak','wood':' in wood','btl':' in bottle','lees':' on the lees','under voile':' under a veil of yeast','from tirage':' from bottling'}[kind])
  lees=re.match(r'\d+(?:\.\d+)?\s*(yr|mo)\s*(lees|from tirage|wood|oak)',spec)
  where=re.sub(r'\s*\(.*?\)','',parent).strip()
  where=re.sub(r'\s*\(.*?\)','',where).strip()
  if ':' in where or 'Generic' in where or where in('Whisky','Whiskey','Rum','Brandy','Spirits','Wine') or where.startswith('Other') or '&' in where or re.search(r'Method|Terms|Categories|Classes|-',where) or name.lower().startswith(where.lower()):where=''
  name=name+(f' ({where})' if where else '')
  if lees:
    k=lees.group(2);s=f"{name} must spend at least {tot} {'on the lees' if k=='lees' else 'from bottling to release' if k=='from tirage' else 'in '+k}."
  else:
    s=(f"{name} must have an average age of at least {tot}" if 'avg' in spec else f"{name} must age at least {tot} before release")+(", including "+" and ".join(extra) if extra else "")+"."
  return s[0].upper()+s[1:]
ABBR={'e.g.':'e\u2024g\u2024','i.e.':'i\u2024e\u2024','approx.':'approx\u2024','U.S.':'U\u2024S\u2024','vs.':'vs\u2024','St.':'St\u2024','No.':'No\u2024','cf.':'cf\u2024'}
def first(t):
  for a,b in ABBR.items():t=t.replace(a,b)
  t=re.sub(r'(\d)\.(\d)',lambda m:m.group(1)+'\u2024'+m.group(2),t)
  r=_first(t).replace('\u2024','.');return r
def _first(t):
  m=re.match(r'(.+?[.!?])(\s|$)',t+' ');return (m.group(1) if m else t).strip()
CLEAN=[(r'regulated by NOM-070',"regulated by Mexico's official mezcal standard"),(r'regulated by NOM-006',"regulated by Mexico's official tequila standard"),(r'^NOM-070 mezcal','Mexican mezcal'),(r'\bapprox\.\s*','about '),(r'\be\.g\.,?\s*','such as '),(r'\bi\.e\.,?\s*',''),(r'\s*\(NOM-\d+[^)]*\)',''),(r'\bUS\b','U.S.'),(r'\s+',' ')]
def shorten(s,n=140):
  if len(s)<=n:return s
  for sep in ['; ',' — ',', which ',', with ',', and ',', ']:
    i=s.rfind(sep,0,n-1)
    if i>50:return s[:i].rstrip(' ,;')+'.'
  return s[:n-1].rsplit(' ',1)[0].rstrip(' ,;')+'.'
def line(k,v):
  t,d=v['term'],v['definition']
  if v['kind']=='group':
    s=SUB.get(k);ac=ACAD.get(k,'').replace(' Academy','').lower()
    if s:
      nm=re.sub(r'^\d+\s+','',s['name']);ex=[re.sub(r'\s*\(.*?\)','',x.split(' · ')[0]) for x in s['styles'][:3]]
      lst=', '.join(ex[:-1])+' and '+ex[-1] if len(ex)>1 else ex[0]
      nm=re.sub(r'\s*\(.*?\)','',nm).strip()
      if ':' in nm or ',' in nm or '%' in nm:nm=''
      pre=f"{nm}: a" if nm else "A"
      out=f"{pre} family of {len(s['styles'])} {ac} entries, including {lst}." if len(s['styles'])>len(ex) else (f"{nm}: {ac} entries covering {lst}." if nm else f"{ac.capitalize()} entries covering {lst}.")
      return shorten(out)
  if 'beer style in BJCP' in d:
    if t in B:return B[t]+'.'
    m=re.search(r'category \d+ (.+?)\.',d);return f"A beer style in the {m.group(1)} family of the BJCP 2021 guidelines." if m else first(d)
  if 'official/legal aging category' in d:
    par=SUB.get(k.rsplit('.',1)[0],{}).get('name','')
    a=aging(t,par)
    if a:return shorten(a)
  s=first(d)
  for p,r in CLEAN:s=re.sub(p,r,s)
  s=s.strip();s=s[0].upper()+s[1:]
  s=re.sub(r'\.\.$','.',s)
  if not s.endswith(('.','!','?')):s+='.'
  return shorten(s)
# Hand-shortened versions of definitions too long for the card (same facts, fewer words).
OVR={'1.1.19.4':'American Vitis species used mainly as parents of phylloxera-resistant rootstocks, not for wine.',
'2.1.7.4':'Decaffeination with dichloromethane, applied to the beans or to their soak water.',
'2.3.8.1':'In the U.S., drinks under 0.5% ABV are not regulated by the TTB as alcoholic beverages.',
'4.1.8.1':'A 1994 U.S. law (DSHEA) that separates dietary supplements from conventional foods.'}
O={k:OVR.get(k) or line(k,v) for k,v in D.items()}
json.dump({'version':'1','count':len(O),'oneliners':O},open('data/oneliners.json','w'),ensure_ascii=False,indent=0)
if __name__=='__main__':
  import random;random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 7)
  print(len(O),'max',max(map(len,O.values())),'>140',sum(len(x)>140 for x in O.values()))
  for k in random.sample(list(O),40):print(k,'|',D[k]['term'],'|',O[k])
