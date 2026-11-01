// 01/11/2026: contratos de preservação da entrada aprovada, sem o molde antigo.
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.join(__dirname,'..'),now=fs.readFileSync(path.join(root,'index.html'),'utf8'),before=cp.execFileSync('git',['show','03ef772:index.html'],{cwd:root,encoding:'utf8'});
const values=(s,re)=>[...s.matchAll(re)].map(m=>m[1]);
test('mantém ligações, âncoras, ferramentas e todos os scripts anteriores',()=>{
 for(const href of values(before,/<a\b[^>]*href="([^"]+)"/g))assert.ok(values(now,/<a\b[^>]*href="([^"]+)"/g).includes(href),href);
 for(const id of values(before,/\bid="([^"]+)"/g))assert.ok(values(now,/\bid="([^"]+)"/g).includes(id),id);
 for(const script of values(before,/<script\b[^>]*>([\s\S]*?)<\/script>/g))assert.ok(now.includes(script),'script preservado');
 assert.deepEqual(values(before,/<li><a href="(https:\/\/pedrohfernandes-klk.github.io\/lente\/[^"]+)"/g),values(now,/<li><a href="(https:\/\/pedrohfernandes-klk.github.io\/lente\/[^"]+)"/g));
 assert.equal((now.match(/class="ld mobile-dest cz-door"/g)||[]).length,2);
});
test('retoma lê as chaves anteriores e não grava visitas',()=>{
 const js=fs.readFileSync(path.join(root,'assets/cartaz-entrada.js'),'utf8');assert.ok(js.includes('epi-ultima'));assert.doesNotMatch(js,/localStorage\.(?:setItem|removeItem|clear)/);
});
