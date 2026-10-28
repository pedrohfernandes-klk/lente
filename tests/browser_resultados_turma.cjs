/* Resultados da turma (28/10/2026): entrega com código no caderno e página do docente, no navegador.
   Caderno: chaves reais dos dois sítios, código inválido (nome sem algarismos) com mensagem, «10A-07», pré-visualização,
   descarga e conferência do JSON; «Guardar num ficheiro» continua igual; teclado. 28/10/2026 (revisão): o código não
   fica guardado nem volta preenchido; códigos que o Excel estraga (10E-07) recusados; «Vai 1 registo, deste percurso»;
   o estado final diz o passo que falta. Docente: coluna Código fixa e ligada ao pormenor; «+» e «−» nos resumos; datas
   no futuro; listas do último lote; foco depois de «Limpar».
   Docente: três entregas, um progresso antigo (e dois com o mesmo nome), um duplicado mais antigo, ficheiros maliciosos
   (__proto__, chave fora da lista, HTML num valor, mais de 1 MB, JSON partido) e um texto com <script>; tabela, aviso,
   recusados, ordem, pormenor, CSV (BOM, «;», CRLF, fórmulas), largar ficheiros, o mesmo ficheiro duas vezes, limpar,
   recarregar fica vazio; nenhum script injetado corre; zero pedidos fora da origem local; nada no armazenamento nem no
   IndexedDB; de 320 a 1440 px nos dois temas, sem deslizar na horizontal. RT_OUT escolhe a pasta das capturas. */
