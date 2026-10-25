'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/appearance.js'), 'utf8');

function events(object) {
  const listeners = new Map();
  object.addEventListener = (type, fn) => {
    if (!listeners.has(type)) listeners.set(type, []);
    listeners.get(type).push(fn);
  };
  object.emit = (type, event = {}) => {
    for (const fn of [...(listeners.get(type) || [])]) fn(event);
  };
  object.listenerCount = type => (listeners.get(type) || []).length;
  return object;
}
class Element {
  constructor(tag = 'DIV') {
    this.tagName = tag.toUpperCase(); this.attributes = {}; this.children = []; this.parentNode = null;
    events(this);
  }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  getAttribute(key) { return this.attributes[key] ?? null; }
  matches(selector) { return selector === '[data-appearance-control]' && this.attributes['data-appearance-control'] !== undefined; }
  querySelector(selector) { return this.children.find(child => child.matches(selector)) || null; }
  appendChild(element) {
    if (element.parentNode) element.parentNode.children.splice(element.parentNode.children.indexOf(element), 1);
    element.parentNode = this; this.children.push(element); return element;
  }
}
function store(initial = {}, blocked = false) {
  const data = new Map(Object.entries(initial));
  const writes = [];
  return {
    data, writes,
    getItem(key) { if (blocked) throw Error('blocked'); return data.get(key) ?? null; },
    setItem(key, value) { if (blocked) throw Error('blocked'); writes.push(['set', key, value]); data.set(key, value); },
    removeItem(key) { if (blocked) throw Error('blocked'); writes.push(['remove', key]); data.delete(key); }
  };
}
function realm(options = {}) {
  const storage = options.storage || store(options.initial, options.blocked);
  const media = events({matches: !!options.dark});
  const documentElement = new Element('HTML');
  const slot = options.slot === false ? null : new Element();
  if (slot) slot.setAttribute('data-appearance-control', '');
  const document = events({documentElement, readyState: options.loading ? 'loading' : 'complete', frames: []});
  document.createElement = tag => new Element(tag);
  document.querySelector = selector => selector === '[data-appearance-control]' ? slot : null;
  document.querySelectorAll = selector => selector === 'iframe' ? document.frames : [];
  const win = events({location: {origin: options.origin || 'https://example.test'}, localStorage: storage, matchMedia: () => media});
  win.self = win; win.top = win; win.parent = win;
  const r = {win, document, slot, storage, media};
  r.start = () => { vm.runInNewContext(source, {window: win, document}, {filename: 'appearance.js'}); return r; };
  r.theme = () => documentElement.getAttribute('data-theme');
  r.button = () => slot && slot.children[0];
  r.click = () => { assert.ok(r.button(), 'explicit control must exist'); r.button().emit('click'); };
  r.system = dark => { media.matches = dark; media.emit('change'); };
  return r;
}
function connect(parent, child) {
  const traffic = [];
  let frameProxy, parentProxy;
  frameProxy = {postMessage(data, targetOrigin) {
    traffic.push({to: 'child', data, targetOrigin});
    child.win.emit('message', {origin: parent.win.location.origin, source: parentProxy, data});
  }};
  parentProxy = {postMessage(data, targetOrigin) {
    traffic.push({to: 'parent', data, targetOrigin});
    parent.win.emit('message', {origin: child.win.location.origin, source: frameProxy, data});
  }};
  child.win.top = parentProxy; child.win.parent = parentProxy;
  const frame = {tagName: 'IFRAME', contentWindow: frameProxy};
  parent.document.frames.push(frame);
  return {traffic, frame, frameProxy, parentProxy};
}
const state = (theme, preference = theme) => ({type: 'epi-appearance', version: 1, action: 'state', theme, preference});
const request = () => ({type: 'epi-appearance', version: 1, action: 'request'});

test('system default changes until a manual choice; reset touches only appearance key', () => {
  const r = realm({initial: {'epi-progress': 'preserve'}}).start();
  assert.equal(r.theme(), 'light');
  r.system(true); assert.equal(r.theme(), 'dark');
  r.click(); assert.equal(r.theme(), 'light'); assert.equal(r.storage.data.get('epi-theme'), 'light');
  assert.equal(r.button().getAttribute('aria-label'), 'Modo noturno');
  assert.equal(r.button().getAttribute('aria-pressed'), 'false');
  r.system(false); r.system(true); assert.equal(r.theme(), 'light');
  r.win.EPIAppearance.reset(); assert.equal(r.theme(), 'dark');
  assert.equal(r.storage.data.get('epi-progress'), 'preserve');
  assert.deepEqual(r.storage.writes.map(x => x[1]), ['epi-theme', 'epi-theme']);
});

