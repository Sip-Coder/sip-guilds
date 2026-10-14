// Data-driven definition infographic. Uses only fields present in data/guilds.json and data/definitions.json.
const GI={1:'M12 3c-4 0-6 2-6 2v4c0 5 3 9 6 12 3-3 6-7 6-12V5s-2-2-6-2z',// cask: glass/barrel-ish shield
2:'M5 9h11v5a5 5 0 0 1-5 5h-1a5 5 0 0 1-5-5zM16 10h2a2 2 0 0 1 0 4h-2M9 3c0 2 2 2 2 4',// steep: cup + steam
3:'M12 3s-6 7-6 11a6 6 0 0 0 12 0c0-4-6-11-6-11z',// source: drop
4:'M13 2 5 13h6l-1 9 8-11h-6z',// energy: bolt
5:'M12 4a8 8 0 1 0 8 8M12 8a4 4 0 1 0 4 4M12 12h.01'};// culture: spiral
const esc=t=>String(t).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let IDX=null;
function index(G){IDX={};for(const g of G)for(const a of g.academies){const subs=a.subgenres;for(const s of subs){const r={g,a,s,subs};IDX[s.id]=r;s.styles.forEach((n,i)=>IDX[s.id+'.'+(i+1)]={...r,i,n})}}}
const U={yr:12,yrs:12,year:12,years:12,mo:1,month:1,months:1};
// Aging bars parsed only from explicit numbers in the term name, e.g. "Reserva · 3 yr (1 oak, 6 mo btl)". Ranges are skipped.
export function parseAging(t){if(/\d\s*–\s*\d/.test(t))return null;const N='(\\d+(?:\\.\\d+)?)',out={};
const m=t.match(new RegExp('(?:·|≥)\\s*'+N+'\\s*(yr|years?|mo|months?)\\b'));const unit=m?U[m[2]]:1;
const rest=m?t.slice(m.index+m[0].length):t;
if(m&&!/^\s*(oak|wood|lees|under|from)/.test(rest))out.total=+m[1]*unit;
const get=(re)=>{const x=t.match(new RegExp(N+'\\s*(yr|mo)?\\s*'+re));if(!x)return null;const v=+x[1];return x[2]?v*U[x[2]]:unit==12&&m&&v>+m[1]?v:v*unit};
const w=get('(?:oak|wood)\\b'),b=get('btl\\b'),l=get('(?:lees|under voile|from tirage)');
if(w)out.wood=w;if(b)out.btl=b;if(l)out.lees=l;return Object.keys(out).length?out:null}
export function parseABV(t){const m=t.match(/(≤|≥|<|>|[Bb]elow |about |approx\.? )?(\d+(?:\.\d+)?)(?:\s*[–-]\s*(\d+(?:\.\d+)?))?\s*%\s*ABV( or less| or more)?/i);if(!m)return null;let q=(m[1]||'').trim();if(/below/i.test(q))q='<';if(m[4])q=/less/.test(m[4])?'≤':'≥';return{lo:+m[2],hi:m[3]?+m[3]:null,q}}
const fm=m=>m%12==0&&m>=12?m/12+' yr':m+' mo';
export function renderIG(id,d,G,DEFS){if(!IDX)index(G);const r=IDX[id];if(!r)return'';const{g,a,s,subs}=r,c=a.color,isT=d.kind=='term'&&r.n!=null;
const crumbs=[g.name.replace(/\b\w+/g,w=>w[0]+w.slice(1).toLowerCase()),a.name];if(s.parent)crumbs.push(s.parent);crumbs.push(s.name);if(isT)crumbs.push(r.n);
let h=`<section class="ig" style="--ic:${c}" aria-label="Infographic"><h3>INFOGRAPHIC</h3>`;
// motif + path
h+=`<div class="ig-top"><svg class="ig-ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="${c}22" stroke="${c}"/><path d="${GI[g.id]||GI[1]}" fill="none" stroke="${c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" transform="translate(3.6 3.6) scale(.7)"/></svg><ol class="ig-path">${crumbs.map((x,i)=>`<li${i==crumbs.length-1?' class="on"':''}><i style="background:${i==0?g.color:c};opacity:${.35+.65*(i+1)/crumbs.length}"></i>${esc(x)}</li>`).join('')}</ol></div>`;
// position / size
const pos=isT?`<div class="ig-k">POSITION</div><div class="ig-dots" aria-label="${r.i+1} of ${s.styles.length} in ${esc(s.name)}">${s.styles.map((_,i)=>`<b${i==r.i?' class="on"':''}></b>`).join('')}</div><div class="ig-v">${r.i+1} of ${s.styles.length} in ${esc(s.name)}</div>`
:(()=>{const mx=Math.max(...subs.map(x=>x.styles.length));return`<div class="ig-k">SIZE IN ${esc(a.name.toUpperCase())}</div><div class="ig-bar"><span style="width:${Math.max(4,100*s.styles.length/mx)}%"></span></div><div class="ig-v">${s.styles.length} entries · largest group here has ${mx}</div>`})();
h+=`<div class="ig-sec">${pos}</div>`;
// aging timeline
const ag=parseAging(d.term);if(ag){const sib=s.styles.map(parseAging).filter(Boolean),mx=Math.max(...sib.map(x=>Math.max(x.total||0,x.wood||0,x.lees||0,(x.wood||0)+(x.btl||0))),1);const pc=v=>Math.max(2,100*v/mx);
h+=`<div class="ig-sec"><div class="ig-k">MINIMUM AGING (from the term)</div>`;
if(ag.total!=null)h+=`<div class="ig-row"><span>Total</span><div class="ig-bar"><span style="width:${pc(ag.total)}%"></span></div><em>${fm(ag.total)}</em></div>`;
if(ag.wood)h+=`<div class="ig-row"><span>Wood</span><div class="ig-bar wd"><span style="width:${pc(ag.wood)}%"></span></div><em>${fm(ag.wood)}</em></div>`;
if(ag.btl)h+=`<div class="ig-row"><span>Bottle</span><div class="ig-bar bt"><span style="width:${pc(ag.btl)}%"></span></div><em>${fm(ag.btl)}</em></div>`;
if(ag.lees)h+=`<div class="ig-row"><span>Lees</span><div class="ig-bar ls"><span style="width:${pc(ag.lees)}%"></span></div><em>${fm(ag.lees)}</em></div>`;
h+=`<div class="ig-v">Scale: longest requirement in ${esc(s.name)} (${fm(mx)})</div></div>`}
// ABV gauge
const ab=parseABV(d.term)||(isT&&!/=/.test(d.definition)?parseABV(d.definition):null);if(ab){const hi=ab.hi??ab.lo,sc=hi>20?100:20,L=100*ab.lo/sc,W=Math.max(1.5,100*(hi-ab.lo)/sc);
h+=`<div class="ig-sec"><div class="ig-k">ALCOHOL (ABV, as stated)</div><div class="ig-bar abv">${ab.q=='≤'||ab.q=='<'?`<span style="left:0;width:${Math.max(1.5,L)}%"></span>`:`<span style="left:${ab.hi?L:L-0.75}%;width:${W}%"></span>`}</div><div class="ig-scale"><b>0%</b><b>${sc/2}%</b><b>${sc}%</b></div><div class="ig-v">${esc((ab.q?ab.q+' ':'')+ab.lo+(ab.hi?'–'+ab.hi:'')+'% ABV')}</div></div>`}
// siblings / members
const list=isT?s.styles.map((n,i)=>[n,s.id+'.'+(i+1),i==r.i]):s.styles.map((n,i)=>[n,s.id+'.'+(i+1),false]);const MAX=12,shown=list.slice(0,MAX);
h+=`<div class="ig-sec"><div class="ig-k">${isT?'RELATED STYLES':'INCLUDES'}</div><div class="ig-chips">${shown.map(([n,k,on])=>`<button type="button" class="ig-chip${on?' on':''}" data-def="${k}"${on?' aria-current="true"':''}>${esc(n)}</button>`).join('')}${list.length>MAX?`<span class="ig-more">+${list.length-MAX} more</span>`:''}</div>`;
if(!isT){const near=subs.filter(x=>x!==s&&(x.parent||'')==(s.parent||'')).slice(0,8);if(near.length)h+=`<div class="ig-k">NEIGHBOURING GROUPS</div><div class="ig-chips">${near.map(x=>`<button type="button" class="ig-chip" data-def="${x.id}">${esc(x.name)}</button>`).join('')}</div>`}
h+=`</div></section>`;return h}
