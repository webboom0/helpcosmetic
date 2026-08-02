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

/** 접근성 헬퍼 */
const a11y = {
  FOCUSABLE:
    'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',

  getFocusable(root) {
    if (!root) return [];
    return util.qsa(this.FOCUSABLE, root).filter((el) => {
      if (el.hasAttribute("disabled")) return false;
      const style = window.getComputedStyle(el);
      if (style.visibility === "hidden" || style.display === "none") return false;
      return true;
    });
  },

  /** Tab 순환 포커스 트랩 */
  trapTab(e, root) {
    if (e.key !== "Tab" || !root) return;
    const list = this.getFocusable(root);
    if (!list.length) {
      e.preventDefault();
      return;
    }
    const first = list[0];
    const last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  },

  setBackgroundHidden(hidden) {
    util.qsa(".wrap, #quickFloat, #quickFloatToggle, #cosBot").forEach((el) => {
      if (!el) return;
      if (hidden) el.setAttribute("aria-hidden", "true");
      else el.removeAttribute("aria-hidden");
    });
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
    if (!util.qs(".gnb.is-open") && !util.qs(".cos-panel.is-open")) {
      util.lockScroll(false);
    }
  },
};
