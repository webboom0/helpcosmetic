/**
 * 공통 플로팅 UI
 * - 우측 퀵메뉴
 * - COS BOT 패널 (다이얼로그: 포커스 트랩 / 복귀 / Esc)
 */
const floatUI = {
  lastFocus: null,
  onKeydown: null,

  init() {
    this.initQuickFloat();
    this.initCosBot();
  },

  initQuickFloat() {
    const panel = util.qs("#quickFloat");
    const toggle = util.qs("#quickFloatToggle");
    if (!panel) return;

    const closeBtn = util.qs(".qf-close", panel);

    util.on(closeBtn, "click", () => {
      panel.classList.add("is-collapsed");
      panel.setAttribute("aria-hidden", "true");
      if (toggle) {
        toggle.classList.add("is-visible");
        toggle.focus();
      }
    });

    util.on(toggle, "click", () => {
      panel.classList.remove("is-collapsed");
      panel.removeAttribute("aria-hidden");
      toggle.classList.remove("is-visible");
      closeBtn?.focus();
    });
  },

  initCosBot() {
    const bot = util.qs("#cosBot");
    const panel = util.qs("#cosPanel");
    if (!bot || !panel) return;

    const closeBtn = util.qs(".cos-panel-close", panel);
    const openers = util.qsa("[data-open-bot]");

    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-modal", "true");
    if (!panel.getAttribute("aria-labelledby")) {
      panel.setAttribute("aria-labelledby", "cosPanelTit");
    }

    const open = (fromEl) => {
      this.lastFocus = fromEl || document.activeElement;
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      bot.setAttribute("aria-expanded", "true");
      a11y.setBackgroundHidden(true);
      util.lockScroll(true);
      requestAnimationFrame(() => {
        (closeBtn || a11y.getFocusable(panel)[0])?.focus();
      });
    };

    const close = () => {
      if (!panel.classList.contains("is-open")) return;
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      bot.setAttribute("aria-expanded", "false");
      a11y.setBackgroundHidden(false);
      const qf = util.qs("#quickFloat");
      if (qf?.classList.contains("is-collapsed")) {
        qf.setAttribute("aria-hidden", "true");
      }
      if (!util.qs(".gnb.is-open")) util.lockScroll(false);
      if (this.lastFocus && typeof this.lastFocus.focus === "function") {
        this.lastFocus.focus();
      } else {
        bot.focus();
      }
      this.lastFocus = null;
    };

    const toggle = () => {
      if (panel.classList.contains("is-open")) close();
      else open(bot);
    };

    util.on(bot, "click", toggle);
    util.on(closeBtn, "click", close);
    openers.forEach((el) =>
      util.on(el, "click", () => {
        open(el);
      })
    );

    this.onKeydown = (e) => {
      if (!panel.classList.contains("is-open")) return;
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      a11y.trapTab(e, panel);
    };
    util.on(document, "keydown", this.onKeydown);
  },
};

document.addEventListener("DOMContentLoaded", () => {
  floatUI.init();
});
