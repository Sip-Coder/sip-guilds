# Procedural, composable SVG card illustrations (Sipopedia-style: pastel ground, flat line art, bold term, one-liner).
# Deterministic per term id. Text comes only from data/definitions.json (term) and data/oneliners.json.
import json,re,html,hashlib,random,sys,os,time
D=json.load(open('data/definitions.json'))['definitions'];O=json.load(open('data/oneliners.json'))['oneliners']
G=json.load(open('data/guilds.json'))['guilds'];ACAD={};SUBNAME={};GUILD={str(g['id']):g['name'] for g in G}
for g in G:
  for a in g['academies']:
    for s in a['subgenres']:ACAD[s['id']]=a['name'].replace(' Academy','');SUBNAME[s['id']]=s.get('parent') and s['name'] or s['name']
PAL={ # bg, bg2, ink, accent
'Wine':('#fbe9e4','#f6d6cf','#6e2436','#e7a093'),'Beer':('#fdf3dc','#f7e3b4','#6a4a12','#f0c45a'),'Spirits':('#f1eaf7','#e3d6ef','#4b2a66','#c6a5e0'),
'Coffee':('#f7ece2','#ecd8c4','#5a3520','#d9a77d'),'Tea':('#ebf4e3','#d6e8c7','#2f5a33','#9cc98a'),'Kombucha':('#f1f6dc','#e2ecbc','#4b5a1d','#c2d36a'),
'Water':('#e4f3f7','#cbe7ef','#1d5566','#86c4d6'),'Juice':('#fff0dd','#fde0b8','#7a4610','#f6b25a'),'Milk':('#f3f6fb','#e1e8f3','#33496b','#a9bfdc'),
'Health':('#e2f6f0','#c7ece1','#1d5c4c','#7fd1b9'),'Protein':('#fbe8e8','#f4d0d0','#6b2a2a','#e79a9a'),'Energy':('#fdf6d8','#f8e9a6','#5e4c0e','#f2cf4b'),
'Carbonated':('#e6f0fb','#cfe0f5','#20466e','#8cb8e6'),'Fermented':('#f8e6f5','#efcde9','#5c2a57','#dc9ad3'),'Regional':('#fdeaf3','#f8d3e5','#6b2b4a','#ec9cc2')}
LIQ={'red':'#8e2340','white':'#eed47c','rose':'#f2a2a6','spark':'#f2de92','amber':'#c27a2e','dark':'#3d2419','gold':'#e8b13a','pale':'#f4da70',
'clear':'#e8f5f8','greentea':'#b6cf72','matcha':'#78a33f','blacktea':'#b4552c','oolong':'#d38f3e','whitetea':'#efe0a8','coffee':'#5b3420','milk':'#fcfbf5',
'orange':'#f59a2a','water':'#c4e7f2','cola':'#4a2516','tawny':'#a8552a','sake':'#f3efdc','green':'#9fd36a','berry':'#9b2d5c','apple':'#f1d77a'}
from PIL import ImageFont
_TF=ImageFont.truetype('/usr/share/fonts/truetype/sand-box/google/Gelasio/Gelasio-VariableFont_wght.ttf',100);_TF.set_variation_by_name('Bold')
_BF=ImageFont.truetype('/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf',100);_CF=ImageFont.truetype('/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf',100)
TITLE_FS,BODY_FS,CHIP_FS,LABEL_FS=66,38,22,21
TITLE_W,BODY_W=864/1.12,864/1.06   # safety for wider fallback fonts (e.g. Noto Serif on Android)
def tw(f,t,fs):return f.getlength(t)*fs/100
def mwrap(text,f,fs,maxw):
  words=text.replace('/','/\u200b').replace('\u200b',' \u200b').split();L=[];c=''
  for w in words:
    cand=(c+' '+w).strip().replace(' \u200b','')
    if c and tw(f,cand.replace('\u200b',''),fs)>maxw:L.append(c.replace(' \u200b','').replace('\u200b',''));c=w.replace('\u200b','')
    else:c=cand
  if c:L.append(c.replace('\u200b',''))
  return L
def trim_to(text,n):
  L=mwrap(text,_BF,BODY_FS,BODY_W)
  if len(L)<=n:return L
  for sep in ['; ',' — ',', which ',', including ',', with ',', giving ']:
    i=text.rfind(sep)
    while i>30:
      cand=text[:i].rstrip(' ,;')+'.';LL=mwrap(cand,_BF,BODY_FS,BODY_W)
      if len(LL)<=n:return LL
      i=text.rfind(sep,0,i)
  last=L[n-1].rstrip(' ,;.')
  while tw(_BF,last+'…',BODY_FS)>BODY_W:last=last.rsplit(' ',1)[0]
  return L[:n-1]+[last.rstrip(' ,;.')+'…']
def esc(t):return html.escape(t,quote=True)
class S:
  def __init__(s,ink,acc,rng):s.ink=ink;s.acc=acc;s.r=rng;s.defs={};s.n=0
  def grad(s,c,light='#ffffff',a=.55):
    k=('g',c,light);
    if k not in s.defs:s.n+=1;i=f'g{s.n}';s.defs[k]=(i,f'<linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mix(c,light,a)}"/><stop offset="1" stop-color="{c}"/></linearGradient>')
    return f'url(#{s.defs[k][0]})'
def hx(c):c=c.lstrip('#');return [int(c[i:i+2],16) for i in (0,2,4)]
def mix(a,b,t):A,B=hx(a),hx(b);return '#'+''.join(f'{round(x+(y-x)*t):02x}' for x,y in zip(A,B))
W=7
def P(d,s,fill='none',sw=W,extra=''):
  st='' if 'stroke=' in extra else f' stroke="{s.ink}"'
  return f'<path d="{d}" fill="{fill}"{st} stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'
