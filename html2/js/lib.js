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

/**
 * 수출절차: 탭 가로 스크롤(PC 휠·드래그) + 세로카드 시 th 타이틀 한 줄
 */
const lawExportUI = {
  stackMq: "(max-width: 1024px)",

  init() {
    if (!util.qs(".law-export")) return;
    this.initTabScroll();
    this.syncRowHeadBreaks();
    window.addEventListener(
      "resize",
      debounce(() => this.syncRowHeadBreaks(), 120)
    );
  },

  initTabScroll() {
    util.qsa(".law-country-tabs, .law-step-nav").forEach((el) => {
      util.on(
        el,
        "wheel",
        (e) => {
          if (el.scrollWidth <= el.clientWidth + 1) return;
          const mostlyVertical = Math.abs(e.deltaY) >= Math.abs(e.deltaX);
          if (!mostlyVertical) return;
          el.scrollLeft += e.deltaY;
          e.preventDefault();
        },
        { passive: false }
      );

      // 클릭과 드래그 구분: 임계값 넘기기 전에는 링크 클릭을 막지 않음
      let tracking = false;
      let dragging = false;
      let startX = 0;
      let startScroll = 0;
      let pointerId = null;

      util.on(el, "pointerdown", (e) => {
        if (e.pointerType === "touch") return; // 터치는 네이티브 가로 스크롤
        if (e.button != null && e.button !== 0) return;
        if (el.scrollWidth <= el.clientWidth + 1) return;
        tracking = true;
        dragging = false;
        startX = e.clientX;
        startScroll = el.scrollLeft;
        pointerId = e.pointerId;
      });

      util.on(el, "pointermove", (e) => {
        if (!tracking) return;
        const dx = e.clientX - startX;
        if (!dragging) {
          if (Math.abs(dx) < 6) return;
          dragging = true;
          el.classList.add("is-dragging");
          try {
            el.setPointerCapture(pointerId);
          } catch (_) {
            /* ignore */
          }
        }
        el.scrollLeft = startScroll - dx;
      });

      const endDrag = (e) => {
        if (!tracking) return;
        const wasDragging = dragging;
        tracking = false;
        dragging = false;
        el.classList.remove("is-dragging");
        if (pointerId != null) {
          try {
            el.releasePointerCapture(pointerId);
          } catch (_) {
            /* ignore */
          }
        }
        pointerId = null;
        // 실제 드래그한 경우에만 이어지는 click 차단
        if (wasDragging) {
          const blockClick = (ev) => {
            ev.preventDefault();
            ev.stopPropagation();
            el.removeEventListener("click", blockClick, true);
          };
          el.addEventListener("click", blockClick, true);
        }
      };

      util.on(el, "pointerup", endDrag);
      util.on(el, "pointercancel", endDrag);
    });
  },

  syncRowHeadBreaks() {
    const stacked = mq(this.stackMq).matches;
    util.qsa(".law-export .law-table th.row-head").forEach((th) => {
      if (!th.dataset.rawHtml) th.dataset.rawHtml = th.innerHTML;
      th.innerHTML = stacked
        ? th.dataset.rawHtml.replace(/<br\s*\/?>/gi, " ")
        : th.dataset.rawHtml;
    });
  },
};

document.addEventListener("DOMContentLoaded", () => {
  lawExportUI.init();
});
