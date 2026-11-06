// Слой движения Agave Advisory. В Тильде вставляется одним блоком T123 вместе с vendor/gsap и ScrollTrigger
(function () {
  const fine = matchMedia("(pointer:fine)").matches;
  const reduce = matchMedia("(prefers-reduced-motion:reduce)").matches;
  const hasGsap = window.gsap && window.ScrollTrigger;
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  // зерно
  const grain = document.createElement("div"); grain.className = "grain"; document.body.appendChild(grain);

  // курсор
  if (fine) {
    const cur = document.createElement("div"); cur.className = "cur"; document.body.appendChild(cur);
    let x = innerWidth / 2, y = innerHeight / 2, tx = x, ty = y;
    addEventListener("mousemove", e => { tx = e.clientX; ty = e.clientY; cur.classList.remove("hide"); });
    addEventListener("mouseleave", () => cur.classList.add("hide"));
    (function loop() { x += (tx - x) * .35; y += (ty - y) * .35; cur.style.transform = `translate(${x}px,${y}px) translate(-50%,-50%)`; requestAnimationFrame(loop); })();
    document.querySelectorAll("a,button,summary,.pt,video,select,.card").forEach(el => {
      el.addEventListener("mouseenter", () => cur.classList.add("on"));
      el.addEventListener("mouseleave", () => cur.classList.remove("on"));
    });
  }

  // печать в углу: появляется после первого экрана
  const corner = document.querySelector(".seal-corner");
  if (corner) addEventListener("scroll", () => corner.classList.toggle("on", scrollY > innerHeight * .8), { passive: true });

  // заголовки построчно: режем h1/h2 на строки по <br> и по словам, если строк нет
  document.querySelectorAll("h1.sp,h2.sp").forEach(h => {
    const parts = h.innerHTML.split(/<br\s*\/?>/i);
    h.innerHTML = parts.map(p => `<span class="ln"><span>${p}</span></span>`).join("");
  });

  // появление: один наблюдатель на всё
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add("in"); io.unobserve(e.target);
    e.target.querySelectorAll(".cnt").forEach(countUp);
  }), { threshold: .18 });
  document.querySelectorAll(".sp,.label.line,.rule,.mask,.facts,.hero-meta,.ceo-stats").forEach(el => io.observe(el));
  // страховка: что уже в экране, показываем сразу, не дожидаясь наблюдателя
  const revealVisible = () => document.querySelectorAll(".rv:not(.in),.sp:not(.in),.label.line:not(.in),.rule:not(.in),.mask:not(.in),.facts:not(.in),.hero-meta:not(.in),.ceo-stats:not(.in)").forEach(el => {
    const r = el.getBoundingClientRect(); if (r.top < innerHeight * .9 && r.bottom > 0) { el.classList.add("in"); el.querySelectorAll(".cnt").forEach(countUp); }
  });
  setTimeout(revealVisible, 150); addEventListener("scroll", revealVisible, { passive: true });

  // счётчики: data-to="2007" data-prefix="" data-suffix=" m"
  function countUp(el) {
    if (el.dataset.done) return; el.dataset.done = 1;
    const to = parseFloat(el.dataset.to), pre = el.dataset.prefix || "", suf = el.dataset.suffix || "";
    const t0 = performance.now(), dur = 1600;
    (function tick(t) {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      const n = Math.round(to * e);
      el.textContent = pre + (to < 10000 ? String(n) : n.toLocaleString("en-US").replace(/,/g, " ")) + suf;  // год без разрядов
      if (p < 1) requestAnimationFrame(tick);
    })(t0);
  }

  // 3D-наклон карточек
  if (fine && !reduce) document.querySelectorAll(".card").forEach(c => {
    c.addEventListener("mousemove", e => {
      const r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
      c.style.transform = `rotateY(${px * 10}deg) rotateX(${-py * 10}deg) translateZ(6px)`;
    });
    c.addEventListener("mouseleave", () => c.style.transform = "");
  });

  // весь сайт как полёт над полями: видео за страницей перематывается общей прокруткой
  const sky = document.querySelector(".sky video");
  if (sky) {
    sky.pause();
    const prog = () => Math.min(1, Math.max(0, scrollY / (document.documentElement.scrollHeight - innerHeight)));
    let target = 0, cur = 0, lastTick = 0;
    const apply = () => { if (sky.duration) sky.currentTime = sky.duration * cur; };
    const step = t => { lastTick = t; cur += (target - cur) * .12; if (Math.abs(target - cur) > .0004) apply(); requestAnimationFrame(step); };
    if (!reduce && innerWidth > 980) {
      if (sky.dataset.sd) { sky.src = innerWidth >= 1600 ? sky.dataset.hd : sky.dataset.sd; sky.load(); }  // 1920 только на больших экранах
      addEventListener("scroll", () => { target = prog(); if (performance.now() - lastTick > 120) { cur = target; apply(); } }, { passive: true });
      target = cur = prog(); sky.addEventListener("loadedmetadata", apply); requestAnimationFrame(step);
    }
    else { sky.removeAttribute("src"); sky.load(); }
    // ролики шагов и внутренних страниц подгружаются, когда до них доскроллили
    const lazy = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { const v = x.target; if (v.preload === "none") { v.preload = "auto"; v.load(); } lazy.unobserve(v); } }), { rootMargin: "600px" });
    document.querySelectorAll('video[preload="none"]').forEach(v => lazy.observe(v));  // на телефоне только постер, 17 МБ видео не грузим
  }
  const hint = document.querySelector(".scroll-hint");
  if (hint) addEventListener("scroll", () => hint.classList.toggle("off", scrollY > 80), { passive: true });

  // процесс: шаги переключают видео в закреплённом окне, линия прогресса растёт
  const proc = document.querySelector(".proc");
  if (proc) {
    const steps = [...proc.querySelectorAll(".pstep")], media = [...proc.querySelectorAll(".screen video,.screen img")], cap = proc.querySelector(".screen .cap"), bar = proc.querySelector(".bar i");
    let cur = -1;
    const show = i => {
      if (i === cur) return; cur = i;
      steps.forEach((s, k) => s.classList.toggle("on", k === i));
      media.forEach((m, k) => { m.classList.toggle("on", k === i); if (m.tagName === "VIDEO") { if (k === i) { m.currentTime = 0; m.play().catch(() => {}); } else m.pause(); } });
      if (cap) cap.textContent = `${String(i + 1).padStart(2, "0")} / ${String(steps.length).padStart(2, "0")} · ${steps[i].dataset.cap || ""}`;
      if (bar) bar.style.height = ((i + 1) / steps.length * 100) + "%";
    };
    const sio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) show(steps.indexOf(e.target)); }), { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach(s => sio.observe(s));
    show(0);
  }

  // параллакс фото в сплитах и дрейф карты
  if (hasGsap && !reduce && innerWidth > 980) {
    document.querySelectorAll(".split .media img, .ceo .media img").forEach(img => {
      gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: "none", scrollTrigger: { trigger: img, start: "top bottom", end: "bottom top", scrub: true } });
    });
    const map = document.querySelector("#client-map");
    if (map) gsap.fromTo(map, { scale: 1.04, x: 10 }, { scale: 1, x: -10, ease: "none", scrollTrigger: { trigger: map, start: "top bottom", end: "bottom top", scrub: true } });
    document.querySelectorAll(".seal .ring").forEach(r => gsap.to(r, { rotation: 180, ease: "none", scrollTrigger: { scrub: 1 } }));
  }
})();