const fs = require('fs'), path = require('path'), http = require('http'), assert = require('assert');
const { chromium } = require('playwright');
const R = path.resolve(__dirname, '..'), OUT = process.env.RT_OUT || path.resolve(R, '../../outputs/resultados-turma');
fs.mkdirSync(OUT, { recursive: true });
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.pdf': 'application/pdf', '.svg': 'image/svg+xml', '.json': 'application/json', '.woff2': 'font/woff2' };
function file(url) {
  const name = decodeURIComponent(new URL(url, 'http://local').pathname).replace(/^\/lente\/?/, '');
  let p = path.resolve(R, name);
  if (!p.startsWith(R + path.sep) && p !== R) throw Error('path');
  if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
  return p;
}
const server = http.createServer((req, res) => {
  try { const p = file(req.url); res.writeHead(fs.existsSync(p) ? 200 : 404, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' }); res.end(fs.existsSync(p) ? fs.readFileSync(p) : 'Not found'); }
  catch (e) { res.writeHead(400); res.end('Invalid path'); }
});
const J = o => JSON.stringify(o);
// Chaves reais dos dois sítios (mesma origem), com valores no formato que as páginas escrevem.
const SEMENTE = {
  'licao-m1-f04': J({ versao: '2026-10-24', tentativas: 2, ult: '0,3,5,8', certas: 9, total: 11, melhor: 10, totalMelhor: 11, xp: 140, seq: 6, lida: true, t: 1761650000000 }),
  'licao-m1-f04-a1': J({ lida: true, t: 1761650000000 }),
  'licao-m4-f27': J({ tentativas: 1, certas: 4, total: 9, melhor: 4, totalMelhor: 9, lida: false, t: 1761650000000 }),
  'epi-ultima': J({ id: 'm1-f04', m: 'M1', t: 1761650000000 }),
  'percurso-sintese-M5-u2': J({ feita: true, modo: 'oral' }),
  'percurso-v2-M3-u1': 'Nesta unidade percebi que a voz do poema muda quando muda o destinatário.',
  'desafio-unidade-v2-M3-u1': J({ tentativas: 1, certas: 7, total: 8, melhor: 7, totalMelhor: 8, lida: true, ganho: true }),
  'epi-pt-quiz-M1': J({ 0: 5, 3: 6 }),
  'epi-pt-candide-jardim': J({ i: 7, n: 7, r: { 4: 'O jardim é o trabalho de cada dia.' }, p: { 1: 10, 2: 10 }, fim: true, ini: true }),
  'epi-atlas': J({ v: 3, p: { 'celeste-caeiro': { qs: 1761650000000, ob: 1761650100000 } }, dom: { PT: 1761650200000 } }),
  'atlas-PT-1': J({ tentativas: 1, certas: 3, total: 3, melhor: 3, lida: true }),
  'epi-pt-prova-m1-a': J({ bloqueio: { c: 'M1-A-XXXX', motivo: 'saiu', t: 1 } }),
  'epi-sala': J({ cod: 'ABCDE', alc: 'Ritinha', t: 1 }),
  'epi-theme': 'light',
  'pt-relogio:tarefas/m1-u1:aquecimento': J({ fim: 1 }),
  'lente-cidadania-m1-sessoes-v2': J({ version: 2, sessions: { '03': { stage: 4, done: true }, '04': { stage: 2 } } }),
  'lente-cidadania-m2-sessoes-v1': J({ version: 1, sessions: { '01': { stage: 4, done: true } } }),
  'lente-cidadania-m1-v2': J({ version: 2, done: { F01: true, F02: false, F04: true } }),
  'epi-cidadania-m1': J({ feitas: { 'passo-03': 1761650000000 } }),
  'cd1-nome': 'Rita Sousa',
  'cd1-aula1-1': 'A imagem mostra uma mesa vazia.',
  'cd-cd1-aula01': J({ nome: 'Rita Sousa', mesa: 'Mesa 3', palavra: 'justo', porque: 'Porque todos falam.' }),
  'lente-justica-licao-2': J({ tentativas: 1, certas: 7, total: 8, melhor: 7, totalMelhor: 8, lida: true }),
  'epi-treinos': J({ feitas: { 'sem-olhos': 1761650000000 }, vezes: { 'sem-olhos': 2 } }),
  'epi-narrativas': J({ feitas: { 'oficina-arco': 1761650000000 } }),
  'epi-narrativas:visto': '5',
  'epi-bairro': J({ feitas: { m01: 1761650000000 } }),
  'bairro-m01': J({ tentativas: 1, certas: 5, total: 6, melhor: 5, lida: true }),
  'epi-investigar': J({ feitas: { 'passo-01': 1761650000000 } })
};
// 28/10/2026: sem 'epi-codigo-entrega' (o código deixou de se guardar no aparelho)
const FORA_DA_ENTREGA = ['epi-pt-prova-m1-a', 'epi-sala', 'epi-theme', 'pt-relogio:tarefas/m1-u1:aquecimento', 'cd1-nome'];
const results = [];
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ headless: true, ...(process.env.RT_CHROMIUM ? { executablePath: process.env.RT_CHROMIUM } : {}) });
  async function context(width = 1440, scheme = 'light') {
    const c = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme, reducedMotion: 'reduce', acceptDownloads: true });
    await c.route('https://pedrohfernandes-klk.github.io/lente/**', async route => { const p = file(route.request().url()); await route.fulfill({ status: fs.existsSync(p) ? 200 : 404, body: fs.existsSync(p) ? fs.readFileSync(p) : '', contentType: MIME[path.extname(p)] || 'application/octet-stream' }); });
    await c.route('https://fonts.googleapis.com/**', r => r.abort()); await c.route('https://fonts.gstatic.com/**', r => r.abort());
    return c;
  }
  const semTransbordo = p => p.evaluate(() => document.documentElement.scrollWidth <= innerWidth);
  const lerDescarga = async d => fs.readFileSync(await d.path());
  try {
    // ---------- 1. Caderno: código, pré-visualização e descarga da entrega ----------
    const c1 = await context(390), p1 = await c1.newPage(), e1 = [], dialogos = [];
    p1.on('pageerror', e => e1.push(e.message)); p1.on('dialog', d => { dialogos.push(d.message()); d.dismiss(); });
    await p1.goto(origin + '/lente/caderno/');
    await p1.evaluate(s => { localStorage.clear(); for (const [k, v] of Object.entries(s)) localStorage.setItem(k, v); }, SEMENTE);
    await p1.reload();
    const pedidos1 = []; p1.on('request', r => pedidos1.push({ url: r.url(), metodo: r.method(), corpo: r.postData() || '' }));
    assert(await p1.evaluate(() => { const a = document.getElementById('progresso'), b = document.getElementById('entregar'); return !!(a && b && (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING)); }), 'a secção vem a seguir ao progresso');
    assert.equal((await p1.locator('#entregar h2').textContent()).trim(), 'Entregar ao docente');
    assert.equal((await p1.locator('#pe-ajuda').textContent()).trim(), 'Escreve o código que o docente te deu. Não escrevas o teu nome.');
    assert.equal(await p1.locator('#entregar [data-pe-estado]').getAttribute('aria-live'), 'polite');
    const campo = p1.getByLabel('O teu código'), preparar = p1.getByRole('button', { name: 'Preparar a entrega' });
    // 28/10/2026: também os códigos que o Excel troca por números (10E-07, 007)
    for (const [mau, msg] of [['Ana', /pelo menos um algarismo.*Não escrevas o teu nome/], ['Ana Rita', /só pode ter letras/], ['A', /entre 2 e 12/], ['ABCDEFGHIJ123', /entre 2 e 12/], ['', /Escreve o código/], ['10E-07', /Excel do docente lê este código como um número.*E10-07/], ['007', /pelo menos uma letra/]]) {
      await campo.fill(mau); await preparar.click();
      assert.match(await p1.locator('[data-pe-erro]').textContent(), msg, mau);
      assert.equal(await campo.getAttribute('aria-invalid'), 'true', mau);
      assert(await p1.locator('[data-pe-pre]').isHidden(), 'sem pré-visualização com código inválido: ' + mau);
    }
    assert.equal(await p1.evaluate(() => localStorage.getItem('epi-codigo-entrega')), null, 'um código inválido não se guarda');
    // o código em minúsculas normaliza; Enter no campo prepara (teclado)
    await campo.fill('10a-07'); await campo.press('Enter');
    assert.equal(await campo.inputValue(), '10A-07');
    assert.equal(await campo.getAttribute('aria-invalid'), 'false');
    assert.equal(await p1.locator('[data-pe-erro]').textContent(), '');
    assert(await p1.locator('[data-pe-pre]').isVisible());
    assert.equal(await p1.evaluate(() => document.activeElement.textContent), 'Antes de entregar', 'o foco vai para a pré-visualização');
    assert.equal((await p1.locator('[data-pe-cod]').textContent()).trim(), 'Código: 10A-07');
    const resumo = await p1.locator('[data-pe-resumo]').textContent(), nAceites = Object.keys(SEMENTE).length - 5;
    assert.equal(resumo, `Vão ${nAceites} registos, destes percursos:`, resumo);
    const grupos = await p1.locator('[data-pe-lista] li').allTextContents();
    assert(grupos.includes('Cidadania e Desenvolvimento (6)'), grupos.join(' | '));
    assert(grupos.includes('Português: lições e percursos dos módulos (7)'), grupos.join(' | '));
    assert(await p1.getByText('Não vai o teu nome.').isVisible());
    assert.match(await p1.locator('[data-pe-nota]').textContent(), /respostas que escreveste.*provas e os testes ficam neste aparelho.*1 registo com o teu nome/);
    // 28/10/2026: o código não fica guardado no aparelho (aparelhos partilhados), nem antes nem depois da descarga
    assert.equal(await p1.evaluate(() => localStorage.getItem('epi-codigo-entrega')), null, 'o código não se guarda');
    assert(await semTransbordo(p1), 'caderno a 390 px com a pré-visualização');
    await p1.screenshot({ path: path.join(OUT, 'caderno-entrega-390.png'), fullPage: false, clip: await p1.locator('#entregar').boundingBox().then(b => ({ x: 0, y: b.y, width: 390, height: Math.min(900, b.height) })) }).catch(() => {});
    const [d1] = await Promise.all([p1.waitForEvent('download'), p1.getByRole('button', { name: 'Descarregar o ficheiro para entregar' }).click()]);
    const hoje = await p1.evaluate(() => EPIRegistos.hoje());
    assert.equal(d1.suggestedFilename(), `entrega-10A-07-${hoje}.json`);
    const bruto = (await lerDescarga(d1)).toString('utf8'), ent = JSON.parse(bruto);
    assert.deepEqual(Object.keys(ent), ['formato', 'versao', 'codigo', 'data', 'origem', 'registos']);
    assert.equal(ent.formato, 'epi-entrega'); assert.equal(ent.versao, 1); assert.equal(ent.codigo, '10A-07'); assert.equal(ent.origem, 'lente/caderno');
    assert(!isNaN(Date.parse(ent.data)) && ent.data.endsWith('Z'), 'data ISO');
    const esperadas = Object.keys(SEMENTE).filter(k => !FORA_DA_ENTREGA.includes(k)).sort();
    assert.deepEqual(Object.keys(ent.registos).sort(), esperadas);
    for (const k of esperadas) if (k !== 'cd-cd1-aula01') assert.equal(ent.registos[k], SEMENTE[k], 'valor igual ao do aparelho: ' + k);
    assert.deepEqual(JSON.parse(ent.registos['cd-cd1-aula01']), { mesa: 'Mesa 3', palavra: 'justo', porque: 'Porque todos falam.' }, 'sem o campo nome');
    assert(!bruto.includes('Rita') && !bruto.includes('Ritinha'), 'nenhum nome no ficheiro');
    // 28/10/2026: o estado final diz o passo que falta, com o peso de um bloco (negrito, borda), e não só uma linha a verde
    assert.match(await p1.locator('[data-pe-estado]').textContent(), /^Falta um passo: envia o ficheiro entrega-10A-07-\d{4}-\d\d-\d\d\.json \(\d+ registos\) ao docente, pelo canal combinado na turma\. Se não o encontrares, procura nas transferências/);
    assert(await p1.locator('[data-pe-estado]').evaluate(e => { const s = getComputedStyle(e); return e.classList.contains('pe-feito') && +s.fontWeight >= 700 && parseFloat(s.borderTopWidth) >= 2; }), 'estado final em bloco');
    assert.equal(await p1.evaluate(() => Object.keys(localStorage).length), Object.keys(SEMENTE).length, 'a entrega não escreve nada no aparelho');
    assert(await p1.locator('[data-pe-pre]').isHidden());
    // Cancelar fecha sem descarregar
    await preparar.click(); assert(await p1.locator('[data-pe-pre]').isVisible());
    await p1.getByRole('button', { name: 'Cancelar' }).click();
    assert(await p1.locator('[data-pe-pre]').isHidden());
    assert.equal((await p1.locator('[data-pe-estado]').textContent()).trim(), 'Cancelaste: nada foi descarregado.');
    // «Guardar num ficheiro» continua igual: leva todas as chaves do aparelho, menos o código da entrega
    const [d2] = await Promise.all([p1.waitForEvent('download'), p1.getByRole('button', { name: 'Guardar num ficheiro' }).click()]);
    assert.match(d2.suggestedFilename(), /^progresso-epi-\d{4}-\d\d-\d\d\.json$/);
    const guardado = JSON.parse((await lerDescarga(d2)).toString('utf8'));
    assert.deepEqual(Object.keys(guardado), ['formato', 'versao', 'data', 'origem', 'registos']);
    assert.equal(guardado.formato, 'epi-progresso');
    assert.deepEqual(Object.keys(guardado.registos).sort(), Object.keys(SEMENTE).sort(), 'Guardar leva tudo o que já levava');
    assert.equal((await p1.locator('[data-pf-conta]').textContent()).trim(), `Neste aparelho: ${Object.keys(SEMENTE).length} registos guardados.`);
    // 28/10/2026: depois de recarregar, o campo vem vazio (antes voltava preenchido com o código do aluno anterior)
    await p1.reload();
    assert.equal(await p1.getByLabel('O teu código').inputValue(), '');
    assert.equal(await p1.evaluate(() => localStorage.getItem('epi-codigo-entrega')), null);
    // 28/10/2026: com um só registo de um só percurso, a pré-visualização concorda no singular
    {
      const c = await context(390), p = await c.newPage();
      await p.goto(origin + '/lente/caderno/');
      await p.evaluate(v => { localStorage.clear(); localStorage.setItem('licao-m1-f04', v); localStorage.setItem('epi-som', 'true'); localStorage.setItem('epi-cartaz', '{"v":2}'); }, SEMENTE['licao-m1-f04']);
      await p.getByLabel('O teu código').fill('10A-07'); await p.getByRole('button', { name: 'Preparar a entrega' }).click();
      assert.equal(await p.locator('[data-pe-resumo]').textContent(), 'Vai 1 registo, deste percurso:', 'epi-som e epi-cartaz não contam');
      await c.close();
    }
    // armazenamento bloqueado: a mensagem aparece, nada parte
    const c1b = await context(390), p1b = await c1b.newPage(), e1b = [];
    p1b.on('pageerror', e => e1b.push(e.message));
    await c1b.addInitScript(() => { Storage.prototype.getItem = function () { throw Error('blocked'); }; Storage.prototype.setItem = function () { throw Error('blocked'); }; });
    await p1b.goto(origin + '/lente/caderno/');
    await p1b.getByLabel('O teu código').fill('10A-07'); await p1b.getByRole('button', { name: 'Preparar a entrega' }).click();
    assert.equal((await p1b.locator('[data-pe-estado]').textContent()).trim(), 'Ainda não há registos para entregar neste aparelho.');
    assert.deepEqual(e1b, []);
    await c1b.close();
    assert.deepEqual(e1, []); assert.deepEqual(dialogos, []);
    const fuga = pedidos1.filter(r => r.metodo !== 'GET' || /10A-07|Rita/.test(r.url + r.corpo));
    assert.deepEqual(fuga, [], 'nenhum pedido leva o código ou dados');
    results.push({ caderno: 'códigos inválidos recusados; 10A-07; pré-visualização; entrega com ' + esperadas.length + ' registos e sem nome; Guardar igual; teclado; armazenamento bloqueado', passou: true });

    // ---------- 2. Docente: muitos ficheiros de uma vez ----------
    const entrega = (codigo, data, registos) => J({ formato: 'epi-entrega', versao: 1, codigo, data, origem: 'lente/caderno', registos });
    const progresso = (data, registos) => J({ formato: 'epi-progresso', versao: 1, data, origem: 'https://pedrohfernandes-klk.github.io', registos });
    const f = (name, texto) => ({ name, mimeType: 'application/json', buffer: Buffer.from(texto, 'utf8') });
    const B = entrega('10A-08', '2026-10-27T09:00:00.000Z', { 'licao-m1-f04': SEMENTE['licao-m1-f04'], 'lente-cidadania-m2-sessoes-v1': J({ version: 1, sessions: { '01': { done: true }, '02': { done: true } } }) });
    const C = entrega('11B-01', '2026-10-26T09:00:00.000Z', { 'epi-treinos': SEMENTE['epi-treinos'] });
    const XSS = '<script>window.__xss=1<\/script><img src=x onerror="window.__xss=2">';
    const ficheiros = [
      f(d1.suggestedFilename(), bruto),
      f('entrega-10A-08-2026-10-27.json', B),
      f('entrega-11B-01-2026-10-26.json', C),
      f('entrega-12C-03-2026-10-25.json', entrega('12C-03', '2026-10-25T09:00:00.000Z', { 'cd1-aula1-1': XSS })),
      f('progresso-epi-2026-10-16.json', progresso('2026-10-16T08:00:00.000Z', { ...SEMENTE, 'outra-aplicacao': 'x', 'epi-projection-text-size': 'large' })),
      f('progresso-epi-2026-10-16.json', progresso('2026-10-16T09:00:00.000Z', { 'epi-narrativas': SEMENTE['epi-narrativas'] })),
      f('=1+1.json', progresso('2026-10-15T09:00:00.000Z', { 'epi-bairro': SEMENTE['epi-bairro'] })),
      f('entrega-10A-07-2026-10-20.json', entrega('10A-07', '2026-10-20T09:00:00.000Z', { 'licao-m1-f05': J({ lida: true }) })),
      f('proto.json', '{"formato":"epi-entrega","versao":1,"codigo":"10A-09","data":"2026-10-28T09:00:00Z","origem":"lente/caderno","registos":{"__proto__":{"polluted":1}}}'),
      f('fora-da-lista.json', entrega('10A-10', '2026-10-28T09:00:00Z', { 'licao-m1-f04': SEMENTE['licao-m1-f04'], 'outra-aplicacao': '1' })),
      f('html.json', entrega('10A-11', '2026-10-28T09:00:00Z', { 'epi-bairro': J({ feitas: { '<img src=x onerror=window.__xss=3>': 1 } }) })),
      f('grande.json', entrega('10A-12', '2026-10-28T09:00:00Z', { 'cd1-aula1-1': 'x'.repeat(1100000) })),
      f('partido.json', '{"formato":"epi-entrega","versao":1,"codigo":"10A-13","registos":{')
    ];
    const c2 = await context(1440), p2 = await c2.newPage(), e2 = [], pedidos2 = [], dial2 = [];
    p2.on('pageerror', e => e2.push(e.message)); p2.on('dialog', d => { dial2.push(d.message()); d.dismiss(); });
    p2.on('request', r => pedidos2.push(r.url()));
    assert.equal((await p2.goto(origin + '/lente/docente/resultados/')).status(), 200);
    assert.equal(await p2.locator('meta[name="robots"]').getAttribute('content'), 'noindex,nofollow');
    assert.equal((await p2.locator('.rt-privacidade').textContent()).trim(), 'Os ficheiros leem-se só neste navegador: nada é enviado, nada fica guardado e, ao fechar a página, tudo desaparece.');
    const antes = await p2.evaluate(async () => ({ ls: Object.keys(localStorage).sort(), ss: Object.keys(sessionStorage).sort(), idb: indexedDB.databases ? (await indexedDB.databases()).map(d => d.name) : [] }));
    await p2.locator('[data-rt-input]').setInputFiles(ficheiros);
    await p2.locator('[data-rt-estado]').filter({ hasText: 'Entraram' }).waitFor();
    assert.equal((await p2.locator('[data-rt-estado]').textContent()).trim(), 'Entraram 7 ficheiros, 5 recusados, 1 aviso. A tabela tem 7 linhas.');
    const linhas = () => p2.locator('.rt-tabela tbody tr');
    assert.equal(await linhas().count(), 7);
    const cabecas = async () => (await linhas().locator('th').allTextContents()).map(t => t.trim());
    assert.deepEqual(await cabecas(), ['10A-07', '10A-08', '11B-01', '12C-03', 'sem código=1+1.json', 'sem códigoprogresso-epi-2026-10-16.json', 'sem códigoprogresso-epi-2026-10-16.json (2)']);
    // o duplicado mais antigo fica de fora, com aviso; a linha é a da entrega de hoje
    const avisos = await p2.locator('[data-rt-avisos] li').allTextContents();
    // 28/10/2026: aviso curto, só com as datas (os nomes dos ficheiros ficam no pormenor)
    assert.equal(avisos.length, 1); assert.match(avisos[0], /^10A-07 tem duas entregas\. Ficou a de \d\d\/\d\d\/\d{4}, \d\d:\d\d; a de 20\/10\/2026, \d\d:00 ficou de fora\.$/);
    const l07 = (await linhas().nth(0).locator('td').allTextContents()).map(t => t.trim());
    assert.equal(l07[1], String(esperadas.length), 'registos da entrega de hoje');
    const cols = (await p2.locator('.rt-tabela thead th').allTextContents()).map(t => t.trim());
    const col = n => cols.indexOf(n);
    // 28/10/2026: «Data» (os progressos antigos levam «(guardado)»); a coluna «Pormenor» saiu, porque o código é a ligação
    assert.deepEqual(cols.slice(0, 3), ['Código↑', 'Data', 'Registos']);
    assert(!cols.includes('Pormenor'), cols.join(' | '));
    assert.equal(l07[col('Português: lições e percursos dos módulos') - 1], '1 lição concluída; 1 desafio ganho; 1 síntese registada; 1 nota escrita');
    assert.equal(l07[col('Cidadania e Desenvolvimento') - 1], 'M1: 1 de 8 sessões com registo (da 03 à 10); M2: 1 de 10 sessões com registo; 2 de 18 apoios do M1 com trabalho registado; 1 passo do percurso anterior; 4 respostas escritas');
    assert.equal(l07[col('Atlas Lusófono') - 1], '1 pessoa conhecida; 1 país conquistado; 1 missão feita');
    const l08 = (await linhas().nth(1).locator('td').allTextContents()).map(t => t.trim());
    assert.equal(l08[col('Cidadania e Desenvolvimento') - 1], 'M2: 2 de 10 sessões com registo');
    const lp = (await linhas().nth(5).locator('td').allTextContents()).map(t => t.trim());
    assert.equal(lp[0], '16/10/2026, ' + lp[0].slice(12, 17) + ' (guardado)', 'data do progresso antigo marcada');
    // recusados, cada um com a razão, sem parar os outros
    const rec = await p2.locator('[data-rt-recusados] li').allTextContents();
    // 28/10/2026: sem razões técnicas; a caixa diz o que pedir ao aluno
    assert.deepEqual(rec, [
      '«proto.json»: O ficheiro foi alterado ou não vem do caderno.',
      '«fora-da-lista.json»: O ficheiro tem um registo que o caderno não entrega («outra-aplicacao»).',
      '«html.json»: O ficheiro foi alterado ou não vem do caderno.',
      '«grande.json»: O ficheiro tem mais de 1 MB.',
      '«partido.json»: O ficheiro está estragado: o conteúdo não se lê.'
    ]);
    assert.match(await p2.locator('[data-rt-recusados-c]').textContent(), /Pede a estes alunos que voltem a fazer «Entregar ao docente»/);
    assert.equal(await p2.evaluate(() => ({}).polluted), undefined, 'sem poluição do protótipo');
    // o texto com <script> mostra-se como texto e nada corre
    const d12 = p2.locator('details.rt-p').filter({ hasText: '12C-03' });
    await d12.locator('summary').first().click();
    await d12.locator('details.rt-t summary').click();
    assert.equal(await d12.locator('.rt-texto').textContent(), XSS);
    assert.equal(await p2.evaluate(() => window.__xss), undefined, 'nenhum script injetado correu');
    assert.equal(await p2.locator('[data-rt] script, [data-rt] img, [data-rt] iframe').count(), 0);
    // o progresso antigo: ficou de fora o que não viaja, e o nome
    const dp = p2.locator('details.rt-p').filter({ hasText: 'progresso-epi-2026-10-16.json (progresso' }).first();
    assert.match(await dp.textContent(), /Ficaram de fora: 1 registo da Sala, desligada; 3 registos que só servem o aparelho; 1 registo de provas e testes, que ficam no aparelho; 1 registo com nome, retirado; 1 registo que o caderno não entrega\./);
    assert(!(await p2.locator('[data-rt]').textContent()).includes('Rita'), 'nenhum nome na página');
    // ordenar pelo código
    await p2.locator('.rt-ordenar').click();
    assert.equal(await p2.locator('.rt-tabela thead th').first().getAttribute('aria-sort'), 'descending');
    assert.equal((await cabecas())[0], '12C-03');
    assert.equal(await p2.evaluate(() => document.activeElement.className), 'rt-ordenar', 'o foco fica no botão de ordenar');
    await p2.keyboard.press('Enter');
    assert.equal(await p2.locator('.rt-tabela thead th').first().getAttribute('aria-sort'), 'ascending');
    assert.equal((await cabecas())[0], '10A-07');
    // pormenor: a ligação abre o painel certo; os resumos abrem com Enter
    // 28/10/2026: o próprio código, na coluna fixa, é a ligação; o resumo fechado mostra «+» e o aberto «−»
    assert.equal(await p2.locator('details.rt-p').count(), 7);
    const sinal = n => p2.locator('details.rt-p').nth(n).locator('summary').first().evaluate(e => getComputedStyle(e, '::before').content);
    assert.equal(await sinal(1), '"+"');
    assert.equal(await p2.locator('[data-rt-pormenor-vazio]').textContent(), 'Carrega num código para abrir o pormenor.');
    await linhas().nth(1).getByRole('link', { name: '10A-08' }).click();
    assert.equal(await sinal(1), '"−"');
    const d08 = p2.locator('details.rt-p').nth(1);
    assert(await d08.evaluate(e => e.open)); assert.equal(await p2.evaluate(() => document.activeElement.tagName), 'SUMMARY');
    await p2.locator('details.rt-p').nth(2).locator('summary').first().focus(); await p2.keyboard.press('Enter');
    assert(await p2.locator('details.rt-p').nth(2).evaluate(e => e.open), 'Enter abre o pormenor');
    assert.match(await p2.locator('details.rt-p').nth(0).textContent(), /M1, lição F04: concluída, melhor resultado 10 de 11, 2 tentativas/);
    // CSV
    const [d3] = await Promise.all([p2.waitForEvent('download'), p2.getByRole('button', { name: 'Descarregar a tabela (CSV)' }).click()]);
    assert.match(d3.suggestedFilename(), /^resultados-turma-\d{4}-\d\d-\d\d\.csv$/);
    const csv = await lerDescarga(d3);
    assert.deepEqual([...csv.subarray(0, 3)], [0xef, 0xbb, 0xbf], 'BOM UTF-8');
    const tcsv = csv.toString('utf8').slice(1), cl = tcsv.split('\r\n');
    assert.equal(cl.length, 9, 'cabeçalho, 7 linhas e o fim com CRLF'); assert.equal(cl[8], '');
    // 28/10/2026: a coluna chama-se «Data»
    assert(cl[0].startsWith('"Código";"Ficheiro";"Data";"Registos";'), cl[0]);
    assert(cl[5].includes(' (guardado)";'), 'a data do progresso antigo vai marcada no CSV: ' + cl[5]);
    assert(!/[^\r]\n/.test(tcsv), 'só CRLF');
    assert(cl[5].startsWith('"sem código";"\'=1+1.json";'), 'proteção contra fórmulas: ' + cl[5]);
    assert(cl[1].startsWith('"10A-07";"entrega-10A-07-'), cl[1]);
    assert(cl.slice(1, 8).every(l => l.split('";"').length === cl[0].split('";"').length), 'todas as linhas com as mesmas colunas');
    // 28/10/2026: as listas mostram o último lote: o ficheiro corrigido entra e os recusados de antes saem da caixa
    await p2.locator('[data-rt-input]').setInputFiles([f('entrega-10A-10-2026-10-28.json', entrega('10A-10', '2026-10-28T09:30:00Z', { 'licao-m1-f04': SEMENTE['licao-m1-f04'] }))]);
    await p2.locator('[data-rt-estado]').filter({ hasText: 'Entrou 1 ficheiro' }).waitFor();
    assert.equal(await p2.locator('[data-rt-recusados] li').count(), 0);
    assert(await p2.locator('[data-rt-recusados-c]').isHidden());
    assert.equal(await linhas().count(), 8);
    // nada guardado, nada enviado
    const depois = await p2.evaluate(async () => ({ ls: Object.keys(localStorage).sort(), ss: Object.keys(sessionStorage).sort(), idb: indexedDB.databases ? (await indexedDB.databases()).map(d => d.name) : [] }));
    assert.deepEqual(depois, antes, 'o armazenamento não mudou');
    assert.deepEqual(depois.idb, [], 'sem IndexedDB');
    // largar ficheiros por arrastar, depois de limpar
    // 28/10/2026: com o teclado; o botão fica desativado e o foco passa para o campo dos ficheiros (não cai no body)
    await p2.getByRole('button', { name: 'Limpar a tabela' }).focus(); await p2.keyboard.press('Enter');
    assert.equal(await linhas().count(), 0); assert(await p2.locator('[data-rt-vazio]').isVisible());
    assert.equal((await p2.locator('[data-rt-estado]').textContent()).trim(), 'A tabela ficou vazia.');
    assert(await p2.evaluate(() => document.activeElement && document.activeElement.matches('[data-rt-input]')), 'o foco fica no campo dos ficheiros');
    assert.equal(await p2.locator('[data-rt-recusados] li').count(), 0);
    const zona = p2.locator('[data-rt-zona]');
    const dt = await p2.evaluateHandle(([a, b]) => { const t = new DataTransfer(); t.items.add(new File([a], 'entrega-10A-08-2026-10-27.json', { type: 'application/json' })); t.items.add(new File([b], 'entrega-11B-01-2026-10-26.json', { type: 'application/json' })); return t; }, [B, C]);
    await zona.dispatchEvent('dragenter', { dataTransfer: dt }); await zona.dispatchEvent('dragover', { dataTransfer: dt });
    assert(await zona.evaluate(e => e.classList.contains('rt-arrastar')), 'a caixa acende-se ao arrastar');
    await zona.dispatchEvent('drop', { dataTransfer: dt });
    await p2.locator('[data-rt-estado]').filter({ hasText: 'Entraram 2' }).waitFor();
    assert.equal(await linhas().count(), 2);
    assert(!(await zona.evaluate(e => e.classList.contains('rt-arrastar'))));
    // o mesmo ficheiro escolhido outra vez: aviso, sem linha nova
    await p2.locator('[data-rt-input]').setInputFiles([f('entrega-10A-08-2026-10-27.json', B)]);
    // 28/10/2026: «Não entrou nenhum ficheiro novo» em vez de «Entraram 0 ficheiros»
    await p2.locator('[data-rt-estado]').filter({ hasText: 'Não entrou nenhum ficheiro novo' }).waitFor();
    assert.equal((await p2.locator('[data-rt-estado]').textContent()).trim(), 'Não entrou nenhum ficheiro novo: 1 aviso. A tabela tem 2 linhas.');
    assert.equal(await linhas().count(), 2);
    assert.deepEqual(await p2.locator('[data-rt-avisos] li').allTextContents(), ['«entrega-10A-08-2026-10-27.json» já tinha sido lido: não entrou outra vez.']);
    // 28/10/2026: uma entrega com o código de outro aluno e data no futuro não substitui a verdadeira
    await p2.locator('[data-rt-input]').setInputFiles([
      f('entrega-10B-01-2026-10-28.json', entrega('10B-01', new Date(Date.now() - 36e5).toISOString(), { 'licao-m1-f04': SEMENTE['licao-m1-f04'] })),
      f('entrega-10B-01-falso.json', entrega('10B-01', '2099-01-01T00:00:00.000Z', { 'licao-m1-f05': J({ lida: true }) }))
    ]);
    await p2.locator('[data-rt-estado]').filter({ hasText: 'Entrou 1 ficheiro' }).waitFor();
    const av = await p2.locator('[data-rt-avisos] li').allTextContents();
    assert.equal(av.length, 1); assert.match(av[0], /^10B-01 tem duas entregas\. Ficou a de .*; a outra tem data no futuro \(01\/01\/2099, \d\d:00\) e ficou de fora\.$/);
    assert.match(await p2.locator('details.rt-p').filter({ hasText: '10B-01' }).locator('.rt-p-f').first().textContent(), /entrega-10B-01-2026-10-28\.json/);
    // uma entrega sozinha com data no futuro entra, marcada
    await p2.locator('[data-rt-input]').setInputFiles([f('entrega-10B-02-falso.json', entrega('10B-02', '2099-01-01T00:00:00.000Z', { 'licao-m1-f05': J({ lida: true }) }))]);
    await p2.locator('[data-rt-estado]').filter({ hasText: 'A tabela tem 4 linhas' }).waitFor();
    const l02 = linhas().filter({ hasText: '10B-02' });
    assert.match(await l02.locator('td').first().textContent(), /^01\/01\/2099, \d\d:00 \(data no futuro\)$/);
    assert.equal(await l02.locator('td.rt-suspeita').count(), 1);
    // teclado: a caixa dos ficheiros alcança-se com Tab, com foco visível
    await p2.locator('.atelier-breadcrumb a').first().focus();
    let chegou = false;
    for (let i = 0; i < 12 && !chegou; i++) { await p2.keyboard.press('Tab'); chegou = await p2.evaluate(() => document.activeElement && document.activeElement.matches('[data-rt-input]')); }
    assert(chegou, 'o campo dos ficheiros alcança-se com Tab');
    assert.equal(await p2.evaluate(() => { const i = document.activeElement; return i.labels && i.labels[0] && i.labels[0].textContent.includes('Escolher ficheiros'); }), true, 'nome acessível pela etiqueta');
    assert(await zona.evaluate(e => { const s = getComputedStyle(e); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2; }), 'foco visível na caixa');
    // recarregar: tudo desaparece
    await p2.reload();
    assert.equal(await linhas().count(), 0); assert(await p2.locator('[data-rt-vazio]').isVisible());
    assert(await p2.locator('[data-rt-csv]').isDisabled());
    const fora = pedidos2.filter(u => !u.startsWith(origin + '/') && !u.startsWith('blob:') && !u.startsWith('data:'));
    assert.deepEqual(fora, [], 'zero pedidos fora da origem local');
    assert(pedidos2.every(u => !/\.json/.test(u)), 'os ficheiros nunca vão para a rede');
    assert.deepEqual(e2, []); assert.deepEqual(dial2, []);
    results.push({ docente: '7 linhas, 5 recusados, 1 aviso de duplicado; ordem; pormenor; CSV; largar; mesmo ficheiro; limpar; recarregar vazio', pedidos_fora_da_origem: 0, armazenamento_alterado: false, passou: true });
    await c2.close(); await c1.close();

    // ---------- 3. A ligação no hub do docente ----------
    {
      const c = await context(1440), p = await c.newPage();
      await p.goto(origin + '/lente/docente/');
      const a = p.locator('#tarefa-90 > a[href="resultados/"]');
      assert.equal(await a.count(), 1, 'ligação em 03 · ACOMPANHAR');
      // 28/10/2026: com o subtítulo «Entregas do caderno» e a seta presa à última palavra (espaço inseparável)
      assert.equal((await a.textContent()).trim(), 'Resultados da turma: ler as entregas do caderno\u00a0→');
      assert.equal(await p.locator('#tarefa-90 > h3 + a[href="resultados/"]').count(), 1);
      assert.equal((await p.locator('#tarefa-90 > h3').textContent()).trim(), 'Entregas do caderno');
      assert((await a.boundingBox()).height >= 44, 'alvo de 44 px');
      await a.click(); await p.waitForURL(/\/docente\/resultados\/$/);
      assert.equal((await p.locator('h1').textContent()).trim(), 'Resultados da turma.');
      await c.close();
    }

    // ---------- 4. De 320 a 1440 px, nos dois temas ----------
    const poucos = [ficheiros[0], ficheiros[1], ficheiros[4], ficheiros[6], ficheiros[8]];
    for (const width of [320, 390, 768, 1024, 1440]) for (const scheme of ['light', 'dark']) {
      const c = await context(width, scheme), p = await c.newPage(), e = [];
      p.on('pageerror', x => e.push(x.message));
      await p.goto(origin + '/lente/docente/resultados/');
      assert(await semTransbordo(p), `${width} ${scheme} vazio`);
      await p.locator('[data-rt-input]').setInputFiles(poucos);
      await p.locator('[data-rt-estado]').filter({ hasText: 'Entraram' }).waitFor();
      await p.locator('details.rt-p').first().locator('summary').first().click();
      assert(await semTransbordo(p), `${width} ${scheme} com a tabela e o pormenor`);
      const caixa = await p.locator('[data-rt-tabela-c]').evaluate(el => ({ sw: el.scrollWidth, cw: el.clientWidth, ov: getComputedStyle(el).overflowX }));
      assert.equal(caixa.ov, 'auto');
      if (width <= 768) assert(caixa.sw > caixa.cw, `${width}: a tabela desliza dentro do contentor`);
      // 28/10/2026: a coluna Código fica fixa e opaca quando a tabela desliza até ao fim; a explicação cabe no ecrã
      const fixa = await p.locator('[data-rt-tabela-c]').evaluate(el => {
        el.scrollLeft = el.scrollWidth;
        const c = el.getBoundingClientRect(), th = el.querySelector('tbody th').getBoundingClientRect(), h = el.querySelector('thead th').getBoundingClientRect();
        const bg = getComputedStyle(el.querySelector('tbody th')).backgroundColor, corpo = getComputedStyle(document.body).backgroundColor;
        const r = { dentro: th.left >= c.left - 1 && th.right <= c.right + 1 && h.left >= c.left - 1, bg, corpo, desliza: el.scrollLeft > 0 };
        el.scrollLeft = 0; return r;
      });
      assert(fixa.dentro, `${width} ${scheme}: a coluna Código continua à vista`);
      assert.equal(fixa.bg, fixa.corpo, `${width} ${scheme}: o fundo da coluna fixa é o da página`);
      const d = await p.locator('[data-rt-tabela-d]').boundingBox();
      assert(d && d.x + d.width <= width, `${width}: a explicação da tabela não sai do ecrã`);
      const fundo = await p.evaluate(() => getComputedStyle(document.body).backgroundColor.match(/\d+/g).slice(0, 3).reduce((a, b) => a + +b, 0));
      assert(scheme === 'dark' ? fundo < 150 : fundo > 650, `${width} ${scheme} tema (soma RGB ${fundo})`);
      await p.keyboard.press('Shift'); // modo teclado: depois de um clique, o foco programático não mostra :focus-visible
      const foco = await p.locator('.rt-ordenar').evaluate(el => { el.focus(); const s = getComputedStyle(el); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2; });
      assert(foco, `${width} ${scheme} foco visível`);
      if ((width === 320 || width === 1440)) await p.screenshot({ path: path.join(OUT, `docente-${width}-${scheme}.png`), fullPage: true });
      // caderno com a pré-visualização aberta
      await p.goto(origin + '/lente/caderno/');
      await p.evaluate(s => { for (const [k, v] of Object.entries(s)) localStorage.setItem(k, v); }, SEMENTE);
      await p.getByLabel('O teu código').fill('10A-07'); await p.getByRole('button', { name: 'Preparar a entrega' }).click();
      assert(await p.locator('[data-pe-pre]').isVisible());
      assert(await semTransbordo(p), `${width} ${scheme} caderno`);
      if (width === 320) await p.locator('#entregar').screenshot({ path: path.join(OUT, `caderno-entrega-320-${scheme}.png`) });
      assert.deepEqual(e, [], `${width} ${scheme}`);
      results.push({ width, scheme, transbordo: false, erros: 0 });
      await c.close();
    }
    fs.writeFileSync(path.join(OUT, 'qa-browser.json'), JSON.stringify(results, null, 2));
    console.log(JSON.stringify({ observations: results.length, passed: true, output: OUT }));
  } finally { await browser.close(); server.close(); }
})().catch(e => { console.error(e); server.close(); process.exitCode = 1; });
