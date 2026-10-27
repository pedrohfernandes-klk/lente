/* Progresso autorrelatado das fichas. Nunca escreve nas chaves anteriores. */
(function(){'use strict';
 var root=document.querySelector('[data-m1-v2]');if(!root)return;
 var KEY='lente-cidadania-m1-v2',memory={version:2,done:{}},projection=window.self!==window.top||new URLSearchParams(location.search).get('projetar')==='1';
 var live=root.querySelector('[data-m1-live]'),check=root.querySelector('[data-m1-done]');
 function valid(s){return s&&s.version===2&&s.done&&typeof s.done==='object'&&!Array.isArray(s.done)}
 function read(){try{var s=JSON.parse(localStorage.getItem(KEY)||'null');if(valid(s))memory=s}catch(e){}return memory}
 function say(s){if(live)live.textContent=s}
 function paint(){var s=read(),total=0;for(var n=1;n<=18;n++){var id='F'+String(n).padStart(2,'0');if(s.done[id]===true)total++}
  var counter=root.querySelector('[data-m1-count]');if(counter)counter.textContent=total+' de 18 fichas com trabalho registado';
  root.querySelectorAll('[data-m1-status]').forEach(function(el){el.textContent=s.done[el.dataset.m1Status]===true?'Trabalho registado':'Por registar'});
  if(check)check.checked=s.done[check.dataset.m1Done]===true;
  var next=root.querySelector('[data-m1-next]');if(next){var id;for(var i=1;i<=18;i++){id='F'+String(i).padStart(2,'0');if(s.done[id]!==true)break}next.href=i>18?'../projeto/':'fichas/'+id.toLowerCase()+'/';next.textContent=i>18?'Rever a entrega do projeto':(total?'Continuar: ':'Começar: ')+id}
 }
 root.querySelectorAll('[data-m1-storage]').forEach(function(el){el.hidden=false});
 if(check){if(projection){check.disabled=true;say('Em projeção, o progresso individual não é alterado. Regista o trabalho no caderno.')}else check.addEventListener('change',function(){var s=read();s.done[check.dataset.m1Done]=check.checked;memory=s;try{localStorage.setItem(KEY,JSON.stringify(s));say('Registo guardado neste aparelho. A qualidade do texto é revista com o docente.')}catch(e){say('O navegador não permite guardar. O registo dura só enquanto esta página estiver aberta; conserva o trabalho no caderno.')}paint()})}
 var legacy=root.querySelector('[data-m1-legacy]');if(legacy){try{var old=JSON.parse(localStorage.getItem('epi-cidadania-m1')||'null');var count=old&&old.feitas&&typeof old.feitas==='object'?Object.keys(old.feitas).length:0;legacy.textContent=count?'O percurso anterior conserva '+count+' registos neste aparelho. As novas fichas têm um registo independente.':'Os registos do percurso anterior conservam-se neste aparelho.'}catch(e){legacy.textContent='Os registos anteriores não foram alterados.'}}
 root.querySelectorAll('[data-m1-print]').forEach(function(b){b.hidden=false;b.addEventListener('click',function(){window.print()})});
 var details=[];window.addEventListener('beforeprint',function(){details=Array.from(root.querySelectorAll('details')).map(function(d){var was=d.open;d.open=true;return[d,was]})});window.addEventListener('afterprint',function(){details.forEach(function(pair){pair[0].open=pair[1]});details=[]});
 function revealHash(){var id;try{id=decodeURIComponent(location.hash.slice(1))}catch(e){return}var target=document.getElementById(id);if(!target)return;var p=target.parentElement;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement}}
 window.addEventListener('hashchange',revealHash);window.addEventListener('storage',function(e){if(e.key===KEY)paint()});window.addEventListener('pageshow',paint);paint();revealHash();
}());
