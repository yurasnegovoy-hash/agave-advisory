// Интерактивная карта клиентов: страны и форматы работы правятся в списке CLIENTS
// В Тильде вставляется одним блоком T123 вместе с подключением d3 и topojson
(function () {
  const HOME = { name: "Los Altos de Jalisco", lon: -102.76, lat: 20.82 };
  // ЧЕРНОВИК: страны и форматы уточняются у клиентки
  const CLIENTS = [
    { name: "United States", lon: -95.7, lat: 38.5, fmt: "Bulk supply · Private label" },
    { name: "Canada", lon: -106.3, lat: 56.1, fmt: "Private label" },
    { name: "Colombia", lon: -74.3, lat: 4.6, fmt: "Bulk supply" },
    { name: "Chile", lon: -71.5, lat: -35.7, fmt: "Private label" },
    { name: "United Kingdom", lon: -1.5, lat: 52.4, fmt: "Private label" },
    { name: "France", lon: 2.2, lat: 46.6, fmt: "Private label" },
    { name: "Netherlands", lon: 5.3, lat: 52.1, fmt: "Bulk supply" },
    { name: "Germany", lon: 10.4, lat: 51.2, fmt: "Bulk supply" },
    { name: "Sweden", lon: 16.3, lat: 62.0, fmt: "Private label" },
    { name: "Ukraine", lon: 31.2, lat: 49.0, fmt: "Private label" },
    { name: "Armenia", lon: 45.0, lat: 40.1, fmt: "Bulk supply" },
    { name: "Russia", lon: 37.6, lat: 55.75, fmt: "Private label · Bulk supply" },
    { name: "Japan", lon: 138.3, lat: 36.2, fmt: "Private label" },
    { name: "South Korea", lon: 127.8, lat: 36.0, fmt: "Private label" },
    { name: "Philippines", lon: 122.0, lat: 12.9, fmt: "Private label" },
    { name: "New Zealand", lon: 174.9, lat: -40.9, fmt: "Private label" },
  ];

  // подписи карты на языке страницы; name остаётся английским для совпадения с данными карты
  const LANG = document.documentElement.lang;
  const T = {
    es: { "United States":"Estados Unidos","Canada":"Canadá","Colombia":"Colombia","Chile":"Chile","United Kingdom":"Reino Unido","France":"Francia","Netherlands":"Países Bajos","Germany":"Alemania","Sweden":"Suecia","Ukraine":"Ucrania","Armenia":"Armenia","Russia":"Rusia","Japan":"Japón","South Korea":"Corea del Sur","Philippines":"Filipinas","New Zealand":"Nueva Zelanda","Bulk supply":"Suministro a granel","Private label":"Marca privada" },
    ru: { "United States":"США","Canada":"Канада","Colombia":"Колумбия","Chile":"Чили","United Kingdom":"Великобритания","France":"Франция","Netherlands":"Нидерланды","Germany":"Германия","Sweden":"Швеция","Ukraine":"Украина","Armenia":"Армения","Russia":"Россия","Japan":"Япония","South Korea":"Южная Корея","Philippines":"Филиппины","New Zealand":"Новая Зеландия","Bulk supply":"Поставки балком","Private label":"Частная марка" }
  }[LANG] || {};
  const tr = t => t.split(" · ").map(x => T[x] || x).join(" · ");
  const box = document.getElementById("client-map");
  if (!box || !window.d3 || !window.topojson) return;
  const W = 1200, H = 600;
  const inner = d3.select(box).append("div").attr("class", "cm-inner");  // карта во всю левую колонку, подсказки считаются от самой карты
  const svg = inner.append("svg").attr("viewBox", `0 0 ${W} ${H}`).attr("role", "img")
    .attr("aria-label", "Map of countries where Agave Advisory clients are based");
  const VY = 20, VH = 473;  // окно карты: от 84° с.ш. до 58° ю.ш., без Антарктиды
  svg.attr("viewBox", `0 ${VY} ${W} ${VH}`);
  svg.append("image").attr("href", (window.AGAVE_BASE || "") + "img/map_world.jpg").attr("width", W).attr("height", H).attr("preserveAspectRatio", "none");
  const proj = d3.geoEquirectangular().scale(W / (2 * Math.PI)).translate([W / 2, H / 2]);  // совпадает с растром
  const path = d3.geoPath(proj);
  const tip = inner.append("div").attr("class", "map-tip");
  const list = d3.select("#client-list");

  // данные карты лежат локально в vendor/world-110m.js: внешние запросы на опубликованной странице блокируются
  const load = window.WORLD ? Promise.resolve(window.WORLD) : fetch((window.AGAVE_BASE || "") + "vendor/countries-110m.json").then(r => r.json());
  load.then(world => {
    const countries = topojson.feature(world, world.objects.countries).features.filter(f => f.properties.name !== "Antarctica");
    const active = new Set(CLIENTS.map(c => c.name).concat(["Mexico"]));
    svg.append("g").selectAll("path").data(countries).join("path")
      .attr("d", path)
      .attr("class", d => "country" + (active.has(d.properties.name) ? " on" : ""));

    const [hx, hy] = proj([HOME.lon, HOME.lat]);
    const arcs = svg.append("g"), dots = svg.append("g");

    CLIENTS.forEach((c, i) => {
      const [x, y] = proj([c.lon, c.lat]);
      const mx = (hx + x) / 2, my = Math.min(hy, y) - Math.abs(x - hx) * 0.22 - 30;
      const arc = arcs.append("path").attr("class", "arc").attr("d", `M${hx},${hy} Q${mx},${my} ${x},${y}`);
      const len = arc.node().getTotalLength();
      arc.attr("stroke-dasharray", len).attr("stroke-dashoffset", len);
      c.arc = arc; c.len = len; c.x = x;
      const g = dots.append("g").attr("class", "pt").attr("transform", `translate(${x},${y})`).attr("tabindex", 0);
      g.append("circle").attr("class", "pulse").attr("r", 5).style("animation-delay", (i * 0.35) + "s");
      g.append("circle").attr("class", "core").attr("r", 4.5);
      const show = () => {
        g.classed("hot", true); arc.classed("hot", true);
        tip.html(`<b>${tr(c.name)}</b><span>${tr(c.fmt)}</span>`).style("left", (x / W * 100) + "%").style("top", ((y - VY) / VH * 100) + "%").classed("on", true);
        list.selectAll("li").classed("hot", d => d === c);
      };
      const hide = () => { g.classed("hot", false); arc.classed("hot", false); tip.classed("on", false); list.selectAll("li").classed("hot", false); };
      g.on("mouseenter", show).on("mouseleave", hide).on("focus", show).on("blur", hide).on("click", show);
      c.show = show; c.hide = hide;
    });

    const home = dots.append("g").attr("class", "pt home").attr("transform", `translate(${hx},${hy})`);
    home.append("circle").attr("class", "pulse").attr("r", 7);
    home.append("circle").attr("class", "core").attr("r", 6.5);
    home.append("text").attr("x", 0).attr("y", 26).attr("text-anchor", "middle").text("JALISCO");

    list.selectAll("li").data(CLIENTS).join("li")
      .html(c => `<b>${tr(c.name)}</b><span>${tr(c.fmt)}</span>`)
      .on("mouseenter", (e, c) => c.show()).on("mouseleave", (e, c) => c.hide())
      .on("click", (e, c) => { c.show(); box.scrollTo({ left: c.x / W * box.scrollWidth - box.clientWidth / 2, behavior: "smooth" }); });
    if (box.scrollWidth > box.clientWidth) box.scrollLeft = hx / W * box.scrollWidth - box.clientWidth * .28;  // телефон: старт от Мексики

    // линии рисуются, когда карта попадает в экран
    const io = new IntersectionObserver(es => {
      if (!es[0].isIntersecting) return;
      CLIENTS.forEach((c, i) => c.arc.transition().delay(300 + i * 220).duration(1600).ease(d3.easeCubicInOut).attr("stroke-dashoffset", 0));
      io.disconnect();
    }, { threshold: 0.3 });
    io.observe(box);
  }).catch(() => box.classList.add("map-fallback"));
})();
