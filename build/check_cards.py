# Asserts every card uses identical font sizes per text role and that no text overflows the 1024 card (80px margins).
import os,re,sys,html,collections
sys.argv=[sys.argv[0]];exec(open('build/cards.py').read().split("if __name__")[0])
d='cards/generated';files=sorted(os.listdir(d));sizes=collections.defaultdict(set);bad=[];maxlines=0;longest=('',0)
F={'tt':_TF,'bd':_BF,'ch':_CF,'lb':_BF}
for f in files:
  s=open(f'{d}/{f}').read();tt=0
  for cls,x,y,fs,txt in re.findall(r'<text class="(\w+)" x="([\d.]+)" y="([\d.]+)"[^>]*font-size="([\d.]+)"[^>]*>([^<]*)</text>',s):
    sizes[cls].add(fs);t=html.unescape(txt);w=tw(F[cls],t,float(fs))*(1.12 if cls=='tt' else 1.06)+(18 if cls=='ch' else 0)
    if cls=='lb':w=tw(_BF,t,float(fs))+len(t)*4
    if float(x)+w>1024-60:bad.append((f,cls,t,round(float(x)+w)))
    if float(y)>990:bad.append((f,cls,'below',y))
    if cls=='tt':tt+=1
  if tt==0:bad.append((f,'no title'))
  maxlines=max(maxlines,tt)
ids=set(D);missing=ids-{f[:-4] for f in files}
for k in D:
  t,_=clean_title(k,D[k]);n=len(mwrap(t,_TF,TITLE_FS,TITLE_W))
  if n>longest[1]:longest=(t,n)
print('cards',len(files),'missing',len(missing),'font sizes',{k:sorted(v) for k,v in sizes.items()},'max title lines',maxlines,'longest title',longest)
ok=not missing and all(len(v)==1 for v in sizes.values()) and not bad and maxlines<=3
print('overflow',bad[:10]);print('PASS' if ok else 'FAIL');sys.exit(0 if ok else 1)
