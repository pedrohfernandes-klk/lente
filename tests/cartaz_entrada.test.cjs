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
// 02/11/2026: decisão 125. Fundo animado «A lente»: decorativo, parado sem JavaScript, na projeção e com movimento reduzido.
// 02/11/2026: decisão 137. O movimento passou para o motor comum (assets/fundos.js): o cabeçalho leva data-fundo e o crédito
// o botão «Parar o desenho»; o teste passa a ler o motor e exige também a pausa com o separador escondido, a paragem em dois
// ciclos e a moldura de projeção marcada depois de carregar.
test('fundo «A lente»: decorativo e parado por omissão',()=>{
 const css=fs.readFileSync(path.join(root,'assets/fundo-lente.css'),'utf8'),js=fs.readFileSync(path.join(root,'assets/fundos.js'),'utf8');
 assert.match(now,/<header class="lente-cab" data-fundo="lf" data-fundo-ciclo="40"><div class="lf-fundo" aria-hidden="true">/);
 assert.match(now,/Desenho nosso, a traço, EPI, 2026\. <button type="button" class="fundo-botao" data-fundo-botao="lf" hidden>Parar o desenho<\/button><\/p>/);
 assert.match(now,/assets\/fundos\.css\?v=/);assert.match(now,/<script defer src="assets\/fundos\.js\?v=/);assert.match(now,/Desenho nosso, a traço, EPI, 2026\./);assert.doesNotMatch(now,/class="lente-cab[^"]*lf-anda/);
 const anim=[...css.matchAll(/animation(?:-name)?:\s*([\w-]+)/g)];assert.ok(anim.length>=2);
 for(const m of anim){const antes=css.slice(0,m.index),bloco=antes.lastIndexOf('@media(prefers-reduced-motion:no-preference)');assert.ok(bloco>=0&&antes.lastIndexOf('}}')<bloco,'animação fora do bloco de movimento');assert.match(css.slice(bloco,m.index),/html:not\(\.em-projecao\)/);}
 assert.match(js,/matchMedia\('\(prefers-reduced-motion: no-preference\)'\)/);assert.match(js,/classList\.add\(p \+ '-anda'\)/);assert.match(js,/IntersectionObserver/);
 assert.match(js,/visibilitychange/);assert.match(js,/setTimeout\(parar, 2 \* ciclo\)/);assert.match(js,/epi-projection/);assert.match(js,/window\.self !== window\.top/);assert.match(js,/MutationObserver/);
 assert.doesNotMatch(fs.readFileSync(path.join(root,'assets/cartaz-entrada.js'),'utf8'),/lf-anda/);
 assert.match(css,/@media print\{[^@]*\.lf-fundo\{display:none\}\}/);
});
