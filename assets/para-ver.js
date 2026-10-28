/* «Para ver» (28/10/2026). O leitor só nasce ao toque (youtube-nocookie, com legendas ligadas).
   Num cartão com várias opções, cada botão troca o vídeo e as perguntas. O motor dos cartões guarda
   cópias para rever: uma cópia com o leitor volta a ser o botão, e os botões voltam a funcionar. */
(function () {
  "use strict";
  var vivos = typeof WeakSet === "function" ? new WeakSet() : null;
  var ID = /^[A-Za-z0-9_-]{11}$/;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function botao(c) {
    var d = c.dataset;
    c.classList.remove("tocado");
    c.innerHTML = '<p class="pv-t" lang="en">' + esc(d.t) + '</p><p class="pv-m">' + esc(d.m) + '</p><button type="button">Ver o vídeo <span>(' + esc(d.dur) + ')</span></button>';
  }
  function arrumar() {
    [].forEach.call(document.querySelectorAll(".pv-video"), function (c) {
      var f = c.querySelector("iframe");
      if (f && !(vivos && vivos.has(f))) botao(c);
    });
    [].forEach.call(document.querySelectorAll(".pv button[disabled]"), function (b) { b.disabled = false; b.removeAttribute("tabindex"); });
  }
  function tocar(c) {
    var d = c.dataset;
    if (!ID.test(d.yt || "")) return;
    [].forEach.call(document.querySelectorAll(".pv-video.tocado"), function (o) { if (o !== c) botao(o); });
    var f = document.createElement("iframe");
    f.src = "https://www.youtube-nocookie.com/embed/" + d.yt + "?autoplay=1&rel=0&cc_load_policy=1&cc_lang_pref=pt&hl=pt-PT" + (d.ini ? "&start=" + d.ini : "") + (d.fim ? "&end=" + d.fim : "");
    f.title = d.titulo || d.t || "Vídeo";
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.setAttribute("allowfullscreen", "");
    f.referrerPolicy = "strict-origin-when-cross-origin";
    if (vivos) vivos.add(f);
    c.innerHTML = "";
    c.classList.add("tocado");
    c.appendChild(f);
    try { f.focus(); } catch (x) {}
  }
  function escolher(b) {
    var pv = b.closest(".pv"), c = pv && pv.querySelector(".pv-video");
    if (!c) return;
    [].forEach.call(pv.querySelectorAll(".pv-opcoes button"), function (o) { o.setAttribute("aria-pressed", String(o === b)); });
    ["yt", "dur", "t", "m", "titulo"].forEach(function (k) { if (b.dataset[k] != null) c.dataset[k] = b.dataset[k]; });
    var a = pv.querySelector(".pv-antes span"), d = pv.querySelector(".pv-depois span"), l = pv.querySelector(".pv-yt a");
    if (a && b.dataset.antes) a.textContent = b.dataset.antes;
    if (d && b.dataset.depois) d.textContent = b.dataset.depois;
    if (l && ID.test(b.dataset.yt || "")) l.href = "https://www.youtube.com/watch?v=" + b.dataset.yt;
    botao(c);
  }
  document.addEventListener("click", function (ev) {
    var t = ev.target;
    if (!t.closest) return;
    var b = t.closest(".pv-video button");
    if (b) { tocar(b.closest(".pv-video")); return; }
    var o = t.closest(".pv-opcoes button");
    if (o) escolher(o);
  });
  function vigiar() {
    var alvo = document.getElementById("baralho");
    if (alvo && window.MutationObserver) new MutationObserver(arrumar).observe(alvo, { childList: true, subtree: true });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", vigiar); else vigiar();
})();
