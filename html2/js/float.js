/**
 * 공통 플로팅 UI
 * - 우측 퀵메뉴 (포커스 트랩 / Esc / aria-expanded)
 * - COS BOT 패널 (다이얼로그: 포커스 트랩 / 복귀 / Esc)
 */
const floatUI = {
  lastFocus: null,
  qfLastFocus: null,
  onKeydown: null,

  init() {
    this.initAlertTooltip();
    this.initQuickFloat();
    this.initCosBot();
    this.initShare();
  },

  /** 알림 툴팁: 키보드 focus-within과 aria-expanded 동기화 */
  initAlertTooltip() {
    const wrap = util.qs(".alert-wrap");
    const btn = util.qs(".alert-btn");
    const tip = util.qs("#alertTooltip");
    if (!wrap || !btn || !tip) return;

    tip.setAttribute("aria-hidden", "true");

    const sync = () => {
      const show =
        wrap.matches(":hover") || wrap.contains(document.activeElement);
      btn.setAttribute("aria-expanded", show ? "true" : "false");
      tip.setAttribute("aria-hidden", show ? "false" : "true");
    };

    util.on(wrap, "mouseenter", sync);
    util.on(wrap, "mouseleave", sync);
    util.on(wrap, "focusin", sync);
    util.on(wrap, "focusout", () => setTimeout(sync, 0));
  },

  /** 공유 버튼 (서브/사이트맵) — alert 대신 aria-live 안내 */
  initShare() {
    const btn = util.qs("#btnShare");
    if (!btn) return;

    let live = util.qs("#a11yLive");
    if (!live) {
      live = document.createElement("div");
      live.id = "a11yLive";
      live.className = "blind";
      live.setAttribute("aria-live", "polite");
      live.setAttribute("aria-atomic", "true");
      document.body.appendChild(live);
    }

    util.on(btn, "click", async () => {
      const url = location.href;
      const title = document.title;
      try {
        if (navigator.share) {
          await navigator.share({ title, url });
          return;
        }
      } catch (_) {
        /* 사용자 취소 등 */
      }
      try {
        await navigator.clipboard.writeText(url);
        live.textContent = "";
        requestAnimationFrame(() => {
          live.textContent = "페이지 주소가 복사되었습니다.";
        });
      } catch (_) {
        live.textContent = "주소 복사에 실패했습니다.";
      }
    });
  },

  initQuickFloat() {
    const panel = util.qs("#quickFloat");
    const toggle = util.qs("#quickFloatToggle");
    if (!panel) return;

    const closeBtn = util.qs(".qf-close", panel);

    panel.classList.remove("is-open");
    panel.setAttribute("aria-hidden", "true");
    if (toggle) {
      toggle.classList.remove("is-hidden");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-controls", "quickFloat");
    }

    const close = () => {
      if (!panel.classList.contains("is-open")) return;
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      if (toggle) {
        toggle.classList.remove("is-hidden");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      } else if (this.qfLastFocus?.focus) {
        this.qfLastFocus.focus();
      }
      this.qfLastFocus = null;
    };

    const open = () => {
      this.qfLastFocus = document.activeElement;
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      if (toggle) {
        toggle.classList.add("is-hidden");
        toggle.setAttribute("aria-expanded", "true");
      }
      requestAnimationFrame(() => {
        (closeBtn || a11y.getFocusable(panel)[0])?.focus();
      });
    };

    util.on(closeBtn, "click", close);
    util.on(toggle, "click", open);

    util.on(document, "keydown", (e) => {
      if (!panel.classList.contains("is-open")) return;
      if (util.qs(".cos-panel.is-open")) return;
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      a11y.trapTab(e, panel);
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
      if (qf && !qf.classList.contains("is-open")) {
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