test('manual choice survives a fresh document and does not follow system changes', () => {
  const s = store(); const first = realm({storage: s}).start(); first.click();
  const next = realm({storage: s}).start();
  assert.equal(next.theme(), 'dark'); assert.equal(next.win.EPIAppearance.current(), 'dark');
  next.system(true); next.system(false); assert.equal(next.theme(), 'dark');
  assert.equal(next.button().getAttribute('aria-pressed'), 'true');
  assert.equal(next.button().title, 'Desativar modo noturno');
});

test('blocked storage degrades to a manual in-memory preference without throwing', () => {
  const r = realm({blocked: true, dark: true}).start();
  r.click(); assert.equal(r.theme(), 'light');
  r.system(false); r.system(true); assert.equal(r.theme(), 'light');
  r.win.EPIAppearance.reset(); assert.equal(r.theme(), 'dark');
  const other = realm({blocked: true, dark: true}).start(); assert.equal(other.theme(), 'dark');
});

test('invalid stored preference is ignored without rewriting it', () => {
  for (const value of ['system', 'auto', 'DARK', '', '{"theme":"dark"}']) {
    const r = realm({initial: {'epi-theme': value}, dark: true}).start();
    assert.equal(r.theme(), 'dark'); assert.equal(r.storage.writes.length, 0);
    r.system(false); assert.equal(r.theme(), 'light');
  }
});

test('storage synchronization accepts only the preference key and local storage area', () => {
  const r = realm().start();
  r.win.emit('storage', {key: 'epi-progress', newValue: 'dark', storageArea: r.storage});
  assert.equal(r.theme(), 'light');
  r.win.emit('storage', {key: 'epi-theme', newValue: 'dark', storageArea: {}});
  assert.equal(r.theme(), 'light');
  r.win.emit('storage', {key: 'epi-theme', newValue: 'dark', storageArea: r.storage});
  assert.equal(r.theme(), 'dark');
  r.win.emit('storage', {key: 'epi-theme', newValue: 'invalid', storageArea: r.storage});
  assert.equal(r.theme(), 'light');
  r.win.emit('storage', {key: null, newValue: null, storageArea: r.storage});
  assert.equal(r.theme(), 'light'); assert.equal(r.storage.writes.length, 0);
});

test('explicit slots only; repeated mounting or script loading never duplicates control', () => {
  const absent = realm({slot: false}).start();
  assert.equal(absent.win.EPIAppearance.mount(), null);
  const r = realm({loading: true}).start(); assert.equal(r.slot.children.length, 0);
  r.document.emit('DOMContentLoaded'); const button = r.button();
  assert.equal(r.win.EPIAppearance.mount(), button); assert.equal(r.win.EPIAppearance.mount(r.slot), button);
  r.start(); assert.equal(r.slot.children.length, 1); assert.equal(r.win.listenerCount('storage'), 1);
  const anotherSlot = new Element(); anotherSlot.setAttribute('data-appearance-control', '');
  r.win.EPIAppearance.mount(anotherSlot); assert.equal(r.slot.children.length, 0);
  assert.equal(anotherSlot.children.length, 1); assert.equal(button.listenerCount('click'), 1);
});

test('same-origin child obtains parent preference on initial handshake and on load', () => {
  const parent = realm({initial: {'epi-theme': 'dark'}});
  const child = realm({blocked: true});
  const link = connect(parent, child);
  parent.start(); child.start();
  assert.equal(child.theme(), 'dark'); assert.equal(child.slot.children.length, 0);
  assert.equal(child.win.EPIAppearance.mount(), null);
  parent.click(); assert.equal(child.theme(), 'light');
  parent.click(); assert.equal(child.theme(), 'dark');
  parent.document.emit('load', {target: link.frame}); child.win.emit('load');
  assert.equal(child.theme(), 'dark');
  assert.ok(link.traffic.length >= 5);
  assert.ok(link.traffic.every(message => message.targetOrigin === 'https://example.test'));
  assert.equal(child.storage.writes.length, 0);
});