def T(x,y,sc,body):return f'<g transform="translate({x:.0f} {y:.0f}) scale({sc:.2f})">{body}</g>'
# ---------- vessels (origin = base center, ~260 tall at scale 1) ----------
def v_wine(s,liq):return P('M-70 -260h140q8 95-20 140q-20 30-50 30t-50-30q-28-45-20-140z',s,'#ffffff80')+P('M-63 -190h126q-4 40-24 66q-18 22-39 22t-39-22q-20-26-24-66z',s,s.grad(liq),5)+P('M0 -88v78M-55 0h110',s)+P('M-38 -240q-6 30 0 60',s,sw=4,extra=' opacity=".5"')
def v_flute(s,liq):b=''.join(P(f'M{s.r.randint(-18,18)} {-120-i*28}h.1',s,sw=7,extra=f' stroke="{mix(liq,"#ffffff",.6)}"') for i in range(4));return P('M-34 -290h68q4 120-14 160q-10 20-20 20t-20-20q-18-40-14-160z',s,'#ffffff80')+P('M-30 -240h60q0 85-12 110q-8 14-18 14t-18-14q-12-25-12-110z',s,s.grad(liq),5)+b+P('M0 -110v100M-45 0h90',s)
def v_snifter(s,liq):return P('M-52 -230h104q50 60 30 130q-18 60-82 64q-64-4-82-64q-20-70 30-130z',s,'#ffffff80')+P('M-88 -150h176q8 46-12 80q-20 34-76 36q-56-2-76-36q-20-34-12-80z',s,s.grad(liq),5)+P('M0 -36v26M-50 0h100',s)
def v_rocks(s,liq):return P('M-80 -170h160l-12 160q-2 10-12 10h-112q-10 0-12-10z',s,'#ffffff80')+P('M-75 -110h150l-8 98q-1 6-8 6h-118q-7 0-8-6z',s,s.grad(liq),5)+P('M-40 -140l30-12 14 28-30 12z',s,'#ffffffb0',5)+P('M8 -128l34-4 4 30-34 4z',s,'#ffffffb0',5)
def v_pint(s,liq):return P('M-70 -280h140l-16 270q-1 10-11 10h-86q-10 0-11-10z',s,s.grad(liq,'#fff4c8',.35))+P('M-74 -280q14-36 44-18q20-30 52-6q30-22 50 14q10 20-8 30h-130q-18-6-8-20z',s,'#fffdf4',6)+''.join(P(f'M{x} {y}h.1',s,sw=6,extra=' stroke="#ffffff" opacity=".8"') for x,y in [(s.r.randint(-40,40),s.r.randint(-200,-60)) for _ in range(5)])
def v_tulip(s,liq):return P('M-60 -280q-14 80 20 140q14 24 40 24t40-24q34-60 20-140z',s,s.grad(liq,'#fff4c8',.35))+P('M-62 -280q20-26 62-12q42-14 62 12q-10 18-62 14q-52 4-62-14z',s,'#fffdf4',6)+P('M0 -116v106M-48 0h96',s)
def v_sake(s,liq):return P('M-46 -250h32v20q44 40 44 110q0 70-30 110h-60q-30-40-30-110q0-70 44-110z',s,s.grad('#f6f1e6','#ffffff',.2))+P('M-70 -150q30 14 60 0',s,sw=5)+T(95,0,1,P('M-46 -70h92l-14 64q-2 6-8 6h-48q-6 0-8-6z',s,'#fbfaf2')+P('M-40 -60h80',s,s.grad(liq),4))
def v_cup(s,liq):st=''.join(P(f'M{x} -250q-18 26 0 52q14 22 0 46',s,sw=5,extra=' opacity=".55"') for x in (-30,25));return P('M-100 -160h200v70q0 90-100 90t-100-90z',s,'#ffffff')+P('M-92 -148h184',s,s.grad(liq),14)+P('M100 -130h18a36 36 0 0 1 0 72h-22',s)+P('M-140 0h280',s)+st
def v_chawan(s,liq):return P('M-120 -140h240q-6 110-80 136h-80q-74-26-80-136z',s,s.grad('#fbf6ec','#e9dcc0',.3))+f'<ellipse cx="0" cy="-140" rx="120" ry="22" fill="{liq}" stroke="{s.ink}" stroke-width="6"/>'+P('M-60 -146q30-10 60 2q30 8 50-4',s,sw=3,extra=' stroke="#d6ecb0"')+P('M-60 -6h120',s)+T(150,-10,1,P('M-18 0v-90q-26-50 0-120q26 70 0 120',s,'#efe2c0',5)+''.join(P(f'M{-14+i*7} -100l{-8+i*4} -90',s,sw=3) for i in range(5)))
def v_espresso(s,liq):return P('M-70 -110h140v40q0 70-70 70t-70-70z',s,'#ffffff')+P('M-64 -100h128',s,'none',12,extra=f' stroke="{liq}"')+P('M70 -90h14a26 26 0 0 1 0 52h-18',s)+P('M-110 0h220',s)+P('M-10 -200q-16 22 0 44',s,sw=5,extra=' opacity=".5"')
def v_bottle(s,liq):return P('M-24 -300h48v60q44 30 44 80v150q0 10-10 10h-116q-10 0-10-10v-150q0-50 44-80z',s,s.grad(liq))+P('M-56 -150h112v70h-112z',s,'#fffaf0',5)+P('M-28 -310h56v20h-56z',s,s.acc,5)
def v_milk(s,liq):return P('M-40 -300h80v40q40 30 40 80v170q0 10-10 10h-140q-10 0-10-10v-170q0-50 40-80z',s,'#ffffff')+P('M-80 -150h160v130h-160z',s,s.grad('#ffffff',s.acc,.25),0)+P('M-46 -320h92v20h-92z',s,s.acc,5)
def v_juice(s,liq):return P('M-66 -250h132l-14 240q-1 10-11 10h-82q-10 0-11-10z',s,s.grad(liq,'#fff3d0',.45))+P('M20 -250l40-70h30',s,sw=8)+T(-60,-250,1,P('M0 0a40 40 0 0 1 80 0z',s,mix(liq,'#ffffff',.2),5))
def v_jar(s,liq):return P('M-80 -260h160v20q20 10 20 40v190q0 10-10 10h-200q-10 0-10-10v-190q0-30 20-40z',s,s.grad(liq,'#ffffff',.5))+P('M-86 -170q86 20 172 0v14q-86 20-172 0z',s,'#f2e3c2',5)+P('M-90 -280h180v24h-180z',s,'#e9d8b5',5)
def v_can(s,liq):return P('M-60 -260h120v250q0 10-10 10h-100q-10 0-10-10z',s,s.grad(s.acc,'#ffffff',.4))+P('M-60 -230h120M-60 -40h120',s,sw=5)+P('M-30 -170l40 0-20 40h30l-50 60 14-44h-24z',s,'#ffffff',5)
def v_shaker(s,liq):return P('M-70 -240h140l-10 230q-1 10-10 10h-100q-10 0-10-10z',s,'#ffffff')+P('M-66 -150h132l-7 140h-118z',s,s.grad(liq),0)+P('M-76 -280h152v40h-152z',s,s.acc,6)+P('M-40 -300h80v20h-80z',s,s.acc,5)
def v_mug(s,liq):return P('M-90 -220h180v190q0 30-30 30h-120q-30 0-30-30z',s,s.grad(liq,'#ffffff',.35))+P('M90 -180h24a40 40 0 0 1 0 100h-24',s)+P('M-90 -220q90-30 180 0',s,'#fffaf0',6)
def v_carafe(s,liq):return P('M-30 -300h60v70q90 60 90 140q0 90-120 90t-120-90q0-80 90-140z',s,s.grad(liq,'#ffffff',.6))+P('M-110 -60q110 30 220 0',s,sw=4,extra=' opacity=".4"')
def v_ingredient_jar(s,liq):return v_jar(s,liq)

