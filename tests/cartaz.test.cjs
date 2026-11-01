// 01/11/2026: decisão 57, D4. Uma visita não equivale a conclusão.
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {stateLabel} = require('../assets/cartaz-components.js');
test('estados escritos por extenso, sem inventar datas', () => {
  assert.equal(stateLabel(), '');
  assert.equal(stateLabel({visited:true}), '');
  assert.equal(stateLabel({next:true}), 'A seguir');
  assert.equal(stateLabel({done:true,next:true}), 'Feita');
  assert.equal(stateLabel({done:true,date:'2026-11-01T23:59:00Z'}), 'Feita 01/11');
  assert.equal(stateLabel({done:true,date:'2026-02-30'}), 'Feita');
  assert.equal(stateLabel({done:true,date:'ontem'}), 'Feita');
});
test('peças não alteram armazenamento e exigem ativação explícita', () => {
  const source = fs.readFileSync(path.join(__dirname,'../assets/cartaz-components.js'),'utf8');
  assert.doesNotMatch(source,/localStorage|sessionStorage/);
  const walk = dir => fs.readdirSync(dir,{withFileTypes:true}).flatMap(e =>
    e.name.startsWith('.') || ['tests','node_modules'].includes(e.name) ? [] :
    e.isDirectory() ? walk(path.join(dir,e.name)) : e.name.endsWith('.html') ? [path.join(dir,e.name)] : []);
  // 01/11/2026: as migrações posteriores ativam as peças apenas no conteúdo marcado.
  for(const file of walk(path.join(__dirname,'..'))) {
    const html=fs.readFileSync(file,'utf8');
    if(/cartaz-components\.(?:css|js)/.test(html)) assert.match(html,/data-cartaz="2"/,file);
  }
});

// 01/11/2026: peças carregadas por appearance.css, ainda sem páginas ativadas.
test('o carregamento comum importa as peças antes das regras existentes', () => {
  const css=fs.readFileSync(path.join(__dirname,'../assets/appearance.css'),'utf8');
  assert.ok(css.startsWith('@import url("cartaz-components.css?v=20261101-1");'));
});
