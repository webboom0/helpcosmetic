/**
 * 공통 유틸 (바닐라 JS)
 */
const util = {
  qs(sel, ctx = document) {
    return ctx.querySelector(sel);
  },
  qsa(sel, ctx = document) {
    return Array.from(ctx.querySelectorAll(sel));
  },
  on(el, type, handler, opts) {
    if (!el) return;
    el.addEventListener(type, handler, opts);
  },
  lockScroll(lock) {
    document.body.classList.toggle("is-locked", !!lock);
  },
};

/** 상단 이동 */
function moveTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/** matchMedia 헬퍼 */
function mq(query) {
  return window.matchMedia(query);
}

/** debounce */
function debounce(fn, wait = 150) {
  let t;
  return function (...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), wait);
  };
}

/** 딤드 오버레이 */
const dimmed = {
  el: null,
  init() {
    this.el = util.qs("#dimmed");
    if (!this.el) return;
    util.on(this.el, "click", () => {
      if (typeof nav !== "undefined") nav.close();
    });
  },
  show() {
    if (!this.el) return;
    this.el.classList.add("is-active");
    this.el.setAttribute("aria-hidden", "false");
    util.lockScroll(true);
  },
  hide() {
    if (!this.el) return;
    this.el.classList.remove("is-active");
    this.el.setAttribute("aria-hidden", "true");
    if (!util.qs(".gnb.is-open")) util.lockScroll(false);
  },
};