# ---------- v4 vessels ----------
def v_bordeaux(s,liq):return P('M-62 -300h124q14 120-14 170q-20 26-48 26t-48-26q-28-50-14-170z',s,'#ffffff80')+P('M-58 -215h116q2 52-20 82q-16 20-38 20t-38-20q-22-30-20-82z',s,s.grad(liq),4)+P('M0 -104v94M-56 0h112',s)
def v_burgundy(s,liq):return P('M-50 -290h100q60 70 30 150q-22 40-80 42q-58-2-80-42q-30-80 30-150z',s,'#ffffff80')+P('M-92 -190h184q10 30-12 52q-24 34-80 36q-56-2-80-36q-22-22-12-52z',s,s.grad(liq),4)+P('M0 -98v88M-58 0h116',s)
def v_coupe(s,liq):b=''.join(f'<circle cx="{s.r.randint(-60,60)}" cy="{s.r.randint(-205,-180)}" r="3.5" fill="none" stroke="#fff" stroke-width="2"/>' for _ in range(6));return P('M-110 -220h220q-10 70-110 74q-100-4-110-74z',s,s.grad(liq),5)+P('M0 -146v136M-56 0h112',s)+b
def v_weizen(s,liq):return P('M-46 -300q-14 0-12 30q8 70 -6 140q-16 70 12 126q4 4 10 4h84q6 0 10-4q28-56 12-126q-14-70-6-140q2-30-12-30z',s,s.grad(liq,'#fff4c8',.35))+P('M-54 -300q16-40 54-22q40-20 56 22q-10 16-56 10q-46 6-54-10z',s,'#fffdf4',5)
def v_stein(s,liq):return P('M-80 -240h160v220q0 20-20 20h-120q-20 0-20-20z',s,s.grad(liq,'#fff4c8',.3))+P('M80 -200h30a40 40 0 0 1 40 40v60a40 40 0 0 1-40 40h-30',s,'none',12)+P('M-84 -240q20-36 50-18q24-28 52-4q30-20 50 12q6 14-6 16h-140q-10-2-6-6z',s,'#fffdf4',5)+P('M-40 -200v170M0 -200v170M40 -200v170',s,sw=3,extra=' opacity=".25"')
def v_glencairn(s,liq):return P('M-28 -290h56q2 50 34 104q26 50 0 92q-20 30-62 30t-62-30q-26-42 0-92q32-54 34-104z',s,'#ffffff80')+P('M-66 -150h132q14 34-4 58q-20 28-62 28t-62-28q-18-24-4-58z',s,s.grad(liq),4)+P('M-16 -64h32v40h-32z',s,'#ffffffb0',5)+P('M-62 -24h124l-6 24h-112z',s,'#ffffffc0',6)
def v_copita(s,liq):return P('M-36 -280h72q14 60 4 120q-12 50-40 50t-40-50q-10-60 4-120z',s,'#ffffff80')+P('M-42 -190h84q-2 50-16 70q-10 12-26 12t-26-12q-14-20-16-70z',s,s.grad(liq),4)+P('M0 -110v100M-46 0h92',s)
def v_jicara(s,liq):return P('M-130 -110q130-30 260 0q-20 104-130 110q-110-6-130-110z',s,s.grad('#c66a2e','#f6c08a',.4))+P('M-130 -110q130 26 260 0',s,s.grad(liq),6)+''.join(P(f'M{x} -80q4 30 0 60',s,sw=2.5,extra=' opacity=".35"') for x in (-60,0,60))
def v_gaiwan(s,liq):return P('M-90 -150h180q-8 100-90 110q-82-10-90-110z',s,s.grad('#ffffff','#dfe9ee',.2))+P('M-100 -150q100-60 200 0',s,'#ffffff',6)+P('M-14 -190h28v14h-28z',s,'#ffffff',5)+P('M-120 -40h240q-10 40-120 40t-120-40z',s,'#ffffff',6)+P('M-60 -110q60 20 120 0',s,sw=3,extra=f' stroke="{s.acc}"')
def v_yixing(s,liq):return P('M-110 -60q0-110 110-110t110 110q0 60-110 60t-110-60z',s,s.grad('#9a4a2e','#e3a17a',.35))+P('M110 -100q50-20 70-70',s,'none',14,extra=' stroke="#9a4a2e"')+P('M110 -100q50-20 70-70',s,sw=3)+f'<path d="M-104 -120q-80-6-80 52q4 54 84 40v-22q-56 10-58-20q0-30 54-26z" fill="#9a4a2e" stroke="{s.ink}" stroke-width="5" stroke-linejoin="round"/>'+P('M-60 -160q60-30 120 0',s,'#b65c38',5)+f'<circle cx="0" cy="-182" r="14" fill="#b65c38" stroke="{s.ink}" stroke-width="5"/>'
def v_glassmug(s,liq):return P('M-80 -220h160v200q0 20-20 20h-120q-20 0-20-20z',s,'#ffffff70')+P('M-74 -170h148v150q0 14-14 14h-120q-14 0-14-14z',s,s.grad(liq,'#ffffff',.4),4)+P('M80 -190h26a40 40 0 0 1 0 120h-26',s)+''.join(T(s.r.randint(-50,50),s.r.randint(-150,-40),1,f'<g transform="rotate({s.r.randint(0,180)})">'+P('M0 0q16-12 32 0q-16 12-32 0z',s,'#9cc98a',2.5)+'</g>') for _ in range(4))
def v_pourover(s,liq):return P('M-90 -320h180l-60 120h-60z',s,s.grad('#ffffff','#e7e0d6',.3))+P('M-80 -310h160',s,sw=4,extra=' opacity=".4"')+P('M-70 -190h140v150q0 40-40 40h-60q-40 0-40-40z',s,'#ffffff70')+P('M-64 -110h128v70q0 30-30 30h-68q-30 0-30-30z',s,s.grad(liq),4)+P('M0 -200v60',s,sw=4,extra=f' stroke="{liq}"')
def v_moka(s,liq):return P('M-70 0l20-130h100l20 130z',s,s.grad('#c8cdd2','#ffffff',.45))+P('M-60 -130h120v-20h-120z',s,'#a9b0b6',5)+P('M-50 -150l-14-110h128l-14 110z',s,s.grad('#c8cdd2','#ffffff',.45))+P('M64 -240q50 10 40 90',s,'none',10)+P('M-70 -260l-20 30',s,sw=8)+P('M-10 -280h20v20h-20z',s,'#3c3c3c',4)
def v_latte(s,liq):return P('M-56 -260h112l-10 250q0 10-10 10h-72q-10 0-10-10z',s,'#ffffff70')+P('M-52 -230h104l-4 70h-96z',s,'#fbf3e4',4)+P('M-48 -160h96l-4 70h-88z',s,s.grad('#c98f58','#ffffff',.3),4)+P('M-44 -90h88l-4 80h-80z',s,s.grad('#5b3420','#ffffff',.2),4)
def v_highball(s,liq):return P('M-56 -280h112l-8 270q0 10-10 10h-76q-10 0-10-10z',s,s.grad(liq,'#ffffff',.45))+P('M10 -280l40-80',s,sw=7)+P('M-40 -250l22-6 6 22-22 6z',s,'#ffffffa0',4)
def v_tumbler(s,liq):return P('M-74 -200h148l-10 190q0 10-10 10h-108q-10 0-10-10z',s,s.grad(liq,'#ffffff',.5))
def v_jug(s,liq):return P('M-60 -280h100l-10 30q60 40 60 110v120q0 20-20 20h-140q-20 0-20-20v-120q0-70 50-110z',s,s.grad(liq,'#ffffff',.35))+P('M60 -220q60 20 40 120',s,sw=10)+P('M-74 -150h138',s,sw=3,extra=' opacity=".3"')
def v_bottle2(s,liq):return P('M-20 -320h40v90q50 20 50 70v150q0 10-10 10h-120q-10 0-10-10v-150q0-50 50-70z',s,s.grad(liq,'#ffffff',.4))+P('M-60 -140h120v80h-120z',s,mix(s.acc,'#ffffff',.5),4)+P('M-24 -330h48v22h-48z',s,s.acc,5)
# ---------- sources ----------
def grapes(s,c):
  o='';berries=[]
  for row,n in enumerate([4,5,4,4,3,2,1]):
    for i in range(n):
      if s.r.random()<.12 and row>0:continue
      x=(i-(n-1)/2)*34+s.r.uniform(-4,4);y=row*30+s.r.uniform(-3,3);r=s.r.uniform(17,22);berries.append((y,x,r))
  stem=P('M0 -26q4-30 30-56',s,sw=6)+P('M0 -20q-20 30-6 60M2 -20q24 40 10 90',s,sw=2.5,extra=' opacity=".55"')
  for y,x,r in sorted(berries):o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{s.grad(c,"#ffffff",.38)}" stroke="{s.ink}" stroke-width="3.5"/><ellipse cx="{x-r*.35:.1f}" cy="{y-r*.4:.1f}" rx="{r*.28:.1f}" ry="{r*.18:.1f}" fill="#ffffff" opacity=".75"/>'
  leaf=P('M26 -60q20-70 90-62q10 30-12 50q30 6 32 34q-40 18-70-6q-4 30-34 30q-14-30 -6-46z',s,s.grad(mix(s.acc,'#7fae6a',.6),'#ffffff',.3),4)+P('M30 -56q40-24 80-50M58 -40l30 10M70 -70l10-30',s,sw=2.5)
  tend=P('M24 -70q-30-10-24-36q8-18 22-6',s,sw=2.5)
  return tend+leaf+stem+o
def cone(s,sc=1):
  o=''
  for r in range(5):
    y=-50+r*22;w=34-abs(r-1.6)*7
    for i in range(3 if r%2==0 else 2):
      x=(i-(1 if r%2==0 else .5))*w*.9
      o+=f'<path d="M{x-w*.55:.1f} {y}q{w*.55:.1f} -30 {w*1.1:.1f} 0q-{w*.15:.1f} 26 -{w*.55:.1f} 30q-{w*.4:.1f} -4 -{w*.55:.1f} -30z" fill="{s.grad("#a9d06a","#f4ffe0",.45)}" stroke="{s.ink}" stroke-width="3.2" stroke-linejoin="round"/>'
  return T(0,0,sc,o+P('M0 -66v-16',s,sw=4))
def hops(s,c):
  o=P('M-10 -140q-40 60 0 110q40 50 0 120',s,sw=5)+P('M-6 -120q60-40 110-6q-30 6-50 34q-26-4-60-28z',s,s.grad('#9cc76a','#ffffff',.3),4)+P('M0 -118q50-10 96 -2',s,sw=2.5)
  for x,y,sc in [(-48,-50,1.05),(40,10,.9),(-26,80,.8)]:o+=T(x,y,1,cone(s,sc))
  return o
def barley(s,c):
  o=''
  for k in range(3):
    dx=(k-1)*44;o+=P(f'M{dx} 140q{-dx*.2} -120 {dx*.6} -230',s,sw=5)
    for j in range(6):y=-80-j*24;x=dx+dx*.6*(j/8);o+=f'<ellipse cx="{x-12}" cy="{y}" rx="10" ry="18" transform="rotate(-25 {x-12} {y})" fill="{s.grad("#e8c46a")}" stroke="{s.ink}" stroke-width="4"/><ellipse cx="{x+12}" cy="{y+6}" rx="10" ry="18" transform="rotate(25 {x+12} {y+6})" fill="{s.grad("#e8c46a")}" stroke="{s.ink}" stroke-width="4"/>'
  return o
def agave(s,c):
  o='';
  for a in (-70,-45,-20,0,20,45,70):o+=f'<path d="M0 60q{a*.6} -80 {a*1.8} {-150+abs(a)}q{-a*.4} 70 {-a*1.6} {150-abs(a)*.6}z" fill="{s.grad("#8fb9a0","#ffffff",.3)}" stroke="{s.ink}" stroke-width="5" stroke-linejoin="round"/>'
  return o+P('M-60 60q60 30 120 0',s,'#d9c09a',5)
def juniper(s,c):
  o=P('M0 120q-10-120 30-240',s,sw=5)
  for j in range(7):y=90-j*32;x=-j*-4;o+=P(f'M{x} {y}l-40 -14M{x} {y}l40 -18',s,sw=4)
  for x,y in [(-30,-40),(36,10),(-22,60),(20,-90)]:o+=f'<circle cx="{x}" cy="{y}" r="15" fill="{s.grad("#5d7fb0","#ffffff",.3)}" stroke="{s.ink}" stroke-width="4"/>'
  return o
def cherries(s,c):
  o=P('M-120 0q120-60 240 -10',s,sw=6)
  for x in (-80,-30,30,80):
    for d in (-1,1):o+=f'<circle cx="{x+d*14}" cy="{(-30 if x<0 else -20)+abs(x)*.1+22}" r="18" fill="{s.grad("#c0392b","#ffffff",.3)}" stroke="{s.ink}" stroke-width="4"/>'
  return o+P('M-40 -26q40-70 100-40q-40 20-60 50z',s,'#7fae6a',5)+P('M40 -14q50-50 100-10q-50 10-60 40z',s,'#7fae6a',5)
