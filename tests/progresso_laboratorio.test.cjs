// 02/11/2026: decisões 115 e 141. Revisões dos cartões não apagam conclusões anteriores.
const {test}=require('node:test'),assert=require('node:assert/strict');
const p=require('../assets/licoes/progresso-laboratorio.js');
test('sessão concluída conserva a data e os resultados, mas não transfere respostas por índice',()=>{
 const old={versao:'2026-11-01-1',lida:true,t:100,melhor:12,totalMelhor:13,tentativas:2,exposicoes:{0:2},ult:'0,1'};
 const copy=JSON.stringify(old),n=p.migrar(old,'2026-11-02-1');
 assert(p.feita(n));assert.equal(p.data(n),100);assert.equal(n.antes.melhor,12);assert.equal(n.antes.total,13);
 assert.equal(n.exposicoes,undefined);assert.equal(n.ult,undefined);assert.equal(n.lida,undefined);assert.equal(JSON.stringify(old),copy);
 assert.strictEqual(p.migrar(n,'2026-11-02-1'),n);
});
test('revisões sucessivas e tentativas incompletas não substituem a conclusão mais antiga',()=>{
 const n=p.migrar({versao:'v2',lida:false,t:300,antes:{versao:'v1',lida:true,data:100,melhor:9,total:12,tentativas:1}},'v3');
 assert(p.feita(n));assert.equal(n.antes.versao,'v1');assert.equal(p.data(n),100);
 const m=p.migrar({...n,versao:'v3',lida:true,t:400},'v4');assert.equal(m.antes.versao,'v1');assert.equal(p.data(m),100);
});
test('conclusão corrente mais antiga prevalece sobre histórico posterior',()=>{
 const n=p.migrar({versao:'v2',lida:true,t:50,antes:{versao:'v1',lida:true,data:100}},'v3');
 assert.equal(n.antes.versao,'v2');assert.equal(p.data(n),50);
});
test('estado incompleto, vazio ou inválido não inventa uma conclusão',()=>{
 for(const st of [null,[],false,'erro',{}, {versao:'v1',tentativas:2}])assert.equal(p.feita(p.migrar(st,'v2')),false);
 assert.deepEqual(p.migrar(null,'v2'),{versao:'v2'});assert.equal(p.data(null),null);
});

test('a entrada mantém a data mais antiga depois de concluir a nova versão',()=>{
 assert.equal(p.data({lida:true,t:400,antes:{lida:true,data:100}}),100);
 assert.equal(p.data({lida:true,t:50,antes:{lida:true,data:100}}),50);
});
