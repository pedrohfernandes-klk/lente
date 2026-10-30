const assert=require('node:assert/strict');
global.window={};require('../assets/formas/tres-cartas-dados.js');
const D=window.LenteTresCartasDados;let certas=0,maisLongas=0;
for(const c of D.cartoes.filter(c=>c.opcoes&&c.tipo!=='autoavaliacao')){
 const ns=c.opcoes.map(o=>[...o.texto].length),min=Math.min(...ns),max=Math.max(...ns),ratio=max/min;
 console.log(`${c.id}: ${ns.join('/')} caracteres; diferença ${((ratio-1)*100).toFixed(2)}%`);
 assert(ratio<=1.2,`${c.id}: excede 20%`);
 if(c.certa){certas++;const idx=c.opcoes.findIndex(o=>o.id===c.certa),err=Math.max(...ns.filter((_,i)=>i!==idx));assert(ns[idx]<err*1.25);if(ns[idx]===max)maisLongas++;}
}
console.log(`Certa entre as mais longas: ${maisLongas}/${certas}; limite para duas opções: ${Math.ceil(certas/2)}.`);
assert(maisLongas<=Math.ceil(certas/2));