def beans(s,c):
  o=''
  for x,y,r in [(-60,0,-30),(10,-24,20),(60,20,-10),(-10,40,50)]:o+=T(x,y,1,f'<g transform="rotate({r})"><ellipse rx="34" ry="24" fill="{s.grad("#7a4a2a","#ffffff",.25)}" stroke="{s.ink}" stroke-width="5"/>{P("M-26 0q26-10 52 0",s,sw=4)}</g>')
  return o
def leafv(s,col,L=110):
  return f'<path d="M0 0q{L*.45:.0f} -{L*.38:.0f} {L} -4q-{L*.45:.0f} {L*.36:.0f} -{L} 4z" fill="{s.grad(col,"#ffffff",.32)}" stroke="{s.ink}" stroke-width="4"/>'+P(f'M4 0q{L*.5:.0f} -6 {L*.92:.0f} -4',s,sw=2.5)+''.join(P(f'M{x} {-1-x*.02:.1f}l{L*.12:.0f} -{L*.12:.0f}M{x} {1-x*.02:.1f}l{L*.12:.0f} {L*.1:.0f}',s,sw=1.6,extra=' opacity=".7"') for x in range(int(L*.18),int(L*.8),int(L*.16)))
def tealeaf(s,c):
  o=P('M0 130q14-120-8-236',s,sw=5)
  for j,(y,d) in enumerate([(84,-1),(44,1),(4,-1),(-36,1),(-74,-1)]):o+=T(0,y,1,f'<g transform="rotate({d*32}) scale({d*(1-j*.07):.2f} {1-j*.07:.2f})">{leafv(s,"#86bd66",112)}</g>')
  return o+f'<path d="M-8 -104q-16-30 0-58q16 28 0 58z" fill="#d7ebba" stroke="{s.ink}" stroke-width="4"/>'
def citrus(s,c):
  col=c if c not in ('#fcfbf5',) else '#f59a2a'
  o=f'<circle r="80" fill="{s.grad(col,"#ffffff",.25)}" stroke="{s.ink}" stroke-width="6"/><circle r="64" fill="{mix(col,"#ffffff",.55)}" stroke="{s.ink}" stroke-width="4"/>'
  o+=''.join(P(f'M0 0L{60*__import__("math").cos(a*0.6283):.0f} {60*__import__("math").sin(a*0.6283):.0f}',s,sw=4) for a in range(10))
  return o+T(110,40,.6,f'<circle r="70" fill="{s.grad(col,"#ffffff",.2)}" stroke="{s.ink}" stroke-width="7"/>'+P('M0 -70q10-30 40-36',s,sw=7)+P('M10 -80q40-30 80 0q-40 20-80 0z',s,'#8fc06a',6))
def apple(s,c):return f'<path d="M0 -60q-40-30-80 0q-40 40 0 120q40 50 80 20q40 30 80-20q40-80 0-120q-40-30-80 0z" fill="{s.grad("#d9483b","#ffffff",.3)}" stroke="{s.ink}" stroke-width="6"/>'+P('M0 -60q0-30 16-50',s,sw=6)+P('M14 -96q40-30 70 0q-40 20-70 0z',s,'#8fc06a',5)
def rice(s,c):
  o=P('M-100 0h200q-10 90-100 100q-90-10-100-100z',s,s.grad('#e7c9a0','#ffffff',.3))
  for i in range(16):x=s.r.randint(-80,80);y=s.r.randint(-30,0);o+=f'<ellipse cx="{x}" cy="{y}" rx="7" ry="13" transform="rotate({s.r.randint(-60,60)} {x} {y})" fill="#fffdf6" stroke="{s.ink}" stroke-width="3"/>'
  return o+T(140,60,.9,P('M0 0q10-120 -10-240',s,sw=5)+''.join(f'<ellipse cx="{-8-j*1.5}" cy="{-120-j*22}" rx="8" ry="14" transform="rotate(20 {-8-j*1.5} {-120-j*22})" fill="#efd58a" stroke="{s.ink}" stroke-width="3"/>' for j in range(6)))
def cow(s,c):
  body=P('M-130 -40q0-50 60-56h120q50 0 54 50v50q0 16-14 16h-206q-14 0-14-16z',s,'#ffffff')
  spots=f'<path d="M-60 -90q30 10 20 50q-30 10-50-20q0-20 30-30z" fill="{s.ink}" opacity=".85"/><path d="M40 -80q30 0 30 30q-20 20-46 0q-4-20 16-30z" fill="{s.ink}" opacity=".85"/>'
  head=P('M84 -110q50-10 70 20q10 40-20 60q-40 10-56-20z',s,'#ffffff')+P('M100 -110l-6-24M140 -100l14-20',s,sw=5)+f'<ellipse cx="146" cy="-50" rx="22" ry="14" fill="#f4c2c2" stroke="{s.ink}" stroke-width="4"/>'
  legs=P('M-110 26v50M-70 26v50M30 26v50M70 26v50',s,sw=10)
  return legs+body+spots+head+P('M-130 -50q-30 10-24 50',s,sw=5)
def mountain(s,c):
  return P('M-220 80l120-200 60 80 80-150 180 270z',s,s.grad('#9cc3cf','#ffffff',.3))+P('M-20 -190l-30 50 30-10 30 14z',s,'#ffffff',5)+P('M-110 -110l-24 40 26-6z',s,'#ffffff',4)+P('M-60 80q30-40 0-70q-20-30 10-60',s,sw=6,extra=f' stroke="{LIQ["water"]}"')+P('M-60 80q30-40 0-70q-20-30 10-60',s,sw=2)
def honey(s,c):
  o=''
  for x,y in [(0,0),(52,30),(52,-30),(-52,30),(-52,-30),(0,60),(0,-60)]:o+=f'<path d="M{x-30} {y}l15-26h30l15 26-15 26h-30z" fill="{s.grad("#f2b632","#ffffff",.3)}" stroke="{s.ink}" stroke-width="4"/>'
  return o+T(110,-80,1,f'<ellipse rx="24" ry="16" fill="#f2c94c" stroke="{s.ink}" stroke-width="4"/>'+P('M-8 -14v28M6 -14v28',s,sw=4)+P('M-6 -14q-20-30 0-34q14 10 6 34M6 -14q20-30 30-20q-4 20-30 20',s,'#ffffffcc',3))
def cane(s,c):return ''.join(P(f'M{x} 120v-260',s,'none',14,extra=f' stroke="{s.grad("#b9cf72")}"')+P(f'M{x-8} 120v-260M{x+8} 120v-260',s,sw=3)+''.join(P(f'M{x-8} {y}h16',s,sw=4) for y in (60,0,-60)) for x in (-40,0,40))+P('M0 -140q50-40 90-10M-40 -140q-50-40-90-10',s,sw=5)
def herbs(s,c):
  o=''
  for k,a in enumerate((-30,0,30)):
    o+=f'<g transform="rotate({a})">'+P('M0 120v-220',s,sw=5)+''.join(P(f'M0 {y}q{d*40} -10 {d*56} -40q{-d*30} -6 {-d*56} 40z',s,mix(s.acc,"#9cc98a",.5),4) for y,d in [(40,1),(0,-1),(-40,1),(-80,-1)])+'</g>'
  return o
def scoby(s,c):return P('M-110 0q110-50 220 0q-110 40-220 0z',s,'#efe0bd')+P('M-80 -6q80-20 160 0',s,sw=3)
def bubbles(s,c):return ''.join(f'<circle cx="{s.r.randint(-80,80)}" cy="{s.r.randint(-140,40)}" r="{s.r.randint(8,20)}" fill="#ffffff90" stroke="{s.ink}" stroke-width="4"/>' for _ in range(7))
def bolt(s,c):return P('M10 -140l-80 140h60l-20 110 90-150h-62z',s,s.grad('#f2cf4b'),6)
def nuts(s,c):return ''.join(T(x,y,1,f'<ellipse rx="30" ry="40" fill="{s.grad("#d8a86a","#ffffff",.3)}" stroke="{s.ink}" stroke-width="5"/>'+P('M0 -36v72',s,sw=3)) for x,y in [(-40,0),(30,20),(0,-50)])
def berries(s,c):return ''.join(f'<circle cx="{x}" cy="{y}" r="24" fill="{s.grad("#9b2d5c","#ffffff",.3)}" stroke="{s.ink}" stroke-width="5"/>' for x,y in [(-40,0),(10,-20),(50,20),(0,30),(-20,-50)])+P('M10 -70q30-50 80-30q-30 20-50 50z',s,'#8fc06a',5)
def spice(s,c):return T(0,0,1,''.join(P(f'M0 0l{40*__import__("math").cos(a):.0f} {40*__import__("math").sin(a):.0f}l{14*__import__("math").cos(a+1.2):.0f} {14*__import__("math").sin(a+1.2):.0f}z',s,'#c98a4a',4) for a in [i*0.785 for i in range(8)]))+T(90,40,1,P('M-60 0q60-20 120 0l-6 14q-54-16-108 0z',s,'#b0703c',4))
def wood(s,c):return P('M-120 -40h240v80h-240z',s,s.grad('#c8925a','#ffffff',.25))+P('M-120 -40q-20 40 0 80M-80 -10q60-10 120 0M-60 14q60 8 140 0',s,sw=4)+f'<ellipse cx="-120" cy="0" rx="18" ry="40" fill="#e6c08c" stroke="{s.ink}" stroke-width="5"/>'+P('M-126 -14a8 14 0 1 0 12 0',s,sw=3)
SRC={k:v for k,v in globals().items() if k in 'grapes hops barley agave juniper cherries beans tealeaf citrus apple rice cow mountain honey cane herbs scoby bubbles bolt nuts berries spice wood'.split()}
# ---------- settings (background, low contrast) ----------
def set_barrels(s,x,y):
  def bar(bx,by):return P(f'M{bx-70} {by-90}q-14 90 0 180h140q14-90 0-180z',s,s.grad('#c08a52','#ffffff',.35),5)+P(f'M{bx-76} {by-45}h152M{bx-76} {by+45}h152',s,sw=5)+P(f'M{bx-30} {by-90}q-6 90 0 180M{bx+30} {by-90}q6 90 0 180',s,sw=3,extra=' opacity=".5"')
  return f'<g opacity=".55">{bar(x,y)}{bar(x+150,y)}{bar(x+75,y-170)}</g>'
