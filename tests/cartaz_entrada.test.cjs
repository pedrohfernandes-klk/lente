// 01/11/2026: contratos de preservação da entrada aprovada, sem o molde antigo.
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.join(__dirname,'..'),now=fs.readFileSync(path.join(root,'index.html'),'utf8'),before=cp.execFileSync('git',['show','03ef772:index.html'],{cwd:root,encoding:'utf8'});
const values=(s,re)=>[...s.matchAll(re)].map(m=>m[1]);
// 12/11/2026: pedido entrada-temas. A entrada abre por quatro temas. O contrato de preservação fica com a mesma força, dito de outro
// modo: (1) cada destino da entrada de 03ef772 continua a ter ligação na entrada ou no mapa (antes: na entrada), e a lista do que passou
// para o mapa é exata; só saem os dois créditos das imagens que saíram da entrada e os dois saltos internos da navegação móvel, cujos
// ids ficam; (2) todos os ids ficam, menos quatro sem uso (três rótulos de dobras e uma âncora vazia), que nenhuma página liga; (3) todos
// os scripts ficam; (4) a lista das ferramentas é exata, na ordem nova, e a Biblioteca e o caderno continuam na entrada; (5) em vez de
// duas portas, quatro temas, pela ordem aprovada.
test('mantém ligações, âncoras, ferramentas e todos os scripts anteriores',()=>{
 const B='https://pedrohfernandes-klk.github.io/lente/',mapa=fs.readFileSync(path.join(root,'mapa/index.html'),'utf8');
 const abs=(s,b)=>values(s,/<a\b[^>]*href="([^"]+)"/g).map(h=>new URL(h,b).href);
 const naEntrada=new Set(abs(now,B)),noMapa=new Set(abs(mapa,B+'mapa/'));
 const sairam=['https://commons.wikimedia.org/wiki/File:An_Experiment_on_a_Bird_in_an_Air_Pump_by_Joseph_Wright_of_Derby,_1768.jpg','https://commons.wikimedia.org/wiki/File:PessoaChapeu.jpg',B+'#inicio-cidadania',B+'#inicio-narrativas'];
 for(const href of abs(before,B)){if(sairam.includes(href))continue;assert.ok(naEntrada.has(href)||noMapa.has(href),href);}
 assert.deepEqual([...new Set(abs(before,B))].filter(h=>!naEntrada.has(h)&&!sairam.includes(h)).sort(),[B+'#ferramentas',B+'cidadania/',B+'cidade/',B+'narrativas/tudo/#criar',B+'narrativas/tudo/#ler-como-quem-escreve',B+'narrativas/tudo/#treinar',B+'olhar-e-decidir/',B+'ver-para-fazer/']);
 // 13/11/2026: pedido temas-01-03-04. Os cartões 01, 03 e 04 abrem a página do seu tema. Os Dilemas e «Ler a cidade» saem da entrada para o
 // mapa (lista acima, que cresce com os dois) e são a primeira ligação de «Ver tudo neste tema» na página do tema; o Laboratório continua na entrada.
 assert.ok(naEntrada.has(B+'narrativas/'));
 for(const [pasta,antigo,rotulo] of [['justica-e-vida-em-comum','olhar-e-decidir/','Dilemas'],['historias-e-criacao','narrativas/','Laboratório'],['imagem-som-e-cidade','cidade/','Ler a cidade']]){const t=fs.readFileSync(path.join(root,pasta,'index.html'),'utf8');assert.ok(t.slice(t.indexOf('<details class="tm-tudo">')).includes('<ul><li><a href="'+B+antigo+'">'+rotulo+'</a></li>'),pasta);assert.equal(t.slice(t.indexOf('<details class="tm-tudo">')).match(/<li><a href="([^"]+)">/)[1],B+antigo,pasta);assert.ok(noMapa.has(B+antigo),antigo);assert.ok(noMapa.has(B+pasta+'/'),pasta);}
 // os dois créditos saíram com as suas imagens; os dois saltos internos saíram, mas os destinos (os ids) ficam na entrada
 assert.doesNotMatch(now,/wright-experiencia|pessoa-1914/);assert.equal((now.match(/id="inicio-cidadania"/g)||[]).length,1);assert.equal((now.match(/id="inicio-narrativas"/g)||[]).length,1);assert.equal((now.match(/id="ferramentas"/g)||[]).length,1);
 const semUso=['ferr-ler','ferr-criar','ferr-fontes','trans-t'],ids=values(now,/\bid="([^"]+)"/g);
 for(const id of values(before,/\bid="([^"]+)"/g)){if(semUso.includes(id)){assert.ok(!mapa.includes('#'+id+'"')&&!now.includes('#'+id+'"'),id);continue;}assert.ok(ids.includes(id),id);}
 assert.equal(new Set(ids).size,ids.length,'ids repetidos');
 for(const script of values(before,/<script\b[^>]*>([\s\S]*?)<\/script>/g))assert.ok(now.includes(script),'script preservado');
 assert.deepEqual(values(now,/<li><a href="(https:\/\/pedrohfernandes-klk.github.io\/lente\/[^"]+)"/g),['ler/','investigar/','praticar/#escrever','apresentar/','direitos/'].map(x=>B+x));
 for(const antes of values(before,/<li><a href="(https:\/\/pedrohfernandes-klk.github.io\/lente\/[^"]+)"/g))assert.ok(naEntrada.has(antes)||noMapa.has(antes),antes);
 assert.ok(naEntrada.has(B+'biblioteca/')&&naEntrada.has(B+'caderno/')&&naEntrada.has(B+'mapa/')&&naEntrada.has(B+'docente/'));
 assert.equal((now.match(/<article class="tm"/g)||[]).length,4);assert.equal((now.match(/class="ld mobile-dest cz-door"/g)||[]).length,0);
 assert.deepEqual([...now.matchAll(/<h3 class="tm-n"><b aria-hidden="true">(\d\d)<\/b><a href="([^"]+)">([^<]+)<\/a><\/h3>/g)].map(m=>m.slice(1)),[['01','justica-e-vida-em-comum/','Justiça e vida em comum'],['02','informacao/','Informação e mundo digital'],['03','historias-e-criacao/','Histórias e criação'],['04','imagem-som-e-cidade/','Imagem, som e cidade']]);
 assert.ok(fs.existsSync(path.join(root,'informacao/index.html')));
});
test('retoma lê as chaves anteriores e não grava visitas',()=>{
 const js=fs.readFileSync(path.join(root,'assets/cartaz-entrada.js'),'utf8');assert.ok(js.includes('epi-ultima'));assert.doesNotMatch(js,/localStorage\.(?:setItem|removeItem|clear)/);
});
// 02/11/2026: decisão 125. Fundo animado «A lente»: decorativo, parado sem JavaScript, na projeção e com movimento reduzido.
// 02/11/2026: decisão 137. O movimento passou para o motor comum (assets/fundos.js): o cabeçalho leva data-fundo e o crédito
// o botão «Parar o desenho»; o teste passa a ler o motor e exige também a pausa com o separador escondido, a paragem em dois
// ciclos e a moldura de projeção marcada depois de carregar.
// 02/11/2026: decisão 139 (docente: «maiores e mais bem feitos»). Sai a paisagem a traço; entra a faixa da página de texto miúdo
// (assets/lupa-texto.svg, gerada por tools/gerar_lupa_texto.py) com a lupa de vidro por cima. O crédito diz o que está na página
// e o teste confere também o ficheiro gerado e as contas da lupa (o texto ampliado anda -2,6 vezes o que a lupa anda).
// 02/11/2026: decisão do docente: atribuir o grafismo ao recurso a IA, conservando a fonte da epígrafe.
test('fundo «A lente»: decorativo e parado por omissão',()=>{
 const css=fs.readFileSync(path.join(root,'assets/fundo-lente.css'),'utf8'),js=fs.readFileSync(path.join(root,'assets/fundos.js'),'utf8');
 assert.match(now,/<header class="lente-cab" data-fundo="lf" data-fundo-ciclo="40"><p class="lente-etq">/);
 // 12/11/2026: pedido entrada-temas. A frase do cabeçalho passa a apresentar os quatro temas; o resto do cabeçalho fica igual.
 assert.match(now,/<p class="lente-frase">Quatro perguntas\. Escolhe uma e começa por aí\.<\/p><div class="lf-mesa" aria-hidden="true"><div class="lf-pagina"><\/div><div class="lf-lupa">/);
 assert.equal((now.match(/class="lf-mesa"/g)||[]).length,1);assert.doesNotMatch(now,/lf-fundo|lf-cena|lf-colinas/);
 // 07/11/2026: decisões 153, 176 e 177, o crédito inteiro passa para o «i» do desenho e o botão sai dele, sempre à vista, com «Parar a animação».
 assert.match(now,/<div class="fundo-acoes lf-credito"><button type="button" class="fundo-botao" data-fundo-botao="lf" hidden>Parar a animação<\/button><details class="info-i info-i--linha" name="info-i"><summary aria-label="Créditos do desenho"><span aria-hidden="true">i<\/span><\/summary><p class="info-i-texto">Grafismo gerado com recurso a IA, EPI, 2026\. Na página, a epígrafe de <i>Ensaio sobre a Cegueira<\/i>, de José Saramago \(1995\): «Se podes olhar, vê\. Se podes ver, repara\.»<\/p><\/details><\/div>/);
 assert.match(now,/assets\/fundos\.css\?v=/);assert.match(now,/<script defer src="assets\/fundos\.js\?v=/);assert.doesNotMatch(now,/Desenho nosso, a traço/);assert.doesNotMatch(now,/class="lente-cab[^"]*lf-anda/);
 const anim=[...css.matchAll(/animation(?:-name)?:\s*([\w-]+)/g)];assert.deepEqual(anim.map(m=>m[1]),['lf-passa','lf-amplia']);
 for(const m of anim){const antes=css.slice(0,m.index),bloco=antes.lastIndexOf('@media(prefers-reduced-motion:no-preference)');assert.ok(bloco>=0&&antes.lastIndexOf('}}')<bloco,'animação fora do bloco de movimento');assert.match(css.slice(bloco,m.index),/html:not\(\.em-projecao\)/);}
 assert.match(js,/matchMedia\('\(prefers-reduced-motion: no-preference\)'\)/);assert.match(js,/classList\.add\(p \+ '-anda'\)/);assert.match(js,/IntersectionObserver/);
 assert.match(js,/visibilitychange/);assert.match(js,/setTimeout\(parar, 2 \* ciclo\)/);assert.match(js,/epi-projection/);assert.match(js,/window\.self !== window\.top/);assert.match(js,/MutationObserver/);
 assert.doesNotMatch(fs.readFileSync(path.join(root,'assets/cartaz-entrada.js'),'utf8'),/lf-anda/);
 assert.match(css,/@media print\{[^@]*\.lf-mesa\{display:none\}\}/);
 // a página corresponde ao gerador e é só texto; a lupa amplia 2,6 vezes e o texto ampliado anda -2,6 vezes o que a lupa anda
 assert.equal(cp.spawnSync('python3',['tools/gerar_lupa_texto.py','--verificar'],{cwd:root}).status,0);
 const svg=fs.readFileSync(path.join(root,'assets/lupa-texto.svg'),'utf8');assert.doesNotMatch(svg,/<script|href=|<image|\son\w+=/);assert.match(svg,/Se podes olhar, vê\. Se podes ver, repara\./);
 assert.match(css,/\.lf-grande\{transform-origin:var\(--lf-x\) 50%;transform:scale\(2\.6\)\}/);
 const passos=nome=>[...css.match(new RegExp('@keyframes '+nome+'\\{(.*?)\\}\\}'))[1].matchAll(/([\d%,]+)\{transform:translate\(([-\d.]+)%?,([-\d.]+)%?\)/g)].map(m=>[m[1],+m[2],+m[3]]);
 const lupa=passos('lf-passa'),zoom=passos('lf-amplia');assert.equal(lupa.length,4);assert.deepEqual(lupa.map(x=>x[0]),zoom.map(x=>x[0]));
 lupa.forEach((x,i)=>{assert.ok(Math.abs(zoom[i][1]+2.6*x[1])<1e-9&&Math.abs(zoom[i][2]+2.6*x[2])<1e-9,x[0])});
});
