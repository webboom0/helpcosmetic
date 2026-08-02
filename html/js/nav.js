/**
 * GNB / 사이드메뉴 (바닐라 JS)
 * - PC: hover/focus 드롭다운
 * - <=1024: 사이드 패널 + 아코디언
 */
const nav = {
  bp: 1024,
  mode: "pc",
  gnb: null,
  openBtn: null,
  closeBtn: null,

  init() {
    this.gnb = util.qs("#gnb");
    this.openBtn = util.qs(".sideMenuBtn");
    this.closeBtn = util.qs(".sideMenuCloseBtn");
    if (!this.gnb) return;

    this.setMode();
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

  bind() {
    util.on(this.openBtn, "click", () => this.open());
    util.on(this.closeBtn, "click", () => this.close());

    // 모바일 1뎁스 아코디언
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
        if (!isOpen) li.classList.add("is-open");
      });
    });

    // ESC
    util.on(document, "keydown", (e) => {
      if (e.key === "Escape") this.close();
    });
  },

  resetAccordion() {
    util.qsa(".depth-1.is-open", this.gnb).forEach((el) => {
      el.classList.remove("is-open");
    });
  },

  open() {
    if (!this.gnb) return;
    // PC에서는 가로 GNB 유지, 사이드 패널은 모바일/태블릿만
    if (this.mode !== "mobile") return;
    this.gnb.classList.add("is-open");
    if (this.openBtn) this.openBtn.setAttribute("aria-expanded", "true");
    dimmed.show();
  },

  close() {
    if (!this.gnb) return;
    this.gnb.classList.remove("is-open");
    if (this.openBtn) this.openBtn.setAttribute("aria-expanded", "false");
    this.resetAccordion();
    dimmed.hide();
  },
};

document.addEventListener("DOMContentLoaded", () => {
  dimmed.init();
  nav.init();
});