def set_still(s,x,y):return f'<g opacity=".5">'+P(f'M{x-90} {y+80}q-20-120 90-150q110 30 90 150z',s,s.grad('#d08a52','#ffffff',.3),6)+P(f'M{x} {y-70}v-60q0-30 40-30h120v220',s,sw=8)+P(f'M{x+140} {y+30}h40v50h-40z',s,'#d6b896',5)+'</g>'
def set_cellar(s,x,y):return f'<g opacity=".4">'+P(f'M{x-200} {y+120}v-160q200-180 400 0v160',s,'none',10)+P(f'M{x-150} {y+120}v-130q150-140 300 0v130',s,sw=5)+''.join(f'<circle cx="{x-120+i*48}" cy="{y+90}" r="16" fill="{s.acc}" stroke="{s.ink}" stroke-width="4"/>' for i in range(6))+'</g>'
def set_field(s,x,y):return f'<g opacity=".45"><path d="M{x-320} {y+40}q160-90 320-30t320 10v80h-640z" fill="{s.grad(mix(s.acc,"#9cc98a",.5),"#ffffff",.3)}"/>'+P(f'M{x-320} {y+40}q160-90 320-30t320 10',s,sw=4)+''.join(P(f'M{x-280+i*70} {y+100}q20-40 60-60',s,sw=4) for i in range(8))+f'<circle cx="{x+200}" cy="{y-180}" r="46" fill="#ffe08a" stroke="{s.ink}" stroke-width="5"/>'+'</g>'
def set_hills(s,x,y):return f'<g opacity=".45"><path d="M{x-320} {y+60}q120-120 260-40q130-110 380-10v80h-640z" fill="{s.grad(mix(s.acc,"#ffffff",.2),"#ffffff",.4)}"/>'+P(f'M{x-320} {y+60}q120-120 260-40q130-110 380-10',s,sw=4)+'</g>'
def set_kettle(s,x,y):return f'<g opacity=".5">'+P(f'M{x-80} {y+60}q-10-120 80-130q90 10 80 130z',s,s.grad('#9aa9b3','#ffffff',.4),6)+P(f'M{x+70} {y}l70-50M{x-40} {y-80}q40-50 80 0',s,sw=7)+'</g>'
def set_sun(s,x,y):return f'<g opacity=".55"><circle cx="{x}" cy="{y}" r="60" fill="#ffe08a" stroke="{s.ink}" stroke-width="5"/>'+''.join(P(f'M{x+80*__import__("math").cos(a*.785):.0f} {y+80*__import__("math").sin(a*.785):.0f}l{20*__import__("math").cos(a*.785):.0f} {20*__import__("math").sin(a*.785):.0f}',s,sw=5) for a in range(8))+'</g>'
def set_bed(s,x,y):return f'<g opacity=".5">'+P(f'M{x-200} {y}h400l-30 40h-340z',s,'#d9c6a3',5)+''.join(f'<circle cx="{x-170+i*26}" cy="{y-8}" r="9" fill="#b0402f" stroke="{s.ink}" stroke-width="3"/>' for i in range(14))+'</g>'
def set_waves(s,x,y):return f'<g opacity=".45">'+''.join(P(f'M{x-300} {y+i*30}q50-24 100 0t100 0t100 0t100 0t100 0t100 0',s,sw=5,extra=f' stroke="{LIQ["water"]}"') for i in range(3))+'</g>'
def set_mount(s,x,y):return f'<g opacity=".6">'+T(512+(x-512)*.3,y+30,1.25,mountain(s,None))+'</g>'
SET={'mount':set_mount,'barrels':set_barrels,'still':set_still,'cellar':set_cellar,'field':set_field,'hills':set_hills,'kettle':set_kettle,'sun':set_sun,'bed':set_bed,'waves':set_waves}
VES={k[2:]:v for k,v in globals().items() if k.startswith('v_')}
# ---------- scene choice from data ----------
def has(t,*w):return any(re.search(r'\b'+x,t,re.I) for x in w)
REDG='cabernet merlot pinot noir syrah shiraz grenache garnacha tempranillo sangiovese nebbiolo malbec zinfandel primitivo gamay barbera mourv monastrell tannat carignan carm.n.re pinotage aglianico'.split()
def scene(k,d):
  ac=ACAD.get(k if d['kind']=='group' else k.rsplit('.',1)[0],'');t=d['term'];p=d['path'];df=d['definition'];all_=t+' '+p+' '+df
  pp=' › '.join(p.split(' › ')[1:]);aged=has(t+' '+pp,'aging','aged','oak','barrel','cask','reserva','riserva','crianza','a.ejo','reposado','XO','VSOP','VS\\b','yr','hors','vieux','colheita','tawny')
  sc={'vessel':'wine','liq':'red','src':[],'set':None}
  if ac=='Wine':
    red=(has(pp,'aging requirements') and not has(t,'white','blanco','ros.','sparkling','cava','lees'))or has(t+' '+pp,'red','tinto','rosso','noir')or has(t,*REDG)or has(df,'red wine','red grape')
    if has(t+' '+pp,'sparkling','champagne','cava','prosecco','cr.mant','sekt','franciacorta','tirage','lees','disgorge'):sc.update(vessel='flute',liq='spark',src=['grapes'],set='cellar')
    elif has(t+' '+pp,'fortified','port','sherry','madeira','marsala','vermouth','banyuls','tawny','rivesaltes'):sc.update(vessel='snifter',liq='tawny',src=['grapes'],set='barrels')
    elif has(t+' '+pp,'ros.'):sc.update(liq='rose',src=['grapes'],set='hills')
    elif has(pp,'rootstock','training','canopy','viticulture','vineyard','harvest','pruning'):sc.update(vessel='wine',liq='red' if red else 'white',src=['grapes'],set='field')
    elif has(pp,'oak','wood','barrel','toast','cask','cooperage') and not has(pp,'aging requirements'):sc.update(vessel='wine',liq='red',src=['wood'],set='barrels')
    else:sc.update(liq='red' if red else 'white',src=['grapes'],set='barrels' if aged else ['hills','field','sun'][s_rng(k)%3])
    sc['grape']=LIQ['red'] if sc['liq'] in('red','rose','tawny') else '#c9d36a'
  elif ac=='Beer':
    liq='dark' if has(all_,'stout','porter','schwarz','black','dark','dunkel','dubbel','mild')else 'amber' if has(all_,'amber','brown','red','bock','m.rzen','vienna','alt','scottish','barley ?wine','old ale','bitter')else 'pale' if has(all_,'wheat','weiss','wit','light','helles','pils','blond','k.lsch','seltzer','golden')else 'gold'
    sc.update(vessel='tulip' if has(all_,'belgian','tripel','strong','barleywine','wee heavy','sour','lambic')else 'pint',liq=liq,src=['hops','barley'] if not has(t,'hop') else ['hops'],set='barrels' if has(all_,'wood','barrel','aged','lambic','flanders')else 'field')
    if has(t,'seltzer'):sc.update(vessel='bottle',liq='clear',src=['bubbles','citrus'],set=None)
  elif ac=='Spirits':
    clear=has(t,'blanco','plata','joven','vodka','gin','white','grappa','pisco','silver','navy','absinthe','sotol','raicilla')and not has(t,'a.ejo','reposado')
    src=['agave'] if has(all_,'agave','tequila','mezcal','sotol','raicilla')else ['juniper'] if has(all_,'gin','juniper','genever')else ['herbs'] if has(all_,'absinthe','herbal','liqueur','bitter','amaro','chartreuse')else ['cane'] if has(all_,'rum','rhum','cacha.a','cane')else ['apple'] if has(all_,'calvados','apple','cider')else ['grapes'] if has(all_,'cognac','armagnac','brandy','grappa','pisco','eau-de-vie','grape')else ['barley']
    sc.update(vessel='rocks' if has(all_,'whisk','bourbon','rye','scotch')else 'snifter' if src==['grapes'] or src==['apple'] else 'rocks',liq='clear' if clear else 'amber',src=src,set='barrels' if aged and not clear else 'still')
    if src==['herbs']:sc['liq']='green' if has(all_,'absinthe')else 'amber'
    if has(t,'orange'):sc.update(src=['citrus'],liq='orange')
    sc['grape']='#c9d36a'
  elif ac=='Coffee':
    sc.update(vessel='espresso' if has(t,'espresso','lungo','ristretto','doppio','macchiato')else 'cup',liq='coffee',src=['cherries'] if has(all_,'cherr','process','washed','natural','honey','pulp','harvest','variet','arabica','robusta','species','farm')else ['beans'],set='bed' if has(all_,'natural','dry','drying','sun')else 'field' if has(all_,'farm','altitude','variet','species','arabica','harvest')else 'kettle')
    if has(all_,'barrel'):sc['set']='barrels'
    if has(all_,'washed','wet'):sc['set']='waves'
  elif ac=='Tea':
    liq='matcha' if has(t,'matcha')else 'whitetea' if has(all_,'white tea','silver needle','white peony','bai')else 'blacktea' if has(all_,'black tea','assam','darjeeling','ceylon','keemun','pu.?erh','dark tea')else 'oolong' if has(all_,'oolong')else 'greentea'
    sc.update(vessel='chawan' if liq=='matcha' else 'cup',liq=liq,src=['tealeaf'],set='hills' if has(all_,'region','garden','mountain','province','grown')else 'kettle' if s_rng(k)%2 else 'hills')
  elif ac=='Kombucha':sc.update(vessel='jar',liq='blacktea',src=['scoby'] if has(all_,'scoby','culture','mother')else ['tealeaf'],set='kettle')
  elif ac=='Water':sc.update(vessel='bottle',liq='water',src=['bubbles'] if has(all_,'sparkling','carbonat','seltzer')else [],set='mount' if not has(all_,'treat','tap','municipal','purif','filter','sparkling','carbonat') else 'waves' if has(all_,'treat','tap','municipal','purif','filter')else 'sun' if has(all_,'spring','artesian','glacier')else 'hills')
  elif ac=='Juice':
    src=['apple'] if has(t,'apple','cider')else ['berries'] if has(t,'berr','grape','cranberr','pomegran')else ['citrus']
    liq={'apple':'apple','berries':'berry','citrus':'orange'}[src[0]];sc.update(vessel='juice',liq=liq,src=src,set='sun' if has(all_,'grove','fruit','orange','juice')else 'field')
  elif ac=='Milk':sc.update(vessel='milk',liq='milk',src=['nuts'] if has(all_,'plant','almond','oat','soy','nut','coconut')else ['cow'],set='hills')
  elif ac=='Protein':sc.update(vessel='shaker',liq='milk',src=['nuts'] if has(all_,'plant','pea','soy')else ['barley'] if has(all_,'grain','rice')else ['bolt'],set=None)
  elif ac=='Energy':sc.update(vessel='can' if not has(all_,'tea','coffee','mate','guayusa')else 'mug',liq='gold',src=['bolt'] if not has(all_,'guarana','mate','tea','coffee')else ['tealeaf'] if has(all_,'tea','mate','guayusa')else ['beans'],set=None)
  elif ac=='Health':sc.update(vessel='carafe',liq='green' if has(all_,'green','juice','vegetable')else 'water',src=['herbs'],set='sun')
  elif ac=='Carbonated':sc.update(vessel='bottle',liq='cola' if has(all_,'cola','root','pepper','dark')else 'clear' if has(all_,'soda','tonic','club','seltzer','water')else 'gold',src=['bubbles','citrus'] if has(all_,'lemon','lime','citrus','tonic')else ['bubbles','spice'] if has(all_,'ginger','root','spice')else ['bubbles'],set=None)
  elif ac=='Fermented':
    if has(all_,'sake','junmai','ginjo','koji','rice','shochu','seimaibuai'):sc.update(vessel='sake',liq='sake',src=['rice'],set='kettle')
    elif has(all_,'mead','honey','braggot','melomel'):sc.update(vessel='snifter',liq='gold',src=['honey'],set='field')
    elif has(all_,'cider','perry','apple','pear'):sc.update(vessel='pint',liq='apple',src=['apple'],set='field')
    elif has(all_,'kefir','milk','yogurt','lassi'):sc.update(vessel='milk',liq='milk',src=['cow'],set='hills')
    else:sc.update(vessel='jar',liq='amber',src=['spice'],set='kettle')
  else:sc.update(vessel='mug',liq='orange',src=['spice'] if has(all_,'spice','ginger','chai','cinnamon')else ['berries'] if has(all_,'hibiscus','berr','fruit')else ['tealeaf'] if has(all_,'tea','mate')else ['herbs'],set='hills')
  if aged and sc['set'] in (None,'hills','field','kettle') and ac in('Wine','Spirits','Beer','Coffee'):sc['set']='barrels'
  return ac,sc

