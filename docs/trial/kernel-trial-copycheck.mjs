import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const R='/workspace/workshop-build/repo', S=R+'/docs/spec';
const keyOf = (h) => h.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
function parseCards(md) {
  const cards = []; let cur = null, fence = false, inFields = false, ln=0;
  for (const line of md.split('\n')) { ln++;
    if (/^(```|~~~)/.test(line)) fence = !fence;
    if (!fence && /^## /.test(line)) { cur = { heading: line.slice(3).trim(), key: keyOf(line.slice(3)), fields: {}, body: [], line: ln }; cards.push(cur); inFields = true; continue; }
    if (!cur) continue;
    if (inFields) { if (line.trim() === '') { inFields = false; continue; }
      const m = /^([A-Za-z][\w.\- ]*?):\s?(.*)$/.exec(line); if (m) { cur.fields[m[1]] = m[2]; continue; } inFields = false; }
    cur.body.push([ln,line]);
  }
  return cards;
}
const norm = s => s.replace(/\*\*|__/g,'').replace(/^\s*(?:[-*]|\d+\.)\s+/,'').replace(/\|/g,' ').replace(/\s+/g,' ').trim().toLowerCase();
const spec = {}; for (const f of readdirSync(S)) spec[f]=readFileSync(join(S,f),'utf8').split('\n');
const all = norm(Object.values(spec).map(a=>a.join(' ')).join(' ').replace(/\|/g,' '));
// MAP sources
const map = readFileSync(R+'/kernel/MAP.md','utf8').split('\n'); let page=null; const src={};
for (const l of map) { let m=/^### `(\S+)`/.exec(l); if (m){page=m[1];continue;}
  m=/^\| (\S+) \| `([^`]+)` \| ([^|]*)\|/.exec(l); if (m&&page) src[`${page}.${m[1]}/${m[2]}`]=m[3].trim(); }
function cited(list){ let t='', lastf=null; for (const c of list.split(/[,;]\s*/)) { let m=/([\w.\-]+\.md):(\d+)(?:-(\d+))?/.exec(c); if(!m){ const mm=/^(\d+)(?:-(\d+))?/.exec(c.trim()); if(mm&&lastf) m=[null,lastf,mm[1],mm[2]]; else continue;} lastf=m[1]; const f=m[1].replace('docs/spec/',''); if(!spec[f]){t+=' MISSINGFILE:'+f; continue;} const a=+m[2], b=+(m[3]||m[2]); t+=' '+spec[f].slice(a-1,b).join(' ');} return norm(t); }
const dirs=[R+'/kernel/00.00.00', ...readdirSync(R+'/kernel/samples').map(d=>R+'/kernel/samples/'+d)];
for (const d of dirs) for (const f of readdirSync(d).sort()) {
  const m=/^(\d\d\.\d\d\.\d\d\.\d{4})\.(\d\d(?:\.\d\d)?)/.exec(f); if(!m||m[2]==='00') continue;
  const md=readFileSync(join(d,f),'utf8');
  for (const c of parseCards(md)) {
    const k=`${m[1]}.${m[2]}/${c.key}`, s=src[k]; const ct = s?cited(s):'';
    const fsrc = c.fields.source||'';
    const fct = cited(fsrc);
    for (const [ln,line] of c.body) { const n=norm(line); if(n.length<12 || /^```/.test(line)) continue;
      // split into sentences
      const parts = n.split(/(?<=[.;:])\s+/).filter(p=>p.length>15);
      for (const p of parts) { const q=p.replace(/[.;:]$/,'');
        const inC = (ct+' '+fct).includes(q), inA = all.includes(q);
        if (!inC) console.log(`${inA?'MISCITE':'NOTFOUND'}\t${f}:${ln}\t[${c.key}] src=${s||'-'} fsrc=${fsrc.slice(0,60)}\t${p.slice(0,140)}`);
      } }
    if (c.fields.why && c.fields.why!=='4.7') { const w=norm(c.fields.why).replace(/[.]$/,''); if(!all.includes(w)) console.log(`WHY-NOTFOUND\t${f}:${c.line}\t[${c.key}]\t${c.fields.why.slice(0,140)}`); else if(!(ct+' '+fct).includes(w)) console.log(`WHY-MISCITE\t${f}:${c.line}\t[${c.key}]\t${c.fields.why.slice(0,100)}`);}
  }
}
