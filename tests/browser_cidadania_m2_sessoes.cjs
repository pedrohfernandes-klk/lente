/* Cidadania M2: dez sessões no molde do M1 (28/10/2026).
   Dez rotas de 320 a 1440 px nos dois temas, sem transbordo nem erros, em todos os passos; teclado; retoma depois
   de recarregar; registo e «Continuar» no índice; impressão; projeção sem registo; sem JavaScript; estado inválido
   e armazenamento bloqueado; chaves antigas intactas; ligações locais a 200. M2_OUT escolhe a pasta das capturas. */
const fs = require('fs'), path = require('path'), http = require('http'), assert = require('assert');
const { chromium } = require('playwright');
const R = path.resolve(__dirname, '..'), OUT = process.env.M2_OUT || path.resolve(R, '../../outputs/revisao-cidadania-m2');
fs.mkdirSync(OUT, { recursive: true });
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.pdf': 'application/pdf', '.svg': 'image/svg+xml', '.json': 'application/json' };
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
const KEY = 'lente-cidadania-m2-sessoes-v1', IDS = Array.from({ length: 10 }, (_, i) => String(i + 1).padStart(2, '0'));
const results = [];
(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = 'http://127.0.0.1:' + server.address().port;
  const browser = await chromium.launch({ headless: true, ...(process.env.M2_CHROMIUM ? { executablePath: process.env.M2_CHROMIUM } : {}) });
  async function context(width = 1440, scheme = 'light') {
    const c = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme, reducedMotion: 'reduce' });
    await c.route('https://pedrohfernandes-klk.github.io/lente/**', async route => { const p = file(route.request().url()); await route.fulfill({ status: fs.existsSync(p) ? 200 : 404, body: fs.existsSync(p) ? fs.readFileSync(p) : '', contentType: MIME[path.extname(p)] || 'application/octet-stream' }); });
    await c.route('https://fonts.googleapis.com/**', r => r.abort()); await c.route('https://fonts.gstatic.com/**', r => r.abort());
    return c;
  }
  const semTransbordo = p => p.evaluate(() => document.documentElement.scrollWidth <= innerWidth);
  try {
    // 1. Dez sessões, de 320 a 1440 px, nos dois temas: capa e cada um dos cinco passos.
    for (const width of [320, 390, 768, 1024, 1440]) for (const scheme of ['light', 'dark']) {
      const ctx = await context(width, scheme), p = await ctx.newPage(), errors = [];
      p.on('pageerror', e => errors.push(e.message));
      for (const id of IDS) {
        const route = 'cidadania/m2/sessoes/' + id + '/';
        assert.equal((await p.goto(origin + '/lente/' + route)).status(), 200, route);
        assert(await semTransbordo(p), `${width} ${scheme} ${route} capa`);
        await p.locator('[data-start]').click();
        for (let i = 0; i < 5; i++) {
          if (i) await p.locator('[data-stage-link]').nth(i).click();
          assert.equal(await p.locator('[data-stage]:visible').count(), 1, route);
          assert(await semTransbordo(p), `${width} ${scheme} ${route} passo ${i + 1}`);
          if (width === 390 && scheme === 'dark' && id === '04' && i === 3) await p.screenshot({ path: path.join(OUT, 'sessao-04-faz-telemovel-escuro.png'), fullPage: true });
          if (width === 1440 && scheme === 'light' && id === '02' && i === 1) await p.screenshot({ path: path.join(OUT, 'sessao-02-ve.png'), fullPage: true });
        }
        await p.evaluate(() => localStorage.clear());
      }
      for (const route of ['cidadania/m2/sessoes/', 'cidadania/m2/', 'cidadania/', 'cidadania/m2/aulas/04/', 'cidadania/m2/imagens/', 'cidadania/m2/glossario/']) {
        assert.equal((await p.goto(origin + '/lente/' + route)).status(), 200, route);
        assert(await semTransbordo(p), `${width} ${scheme} ${route}`);
        if (width === 1440 && scheme === 'light' && route === 'cidadania/m2/') await p.screenshot({ path: path.join(OUT, 'modulo-m2.png'), fullPage: true });
        // 28/10/2026: o guia a 320 px passa os 16 384 px de altura que o Chromium consegue capturar; a captura fica
        // pelos primeiros 16 000 px (a verificação de transbordo acima cobre a página inteira).
        // 28/10/2026: 16 000 px ainda falhava («Unable to capture screenshot») neste ambiente; a captura fica pelos primeiros 6000 px.
        if (width === 320 && scheme === 'light' && route === 'cidadania/m2/sessoes/') await p.screenshot({ path: path.join(OUT, 'guia-320.png'), fullPage: true, clip: { x: 0, y: 0, width: 320, height: Math.min(6000, await p.evaluate(() => document.documentElement.scrollHeight)) } });
      }
      assert.deepEqual(errors, [], `${width} ${scheme}`);
      results.push({ width, scheme, rotas: 16, passos: 50, transbordo: false, erros: 0 });
      await ctx.close();
    }

    // 2. Estrutura, ligações locais a 200 e chaves antigas intactas.
    const ctx = await context(), p = await ctx.newPage(), errors = [];
    p.on('pageerror', e => errors.push(e.message));
    await p.goto(origin + '/lente/cidadania/m2/');
    const antigas = { 'epi-cidadania-m2': '{"feitas":{"passo-01":123}}', 'lente-cidadania-m1-sessoes-v2': '{"version":2,"sessions":{"03":{"done":true,"stage":4}}}', 'lente-justica-licao-2': '{"lida":true}' };
    await p.evaluate(v => { for (const [k, x] of Object.entries(v)) localStorage.setItem(k, x); }, antigas);
    const vistos = new Set();
    for (const route of IDS.map(id => 'cidadania/m2/sessoes/' + id + '/').concat(['cidadania/m2/sessoes/', 'cidadania/m2/'])) {
      await p.goto(origin + '/lente/' + route);
      assert.equal(await p.locator('h1').count(), 1, route);
      const links = await p.locator('a').evaluateAll(es => es.map(e => e.href.split('#')[0]).filter(h => h.startsWith(location.origin)));
      for (const href of links) if (!vistos.has(href)) { vistos.add(href); assert.equal((await ctx.request.get(href)).status(), 200, route + ' -> ' + href); }
      if (route.match(/sessoes\/\d\d\//)) {
        assert.equal(await p.locator('[data-stage]').count(), 5);
        assert.equal(await p.locator('[data-session-done]').count(), 1);
        assert.equal(await p.locator('[data-stage]:visible').count(), 0, 'abre na capa');
        // 01/11/2026: #77 substituiu as obras das sessões 03/09 por casos; exigir o contrato publicado completo.
        const caso = /sessoes\/(03|09)\//.test(route);
        assert.equal(await p.locator('.c10-obra').count(), caso || route.includes('/10/') ? 0 : 1, route);
        assert.equal(await p.locator('#caso-reciclado').count(), caso ? 1 : 0, route);
        assert.equal(await p.locator('#caso-reciclado [data-opcoes-reciclagem]').count(), caso ? 2 : 0, route);
        if (caso) assert.equal(await p.locator('#caso-reciclado summary', { hasText: 'Ler o relato em português' }).count(), 1, route);
        assert.equal(await p.locator('.c10-mapa li[aria-current="step"]').count(), 1, route);
      }
    }
    results.push({ ligacoes_locais_200: vistos.size });

    // 3. Teclado: setas entre passos; «Comparar razões» abre com Enter; foco visível no passo.
    await p.goto(origin + '/lente/cidadania/m2/sessoes/03/');
    await p.locator('[data-start]').focus(); await p.keyboard.press('Enter');
    assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-1');
    assert.equal(await p.evaluate(() => document.activeElement.id), 'momento-1');
    await p.keyboard.press('ArrowRight'); assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-2');
    await p.keyboard.press('ArrowRight'); assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-3');
    await p.locator('[data-feedback]>summary').focus(); await p.keyboard.press('Enter');
    assert(await p.locator('[data-feedback]').evaluate(e => e.open));
    await p.keyboard.press('ArrowLeft'); assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-3', 'as setas não roubam o foco de um resumo');
    await p.locator('[data-next]').focus(); await p.keyboard.press('Enter');
    assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-4');
    const foco = await p.locator('[data-stage-link]').nth(0).evaluate(e => { e.focus(); const s = getComputedStyle(e); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2; });
    assert(foco, 'foco visível');

    // 4. Retoma depois de recarregar, sem âncora: «Retomar no passo 4».
    await p.goto(origin + '/lente/cidadania/m2/sessoes/03/');
    assert.equal((await p.locator('[data-start]').textContent()).trim(), 'Retomar no passo 4');
    await p.locator('[data-start]').click();
    assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-4');
    await p.reload();
    assert.equal(await p.locator('[data-stage]:visible').getAttribute('id'), 'momento-4', 'a âncora mantém o passo');

    // 5. Registo no último passo; o índice do módulo mostra o estado e continua na sessão certa.
    for (const id of ['01', '02']) {
      await p.goto(origin + '/lente/cidadania/m2/sessoes/' + id + '/');
      await p.locator('[data-start]').click(); await p.locator('[data-stage-link]').nth(4).click();
      await p.locator('[data-session-done]').check();
      assert((await p.locator('[data-live]').textContent()).includes('guardado'));
      await p.reload(); assert(await p.locator('[data-session-done]').isChecked());
    }
    await p.goto(origin + '/lente/cidadania/m2/');
    assert.equal(await p.locator('[data-session-card]').count(), 10);
    assert.equal(await p.locator('[data-continue]').getAttribute('href'), 'sessoes/03/');
    assert.equal((await p.locator('[data-continue]').textContent()).trim(), 'Continuar na sessão 03');
    assert.equal((await p.locator('[data-session-card="01"] [data-status]').textContent()).trim(), 'Registado');
    assert.equal((await p.locator('[data-session-card="03"] [data-status]').textContent()).trim(), 'Em curso');
    assert.equal(await p.locator('[data-session-card="03"]').getAttribute('data-current'), 'true');
    assert.equal((await p.locator('[data-count]').textContent()).trim(), '2 registos de trabalho');
    assert.deepEqual(await p.evaluate(k => Object.fromEntries(k.map(x => [x, localStorage.getItem(x)])), Object.keys(antigas)), antigas, 'chaves antigas intactas');
    // 28/10/2026: o cartão do M2 no portal mostra as sessões registadas (só lê a chave nova).
    await p.goto(origin + '/lente/cidadania/');
    assert.equal((await p.locator('[data-prog="m2"]').textContent()).trim(), '2 de 10 sessões registadas');
    assert.deepEqual(await p.evaluate(k => Object.fromEntries(k.map(x => [x, localStorage.getItem(x)])), Object.keys(antigas)), antigas, 'o portal não toca nas chaves');
    const guardado = JSON.parse(await p.evaluate(k => localStorage.getItem(k), KEY));
    assert.equal(guardado.version, 1); assert.equal(guardado.sessions['01'].done, true);

    // 6. Impressão: os cinco passos e os detalhes abertos; depois volta a um passo.
    await p.goto(origin + '/lente/cidadania/m2/sessoes/06/');
    await p.locator('[data-start]').click();
    await p.evaluate(() => dispatchEvent(new Event('beforeprint')));
    assert.equal(await p.locator('[data-stage]:visible').count(), 5);
    assert(await p.locator('details.c10-fonte').first().evaluate(e => e.open));
    await p.emulateMedia({ media: 'print' });
    await p.pdf({ path: path.join(OUT, 'sessao-06-impressao.pdf'), format: 'A4', printBackground: true });
    assert(await p.locator('.c10-mapa span').first().isVisible(), 'o mapa imprime as legendas');
    await p.emulateMedia({ media: 'screen' });
    await p.evaluate(() => dispatchEvent(new Event('afterprint')));
    assert.equal(await p.locator('[data-stage]:visible').count(), 1);

    // 7. Projeção: a moldura não grava nada e o registo fica desligado.
    const antes = await p.evaluate(k => localStorage.getItem(k), KEY);
    await p.goto(origin + '/lente/projetar/?pagina=/lente/cidadania/m2/sessoes/04/');
    const f = p.frameLocator('#lesson-frame');
    await f.locator('[data-session-done]').waitFor({ state: 'attached' });
    assert(await f.locator('[data-session-done]').isDisabled());
    for (const size of ['small', 'medium', 'large']) { await p.locator(`[data-projection-size="${size}"]`).click(); assert(await f.locator('html').evaluate(e => e.scrollWidth <= e.clientWidth), size); }
    await f.locator('[data-start]').click(); await f.locator('[data-next]').click(); await f.locator('[data-next]').click();
    assert.equal(await p.evaluate(k => localStorage.getItem(k), KEY), antes, 'projeção sem registo');
    await p.screenshot({ path: path.join(OUT, 'projecao-m2.png') });
    // ?projetar=1 fora da moldura também não grava
    await p.goto(origin + '/lente/cidadania/m2/sessoes/05/?projetar=1');
    await p.locator('[data-start]').click(); await p.locator('[data-next]').click();
    assert.equal(await p.evaluate(k => localStorage.getItem(k), KEY), antes);
    assert.deepEqual(errors, []);
    results.push({ funcoes: 'teclado; retoma; registo e continuar; impressão; projeção sem registo; chaves antigas intactas', passou: true });
    await ctx.close();

    // 28/10/2026 (revisão de design). 7a. Com Tab e Shift+Tab, o elemento com o foco nunca fica por baixo das barras
    // fixas; no telemóvel, o botão do tema sai durante a sessão; o índice tem um só «começa aqui».
    for (const [w, h] of [[390, 844], [1440, 900]]) {
      const c7 = await browser.newContext({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
      await c7.route('https://fonts.googleapis.com/**', r => r.abort()); await c7.route('https://fonts.gstatic.com/**', r => r.abort());
      const q = await c7.newPage(), tapados = [];
      let vistos7 = 0;
      for (const id of IDS) for (const st of [2, 4, 5]) {
        await q.goto(origin + `/lente/cidadania/m2/sessoes/${id}/#momento-${st}`);
        await q.locator(`#momento-${st}`).focus();
        for (const dir of ['Tab', 'Shift+Tab']) {
          if (dir === 'Shift+Tab') await q.locator('[data-next], [data-next-session]').filter({ visible: true }).first().focus();
          for (let i = 0; i < 40; i++) {
            await q.keyboard.press(dir);
            const r = await q.evaluate(() => {
              const e = document.activeElement; if (!e || e === document.body || !e.closest('[data-stage]')) return null;
              const a = e.getBoundingClientRect(), bar = document.querySelector('.c10-stagebar').getBoundingClientRect(), ctl = document.querySelector('.c10-control').getBoundingClientRect();
              const sob = (a.top < bar.bottom - 2 && a.bottom > bar.top) || (a.bottom > ctl.top + 2 && a.top < ctl.bottom);
              return { t: (e.textContent || '').trim().slice(0, 40), sob };
            });
            if (!r) break;
            vistos7++;
            if (r.sob) tapados.push(`${w} ${id} p${st} ${dir} «${r.t}»`);
          }
        }
      }
      assert.deepEqual(tapados, [], 'foco tapado pelas barras');
      results.push({ largura: w, focos_vistos: vistos7, focos_tapados: 0 });
      if (w === 390) {
        await q.goto(origin + '/lente/cidadania/m2/sessoes/02/');
        assert(await q.locator('[data-appearance-floating]').isVisible(), 'o tema está na abertura');
        await q.locator('[data-start]').click();
        assert(!(await q.locator('[data-appearance-floating]').isVisible()), 'o botão do tema não tapa a sessão');
      }
      await c7.close();
    }
    {
      const c8 = await context(), q = await c8.newPage();
      await q.goto(origin + '/lente/cidadania/m2/');
      assert.equal(await q.locator('.missao[data-id="passo-00"]').evaluate(e => e.classList.contains('p-atual')), false, 'sem passos feitos, o passo 00 não se destaca');
      assert(!(await q.locator('.missao[data-id="passo-00"]').textContent()).includes('começa por aqui'));
      assert.equal((await q.locator('[data-continue]').textContent()).trim(), 'Começar na sessão 01');
      await q.evaluate(() => localStorage.setItem('epi-cidadania-m2', '{"feitas":{"passo-00":1}}')); await q.reload();
      assert((await q.locator('.missao[data-id="passo-01"]').textContent()).includes('Sugerida: a seguir'), 'depois do primeiro passo, volta a sugestão');
      await c8.close();
    }

    // 7b. A fonte do Google não bloqueia: com o pedido pendurado (sem resposta), a página aparece na mesma.
    {
      const c9 = await browser.newContext({ viewport: { width: 390, height: 844 } }), q = await c9.newPage();
      await c9.route('https://fonts.googleapis.com/**', () => {}); await c9.route('https://fonts.gstatic.com/**', () => {});
      await c9.route('https://pedrohfernandes-klk.github.io/lente/**', async route => { const f = file(route.request().url()); await route.fulfill({ status: fs.existsSync(f) ? 200 : 404, body: fs.existsSync(f) ? fs.readFileSync(f) : '', contentType: MIME[path.extname(f)] || 'application/octet-stream' }); });
      for (const route of ['cidadania/m2/sessoes/03/', 'cidadania/m2/sessoes/']) {
        await q.goto(origin + '/lente/' + route, { waitUntil: 'domcontentloaded', timeout: 8000 });
        await q.locator('h1').waitFor({ state: 'visible', timeout: 4000 });
        const fcp = await q.evaluate(() => new Promise(r => { const e = performance.getEntriesByName('first-contentful-paint')[0]; if (e) return r(e.startTime); new PerformanceObserver(l => r(l.getEntries()[0].startTime)).observe({ type: 'paint', buffered: true }); setTimeout(() => r(null), 3000); }));
        assert(fcp !== null && fcp < 4000, route + ' sem primeira pintura com a fonte pendurada');
      }
      results.push({ fonte_pendurada: 'a página aparece', passou: true });
      await c9.close();
    }

    // 8. Estado inválido e armazenamento bloqueado: a página funciona na mesma.
    for (const seed of ['{invalid', '{"version":1,"sessions":[]}', '{"version":7,"sessions":{}}']) {
      const c = await context(), q = await c.newPage(), e2 = [];
      q.on('pageerror', e => e2.push(e.message));
      await q.goto(origin + '/lente/cidadania/m2/'); await q.evaluate(([k, s]) => localStorage.setItem(k, s), [KEY, seed]); await q.reload();
      assert.equal(await q.locator('[data-continue]').getAttribute('href'), 'sessoes/01/');
      await q.goto(origin + '/lente/cidadania/m2/sessoes/01/'); assert.equal((await q.locator('[data-start]').textContent()).trim(), 'Começar');
      assert.deepEqual(e2, [], seed); await c.close();
    }
    const c = await context(), q = await c.newPage();
    await c.addInitScript(() => { Storage.prototype.getItem = function () { throw Error('blocked'); }; Storage.prototype.setItem = function () { throw Error('blocked'); }; });
    await q.goto(origin + '/lente/cidadania/m2/sessoes/07/'); await q.locator('[data-start]').click(); await q.locator('[data-stage-link]').nth(4).click();
    await q.locator('[data-session-done]').check();
    assert((await q.locator('[data-live]').textContent()).includes('não permite guardar'));
    await c.close();

    // 9. Sem JavaScript: os cinco passos à vista, os detalhes abrem, nada transborda.
    const no = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } }), np = await no.newPage();
    for (const id of ['01', '10']) {
      await np.goto(origin + '/lente/cidadania/m2/sessoes/' + id + '/');
      assert.equal(await np.locator('[data-stage]:visible').count(), 5);
      assert(await semTransbordo(np));
      await np.locator('[data-feedback]>summary').click(); assert(await np.locator('[data-feedback] p').isVisible());
      // 28/10/2026: sem JavaScript, a barra de controlo (vazia) não aparece
      assert(!(await np.locator('.c10-control').isVisible()), 'barra de controlo vazia sem JavaScript');
    }
    await np.goto(origin + '/lente/cidadania/m2/');
    assert.equal(await np.locator('[data-continue]').getAttribute('href'), 'sessoes/01/');
    await no.close();
    results.push({ alternativas: 'estado inválido; armazenamento bloqueado; sem JavaScript', passou: true });
    fs.writeFileSync(path.join(OUT, 'qa-browser.json'), JSON.stringify(results, null, 2));
    console.log(JSON.stringify({ observations: results.length, passed: true, output: OUT }));
  } finally { await browser.close(); server.close(); }
})().catch(e => { console.error(e); server.close(); process.exitCode = 1; });