def set_agave(s,x,y):return '<g opacity=".5">'+''.join(T(x-330+i*66+(r%2)*33,y+40-r*34,.32-r*.05,agave(s,None)) for r in range(3) for i in range(11))+'</g>'
def set_rows(s,x,y):return '<g opacity=".5">'+''.join(P(f'M{x-360+i*40} {y+90}L{x-40+i*12} {y-30}',s,sw=3) for i in range(18))+P(f'M{x-380} {y-30}h760',s,sw=3)+''.join(f'<circle cx="{x-300+i*60}" cy="{y-30}" r="10" fill="{mix(s.acc,"#7fae6a",.5)}" stroke="{s.ink}" stroke-width="2.5"/>' for i in range(11))+'</g>'
def set_distillery(s,x,y):return '<g opacity=".45">'+P(f'M{x-160} {y+60}v-140l80-50 80 50v140z',s,mix(s.acc,'#ffffff',.5),5)+P(f'M{x+40} {y+60}v-160h40v160',s,mix(s.acc,'#ffffff',.3),5)+P(f'M{x+60} {y-110}q-20-24 8-44q24-14 8-34',s,sw=4,extra=' opacity=".5"')+P(f'M{x-120} {y+60}v-60h40v60M{x-40} {y-10}h30v30h-30z',s,sw=4)+'</g>'
def set_terraces(s,x,y):return '<g opacity=".5">'+''.join(f'<path d="M{x-380} {y+60-i*46}q380 -{40+i*10} 760 0v40q-380 -{40+i*10} -760 0z" fill="{mix(s.acc,"#ffffff",.15+i*.12)}"/>'+P(f'M{x-380} {y+60-i*46}q380 -{40+i*10} 760 0',s,sw=3)+''.join(f'<circle cx="{x-340+j*68}" cy="{y+48-i*46-(abs(j-5)<3)*12}" r="9" fill="#7fae6a" opacity=".8"/>' for j in range(11)) for i in range(4))+'</g>'
def set_farm(s,x,y):return '<g opacity=".5">'+P(f'M{x-380} {y+70}q190-120 380-60t380 20v60h-760z',s,mix(s.acc,"#9cc98a",.45),3)+''.join(T(x-300+i*90,y+20-(i%2)*20,1,f'<ellipse rx="34" ry="28" fill="#7fae6a" stroke="{s.ink}" stroke-width="3"/>'+''.join(f'<circle cx="{a}" cy="{b}" r="5" fill="#c0392b"/>' for a,b in((-12,-4),(8,6),(14,-10)))) for i in range(7))+'</g>'
def set_pasture(s,x,y):return '<g opacity=".5">'+P(f'M{x-380} {y+60}q200-90 400-40t360 0v80h-760z',s,mix(s.acc,"#b9dca0",.5),3)+''.join(P(f'M{x-330+i*70} {y+30}v-60',s,sw=5) for i in range(10))+P(f'M{x-330} {y-10}h630M{x-330} {y+10}h630',s,sw=3)+'</g>'
def set_orchard(s,x,y):return '<g opacity=".5">'+''.join(T(x-300+i*120,y+40-(i%2)*24,1,P('M0 0v-70',s,sw=8)+f'<circle cy="-110" r="56" fill="{mix(s.acc,"#8fc06a",.55)}" stroke="{s.ink}" stroke-width="3"/>'+''.join(f'<circle cx="{a}" cy="{b}" r="7" fill="{s.acc}" stroke="{s.ink}" stroke-width="2"/>' for a,b in((-20,-120),(18,-96),(10,-140),(-26,-90)))) for i in range(6))+'</g>'
SET.update(agave=set_agave,rows=set_rows,distillery=set_distillery,terraces=set_terraces,farm=set_farm,pasture=set_pasture,orchard=set_orchard)
VES.update({k[2:]:v for k,v in globals().items() if k.startswith('v_') and k[2:] not in VES})
VAR={'wine':['wine','bordeaux','burgundy'],'flute':['flute','flute','coupe'],'snifter':['snifter','glencairn','copita'],'rocks':['rocks','glencairn','rocks'],'pint':['pint','stein','weizen','pint'],
'tulip':['tulip','snifter'],'cup':['cup','gaiwan','glassmug','yixing'],'espresso':['espresso','moka'],'bottle':['bottle','bottle2'],'juice':['juice','highball','jug','tumbler'],'milk':['milk','jug'],'carafe':['carafe','jug']}
SETVAR={'hills':['hills','rows','orchard'],'field':['field','rows','farm'],'barrels':['barrels','cellar','barrels'],'still':['still','distillery'],'kettle':['kettle','terraces'],'sun':['sun','orchard']}
TOD={'dawn':('#fbe3e8',.25),'noon':('#ffffff',.0),'golden':('#ffe1a8',.3),'dusk':('#d9c7ef',.3)}
def s_rng(k):return int(hashlib.md5(k.encode()).hexdigest()[:8],16)
def wrap(t,n):
  w=t.replace('\u200b',' \u200b').split();L=[];c=''
  for x in w:
    if len(c)+len(x)+1>n and c:L.append(c.replace(' \u200b',''));c=x.replace('\u200b','')
    else:c=(c+' '+x).strip()
  return [x.replace(' \u200b','').replace('\u200b','') for x in L+([c] if c else [])]
