#!/bin/bash
# Opens every definition card at 390x844, 768x1024, 1440x900 and asserts each renders an infographic with no horizontal overflow.
cd "$(dirname "$0")/.." ; PORT=18433
python3 -m http.server $PORT --bind 127.0.0.1 -d "$PWD" >/dev/null 2>&1 & SRV=$!; sleep 1
out=$(google-chrome --headless=new --user-data-dir=$(mktemp -d) --no-sandbox --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --window-size=1600,1200 --virtual-time-budget=300000 --dump-dom "http://127.0.0.1:$PORT/build/igcheck.html" 2>/dev/null | grep -o '<pre id="out">RESULT [^<]*' | sed 's/<pre id="out">//; s/&quot;/"/g; s/&amp;/\&/g')
kill $SRV; echo "$out" | python3 -c "
import sys,json;s=sys.stdin.read().strip()
if not s.startswith('RESULT'): print('NO RESULT');sys.exit(2)
r=json.loads(s[7:]);ok=True
for x in r: print(x['vp'],'terms',x['terms'],'rendered',x['rendered'],'fails',x['fails'],x['kinds'],x['detail'][:3]);ok&=x['fails']==0 and x['rendered']==x['terms']
print('PASS' if ok and len(r)==3 else 'FAIL');sys.exit(0 if ok else 1)"
