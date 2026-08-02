/**
 * 메인 페이지 인터랙션
 * - 배너 Swiper
 * - 해외동향 Swiper
 * - 통합검색
 * (퀵메뉴·COS BOT → float.js)
 */
const mainPage = {
  banner: null,
  trend: null,

  init() {
    this.initBanner();
    this.initTrend();
    this.initSearch();
  },

  /* ----- Banner Swiper ----- */
  initBanner() {
    const el = util.qs("#bannerSwiper");
    if (!el || typeof Swiper === "undefined") return;

    const current = util.qs(".banner-ctrl .current", el);
    const total = util.qs(".banner-ctrl .total", el);
    const playBtn = util.qs(".banner-ctrl .play-toggle", el);

    this.banner = new Swiper(el, {
      loop: true,
      autoplay: {
        delay: 4000,
        disableOnInteraction: false,
      },
      speed: 500,
      navigation: {
        nextEl: util.qs(".banner-next", el),
        prevEl: util.qs(".banner-prev", el),
      },
      on: {
        init(sw) {
          const realTotal = el.querySelectorAll(
            ".swiper-slide:not(.swiper-slide-duplicate)"
          ).length;
          if (total) total.textContent = String(realTotal || 1);
          if (current) current.textContent = String(sw.realIndex + 1);
        },
        slideChange(sw) {
          if (current) current.textContent = String(sw.realIndex + 1);
        },
      },
    });

    util.on(playBtn, "click", () => {
      if (!this.banner) return;
      const playing = playBtn.classList.contains("is-playing");
      if (playing) {
        this.banner.autoplay.stop();
        playBtn.classList.remove("is-playing");
        playBtn.setAttribute("aria-label", "자동재생 시작");
      } else {
        this.banner.autoplay.start();
        playBtn.classList.add("is-playing");
        playBtn.setAttribute("aria-label", "자동재생 일시정지");
      }
    });
  },

  /* ----- Trend Swiper ----- */
  initTrend() {
    const el = util.qs("#trendSwiper");
    if (!el || typeof Swiper === "undefined") return;

    this.trend = new Swiper(el, {
      slidesPerView: 1.2,
      spaceBetween: 16,
      speed: 450,
      watchOverflow: true,
      pagination: {
        el: util.qs(".trend-pagination", el),
        clickable: true,
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
    util.on(form, "submit", (e) => {
      e.preventDefault();
      const q = util.qs("input", form)?.value?.trim();
      if (!q) {
        util.qs("input", form)?.focus();
        return;
      }
      // 퍼블: 실제 검색 연동 전
      console.info("[search]", q);
    });
  },
};

document.addEventListener("DOMContentLoaded", () => {
  mainPage.init();
});