FX={'wine':(70,-260,-110,-190,63),'flute':(34,-290,-110,-240,30),'snifter':(84,-230,-40,-150,86),'rocks':(80,-170,0,-110,75),'pint':(70,-262,0,None,0),
'tulip':(58,-262,-120,None,0),'sake':(66,-230,0,None,0),'cup':(100,-160,0,-148,92),'chawan':(118,-140,-6,None,0),'espresso':(70,-110,0,-100,64),'bottle':(66,-230,0,None,0),
'milk':(78,-250,0,None,0),'juice':(64,-250,0,-236,62),'jar':(98,-240,0,None,0),'can':(60,-260,0,None,0),'shaker':(68,-240,0,None,0),'mug':(88,-220,0,-214,82),'carafe':(110,-220,0,None,0),'ingredient_jar':(98,-240,0,None,0)}
FX.update({'bordeaux':(60,-300,-110,-215,58),'burgundy':(92,-290,-100,-190,92),'coupe':(110,-220,-150,-218,108),'weizen':(48,-280,0,None,0),'stein':(80,-222,0,None,0),
'glencairn':(70,-280,-64,-150,64),'copita':(42,-280,-110,-190,42),'jicara':(130,-110,-4,-110,128),'gaiwan':(90,-150,-40,None,0),'yixing':(110,-170,0,None,0),'glassmug':(80,-220,0,-170,74),
'pourover':(70,-190,0,-110,64),'moka':(70,-260,0,None,0),'latte':(56,-260,0,None,0),'highball':(56,-280,0,None,0),'tumbler':(74,-200,0,None,0),'jug':(80,-250,0,None,0),'bottle2':(70,-230,0,None,0)})
def shadow(s,v):hw=FX[v][0];return f'<ellipse cx="{hw*.25:.0f}" cy="4" rx="{hw*1.45:.0f}" ry="16" fill="{s.ink}" opacity=".14"/><ellipse cx="{hw*.1:.0f}" cy="2" rx="{hw*.9:.0f}" ry="9" fill="{s.ink}" opacity=".12"/>'
def gloss(s,v,liq,sc):
  hw,yt,yb,sy,shw=FX[v];o=''
  if sy is not None:o+=f'<ellipse cx="0" cy="{sy}" rx="{shw}" ry="9" fill="{mix(liq,"#ffffff",.35)}" stroke="{s.ink}" stroke-width="2.5" opacity=".95"/>'
  o+=f'<path d="M{-hw*.62:.0f} {yt+24} q{-hw*.12:.0f} {(yb-yt)*.4:.0f} {hw*.04:.0f} {(yb-yt)*.72:.0f}" stroke="#ffffff" stroke-width="{max(5,hw*.09):.0f}" stroke-linecap="round" fill="none" opacity=".8"/>'
  o+=f'<circle cx="{-hw*.62:.0f}" cy="{yt+(yb-yt)*.86:.0f}" r="4" fill="#ffffff" opacity=".6"/>'
  o+=f'<path d="M{hw*.7:.0f} {yt+30} q{hw*.18:.0f} {(yb-yt)*.4:.0f} {-hw*.05:.0f} {(yb-yt)*.75:.0f}" stroke="{s.ink}" stroke-width="{max(8,hw*.18):.0f}" stroke-linecap="round" fill="none" opacity=".09"/>'
  if sc.get('bub'):o+=''.join(f'<circle cx="{s.r.uniform(-hw*.5,hw*.5):.0f}" cy="{s.r.uniform(yt+(yb-yt)*.35,yb-20):.0f}" r="{s.r.uniform(2.5,5.5):.1f}" fill="none" stroke="#ffffff" stroke-width="2.2" opacity=".9"/>' for _ in range(12))
  if v in('pint','tulip'):o+=''.join(f'<circle cx="{s.r.uniform(-hw*.9,hw*.9):.0f}" cy="{yt+s.r.uniform(-34,4):.0f}" r="{s.r.uniform(3,7):.1f}" fill="none" stroke="{s.ink}" stroke-width="1.6" opacity=".35"/>' for _ in range(14))
  if v in('cup','espresso') and liq==LIQ['coffee']:o+=f'<ellipse cx="0" cy="{sy}" rx="{shw}" ry="9" fill="#c98f58" stroke="{s.ink}" stroke-width="2.5"/><path d="M{-shw*.5:.0f} {sy-1}q{shw*.3:.0f} -6 {shw*.6:.0f} 2q{shw*.2:.0f} 4 {shw*.4:.0f} -2" stroke="#efd2a8" stroke-width="3" fill="none" stroke-linecap="round"/>'
  if v in('cup','espresso','mug','chawan') and liq not in (LIQ['orange'],):o+=''.join(f'<path d="M{x} {yt-30}q-16 -26 0 -52q14 -24 0 -48" stroke="{s.ink}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".35"/>' for x in (-hw*.3,hw*.15))
  return o
def backdrop(s,bg,bg2,acc,ink,rng,ac):
  sky=f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mix(bg,"#ffffff",.55)}"/><stop offset=".62" stop-color="{bg}"/><stop offset="1" stop-color="{bg2}"/></linearGradient>'
  gnd=f'<linearGradient id="gnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{mix(bg2,acc,.18)}"/><stop offset=".3" stop-color="{mix(bg,"#ffffff",.3)}"/><stop offset="1" stop-color="{mix(bg,"#ffffff",.45)}"/></linearGradient>'
  vig=f'<radialGradient id="vig" cx=".5" cy=".42" r=".75"><stop offset=".6" stop-color="{ink}" stop-opacity="0"/><stop offset="1" stop-color="{ink}" stop-opacity=".16"/></radialGradient>'
  hz=rng.randint(560,585);h1=rng.randint(470,520);h2=rng.randint(500,540)
  a1,a2=rng.randint(300,420),rng.randint(640,760)
  far=f'<path d="M0 {hz}V{h1}C{a1*.5:.0f} {h1-rng.randint(40,90)} {a1} {h1-rng.randint(0,40)} {a1} {h1-10}S{a2} {h1+rng.randint(-30,10)} {a2} {h1-20}S1024 {h1-rng.randint(20,70)} 1024 {h1}V{hz}z" fill="{mix(bg2,acc,.22)}" opacity=".55"/>'
  mid=f'<path d="M0 {hz}V{h2}C{rng.randint(150,250)} {h2+40} {rng.randint(350,450)} {h2-30} 520 {h2}S{rng.randint(800,900)} {h2+30} 1024 {h2-10}V{hz}z" fill="{mix(bg2,acc,.35)}" opacity=".45"/>'
  ground=f'<rect y="{hz}" width="1024" height="{1024-hz}" fill="url(#gnd)"/>'
  sun=f'<circle cx="{rng.choice([180,840])}" cy="{rng.randint(150,200)}" r="{rng.randint(46,64)}" fill="{mix(acc,"#ffffff",.6)}" opacity=".6"/>' if rng.random()<.5 else ''
  return sky+gnd+vig,f'<rect width="1024" height="1024" fill="url(#sky)"/>{sun}{far}{mid}{ground}'
def clean_title(k,d):
  t=d['term'];chips=[]
  if ' · ' in t:t,spec=t.split(' · ',1);m=re.match(r'([^()]+)',spec);chips.append(m.group(1).strip().rstrip(','))
  m=re.search(r'\s*\(([^)]*)\)\s*$',t)
  if m:t=t[:m.start()];chips.append(m.group(1).replace('/',' / '))
  par=SUBNAME.get(k.rsplit('.',1)[0],'') if d['kind']=='term' else ''
  par=re.sub(r'\s*\(.*?\)','',re.sub(r'^\d+\s+','',par)).strip()
  if chips and par and len(par)<=22 and not re.search(r'[:&%]|Method|Terms|Other|Generic|Requirements|Categories',par):chips.insert(0,par)
  return t.strip(),' · '.join(chips)[:44]
