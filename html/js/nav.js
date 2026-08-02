/**
 * GNB / 사이드메뉴 (바닐라 JS)
 * - PC: hover/focus 드롭다운
 * - <=1024: 사이드 패널 + 아코디언
 * - 포커스 트랩 / Esc / aria-expanded
 */
const nav = {
  bp: 1024,
  mode: "pc",
  gnb: null,
  openBtn: null,
  closeBtn: null,
  lastFocus: null,
  onKeydown: null,

  init() {
    this.gnb = util.qs("#gnb");
    this.openBtn = util.qs(".sideMenuBtn");
    this.closeBtn = util.qs(".sideMenuCloseBtn");
    if (!this.gnb) return;

    this.setMode();
    this.setupAccordionAria();
    this.bind();
    window.addEventListener("resize", debounce(() => this.onResize(), 120));
  },

  setMode() {
    this.mode = mq(`(max-width: ${this.bp}px)`).matches ? "mobile" : "pc";
  },

  onResize() {
    const prev = this.mode;
    this.setMode();
    if (prev !== this.mode) {
      this.close();
      this.resetAccordion();
    }
  },

  /** 하위메뉴 있는 1뎁스에 aria-expanded 초기화 */
  setupAccordionAria() {
    util.qsa(".depth-1", this.gnb).forEach((li) => {
      const link = li.querySelector(":scope > a");
      const sub = li.querySelector(".depth-2");
      const hasItems = sub && sub.querySelector("li");
      if (!link || !hasItems) return;
      link.setAttribute("aria-expanded", "false");
      if (!sub.id) {
        const slug = (link.textContent || "menu").trim().replace(/\s+/g, "-");
        sub.id = `gnb-sub-${slug}`;
      }
      link.setAttribute("aria-controls", sub.id);
    });
  },

  bind() {
    util.on(this.openBtn, "click", () => this.open());
    util.on(this.closeBtn, "click", () => this.close());

    util.qsa(".depth-1 > a", this.gnb).forEach((link) => {
      util.on(link, "click", (e) => {
        if (this.mode !== "mobile") return;
        const li = link.parentElement;
        const sub = li.querySelector(".depth-2");
        const hasItems = sub && sub.querySelector("li");
        if (!hasItems) return;

        e.preventDefault();
        const isOpen = li.classList.contains("is-open");
        this.resetAccordion();
        if (!isOpen) {
          li.classList.add("is-open");
          link.setAttribute("aria-expanded", "true");
        }
      });
    });

    this.onKeydown = (e) => {
      if (!this.gnb?.classList.contains("is-open")) return;
      if (e.key === "Escape") {
        e.preventDefault();
        this.close();
        return;
      }
      a11y.trapTab(e, this.gnb);
    };
    util.on(document, "keydown", this.onKeydown);
  },

  resetAccordion() {
    util.qsa(".depth-1.is-open", this.gnb).forEach((el) => {
      el.classList.remove("is-open");
      const link = el.querySelector(":scope > a");
      if (link?.hasAttribute("aria-expanded")) {
        link.setAttribute("aria-expanded", "false");
      }
    });
  },

  open() {
    if (!this.gnb) return;
    if (this.mode !== "mobile") return;
    this.lastFocus = document.activeElement;
    this.gnb.classList.add("is-open");
    if (this.openBtn) this.openBtn.setAttribute("aria-expanded", "true");
    dimmed.show();
    // 배경 숨김(스크린리더) — 메뉴는 wrap 안이므로 wrap은 유지, 본문만 가리기 어려움
    // 대신 메뉴에 포커스 이동
    requestAnimationFrame(() => {
      (this.closeBtn || a11y.getFocusable(this.gnb)[0])?.focus();
    });
  },

  close() {
    if (!this.gnb) return;
    const wasOpen = this.gnb.classList.contains("is-open");
    this.gnb.classList.remove("is-open");
    if (this.openBtn) this.openBtn.setAttribute("aria-expanded", "false");
    this.resetAccordion();
    dimmed.hide();
    if (wasOpen && this.lastFocus && typeof this.lastFocus.focus === "function") {
      this.lastFocus.focus();
      this.lastFocus = null;
    }
  },
};

document.addEventListener("DOMContentLoaded", () => {
  dimmed.init();
  nav.init();
});
