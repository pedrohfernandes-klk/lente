// 01/11/2026: quatro entradas, sem alterar a navegação de topo nem perder destinos.
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.join(__dirname,'..');
for(const rel of ['narrativas/index.html','narrativas/ver/index.html','narrativas/treinar/index.html','narrativas/criar/index.html'])test('preservação: '+rel,()=>{
 const old=cp.execFileSync('git',['show','03ef772:'+rel],{cwd:root,encoding:'utf8'}),now=fs.readFileSync(path.join(root,rel),'utf8');
 for(const match of old.matchAll(/<a\b[^>]*href="([^"]+)"/g))assert.ok(now.includes('href="'+match[1]+'"'),match[1]);
 for(const match of old.matchAll(/\bid="([^"]+)"/g))assert.ok(now.includes('id="'+match[1]+'"'),match[1]);
 // 01/11/2026: decisão 54; só o rótulo muda, mantendo a barra e os destinos exatos.
 assert.equal(now.match(/<nav class="barra-nav"[\s\S]*?<\/nav>/)[0],old.match(/<nav class="barra-nav"[\s\S]*?<\/nav>/)[0].replace('>Ver<','>Observar<'));
 assert.equal(now.match(/<script type="application\/json" id="lab-dados">([\s\S]*?)<\/script>/)[1],old.match(/<script type="application\/json" id="lab-dados">([\s\S]*?)<\/script>/)[1]);
});
