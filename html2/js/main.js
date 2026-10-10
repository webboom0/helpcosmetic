/**
 * html2 main — live-design1 스냅/캐러셀/글로브
 * PC(≥1101): 풀페이지 스냅
 * ≤1100: 일반 스크롤 (스냅·휠 가로채기 없음)
 */
(() => {
  "use strict";

  const BP = 1100;
  const mq = window.matchMedia(`(max-width: ${BP}px)`);
  const isMobile = () => mq.matches;

  const track = document.getElementById("hc-track");
  const header = document.getElementById("hc-header");
  const navi = document.getElementById("hc-navi");
  const quick = document.getElementById("hc-quick");
  const fixed = document.getElementById("hc-fixed");
  const spacer = document.getElementById("hc-spacer");
  const sections = Array.from(document.querySelectorAll(".hc-section"));
  const naviBtns = navi ? Array.from(navi.querySelectorAll("button")) : [];
  const sectionCount = sections.length;

  if (!track || !sections.length) return;

  const TRANS = 850;
  const WHEEL_GAP = 150;

  let index = 0;
  let mode = "locked"; // locked | free
  let animating = false;
  let lastWheelAt = 0;
  let lastWheelDir = 0;
  let wheelLocked = false;
  let queuedDir = null;
  let enterTimer = null;
  let snapEnabled = !isMobile();

  function applyTheme(i) {
    const theme = sections[i]?.dataset.theme || "dark";
    [header, navi, quick].forEach((el) => {
      if (!el) return;
      el.classList.toggle("theme-dark", theme === "dark");
      el.classList.toggle("theme-light", theme === "light");
    });
    naviBtns.forEach((btn, n) => {
      const on = n === i;
      btn.classList.toggle("active", on);
      if (on) btn.setAttribute("aria-current", "true");
      else btn.removeAttribute("aria-current");
    });
  }

  /** 활성 섹션만 Tab 진입 가능 — 화면 밖 섹션으로 포커스가 새는 것 방지 */
  function syncSectionInert(activeIdx) {
    sections.forEach((sec, n) => {
      if (n === activeIdx) {
        sec.removeAttribute("inert");
        sec.removeAttribute("aria-hidden");
      } else {
        sec.setAttribute("inert", "");
        sec.setAttribute("aria-hidden", "true");
      }
    });
    // 휠로 섹션 이동 시 이전 섹션에 포커스가 남으면 제거
    const active = document.activeElement;
    if (
      active instanceof Element &&
      active.closest?.(".hc-section[inert], .hc-section[aria-hidden='true']")
    ) {
      active.blur();
    }
  }

  function clearSectionInert() {
    sections.forEach((sec) => {
      sec.removeAttribute("inert");
      sec.removeAttribute("aria-hidden");
    });
  }

  function focusSectionEdge(i, edge) {
    const list = typeof a11y !== "undefined" ? a11y.getFocusable(sections[i]) : [];
    const el = edge === "last" ? list[list.length - 1] : list[0];
    el?.focus({ preventScroll: true });
  }

  function enterSection(i) {
    sections.forEach((sec, n) => {
      if (n === i) {
        sec.classList.remove("in-view");
        void sec.offsetWidth;
        sec.classList.add("in-view");
      } else {
        sec.classList.remove("in-view");
      }
    });
    syncSectionInert(i);
    document.dispatchEvent(new CustomEvent("hc:section", { detail: i }));
  }

  function goSnap(to, { immediateEnter = false } = {}) {
    index = Math.max(0, Math.min(sectionCount - 1, to));
    track.style.transform = `translateY(-${index * 100}vh)`;
    applyTheme(index);
    syncSectionInert(index);
    clearTimeout(enterTimer);
    const captured = index;
    if (immediateEnter) {
      enterSection(captured);
    } else {
      enterTimer = window.setTimeout(() => enterSection(captured), TRANS);
    }
  }

  /** 스냅 잠금용 400vh / 푸터 해제용 100vh */
  function setSpacerLocked() {
    spacer.style.removeProperty("height");
    spacer.style.removeProperty("min-height");
    spacer.classList.remove("is-footer");
  }

  function setSpacerForFooter() {
    // 1뷰포트만 남김 → 문서 스크롤량은 푸터 높이뿐
    spacer.style.setProperty("height", "100vh", "important");
    spacer.style.setProperty("min-height", "100vh", "important");
    spacer.classList.add("is-footer");
  }

  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);

  function animateScroll(from, to, ms, done) {
    let start = null;
    const dist = to - from;
    if (Math.abs(dist) < 1) {
      window.scrollTo(0, to);
      done?.();
      return;
    }
    function frame(ts) {
      if (start === null) start = ts;
      const p = Math.min(1, (ts - start) / ms);
      window.scrollTo(0, from + dist * ease(p));
      if (p < 1) requestAnimationFrame(frame);
      else done?.();
    }
    requestAnimationFrame(frame);
  }

  function unlockAnim() {
    animating = false;
    if (mode === "free") {
      queuedDir = null;
      return;
    }
    if (queuedDir !== null) {
      const d = queuedDir;
      queuedDir = null;
      step(d);
    }
  }

  function toFooter() {
    if (mode === "free" || animating) return;
    animating = true;
    mode = "free";
    queuedDir = null;
    wheelLocked = true;
    // 푸터로 나갈 때 섹션 Tab 차단 유지
    sections.forEach((sec) => {
      sec.setAttribute("inert", "");
      sec.setAttribute("aria-hidden", "true");
    });

    /*
      푸터 높이만큼만 이동:
      1) fixed 유지한 채 스페이서를 100vh로 축소 (화면 변화 없음, 400vh 스크롤 제거)
      2) is-free → absolute가 뷰포트에 안착
      3) 0 → 푸터높이 만 짧게 스크롤
    */
    window.scrollTo(0, 0);
    setSpacerForFooter();
    fixed.classList.add("is-free");
    // 강제 리플로우 후 실제 스크롤 가능 거리(=푸터) 측정
    void spacer.offsetHeight;

    const maxY = Math.max(
      0,
      document.documentElement.scrollHeight - window.innerHeight
    );
    if (maxY < 2) {
      unlockAnim();
      return;
    }
    animateScroll(0, maxY, TRANS, unlockAnim);
  }

  function fromFooter(focusEdge) {
    if (animating) return;
    animating = true;
    queuedDir = null;
    animateScroll(window.scrollY, 0, TRANS, () => {
      fixed.classList.remove("is-free");
      setSpacerLocked();
      mode = "locked";
      window.scrollTo(0, 0);
      syncSectionInert(index);
      unlockAnim();
      if (focusEdge) focusSectionEdge(index, focusEdge);
    });
  }

  function jumpTo(i) {
    if (!snapEnabled) {
      sections[i]?.scrollIntoView({ behavior: "smooth", block: "start" });
      applyTheme(i);
      enterSection(i);
      return;
    }
    if (mode !== "locked") {
      mode = "locked";
      fixed.classList.remove("is-free");
      setSpacerLocked();
      window.scrollTo(0, 0);
    } else if (window.scrollY !== 0) {
      window.scrollTo(0, 0);
    }
    if (animating || i === index) return;
    animating = true;
    goSnap(i);
    window.setTimeout(unlockAnim, TRANS);
  }

  function step(dir) {
    if (!snapEnabled) return;
    if (dir > 0) {
      if (mode === "free") return; // 원본: free에서 아래 휠은 무시(이미 푸터 노출)
      if (index >= sectionCount - 1) return toFooter();
      animating = true;
      goSnap(index + 1);
      window.setTimeout(unlockAnim, TRANS);
    } else {
      if (mode === "free") return fromFooter();
      if (index <= 0) return;
      animating = true;
      goSnap(index - 1);
      window.setTimeout(unlockAnim, TRANS);
    }
  }

  function queueStep(dir) {
    if (!snapEnabled) return;
    // 전환 중 휠은 무시 (큐에 쌓아 왕복하지 않음)
    if (animating) return;
    step(dir);
  }

  /* ---- Snap listeners (PC only) ----
     capture:true — Swiper 영역 휠/스크롤체이닝보다 먼저 가로채기 */
  const onWheel = (e) => {
    if (!snapEnabled) return;
    e.preventDefault();
    e.stopPropagation();
    if (animating) return;
    const dir = Math.sign(e.deltaY);
    if (dir === 0) return;
    // free 모드에서 아래 휠은 무시 (푸터 이미 노출)
    if (mode === "free" && dir > 0) return;
    const now = Date.now();
    if (now - lastWheelAt >= WHEEL_GAP || dir !== lastWheelDir) wheelLocked = false;
    lastWheelAt = now;
    lastWheelDir = dir;
    if (!wheelLocked) {
      wheelLocked = true;
      queueStep(dir);
    }
  };

  const onKey = (e) => {
    if (!snapEnabled) return;
    if (e.target.closest("input, textarea")) return;
    if (["ArrowDown", "PageDown", " "].includes(e.key)) {
      e.preventDefault();
      queueStep(1);
    } else if (["ArrowUp", "PageUp"].includes(e.key)) {
      e.preventDefault();
      queueStep(-1);
    }
  };

  let touchY = null;
  const onTouchStart = (e) => {
    touchY = e.touches[0].clientY;
  };
  const onTouchMove = (e) => {
    if (!snapEnabled || touchY === null) return;
    e.preventDefault();
    const dy = touchY - e.touches[0].clientY;
    if (Math.abs(dy) > 40) {
      queueStep(Math.sign(dy));
      touchY = null;
    }
  };

  /** 섹션 끝에서 Tab / 시작에서 Shift+Tab → 인접 섹션으로 스냅 */
  const onTabNav = (e) => {
    if (!snapEnabled || e.key !== "Tab") return;
    if (e.target.closest?.("input, textarea, [contenteditable='true']")) return;
    // 사이드메뉴·봇·퀵메뉴 열린 동안은 해당 UI가 Tab 처리
    if (
      document.querySelector(".gnb.is-open, .cos-panel.is-open, #quickFloat.is-open")
    ) {
      return;
    }

    if (mode === "free") {
      if (!e.shiftKey) return;
      const footer = document.querySelector(".hc-footer");
      if (!footer || !footer.contains(e.target)) return;
      const fList = a11y.getFocusable(footer);
      if (e.target === fList[0]) {
        e.preventDefault();
        fromFooter("last");
      }
      return;
    }

    if (animating) {
      e.preventDefault();
      return;
    }

    const sec = sections[index];
    if (!sec || !sec.contains(e.target)) return;
    const list = a11y.getFocusable(sec);
    if (!list.length) return;

    if (!e.shiftKey && e.target === list[list.length - 1]) {
      e.preventDefault();
      if (index >= sectionCount - 1) {
        toFooter();
        window.setTimeout(() => {
          const footer = document.querySelector(".hc-footer");
          a11y.getFocusable(footer)[0]?.focus({ preventScroll: true });
        }, TRANS);
        return;
      }
      animating = true;
      queuedDir = null;
      goSnap(index + 1, { immediateEnter: true });
      requestAnimationFrame(() => {
        focusSectionEdge(index, "first");
        if (window.scrollY !== 0) window.scrollTo(0, 0);
      });
      window.setTimeout(unlockAnim, TRANS);
    } else if (e.shiftKey && e.target === list[0]) {
      if (index <= 0) return; // 헤더·내비로 네이티브 이동
      e.preventDefault();
      animating = true;
      queuedDir = null;
      goSnap(index - 1, { immediateEnter: true });
      requestAnimationFrame(() => {
        focusSectionEdge(index, "last");
        if (window.scrollY !== 0) window.scrollTo(0, 0);
      });
      window.setTimeout(unlockAnim, TRANS);
    }
  };

  /** locked 중 focus/스크롤체이닝으로 문서가 밀리면 즉시 복구 */
  const onScrollClamp = () => {
    if (!snapEnabled || mode !== "locked") return;
    if (window.scrollY !== 0) window.scrollTo(0, 0);
  };

  function bindSnap() {
    // capture 단계에서 Swiper보다 먼저 처리
    window.addEventListener("wheel", onWheel, { passive: false, capture: true });
    window.addEventListener("keydown", onKey);
    window.addEventListener("keydown", onTabNav, true);
    window.addEventListener("touchstart", onTouchStart, { passive: true, capture: true });
    window.addEventListener("touchmove", onTouchMove, { passive: false, capture: true });
    window.addEventListener("scroll", onScrollClamp, { passive: true });
  }

  function unbindSnap() {
    window.removeEventListener("wheel", onWheel, { capture: true });
    window.removeEventListener("keydown", onKey);
    window.removeEventListener("keydown", onTabNav, true);
    window.removeEventListener("touchstart", onTouchStart, { capture: true });
    window.removeEventListener("touchmove", onTouchMove, { capture: true });
    window.removeEventListener("scroll", onScrollClamp);
  }

  function enableSnapMode() {
    snapEnabled = true;
    mode = "locked";
    animating = false;
    queuedDir = null;
    fixed?.classList.remove("is-free");
    setSpacerLocked();
    document.documentElement.classList.remove("hc-snap-lock");
    document.body.classList.remove("hc-snap-lock");
    track.style.transform = `translateY(-${index * 100}vh)`;
    window.scrollTo(0, 0);
    bindSnap();
    applyTheme(index);
    enterSection(index);
  }

  function enableFlowMode() {
    snapEnabled = false;
    unbindSnap();
    clearSectionInert();
    track.style.transform = "";
    fixed?.classList.remove("is-free");
    setSpacerLocked();
    document.documentElement.classList.remove("hc-snap-lock");
    document.body.classList.remove("hc-snap-lock");
    mode = "free";
    applyTheme(0);
    // 첫 섹션 리빌/슬로건이 observer 대기 없이 바로 보이도록
    sections[0]?.classList.add("in-view");
    document.dispatchEvent(new CustomEvent("hc:section", { detail: 0 }));
    setupMobileObserver();
  }

  let io = null;
  function setupMobileObserver() {
    io?.disconnect();
    io = new IntersectionObserver(
      (entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) en.target.classList.add("in-view");
        });
        const visible = entries
          .filter((en) => en.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;
        const i = sections.indexOf(visible.target);
        if (i < 0) return;
        index = i;
        applyTheme(i);
        document.dispatchEvent(new CustomEvent("hc:section", { detail: i }));
      },
      { threshold: [0.25, 0.45, 0.6] }
    );
    sections.forEach((sec) => io.observe(sec));
  }

  function onBreakpointChange() {
    if (isMobile()) enableFlowMode();
    else {
      io?.disconnect();
      enableSnapMode();
    }
  }

  naviBtns.forEach((btn) =>
    btn.addEventListener("click", () => jumpTo(Number(btn.dataset.index)))
  );
  document.querySelector('[data-goto="0"]')?.addEventListener("click", (e) => {
    e.preventDefault();
    jumpTo(0);
  });

  /* ---- Hero title rotate ---- */
  {
    const sets = Array.from(document.querySelectorAll("#s1-title .title-set"));
    const delays = [2000, 5000];
    let cur = 0;
    let timer;
    const setState = (el, state) => {
      if (!el) return;
      el.classList.toggle("is-in", state === "in");
      el.classList.toggle("is-out", state === "out");
      if (state === "in") el.removeAttribute("aria-hidden");
      else el.setAttribute("aria-hidden", "true");
    };
    const schedule = () => {
      timer = window.setTimeout(tick, 1100 + delays[cur % delays.length]);
    };
    const tick = () => {
      setState(sets[cur], "out");
      cur = (cur + 1) % sets.length;
      timer = window.setTimeout(() => {
        setState(sets[cur], "in");
        schedule();
      }, 350);
    };
    const showHeroTitle = () => {
      if (!sets.length) return;
      clearTimeout(timer);
      sets.forEach((el) => setState(el, "hidden"));
      cur = 0;
      void sets[0].offsetWidth;
      setState(sets[0], "in");
      schedule();
    };
    document.addEventListener("hc:section", (ev) => {
      clearTimeout(timer);
      sets.forEach((el) => setState(el, "hidden"));
      cur = 0;
      if (ev.detail === 0) showHeroTitle();
    });
    // 스크롤 모드 부트 시 이벤트 타이밍과 무관하게 첫 슬로건 표시
    if (isMobile()) {
      requestAnimationFrame(showHeroTitle);
    }
  }

  /* ---- Hero video ---- */
  {
    const video = document.getElementById("s1-video");
    if (video) {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        video.removeAttribute("autoplay");
        video.pause();
      }
      document.addEventListener("hc:section", (ev) => {
        if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
          video.pause();
          return;
        }
        if (ev.detail === 0) video.play().catch(() => {});
        else video.pause();
      });
    }
  }

  /* ---- Swiper: s2 / s3 / s4 ---- */
  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function initS2Swiper() {
    const wrap = document.getElementById("s2-slider");
    const el = document.getElementById("s2-swiper") || wrap;
    if (!el || typeof Swiper === "undefined") return null;

    let status = wrap?.querySelector(".carousel-status");
    if (!status && wrap) {
      status = document.createElement("p");
      status.className = "blind carousel-status";
      status.setAttribute("aria-live", "polite");
      status.setAttribute("aria-atomic", "true");
      wrap.prepend(status);
    }
    const total = el.querySelectorAll(".swiper-slide").length;
    const syncStatus = (sw) => {
      if (status) status.textContent = `해외 법령 목록 ${sw.realIndex + 1} / ${total}`;
    };

    return new Swiper(el, {
      slidesPerView: 1.15,
      spaceBetween: 16,
      watchOverflow: true,
      // 세로 페이지 스냅과 충돌 방지
      simulateTouch: true,
      touchStartPreventDefault: false,
      nested: true,
      navigation: {
        prevEl: wrap?.querySelector(".s2-arrow.prev"),
        nextEl: wrap?.querySelector(".s2-arrow.next"),
      },
      breakpoints: {
        480: { slidesPerView: 1.4, spaceBetween: 16 },
        768: { slidesPerView: 2, spaceBetween: 18 },
        900: { slidesPerView: 2.4, spaceBetween: 20 },
        1101: { slidesPerView: 3, spaceBetween: 22 },
        1280: { slidesPerView: 4, spaceBetween: 24 },
      },
      on: {
        init: syncStatus,
        slideChange: syncStatus,
      },
    });
  }

  function initSectionSwiper(id, pagerKey, sectionIndex, opts) {
    const el = document.getElementById(id);
    if (!el || typeof Swiper === "undefined") return null;
    const pager = document.querySelector(`[data-carousel="${pagerKey}"]`);
    const currentEl = pager?.querySelector("[data-current]");
    const totalEl = pager?.querySelector(".nums .num:not([data-current])");
    const toggleBtn = pager?.querySelector(".toggle");
    const total = el.querySelectorAll(".swiper-slide").length;
    if (totalEl) totalEl.textContent = pad2(total);

    let status = el.querySelector(".carousel-status");
    if (!status) {
      status = document.createElement("p");
      status.className = "blind carousel-status";
      status.setAttribute("aria-live", "polite");
      status.setAttribute("aria-atomic", "true");
      el.prepend(status);
    }

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const label = el.getAttribute("aria-label") || "슬라이드";

    const syncStatus = (sw) => {
      const n = sw.realIndex + 1;
      if (currentEl) currentEl.textContent = pad2(n);
      status.textContent = `${label} ${n} / ${total}`;
    };

    const syncToggle = (paused) => {
      if (!toggleBtn) return;
      toggleBtn.setAttribute("aria-pressed", paused ? "false" : "true");
      toggleBtn.setAttribute(
        "aria-label",
        paused ? "자동재생 시작" : "자동재생 일시정지"
      );
    };

    const swiper = new Swiper(el, {
      slidesPerView: opts.mobile,
      spaceBetween: 16,
      loop: false,
      watchOverflow: true,
      // observer는 레이아웃 요동·의도치 않은 스크롤을 유발할 수 있어 사용하지 않음
      nested: true,
      touchStartPreventDefault: false,
      autoplay: reduceMotion
        ? false
        : {
            delay: 4000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true,
          },
      breakpoints: {
        768: { slidesPerView: opts.tablet, spaceBetween: 20 },
        // PC 스냅: ≤1200 → 1 / ≤1380 → 1.5 / ≤1499 → 2 / ≥1500 → 3
        1101: { slidesPerView: 1, spaceBetween: 20 },
        1201: { slidesPerView: 1.5, spaceBetween: 28 },
        1381: { slidesPerView: opts.mid ?? 2, spaceBetween: opts.midGap ?? 36 },
        1500: {
          slidesPerView: opts.desktop,
          spaceBetween: opts.desktopGap || 60,
        },
      },
      on: {
        init(sw) {
          syncStatus(sw);
        },
        slideChange(sw) {
          syncStatus(sw);
        },
      },
    });

    if (reduceMotion) {
      pager?.classList.add("paused");
      syncToggle(true);
    } else {
      syncToggle(false);
    }

    pager?.querySelector(".prev")?.addEventListener("click", () => swiper.slidePrev());
    pager?.querySelector(".next")?.addEventListener("click", () => swiper.slideNext());
    toggleBtn?.addEventListener("click", () => {
      if (!swiper.autoplay) return;
      const paused = pager.classList.toggle("paused");
      if (paused) swiper.autoplay.stop();
      else swiper.autoplay.start();
      syncToggle(paused);
    });

    document.addEventListener("hc:section", (ev) => {
      if (ev.detail === sectionIndex) {
        if (swiper.autoplay && !pager?.classList.contains("paused") && !reduceMotion) {
          swiper.autoplay.start();
        }
        // PC 스냅 전환 후 크기만 조용히 맞춤 (스크롤 유발 없는 update)
        requestAnimationFrame(() => swiper.updateSize());
      } else if (swiper.autoplay) {
        swiper.autoplay.stop();
      }
    });

    if (index !== sectionIndex && swiper.autoplay) swiper.autoplay.stop();

    return swiper;
  }

  initS2Swiper();
  // 인허가·해외시장: <1500 2장 / ≥1500 3장
  initSectionSwiper("s3-carousel", "s3", 2, {
    mobile: 1.15,
    tablet: 2,
    mid: 2,
    midGap: 36,
    desktop: 3,
    desktopGap: 60,
  });
  initSectionSwiper("s4-carousel", "s4", 3, {
    mobile: 1.15,
    tablet: 2,
    mid: 2,
    midGap: 36,
    desktop: 3,
    desktopGap: 60,
  });

  /* ---- S4 globe canvas ---- */
  {
    const canvas = document.getElementById("s4-globe");
    if (canvas) {
      const maskUrl =
        canvas.getAttribute("data-mask") || "images/land-mask.json";
      const ctx = canvas.getContext("2d");
      const SIZE = 1600;
      const TILT = (24 * Math.PI) / 180;
      const RGB = [240, 240, 240];
      const DEG = Math.PI / 180;
      const cosT = Math.cos(TILT);
      const sinT = Math.sin(TILT);
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      canvas.width = SIZE * dpr;
      canvas.height = SIZE * dpr;
      ctx.scale(dpr, dpr);

      function project(lat, lon, rot) {
        const cl = Math.cos(lat);
        const x = cl * Math.sin(lon + rot);
        const y = Math.sin(lat);
        const z = cl * Math.cos(lon + rot);
        const yt = y * cosT - z * sinT;
        const zt = y * sinT + z * cosT;
        return [SIZE / 2 + 680 * x, SIZE / 2 - 680 * yt, zt];
      }

      const land = [];
      fetch(maskUrl)
        .then((res) => {
          if (!res.ok) throw new Error(`land-mask fetch ${res.status}`);
          return res.json();
        })
        .then(({ w, h, data }) => {
          const bytes = Uint8Array.from(atob(data), (c) => c.charCodeAt(0));
          const has = (lat, lon) => {
            const row = Math.min(h - 1, Math.floor(90 - lat));
            const col = Math.min(w - 1, Math.floor(lon + 180));
            const bit = row * w + col;
            return (bytes[bit >> 3] >> (bit & 7)) & 1;
          };
          for (let lat = -87.5; lat <= 87.5; lat += 2.5) {
            const step = 1.2 / Math.max(Math.cos(lat * DEG), 0.15);
            for (let lon = -180; lon < 180; lon += step) {
              if (has(lat, lon)) land.push([lat * DEG, lon * DEG]);
            }
          }
          draw(performance.now());
        })
        .catch(() => {
          /* 마스크 로드 실패 시 격자만 표시 */
          draw(performance.now());
        });

      function strokeLine(pts) {
        let drawing = false;
        ctx.beginPath();
        for (const [x, y, z] of pts) {
          if (z > 0) {
            if (drawing) ctx.lineTo(x, y);
            else ctx.moveTo(x, y);
            drawing = true;
          } else drawing = false;
        }
        ctx.stroke();
      }

      function draw(ts) {
        const rot = ts * 6e-5;
        ctx.clearRect(0, 0, SIZE, SIZE);
        ctx.strokeStyle = "#f0f0f0";
        ctx.lineWidth = 1;
        for (let lat = -75; lat <= 75; lat += 15) {
          const pts = [];
          for (let lon = 0; lon <= 360; lon += 3) pts.push(project(lat * DEG, lon * DEG, rot));
          strokeLine(pts);
        }
        for (let lon = 0; lon < 360; lon += 15) {
          const pts = [];
          for (let lat = -90; lat <= 90; lat += 3) pts.push(project(lat * DEG, lon * DEG, rot));
          strokeLine(pts);
        }
        for (const [lat, lon] of land) {
          const [x, y, z] = project(lat, lon, rot);
          if (z <= 0.02) continue;
          const a = (0.5 + z * 0.5).toFixed(3);
          ctx.fillStyle = `rgba(${RGB[0]}, ${RGB[1]}, ${RGB[2]}, ${a})`;
          ctx.fillRect(x - 1.2, y - 1.2, 2.4, 2.4);
        }
      }

      let raf = 0;
      const loop = (ts) => {
        draw(ts);
        raf = requestAnimationFrame(loop);
      };
      document.addEventListener("hc:section", (ev) => {
        cancelAnimationFrame(raf);
        if (ev.detail === 3) raf = requestAnimationFrame(loop);
      });
    }
  }

  /* ---- boot ---- */
  if (isMobile()) enableFlowMode();
  else {
    window.scrollTo(0, 0);
    enableSnapMode();
  }
  mq.addEventListener("change", onBreakpointChange);
})();
