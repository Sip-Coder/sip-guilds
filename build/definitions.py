# Builds data/definitions.json (keyed by id) and appends a glossary to build/guilds.html.
import json,re,os,html
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/..')
from defs_curated import C
D=json.load(open('data/guilds.json'));out={}
def look(ac,t):
  for k in (ac+'|'+t,t,re.split(r' \(| · |: ',t)[0],t.split('/')[0]):
    if k in C:return C[k]
def flagged(std):return bool(std) and bool(re.search(r'unverified|from memory|partially verified',std))
def src(std):
  m=re.findall(r'Sources?: ([^\[]+)',std or '');return '; '.join(x.strip(' .;') for x in m) or None
for g in D['guilds']:
  for a in g['academies']:
    an=a['name']
    for s in a['subgenres']:
      sid=s['id'];par=s.get('parent');std=s.get('standards');path=f"{g['name'].title()} › {an} › "+(par+' › ' if par else '')+s['name']
      ex=', '.join(s['styles'][:3])
      out[sid]={"term":s['name'],"path":path,"kind":"group","definition":f"{s['name']} is a group of {len(s['styles'])} entries in the {an}"+(f", under {par}" if par else '')+f". It includes {ex}"+('…' if len(s['styles'])>3 else '')+'.',"facts":[std] if std else [],"source":src(std),"needs_review":False}
      for j,t in enumerate(s['styles']):
        tid=f"{sid}.{j+1}";facts=[];nr=False;d=look(an,t)
        if par=='Aging Requirements':
          L,_,R=t.partition(' · ')
          d=(f"{L}: official/legal aging category." if R else t+'.')+(f" Requirement: {R}." if R else '')+' Times are minimums unless stated; see facts for barrel/bottle detail and source.'
          if std:facts.append(std)
          nr=flagged(std);d=d if L!=t else t+'.'
          c=C.get(f"{an}|{s['name']}|{L}") or look(an,L)
          if c and R:d=c+f" Requirement: {R}."
        elif d: pass
        elif an=='Beer Academy' and re.match(r'\d',s['name']):
          d=f"{t} is a beer style in BJCP 2021 Style Guidelines category {s['name']}."
        else:
          m=re.match(r'(.+?) \((.+)\)$',t)
          d=(f"{m.group(1)} — {m.group(2)}. " if m else f"{t}. ")+f"Listed under {s['name']}"+(f" ({par})" if par else '')+f" in the {an}. A fuller definition has not been written yet."
          nr=True
        if std and par!='Aging Requirements' and not facts:facts.append(std)
        out[tid]={"term":t,"path":path+' › '+t,"kind":"term","definition":d,"facts":facts,"source":src(std) if par=='Aging Requirements' else None,"needs_review":nr}
json.dump({"version":D.get('version'),"count":len(out),"needs_review":sum(v['needs_review'] for v in out.values()),"definitions":out},open('data/definitions.json','w'),ensure_ascii=False,separators=(',',':'))
h=open('build/guilds.html').read().replace('</body></html>','')
gl=['<h2 style="page-break-before:always">Glossary</h2><p class=s>Reviewed definitions only; entries flagged “needs review” in data/definitions.json are omitted here.</p>']
seen=set()
for k,v in out.items():
  if v['kind']=='term' and not v['needs_review'] and v['term'] not in seen:
    seen.add(v['term']);gl.append(f"<p><b>{html.escape(v['term'])}</b> — {html.escape(v['definition'])}</p>")
open('build/guilds.html','w').write(h+''.join(gl)+'</body></html>')
print('defs',len(out),'needs_review',sum(v['needs_review'] for v in out.values()),'glossary',len(seen))
