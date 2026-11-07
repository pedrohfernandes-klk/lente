// 01/11/2026: quatro entradas, sem alterar a navegação de topo nem perder destinos.
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const root=path.join(__dirname,'..');
// 05/11/2026: decisão 147 (Laboratório sem o Português): só podem faltar as ligações, os percursos e os dados das peças
// que constam de assets/laboratorio/retiradas.json; essas têm de ter saído de facto. Tudo o resto continua igual.
const RET=new Set(JSON.parse(fs.readFileSync(path.join(root,'assets/laboratorio/retiradas.json'),'utf8')).retiradas.map(x=>x.url));
const retirada=(rel,href)=>{const u=path.posix.normalize(path.posix.join(path.posix.dirname(rel),href.split('#')[0]));return RET.has(u.endsWith('/')?u:u+'/');};
for(const rel of ['narrativas/index.html','narrativas/ver/index.html','narrativas/treinar/index.html','narrativas/criar/index.html'])test('preservação: '+rel,()=>{
 const old=cp.execFileSync('git',['show','03ef772:'+rel],{cwd:root,encoding:'utf8'}),now=fs.readFileSync(path.join(root,rel),'utf8');
 for(const match of old.matchAll(/<a\b[^>]*href="([^"]+)"/g))assert.equal(now.includes('href="'+match[1]+'"'),!retirada(rel,match[1]),match[1]);
 for(const match of old.matchAll(/\bid="([^"]+)"/g))assert.equal(now.includes('id="'+match[1]+'"'),!RET.has('narrativas/percursos/'+match[1]+'/'),match[1]);
 // 02/11/2026: decisão do docente (141): o «Ideias» é público e tem ligação a partir das páginas públicas.
 // A barra mantém todos os destinos e recebe exatamente uma ligação, a seguir a Laboratório.
 const ideia='<a href="'+(rel==='narrativas/index.html'?'ideias/':'../ideias/')+'">Ideias</a>';
 // 05/11/2026: decisão 163 (menus do Laboratório). Sai a barra preta: «Lente» e «Laboratório» passam à barra única (a mesma
 // ligação, o mesmo atual); o Ideias e as portas passam ao fio do método (nas portas) ou à região do Ideias e às portas (na
 // entrada). Cada ligação da barra antiga continua na página, com o mesmo destino, o mesmo nome e o mesmo «aria-current».
 const antiga=old.match(/<nav class="barra-nav"[\s\S]*?<\/nav>/)[0].replace('>Ver<','>Observar<').replace(/(<a[^>]*>Laboratório<\/a>)/,'$1'+ideia);
 const barra=now.match(/<header class="lab-barra">[\s\S]*?<\/header>/)[0],fio=(now.match(/<nav class="lab-fio"[\s\S]*?<\/nav>/)||[''])[0];
 assert.equal(now.match(/<header class="lab-barra">/g).length,1);assert.ok(!now.includes('barra-nav'));
 const links=[...antiga.matchAll(/<a href="([^"]+)"( aria-current="[^"]+")?>([^<]+)<\/a>/g)];assert.equal(links.length,6);
 for(const [,href,cur='',nome] of links){
  if(['Lente','Laboratório'].includes(nome)){assert.ok(barra.includes('<a href="'+href+'"'+cur+'>'+nome+'</a>'),nome);continue;}
  if(rel==='narrativas/index.html'){assert.ok(new RegExp('<a [^>]*?href="'+href.replace(/[.]/g,'\\.')+'"[^>]*>(?:(?!</a>).)*'+nome).test(now),nome);continue;}
  // 07/11/2026: decisão 180 (docente). O fio diz só os nomes, sem o <span class="n"> dos passos: a mesma ligação, o mesmo nome
  // e o mesmo «aria-current».
  assert.ok(fio.includes('<a href="'+href+'"'+cur+'><b>'+nome+'</b></a>'),nome);assert.ok(!fio.includes('class="n"'),nome);
 }
 const dados=s=>JSON.parse(s.match(/<script type="application\/json" id="lab-dados">([\s\S]*?)<\/script>/)[1]);
 assert.deepEqual(dados(now),dados(old).filter(x=>!RET.has(x.url)));
});