def refine(k,d,ac,sc,rng):
  t=d['term'];a=t+' '+d['path']+' '+d['definition'];v=sc['vessel']
  if ac=='Wine' and v=='wine':v='bordeaux' if has(a,'cabernet','merlot','bordeaux','carm','malbec') else 'burgundy' if has(a,'pinot noir','nebbiolo','burgund','chardonnay','gamay') else rng.choice(VAR['wine'])
  elif ac=='Spirits':v='jicara' if has(a,'mezcal','raicilla','sotol') else 'copita' if has(a,'sherry','brandy de jerez','pisco') else 'glencairn' if has(a,'scotch','single malt','whisk') and rng.random()<.6 else rng.choice(VAR.get(v,[v]))
  elif ac=='Beer':v='weizen' if has(a,'wheat','weiss','weizen','wit') else 'stein' if has(a,'m.rzen','festbier','helles','dunkel','bock','german') else 'snifter' if has(a,'barley ?wine','imperial','eisbock','strong') else rng.choice(VAR.get(v,[v]))
  elif ac=='Tea' and v=='cup':v='yixing' if has(a,'pu.?erh','oolong','dark tea') else 'gaiwan' if has(a,'white tea','yellow','chinese','china') else 'glassmug' if has(a,'green tea','herbal') else rng.choice(VAR['cup'])
  elif ac=='Coffee':v='pourover' if has(t,'pour','v60','chemex','kalita','drip','filter') else 'moka' if has(t,'moka') else 'latte' if has(t,'latte','flat white','cappuccino','cortado') else 'espresso' if v=='espresso' else rng.choice(['cup','cup','espresso','pourover'])
  elif v in VAR:v=rng.choice(VAR[v])
  sc['vessel']=v
  st=sc['set']
  if st:
    if ac=='Wine' and st=='hills':st='rows'
    elif ac=='Tea' and st in('kettle','hills'):st='terraces' if rng.random()<.6 else st
    elif ac=='Coffee' and st=='field':st='farm'
    elif ac in('Milk',) and st=='hills':st='pasture'
    elif ac=='Juice' and 'apple' in sc['src']:st='orchard'
    elif ac=='Spirits' and st=='still':st=rng.choice(['still','distillery'])
    elif st in SETVAR:st=rng.choice(SETVAR[st])
  if ac=='Spirits' and 'agave' in sc['src']:st='agave'
  sc['set']=st
  sc['tod']='golden' if st in('rows','agave') else 'dusk' if st=='cellar' else rng.choice(list(TOD))
def card(k):
  d=D[k];ac,sc=scene(k,d);bg,bg2,ink,acc=PAL.get(ac,PAL['Regional']);rng=random.Random(s_rng(k));s=S(ink,acc,rng);refine(k,d,ac,sc,rng)
  tc,ta=TOD[sc['tod']];bg=mix(bg,tc,ta*.6)
  liq=LIQ[sc['liq']];lay=rng.randint(0,4);sw=rng.choice([1,-1]);sc['bub']=sc['vessel'] in('flute',) or (sc['vessel']=='bottle' and 'bubbles' in sc['src']) or sc['liq'] in ('spark',)
  vx={0:512,1:600,2:430,3:380,4:650}[lay];vx=512+(vx-512)*sw;vy=560
  defs0,back=backdrop(s,bg,bg2,acc,ink,rng,ac)
  if sc['set'] in('field','sun'):back=re.sub(r'<circle cx="(180|840)"[^>]*/>','',back)
  parts=[]
  if sc['set']:
    sx=((vx-300 if vx>512 else vx+300) if sc['set'] in('kettle','still') else 512+sw*rng.randint(-120,120))-(75 if sc['set']=='barrels' else 0);sy=rng.randint(430,450);parts.append(SET[sc['set']](s,sx,sy))
  srcs=sc['src'][:2];slots=[(vx-sw*270,rng.randint(380,420)),(vx+sw*250,rng.randint(390,430))]
  if lay==0:slots=[(vx-260,rng.randint(380,420)),(vx+260,rng.randint(390,430))]
  for i,nm in enumerate(srcs or []):
    x,y=slots[i];x=max(250 if nm not in('mountain','cow') else 300,min(774 if nm not in('mountain','cow') else 640,x));col=sc.get('grape',liq);big=1.35 if nm in('bubbles','citrus') and ac=='Beer' else 1;parts.append(T(x,y,big*rng.uniform(.82,.98)*(1 if nm not in('cow','mountain') else .8),SRC[nm](s,col)))
  if len(srcs)==1 and rng.random()<.6:
    nm=srcs[0];x,y=slots[1];x=max(250,min(774,x))
    if nm in('grapes','hops','tealeaf','beans','citrus','cherries','berries','herbs','juniper','barley'):parts.append(T(x,y+10,rng.uniform(.6,.72),SRC[nm](s,sc.get('grape',liq))))
  vs=rng.uniform(1.0,1.12)*(1.05 if lay in(3,4) else 1);parts.append(T(vx,vy,vs,shadow(s,sc['vessel'])+VES[sc['vessel']](s,liq)+gloss(s,sc['vessel'],liq,sc)))
  for _ in range(rng.randint(0,2)):x=rng.randint(120,904);y=rng.randint(140,300);r=rng.randint(4,7);parts.append(f'<path d="M{x} {y-r}v{2*r}M{x-r} {y}h{2*r}" stroke="{acc}" stroke-width="3" stroke-linecap="round" opacity=".8"/>')
  title,chip=clean_title(k,d)
  gl=GUILD.get(k.split('.')[0],'');label=(gl+' · '+ac.upper()+(' ACADEMY' if ac else '')).strip(' ·')
  M=80;txt=f'<text class="lb" x="{M}" y="74" font-family="Helvetica,Arial,sans-serif" font-size="{LABEL_FS}" letter-spacing="4" fill="{ink}" opacity=".7">{esc(label)}</text>'
  fs,mfs=TITLE_FS,BODY_FS;tl=mwrap(title,_TF,fs,TITLE_W)[:3];ty=704
  cy=ty+(len(tl)-1)*fs*1.06+(30 if chip else 0);my=cy+(52 if chip else 16)+mfs;n=max(1,int((978-my)//(mfs*1.3))+1);ml=trim_to(O[k],n);bottom=my+(len(ml)-1)*mfs*1.3
  txt+=''.join(f'<text class="tt" x="{M}" y="{ty+i*fs*1.06:.0f}" font-family="Georgia,\'Iowan Old Style\',\'Palatino Linotype\',\'Book Antiqua\',\'Noto Serif\',\'Gelasio\',serif" font-size="{fs}" font-weight="700" fill="{ink}">{esc(x)}</text>' for i,x in enumerate(tl))
  if chip:cw=tw(_CF,chip,CHIP_FS)*1.08+36;txt+=f'<rect x="{M}" y="{cy:.0f}" width="{cw:.0f}" height="38" rx="19" fill="{mix(acc,"#ffffff",.55)}" stroke="{ink}" stroke-opacity=".35" stroke-width="1.5"/><text class="ch" x="{M+18}" y="{cy+26:.0f}" font-family="Helvetica,Arial,sans-serif" font-size="{CHIP_FS}" font-weight="600" fill="{ink}">{esc(chip)}</text>'
  txt+=''.join(f'<text class="bd" x="{M}" y="{my+i*mfs*1.3:.0f}" font-family="Helvetica,Arial,sans-serif" font-size="{mfs}" fill="{ink}" opacity=".88">{esc(x)}</text>' for i,x in enumerate(ml))
  defs=''.join(v[1] for v in s.defs.values())
  grain=f'<filter id="gr" x="0" y="0" width="1" height="1"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="{s_rng(k)%97}"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .06 0"/></filter>'
  svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="{esc(d["term"])}"><defs>{defs0}{grain}{defs}</defs>{back}'
   f'<g transform="translate(512 590) scale(1.24) translate(-512 -560)">{"".join(parts)}</g>'
   f'<rect width="1024" height="1024" fill="url(#vig)"/><rect width="1024" height="1024" filter="url(#gr)"/>{txt}</svg>')
  return svg,(ty,bottom,sc)
if __name__=='__main__':
  ids=list(D) if '--all' in sys.argv else [a for a in sys.argv[1:] if not a.startswith('-')]
  out=sys.argv[sys.argv.index('--out')+1] if '--out' in sys.argv else 'cards/generated';os.makedirs(out,exist_ok=True);t0=time.time();bad=[]
  for k in ids:
    svg,(ty,bottom,sc)=card(k);open(f'{out}/{k}.svg','w').write(svg)
    if bottom>990:bad.append((k,bottom))
  print(len(ids),'cards in %.2fs'%(time.time()-t0),'text-overflow',bad[:10])
