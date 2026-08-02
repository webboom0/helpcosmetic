/**
 * 메인 페이지 인터랙션
 * - 배너 Swiper (자동재생 제어 + 상태 안내)
 * - 해외동향 Swiper
 * - 통합검색
 */
const mainPage = {
  banner: null,
  trend: null,

  init() {
    this.initBanner();
    this.initTrend();
    this.initSearch();
  },

  prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  },

  /* ----- Banner Swiper ----- */
  initBanner() {
    const el = util.qs("#bannerSwiper");
    if (!el || typeof Swiper === "undefined") return;

    const current = util.qs(".banner-ctrl .current", el);
    const total = util.qs(".banner-ctrl .total", el);
    const playBtn = util.qs(".banner-ctrl .play-toggle", el);
    const status = util.qs("#bannerStatus");
    const reduceMotion = this.prefersReducedMotion();

    const announce = (sw) => {
      const idx = sw.realIndex + 1;
      const tot =
        el.querySelectorAll(".swiper-slide:not(.swiper-slide-duplicate)")
          .length || 1;
      if (current) current.textContent = String(idx);
      if (total) total.textContent = String(tot);
      if (status) {
        status.textContent = `배너 ${idx} / ${tot}`;
      }
    };

    this.banner = new Swiper(el, {
      loop: true,
      autoplay: reduceMotion
        ? false
        : {
            delay: 4000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
          },
      speed: reduceMotion ? 0 : 500,
      a11y: {
        enabled: true,
        prevSlideMessage: "이전 배너",
        nextSlideMessage: "다음 배너",
      },
      navigation: {
        nextEl: util.qs(".banner-next", el),
        prevEl: util.qs(".banner-prev", el),
      },
      on: {
        init(sw) {
          announce(sw);
        },
        slideChange(sw) {
          announce(sw);
        },
      },
    });

    if (reduceMotion && playBtn) {
      playBtn.classList.remove("is-playing");
      playBtn.setAttribute("aria-label", "자동재생 시작");
      playBtn.setAttribute("aria-pressed", "false");
    } else if (playBtn) {
      playBtn.setAttribute("aria-pressed", "true");
    }

    util.on(playBtn, "click", () => {
      if (!this.banner) return;
      const playing = playBtn.classList.contains("is-playing");
      if (playing) {
        this.banner.autoplay?.stop?.();
        playBtn.classList.remove("is-playing");
        playBtn.setAttribute("aria-label", "자동재생 시작");
        playBtn.setAttribute("aria-pressed", "false");
      } else {
        if (!this.banner.params.autoplay) {
          this.banner.params.autoplay = {
            delay: 4000,
            disableOnInteraction: false,
          };
          this.banner.autoplay.start();
        } else {
          this.banner.autoplay.start();
        }
        playBtn.classList.add("is-playing");
        playBtn.setAttribute("aria-label", "자동재생 일시정지");
        playBtn.setAttribute("aria-pressed", "true");
      }
    });
  },

  /* ----- Trend Swiper ----- */
  initTrend() {
    const el = util.qs("#trendSwiper");
    if (!el || typeof Swiper === "undefined") return;

    const reduceMotion = this.prefersReducedMotion();

    this.trend = new Swiper(el, {
      slidesPerView: 1.2,
      spaceBetween: 16,
      speed: reduceMotion ? 0 : 450,
      watchOverflow: true,
      a11y: { enabled: true },
      pagination: {
        el: util.qs(".trend-pagination", el),
        clickable: true,
        renderBullet(index, className) {
          return `<button type="button" class="${className}" aria-label="해외동향정보지 ${index + 1}번째 슬라이드"></button>`;
        },
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 18,
        },
        1025: {
          slidesPerView: 4,
          spaceBetween: 18,
        },
      },
    });
  },

  /* ----- Search ----- */
  initSearch() {
    const form = util.qs(".hero-search-form");
    if (!form) return;
    const err = util.qs("#searchError");
    util.on(form, "submit", (e) => {
      e.preventDefault();
      const input = util.qs("input", form);
      const q = input?.value?.trim();
      if (!q) {
        input?.focus();
        if (err) {
          err.textContent = "검색어를 입력해 주세요.";
          input?.setAttribute("aria-invalid", "true");
          input?.setAttribute("aria-describedby", "searchError");
        }
        return;
      }
      if (err) err.textContent = "";
      input?.removeAttribute("aria-invalid");
      // 퍼블: 실제 검색 연동 전
      console.info("[search]", q);
    });
  },
};

document.addEventListener("DOMContentLoaded", () => {
  mainPage.init();
});
