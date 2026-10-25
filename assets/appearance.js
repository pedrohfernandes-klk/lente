/* Fundação experimental de aparência. Sem integração automática nas páginas reais. */
(function (win, doc) {
  'use strict';
  if (win.EPIAppearance) return;
  var KEY = 'epi-theme', CHANNEL = 'epi-appearance', VERSION = 1;
  var media = win.matchMedia ? win.matchMedia('(prefers-color-scheme: dark)') : null;
  var manual = null, button = null;
  var origin = win.location.origin;
  var canMessage = /^https?:\/\//.test(origin);
  var framed = win.self !== win.top;

  function valid(value) { return value === 'light' || value === 'dark'; }
  function stored() {
    try { var value = win.localStorage.getItem(KEY); return valid(value) ? value : null; }
    catch (error) { return null; }
  }
  manual = stored();
  function current() { return manual || (media && media.matches ? 'dark' : 'light'); }
  function payload(action) {
    return {type: CHANNEL, version: VERSION, action: action, theme: current(), preference: manual};
  }
  function send(target, message) {
    if (!canMessage || !target) return;
    try { target.postMessage(message, origin); } catch (error) { /* A frame may have navigated. */ }
  }
  function frames() { return Array.prototype.slice.call(doc.querySelectorAll('iframe')); }
  function broadcast() {
    frames().forEach(function (frame) { send(frame.contentWindow, payload('state')); });
  }
  function requestParent() { if (framed) send(win.parent, payload('request')); }
  function render() {
    var theme = current();
    doc.documentElement.setAttribute('data-theme', theme);
    if (button) {
      button.setAttribute('aria-pressed', String(theme === 'dark'));
      button.title = theme === 'dark' ? 'Desativar modo noturno' : 'Ativar modo noturno';
    }
  }
  function apply() { render(); broadcast(); }
  function choose(value) {
    manual = value;
    try {
      if (value === null) win.localStorage.removeItem(KEY);
      else win.localStorage.setItem(KEY, value);
    } catch (error) { /* The choice remains in memory for this page. */ }
    apply();
  }
  function mount(root) {
    if (framed) return null;
    root = root || doc;
    var slot = root.matches && root.matches('[data-appearance-control]') ? root : root.querySelector('[data-appearance-control]');
    if (!slot) return null;
    if (!button) {
      button = doc.createElement('button');
      button.type = 'button';
      button.className = 'epi-appearance-toggle';
      button.setAttribute('aria-label', 'Modo noturno');
      button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20 15.1A8.5 8.5 0 0 1 8.9 4 8.5 8.5 0 1 0 20 15.1Z"/></svg>';
      button.addEventListener('click', function () { choose(current() === 'dark' ? 'light' : 'dark'); });
    }
    if (button.parentNode !== slot) slot.appendChild(button);
    render();
    return button;
  }

  win.addEventListener('storage', function (event) {
    if (event.key !== KEY && event.key !== null) return;
    try { if (event.storageArea && event.storageArea !== win.localStorage) return; }
    catch (error) { /* A blocked storage object cannot be compared. */ }
    manual = valid(event.newValue) ? event.newValue : null;
    apply();
  });
  if (media) {
    var systemChanged = function () { if (manual === null) apply(); };
    if (media.addEventListener) media.addEventListener('change', systemChanged);
    else if (media.addListener) media.addListener(systemChanged);
  }
  win.addEventListener('message', function (event) {
    if (!canMessage || event.origin !== origin) return;
    var data = event.data;
    if (!data || typeof data !== 'object' || data.type !== CHANNEL || data.version !== VERSION) return;
    if (data.action === 'request') {
      var ownFrame = frames().some(function (frame) { return frame.contentWindow === event.source; });
      if (ownFrame) send(event.source, payload('state'));
      return;
    }
    if (data.action !== 'state' || !framed || event.source !== win.parent || !valid(data.theme)) return;
    if (data.preference !== null && !valid(data.preference)) return;
    /* An automatic parent must agree with this origin's system preference. */
    if (data.preference !== null && data.preference !== data.theme) return;
    if (data.preference === null && data.theme !== (media && media.matches ? 'dark' : 'light')) return;
    manual = data.preference;
    apply();
  });
  function ready() { mount(); apply(); requestParent(); }
  doc.addEventListener('load', function (event) {
    if (event.target && event.target.tagName === 'IFRAME') send(event.target.contentWindow, payload('state'));
  }, true);
  win.addEventListener('load', function () { apply(); requestParent(); });
  win.EPIAppearance = Object.freeze({mount: mount, reset: function () { choose(null); }, current: current});
  render();
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', ready, {once: true});
  else ready();
}(window, document));
