/**
 * 공통 플로팅 UI
 * - 우측 퀵메뉴
 * - COS BOT 패널
 */
const floatUI = {
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
      if (toggle) toggle.classList.add("is-visible");
    });

    util.on(toggle, "click", () => {
      panel.classList.remove("is-collapsed");
      toggle.classList.remove("is-visible");
    });
  },

  initCosBot() {
    const bot = util.qs("#cosBot");
    const panel = util.qs("#cosPanel");
    if (!bot || !panel) return;

    const closeBtn = util.qs(".cos-panel-close", panel);
    const openers = util.qsa("[data-open-bot]");

    const open = () => {
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      bot.setAttribute("aria-expanded", "true");
    };

    const close = () => {
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      bot.setAttribute("aria-expanded", "false");
    };

    const toggle = () => {
      if (panel.classList.contains("is-open")) close();
      else open();
    };

    util.on(bot, "click", toggle);
    util.on(closeBtn, "click", close);
    openers.forEach((el) => util.on(el, "click", open));

    util.on(document, "keydown", (e) => {
      if (e.key === "Escape" && panel.classList.contains("is-open")) close();
    });
  },
};

document.addEventListener("DOMContentLoaded", () => {
  floatUI.init();
});