test('messages validate origin, parent emitter, version, state and direct-child requests', () => {
  const parent = realm().start(); const child = realm(); const link = connect(parent, child); child.start();
  const send = (data, origin = 'https://example.test', source = link.parentProxy) => child.win.emit('message', {data, origin, source});
  send(state('dark'), 'https://evil.test'); assert.equal(child.theme(), 'light');
  send(state('dark'), undefined, {}); assert.equal(child.theme(), 'light');
  send({...state('dark'), version: 2}); assert.equal(child.theme(), 'light');
  send({...state('dark'), type: 'other'}); assert.equal(child.theme(), 'light');
  send(state('dark', 'auto')); assert.equal(child.theme(), 'light');
  send(state('dark', 'light')); assert.equal(child.theme(), 'light');
  send(state('dark', null)); assert.equal(child.theme(), 'light');
  send(state('dark')); assert.equal(child.theme(), 'dark');
  const before = link.traffic.length;
  parent.win.emit('message', {data: request(), origin: 'https://example.test', source: {}});
  parent.win.emit('message', {data: request(), origin: 'https://evil.test', source: link.frameProxy});
  parent.win.emit('message', {data: state('dark'), origin: 'https://example.test', source: link.frameProxy});
  assert.equal(link.traffic.length, before); assert.equal(parent.theme(), 'light');
});

test('no messaging on opaque file origin and no fallback control in an iframe', () => {
  const parent = realm({origin: 'null'}); const child = realm({origin: 'null'}); const link = connect(parent, child);
  parent.start(); child.start(); parent.click(); child.win.emit('load');
  assert.equal(link.traffic.length, 0); assert.equal(child.slot.children.length, 0);
});

test('late parent initialization and iframe insertion synchronize without a timer', () => {
  const parent = realm({initial: {'epi-theme': 'dark'}});
  const earlyChild = realm({blocked: true}); const earlyLink = connect(parent, earlyChild);
  earlyChild.start(); assert.equal(earlyChild.theme(), 'light');
  parent.start(); assert.equal(earlyChild.theme(), 'dark');
  const lateChild = realm({blocked: true, loading: true});
  const lateLink = connect(parent, lateChild); lateChild.start();
  assert.equal(lateChild.theme(), 'light');
  parent.document.emit('load', {target: lateLink.frame}); assert.equal(lateChild.theme(), 'dark');
  lateChild.document.emit('DOMContentLoaded'); assert.equal(lateChild.theme(), 'dark');
  assert.ok([...earlyLink.traffic, ...lateLink.traffic].every(message => message.targetOrigin !== '*'));
});

test('a throwing localStorage property and legacy media listener remain usable', () => {
  const r = realm({dark: true});
  Object.defineProperty(r.win, 'localStorage', {get() { throw Error('SecurityError'); }});
  const handlers = [];
  r.media.addEventListener = undefined; r.media.addListener = fn => handlers.push(fn);
  r.start(); assert.equal(r.theme(), 'dark');
  r.click(); assert.equal(r.theme(), 'light');
  r.media.matches = false; handlers[0](); r.media.matches = true; handlers[0]();
  assert.equal(r.theme(), 'light');
  r.win.EPIAppearance.reset(); assert.equal(r.theme(), 'dark');
});

test('CSS uses exact Cartaz tokens, body-specific PT overrides and clear print palette', () => {
  const css = fs.readFileSync(path.join(__dirname, '../assets/appearance.css'), 'utf8');
  for (const token of ['--tinta:#ecebe5', '--papel:#121210', '--fundo:#1d1d1a', '--suave:#b3b1aa', '--mostarda:#e0b23a', '--vermelho:#e4555c', '--cinza:#3d3c38', '--campo:#9a7a22']) assert.ok(css.includes(token));
  assert.match(css, /:root\[data-theme="dark"\] body\[data-sitio="pt"\]\{--acento:#e0876f;--campo:#b86a54\}/);
  assert.match(css, /:root\[data-theme="light"\] body\[data-sitio="pt"\]\{--acento:#a84939;--campo:#e8967a\}/);
  assert.match(css, /@media print\{[\s\S]*:root\[data-theme\]\{--tinta:#000;--papel:#fff/);
  assert.match(css, /width:44px;height:44px;min-width:44px;min-height:44px/);
  assert.match(css, /:focus-visible\{outline:3px solid var\(--tinta\)/);
});
