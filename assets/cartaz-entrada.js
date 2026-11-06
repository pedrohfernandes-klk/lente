/* 01/11/2026: retoma das três áreas, sem escrever progresso. */
(function(){'use strict';
 const main=document.querySelector('[data-cartaz-entrada]');if(!main)return;
 // 02/11/2026: D5, as dobras só fecham abaixo de 640 px e nunca na projeção (o click também apanha Enter e Espaço).
 main.querySelectorAll('.cz-fold>summary').forEach(s=>s.addEventListener('click',e=>{if(!matchMedia('(max-width:639px)').matches||document.documentElement.classList.contains('em-projecao'))e.preventDefault();}));
 matchMedia('(min-width:640px)').addEventListener('change',e=>{if(e.matches)main.querySelectorAll('.cz-fold').forEach(f=>f.open=true);});
 // 02/11/2026: decisão 137. O movimento do fundo «A lente» passou para o motor comum (assets/fundos.js).
 const projetada=new URLSearchParams(location.search).get('projetar')==='1'||self!==top;
 if(projetada){document.documentElement.classList.add('em-projecao');return;}
 const read=k=>{try{return JSON.parse(localStorage.getItem(k)||'null')||{};}catch{return {};}};
 // 02/11/2026: decisão 131 (docente). Sem a caixa «A seguir», a retoma só escolhe a divisão marcada e, no telemóvel, a que fica aberta.
 function show(url){
  const target=url.includes('cidadania/')?'inicio-cidadania':'inicio-narrativas';
  main.querySelectorAll('.ld details.cz-fold').forEach(f=>{const current=f.closest('.ld').id===target;f.querySelector('summary').toggleAttribute('data-cz-next',current);if(matchMedia('(max-width:639px)').matches&&!location.hash)f.open=current;});
 }
 // 02/11/2026: as três chaves reais da Cidadania (M1 com 8 sessões, 03 a 10; M2 atual com 10; passos antigos do M2, 00 a 08), só lidas.
 const one=read('lente-cidadania-m1-sessoes-v2'),two=read('lente-cidadania-m2-sessoes-v1'),old=read('epi-cidadania-m2');
 const feitas=(o,ids)=>ids.filter(id=>o.sessions&&o.sessions[id]&&o.sessions[id].done===true).length;
 const m1=one.version===2?feitas(one,['03','04','05','06','07','08','09','10']):0,m2=two.version===1?feitas(two,['01','02','03','04','05','06','07','08','09','10']):0,p2=Object.keys(old.feitas||{}).filter(k=>/^passo-0[0-8]$/.test(k)&&old.feitas[k]).length;
 if((m2>0&&m2<10)||(m2===0&&p2>0&&p2<9))show('cidadania/m2/');
 else if(m1>0&&m1<8)show('cidadania/m1/');
 const ultima=read('epi-ultima');
 const portuguese=(async()=>{if(typeof ultima.id!=='string'||!/^m[1-9]-f\d+$/i.test(ultima.id))return null;const id=ultima.id.toLowerCase(),url=new URL('../pt/'+id.split('-')[0]+'/licao-'+id+'/',location.href);try{const r=await fetch(url,{method:'HEAD',signal:AbortSignal.timeout(3000)});return r.ok?{url:url.href,time:Number(ultima.t)||0}:null;}catch{return null;}})();
 Promise.all([portuguese,fetch('assets/laboratorio/percursos.json').then(r=>{if(!r.ok)throw Error();return r.json();}).catch(()=>null)]).then(([pt,data])=>{
  if(!data){if(pt)show(pt.url);return;}
  const states=new Map();for(const p of data.pieces){const q=p.progress,s=read(q.key);let value;if(q.kind==='formas'){const item=s.version===1&&s.itens&&s.itens[q.id];value=item&&(item.revi||item.experimentei);}else if(q.kind==='montagem')value=s.version===1&&Array.isArray(s.done)&&q.ids.every(id=>s.done.includes(id));else value=s.feitas&&s.feitas[q.id];states.set(p.id,{done:!!value,time:typeof value==='number'&&value>1?value:0});}
  let last=null,latest=0;for(const p of data.pieces){const st=states.get(p.id);if(st.time>latest||(!last&&st.done)){latest=st.time;last=p;}}
  if(pt&&pt.time>latest)show(pt.url);
  else if(last){const order=data.routes.flatMap(r=>r.pieces),next=order.slice(Math.max(0,order.indexOf(last.id))).concat(order).find(id=>!states.get(id).done),p=data.pieces.find(p=>p.id===next);if(p)show(p.url);else{const route=data.routes.find(r=>r.pieces.includes(last.id));show('narrativas/percursos/'+route.id+'/');}}
  const links=main.querySelectorAll('#inicio-narrativas .lab-sets a');data.blocks.forEach((b,i)=>{/* 05/11/2026: decisão 163. A porta pela âncora do href (o Ideias passou a vir primeiro). */const a=[...links].find(l=>l.getAttribute('href').endsWith('#'+b.anchor));if(!a)return;const ids=data.routes.filter(r=>r.block===b.id).flatMap(r=>r.pieces),done=ids.length>0&&ids.every(id=>states.get(id).done),times=ids.map(id=>states.get(id).time),date=done&&times.every(Boolean)?new Date(Math.max(...times)).toISOString():null,next=!done&&i===data.blocks.findIndex(block=>data.routes.filter(r=>r.block===block.id).some(r=>r.pieces.some(id=>!states.get(id).done)));const span=document.createElement('span');span.className='cz-state'+(done?' done':next?' current':'');span.textContent=window.EPICartaz.stateLabel({done,next,date});a.append(span);a.classList.toggle('current',next);});
 }).catch(()=>{});
})();