// ===== Слой стиля 2: интро, главы, магнитные кнопки, переход между страницами =====
(function () {
  const reduce = matchMedia("(prefers-reduced-motion:reduce)").matches;
  const fine = matchMedia("(pointer:fine)").matches;

  // интро: один раз за сессию, печать рисует себя, шторы разъезжаются
  let seen = false; try { seen = sessionStorage.getItem("intro") === "1"; } catch (e) {}
  const age = document.getElementById("age");
  const runSeal = () => {  // запасное интро: печать рисует себя, шторы разъезжаются
    const el = document.createElement("div"); el.className = "intro";
    el.innerHTML = `<div class="half l"></div><div class="half r"></div>
      <svg viewBox="0 0 200 250"><circle class="draw" cx="100" cy="100" r="92"/><circle class="draw" cx="100" cy="100" r="84" style="animation-delay:.3s"/>
      <image class="ag" href="img/seal_core.svg" x="40" y="40" width="120" height="120"/><text x="100" y="238" text-anchor="middle">AGAVE ADVISORY</text></svg>`;
    document.body.appendChild(el); document.body.classList.add("lock");
    setTimeout(() => { el.classList.add("go"); document.body.classList.remove("lock"); try { sessionStorage.setItem("intro", "1"); } catch (e) {} setTimeout(() => el.remove(), 1800); }, 2300);
  };
  // основное интро: кукурузник летит над агавой и разрезает экран, за хвостом открывается сайт
  const base = (document.querySelector("base") || {}).href || "";
  const plane = document.createElement("video");
  plane.className = "plane"; plane.muted = true; plane.playsInline = true; plane.preload = "auto";
  plane.src = base + "video/plane.mp4";
  const PATH = [[0.3, 0], [0.4, 8], [0.9, 20], [1.4, 31], [1.9, 45], [2.4, 56], [2.9, 68], [3.4, 83], [3.9, 98], [4.4, 112], [4.9, 130]];  // секунда ролика → x носа самолёта в % ширины, снято по кадрам
  const noseAt = t => { let a = PATH[0], b = PATH[PATH.length - 1]; for (let i = 1; i < PATH.length; i++) if (PATH[i][0] >= t) { a = PATH[i - 1]; b = PATH[i]; break; } const k = (t - a[0]) / Math.max(.001, b[0] - a[0]); return a[1] + (b[1] - a[1]) * Math.min(1, Math.max(0, k)); };
  const runIntro = () => {
    if (reduce || !plane.canPlayType("video/mp4")) return runSeal();
    const el = document.createElement("div"); el.className = "intro plane-intro";
    el.appendChild(plane);
    const edge = document.createElement("div"); edge.className = "edge"; el.appendChild(edge);
    document.body.appendChild(el); document.body.classList.add("lock");
    let started = false;
    const finish = () => { el.classList.add("go"); document.body.classList.remove("lock"); try { sessionStorage.setItem("intro", "1"); } catch (e) {} setTimeout(() => el.remove(), 900); };
    const tick = () => {
      if (!el.isConnected) return;
      // видео 16:9 лежит в окне как object-fit:cover: переводим x носа из % ширины видео в % ширины окна
      const dispW = Math.max(innerWidth, innerHeight * 16 / 9), off = (dispW - innerWidth) / 2;
      const nose = (noseAt(plane.currentTime) / 100 * dispW - off) / innerWidth * 100;
      const x = nose - 18 * dispW / innerWidth, tail = x - 14;  // разрез идёт позади хвоста, с наклоном
      el.style.clipPath = `polygon(${x}% 0, 100% 0, 100% 100%, ${tail}% 100%)`;
      edge.style.left = x + "%"; edge.style.transform = `rotate(${Math.atan2((x - tail) / 100 * innerWidth, innerHeight)}rad)`;
      if (x > 112 || plane.ended) return finish();
      requestAnimationFrame(tick);
    };
    plane.addEventListener("ended", finish, { once: true });  // страховка: вкладка в фоне, кадры анимации не идут
    setTimeout(() => { if (el.isConnected && !el.classList.contains("go")) finish(); }, 7000);
    const go = () => { if (started) return; started = true; plane.play().then(() => requestAnimationFrame(tick)).catch(() => { el.remove(); runSeal(); }); };
    if (plane.readyState >= 3) go(); else { plane.addEventListener("canplay", go, { once: true }); setTimeout(() => { if (!started) { el.remove(); runSeal(); } }, 2500); }  // видео не успело: печать
  };
  if (!seen && !reduce) {
    if (age.classList.contains("hide")) runIntro();
    else age.querySelector(".btn.fill").addEventListener("click", runIntro, { once: true });  // интро после окна возраста
  }

  // главы справа: по секциям с data-ch
  const secs = [...document.querySelectorAll("section[data-ch]")];
  if (secs.length > 2 && innerWidth > 980) {
    const nav = document.createElement("nav"); nav.className = "chapters";
    nav.innerHTML = secs.map((s, i) => `<a href="#${s.id || ("ch" + i)}"><b>${s.dataset.title || ""}</b><i></i>${s.dataset.ch.split(" ")[0]}</a>`).join("");
    secs.forEach((s, i) => { if (!s.id) s.id = "ch" + i; });
    document.body.appendChild(nav);
    const links = [...nav.querySelectorAll("a")];
    const cio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { const i = secs.indexOf(e.target); links.forEach((l, k) => l.classList.toggle("on", k === i)); } }), { rootMargin: "-40% 0px -50% 0px" });
    secs.forEach(s => cio.observe(s));
  }

  // магнитные кнопки
  if (fine && !reduce) document.querySelectorAll(".btn").forEach(b => {
    b.addEventListener("mousemove", e => { const r = b.getBoundingClientRect(); b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * .18}px,${(e.clientY - r.top - r.height / 2) * .3}px)`; });
    b.addEventListener("mouseleave", () => b.style.transform = "");
  });

  // золотая шторка при переходе на другую страницу сайта
  if (!reduce) {
    const w = document.createElement("div"); w.className = "wipe"; w.innerHTML = '<span class="seal"><img src="img/seal_core.svg" alt=""></span>'; document.body.appendChild(w);
    document.querySelectorAll('a[href$=".html"],a[href*=".html#"]').forEach(a => a.addEventListener("click", e => {
      if (e.metaKey || e.ctrlKey || a.target === "_blank") return;
      e.preventDefault(); w.classList.add("on"); setTimeout(() => location.href = a.href, 560);
    }));
    addEventListener("pageshow", () => w.classList.remove("on"));
  }

  // кинолента: параллакс
  if (window.gsap && window.ScrollTrigger && !reduce && innerWidth > 980) document.querySelectorAll(".film img").forEach(img => {
    gsap.fromTo(img, { yPercent: -10 }, { yPercent: 10, ease: "none", scrollTrigger: { trigger: img.parentElement, start: "top bottom", end: "bottom top", scrub: true } });
  });

  // перелив золота в заголовках, когда они в экране
  const gio = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); gio.unobserve(e.target); } }), { threshold: .3 });
  document.querySelectorAll("h1,h2,.quote").forEach(h => gio.observe(h));
})();

// ===== Языки: автоопределение при первом заходе и запоминание выбора =====
(function () {
  const lang = document.documentElement.lang || "en";
  let saved = null; try { saved = localStorage.getItem("lang"); } catch (e) {}
  document.querySelectorAll(".lang a[data-lang]").forEach(a => a.addEventListener("click", () => { try { localStorage.setItem("lang", a.dataset.lang); } catch (e) {} }));
  if (lang === "en" && !saved) {
    const nav = (navigator.languages || [navigator.language || ""]).join(",").toLowerCase();
    const want = /(^|,)es/.test(nav) ? "es" : /(^|,)ru/.test(nav) ? "ru" : null;
    if (want) {
      try { localStorage.setItem("lang", want); } catch (e) {}
      const page = location.pathname.split("/").pop() || "index.html";
      location.replace(location.pathname.replace(/[^/]*$/, "") + want + "/" + page + location.hash);
    }
  }
})();
