"""Собирает прототип Agave Advisory v2: главная, About, How We Work, Clients и 5 страниц услуг.
Запуск: python3 build/build.py — пишет html в корень папки сайта."""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = re.search(r"<svg width=\"0\".*?</svg>", open(f"{ROOT}/index_v1.html", encoding="utf-8").read(), re.S).group(0)

SERVICES = [
    ("private-label", "Private Label & Turnkey Development", "bottle"),
    ("bulk-tequila", "Bulk Tequila Supply", "barrel"),
    ("brand-market-advisory", "Brand & Market Advisory", "compass"),
    ("rtd", "RTD Development", "glass"),
    ("barrel-aging", "Barrel & Aging Advisory", "star"),
]

def ic(name):
    return f'<svg><use href="#i-{name}"/></svg>'

def header(active):
    dd = "".join(f'<a href="{s}.html">{t}</a>' for s, t, _ in SERVICES)
    def on(k):
        return ' class="on"' if k == active else ""
    return f"""<header class="hdr" id="hdr"><div class="wrap">
  <a href="index.html" class="logo">{ic('agave')}<span><b>AGAVE</b><small>ADVISORY</small></span></a>
  <nav class="nav">
    <a href="about.html"{on('about')}>About</a>
    <span class="dd"><a href="index.html#services"{on('services')}>Services</a><span class="dd-menu">{dd}</span></span>
    <a href="how-we-work.html"{on('process')}>How we work</a>
    <a href="clients.html"{on('clients')}>Clients &amp; partners</a>
    <a href="contact.html"{on('contact')}>Contact</a>
  </nav>
  <div class="hdr-r"><span class="lang"><b>EN</b> · ES · RU</span><a href="#contact" class="btn ghost">Discuss your project</a><button class="burger" aria-label="Menu"></button></div>
</div></header>"""

CONTACT = """<section class="pad cta" id="contact"><div class="wrap cta-grid">
  <div class="rv">
    <div class="label line">Contact</div>
    <h2 style="margin-top:24px">Discuss <span class="g">your project</span></h2>
    <p class="lead" style="margin-top:26px">Tell us what you would like to create or source. We will come back to you with the next steps</p>
    <div class="contacts">
      <div><span class="ic">""" + ic("pin") + """</span><span><small>Offices</small>Guadalajara · Los Altos de Jalisco, Mexico</span></div>
      <div><span class="ic">""" + ic("phone") + """</span><span><small>Phone · WhatsApp</small><a href="https://wa.me/523314201317">+52 33 1420 1317</a></span></div>
      <div><span class="ic">""" + ic("mail") + """</span><span><small>E-mail</small><a href="mailto:agaveadvisoryagency@gmail.com">agaveadvisoryagency@gmail.com</a></span></div>
    </div>
  </div>
  <form class="form rv" action="https://formsubmit.co/ajax/agaveadvisoryagency@gmail.com" method="POST" onsubmit="return sendForm(event,this)" data-sending="Sending…" data-ok="Thank you. We will be in touch shortly" data-fail="Could not send. Please write to agaveadvisoryagency@gmail.com">
    <input type="hidden" name="_subject" value="New request from the Agave Advisory website"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
    <h3>Request a consultation</h3>
    <div class="f2"><div class="f"><label>Name</label><input name="name" required></div><div class="f"><label>Company</label><input name="company"></div></div>
    <div class="f2"><div class="f"><label>E-mail</label><input type="email" name="email" required></div><div class="f"><label>Phone · WhatsApp</label><input type="tel" name="phone"></div></div>
    <div class="f"><label>Service</label><select name="service">""" + "".join(f"<option>{t}</option>" for _, t, _ in SERVICES) + """<option>Not sure yet</option></select></div>
    <div class="f"><label>Tell us about your project</label><textarea name="message" rows="2"></textarea></div>
    <button class="btn fill" type="submit">Discuss your project</button>
    <p class="note">Your request stays confidential</p>
  </form>
</div></section>"""

FOOTER = """<footer class="ftr"><div class="wrap">
  <div class="word">AGAVE ADVISORY</div>
  <div class="ftr-top">
    <span class="seal" style="width:140px;height:140px"><img class="ring" src="img/seal_ring.svg" alt=""><img src="img/seal_core.svg" alt="Agave Advisory"></span>
    <div><h4>Services</h4>""" + "".join(f'<a href="{s}.html">{t}</a>' for s, t, _ in SERVICES) + """</div>
    <div><h4>Agency</h4><a href="about.html">About</a><a href="how-we-work.html">How we work</a><a href="clients.html">Clients &amp; partners</a><a href="contact.html">Contact</a></div>
    <div><h4>Follow</h4><a href="https://www.linkedin.com/in/anastasia-strizheva-489446122/" target="_blank" rel="noopener">LinkedIn</a><a href="https://www.instagram.com/hacienda.la.capilla" target="_blank" rel="noopener">Instagram</a><p>agaveadvisoryagency@gmail.com</p></div>
  </div>
  <div class="ftr-bot"><span>© 2026 Agave Advisory Agency</span><span>Guadalajara · Los Altos de Jalisco · Mexico</span><a href="privacy.html">Privacy notice</a></div>
</div></footer>"""

AGE = """<div class="age" id="age"><div class="age-box">
  <span class="seal" style="width:130px;height:130px;margin:0 auto 26px"><img class="ring" src="img/seal_ring.svg" alt=""><img src="img/seal_core.svg" alt=""></span>
  <h3>Are you of legal drinking age?</h3>
  <p>This website contains information about alcoholic beverages</p>
  <div class="row"><button class="btn fill" onclick="try{sessionStorage.setItem('age','1')}catch(e){};document.getElementById('age').classList.add('hide')">Yes, enter</button><a class="btn ghost" href="https://www.google.com">No</a></div>
</div></div>"""

SCRIPT = """<script>
window.sendForm=async function(e,f){e.preventDefault();var n=f.querySelector(".note"),b=f.querySelector("button");b.disabled=true;n.textContent=f.dataset.sending;try{var r=await fetch(f.action,{method:"POST",headers:{Accept:"application/json"},body:new FormData(f)});if(!r.ok)throw 0;n.textContent=f.dataset.ok;f.reset()}catch(x){n.textContent=f.dataset.fail}b.disabled=false;return false};
try{if(sessionStorage.getItem('age'))document.getElementById('age').classList.add('hide')}catch(e){}
const hdr=document.getElementById('hdr');const onS=()=>hdr.classList.toggle('solid',scrollY>60);addEventListener('scroll',onS,{passive:true});onS();
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.rv').forEach((el,i)=>{el.style.transitionDelay=(i%4)*0.07+'s';io.observe(el)});
</script>"""

import time
BUILD_V = str(int(time.time()))  # версия сборки: браузеры и GitHub Pages не держат старые стили и скрипты
def page(fname, title, active, body, desc):
    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="fonts.css?v={BUILD_V}">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="img/touch.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Agave Advisory"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://yurasnegovoy-hash.github.io/agave-advisory/img/og.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="style.css?v={BUILD_V}">
<link rel="stylesheet" href="fx.css?v={BUILD_V}">
</head><body>
{ICONS}
<div class="sky"><video data-hd="video/fly.mp4" data-sd="video/fly_1280.mp4" poster="video/fly.jpg" muted playsinline preload="auto"></video></div>
{AGE}
{header(active)}
<main>
{body}
{CONTACT}
</main>
{FOOTER}
<div class="seal-corner"><img class="ring" src="img/seal_ring.svg" alt=""><img class="core" src="img/seal_core.svg" alt=""></div>
{SCRIPT}
<script src="vendor/gsap.min.js"></script><script src="vendor/ScrollTrigger.min.js"></script><script src="fx.js?v={BUILD_V}"></script>
{MAP_JS if 'id="client-map"' in body else ''}
</body></html>
"""
    for s, t, _ in SERVICES:  # на странице услуги в форме уже выбрана эта услуга
        if s == fname[:-5]:
            html = html.replace(f"<option>{t}</option>", f"<option selected>{t}</option>", 1)
    open(f"{ROOT}/{fname}", "w", encoding="utf-8").write(html)
    print("ok", fname)

STEPS = [
    ("search", "Brief", "Your idea, market and requirements"),
    ("eye", "Assessment", "We review the project and what it needs"),
    ("compass", "Proposal", "A clear plan of work for your project"),
    ("bottle", "Development", "Liquid, packaging and documents"),
    ("barrel", "Production", "Bottling under our on-site control"),
    ("globe", "Delivery", "Export and delivery to your market"),
]

def steps_html():
    return '<div class="steps">' + "".join(
        f'<div class="step rv"><span class="c">{ic(i)}</span><span class="num">0{n+1}</span><h3>{t}</h3><p>{d}</p></div>'
        for n, (i, t, d) in enumerate(STEPS)) + "</div>"

LOCAL_MAP = """<img class="lmap-img" src="img/map_jalisco.jpg" alt="Relief map of Jalisco">
<svg viewBox="0 0 1400 1229" preserveAspectRatio="xMidYMid slice">
  <defs><radialGradient id="lm-v" cx="50%" cy="50%" r="70%"><stop offset="60%" stop-color="rgba(14,12,10,0)"/><stop offset="100%" stop-color="rgba(14,12,10,.6)"/></radialGradient></defs>
  <rect width="1400" height="1229" fill="url(#lm-v)"/>
  <ellipse cx="960" cy="625" rx="190" ry="120" fill="rgba(201,163,78,.10)" stroke="#C9A34E" stroke-width="2"/>
  <text x="960" y="475" fill="#C9A34E" font-family="Oswald" font-size="28" letter-spacing="8" text-anchor="middle">LOS ALTOS DE JALISCO</text>
  <path d="M729 637 Q813 547 897 594" fill="none" stroke="#C9A34E" stroke-width="2.5" stroke-dasharray="5 10"/>
  <circle cx="729" cy="637" r="16" fill="#E2C88E"/><circle cx="729" cy="637" r="36" fill="none" stroke="rgba(226,200,142,.45)" stroke-width="2"/>
  <text x="729" y="722" fill="#E4E1D7" font-family="Oswald" font-size="30" letter-spacing="8" text-anchor="middle">GUADALAJARA</text>
  <circle cx="897" cy="594" r="14" fill="#C9A34E"/><circle cx="1014" cy="629" r="14" fill="#C9A34E"/><circle cx="969" cy="672" r="14" fill="#C9A34E"/>
  <text x="700" y="90" fill="rgba(228,225,215,.55)" font-family="Oswald" font-size="26" letter-spacing="10" text-anchor="middle">JALISCO · MEXICO</text>
</svg>"""

MAP_JS = """<script src="vendor/d3.min.js"></script>
<script src="vendor/topojson-client.min.js"></script>
<script src="vendor/world-110m.js"></script>
<script src="map.js?v=""" + BUILD_V + """"></script>"""

def client_map_html():
    return """<div class="client-map-wrap">
  <div class="map-swipe">Swipe the map</div>
  <div id="client-map" class="rv"></div>
  <div class="rv"><div class="label" style="margin-bottom:18px">Our clients are in</div><ul id="client-list"></ul><span class="draft">Draft countries</span></div>
</div>"""

def maps_html():
    return f"""<div class="maps" style="grid-template-columns:1fr 1fr">
  <div class="map-card rv">{LOCAL_MAP}<div class="cap"><b>Our offices</b><span>Guadalajara · Los Altos de Jalisco</span></div></div>
  <div class="map-card rv graded" style="background:url(video/aerial_rows.jpg) center/cover"><div class="cap" style="background:linear-gradient(0deg,rgba(14,12,10,.9),transparent);margin:-26px -30px;padding:60px 30px 26px"><b>Next to the fields</b><span>Highland agave of Los Altos</span></div></div>
</div>"""

REEL = [("aerial_rows", "Highland fields"), ("jimadores", "Harvest"), ("tanks", "Fermentation"), ("lab", "Quality control"), ("img:ceo_50", "Aging"), ("bottling_line", "Bottling")]
def reel_html():
    return '<div class="reel">' + "".join(
        f'<figure class="rv">' + (f'<img src="img/{v[4:]}.jpg" alt="">' if v.startswith("img:") else f'<video src="video/{v}.mp4" poster="video/{v}.jpg" muted loop playsinline autoplay preload="none"></video>') + f'<figcaption><span class="num">0{i+1}</span><b>{t}</b></figcaption></figure>'
        for i, (v, t) in enumerate(REEL)) + "</div>"

FACTS = [("<span class=\"cnt\" data-to=\"2000\" data-suffix=\" m\">2000 m</span>", "Altitude of the highland agave fields of Los Altos"),
         ("Sweeter", "Highland agave grows larger, with more sugar and aroma"),
         ("<span class=\"cnt\" data-to=\"1895\">1895</span>", "Heritage of our partner distillery in Los Altos"),
         ("Copper", "Stills in use for over a century")]
def facts_html():
    return '<div class="facts">' + "".join(f'<div class="rv"><strong>{a}</strong><span>{b}</span></div>' for a, b in FACTS) + "</div>"

LOGOS = [("Askaneli Brothers", "Client"), ("Global Spirits", "Client"), ("Magnit", "Client"), ("Old Barrel", "Barrel partner"), ("Artesanal Destilería", "Distillery partner"), ("Patrizia Lamborghini", "Partner")]
def logos_html():
    return '<div class="logos rv">' + "".join(f"<div><b>{n.upper()}</b><small>{r} · logo pending</small></div>" for n, r in LOGOS) + "</div>"

REVIEWS = [
    ("Working with a team on the ground in Jalisco changed everything for us. Every stage was under control and we always knew where our project stood", "Distributor · name after approval"),
    ("They found the right liquid for our specification and organised the supply from samples to shipment", "Spirits producer · name after approval"),
    ("One partner for documents, components, production and delivery. Exactly what we needed to launch our own label", "Retail chain · name after approval"),
]
def reviews_html():
    return '<div class="reviews">' + "".join(f'<div class="review rv"><span class="q">“</span><p>{t}</p><cite>{a}</cite><span class="draft">Draft text</span></div>' for t, a in REVIEWS) + "</div>"

def cards_html():
    descr = {
        "private-label": "Your own tequila brand from product development to bottled and delivered goods",
        "bulk-tequila": "Tequila selected to your requirements: samples, agreed specification and organised supply",
        "brand-market-advisory": "Positioning, product line, price architecture and preparation for your markets",
        "rtd": "Tequila-based ready-to-drink products with the right production and packaging partners",
        "barrel-aging": "Barrel selection and aging guidance to shape the flavour profile you want",
    }
    out = '<div class="cards">'
    for n, (s, t, i) in enumerate(SERVICES):
        out += f'<a class="card rv" href="{s}.html"><span class="num">0{n+1}</span>{ic(i)}<h3>{t}</h3><p>{descr[s]}</p><span class="link">Learn more</span></a>'
    out += '<div class="card cta-card rv"><h3>Not sure where to start</h3><p>Tell us about your idea and we will suggest the right format</p><a href="#contact" class="btn ghost">Discuss your project</a></div></div>'
    return out

MARQ = "".join(f"<span>{t}</span>" for t in ["Mexico to the world","Since 2007","Los Altos de Jalisco","One partner. Every detail","Private label","Bulk tequila","Barrel & aging","From concept to global delivery"])

# процесс производства: видео под каждый шаг, img: для шагов, где ролика пока нет
PROCESS = [
    ("aerial_rows", "Highland fields", "Agave grows for 6 to 10 years at 2000 metres", "Blue Weber agave of Los Altos grows slowly in red volcanic soil. Bigger piñas, more sugar, more aroma", "Cultivation"),
    ("jimadores", "Harvest", "Jimadores cut the piña by hand with the coa", "Only ripe plants are harvested. A highland piña can weigh up to 110 kg", "Harvest"),
    ("cooking", "Cooking", "12 hours at 110 °C", "Slow cooking turns the starches of the piña into sugars and sets the foundation of flavour", "Cooking"),
    ("milling", "Milling", "Agua miel and bagazo", "The cooked piñas are crushed in the mill. The sweet juice, agua miel, goes to fermentation. The fibre, bagazo, returns to the fields as fertiliser", "Milling"),
    ("ferment", "Fermentation", "Up to 72 hours on the distillery's own yeast", "Yeast and time give each tequila its aroma: citrus, flowers and fruit from the agave, vanilla from the process. We follow every tank with our partner distillery", "Fermentation"),
    ("distill", "Distillation", "Twice, in copper", "The first run removes heads and tails, the second sets the strength. Copper stills at our partner distillery are over a century old", "Distillation"),
    ("lab", "Filtration", "Clean, not stripped", "Filtration removes what does not belong in the glass and keeps the agave", "Filtration"),
    ("barrels", "Aging", "American and French oak", "Reposado from 2 months, añejo from 1 year, extra añejo from 3. Barrels rest in rooms with controlled humidity", "Aging"),
    ("bottling_line", "Bottling", "Under our supervision", "We stand at the line: packaging check, quality inspection, photo and video report, final approval before shipment", "Bottling"),
    ("port", "Delivery", "To your market", "Export documents, forwarder, port and door-to-door delivery on EXW, FOB, CIF or other terms", "Delivery"),
]
def process_html():
    media = "".join((f'<img src="img/{v[4:]}.jpg" alt="">' if v.startswith("img:") else f'<video src="video/{v}.mp4" poster="video/{v}.jpg" muted loop playsinline preload="none"></video>') for v, *_ in PROCESS)
    steps = "".join(f'<div class="pstep" data-cap="{cap}"><span class="num">{i+1:02d}</span><h3>{t}</h3><p class="tagline" style="font-size:19px">{sub}</p><p>{d}</p></div>' for i, (v, t, sub, d, cap) in enumerate(PROCESS))
    return f"""<div class="proc">
  <div class="steps-col"><div class="bar"><i></i></div>{steps}</div>
  <div class="vid-col"><div class="screen">{media}<div class="cap"></div></div></div>
</div>"""

# ================= ГЛАВНАЯ =================
home = f"""
<section data-ch="I / IX" data-title="Home" class="hero home-hero" id="top">
  <video class="home-video" src="video/hero.mp4" poster="video/hero.jpg" autoplay muted loop playsinline preload="auto"></video>
  <div class="side-txt">MEXICO TO THE WORLD</div>
  <div class="wrap">
    <div class="label rv">Tequila brand development · Los Altos de Jalisco</div>
    <h1 class="sp" style="max-width:1000px"><span class="nw">One partner. Every detail</span><br><span class="g">From concept to global delivery</span></h1>
    <p class="lead rv">We help companies create and source tequila products, coordinating every stage from liquid selection and packaging to production and international delivery</p>
    <div class="hero-cta rv"><a href="#contact" class="btn fill">Discuss your project</a><a href="#services" class="btn ghost">Our services</a></div>
    <div class="hero-meta rv"><div><strong>Since <span class="cnt" data-to="2007">2007</span></strong>In the tequila industry</div><div><strong>Jalisco</strong>On the ground in Mexico</div><div><strong>Worldwide</strong>Any market, any Incoterms</div></div>
  </div>
  <div class="scroll-hint">Fly over the fields<i></i></div>
</section>
<div class="marquee"><div class="track">{MARQ}{MARQ}</div></div>

<section data-ch="II / IX" data-title="Why an agency" class="pad">
  <div class="wrap split">
    <div class="media frame mask" style="aspect-ratio:4/5"><img src="img/ceo_66.jpg" alt="Anastasia Strizheva at the agave ovens of a partner distillery in Jalisco"></div>
    <div class="rv">
      <div class="label line">Why an agency</div>
      <h2 class="sp"><span class="nw">Your eyes and ears</span><br><span class="g">in Jalisco</span></h2>
      <div class="rule"></div>
      <p class="lead">When you are thousands of kilometres away, working directly with a distillery is hard. We represent your interests on the ground</p>
      <ul class="checks">
        <li>We choose the right distillery and suppliers for your project</li>
        <li>We coordinate documents, components and production</li>
        <li>We control quality on site and report at every stage</li>
        <li>We organise export and delivery to your market</li>
      </ul>
      <a href="how-we-work.html" class="link">How we work</a>
    </div>
  </div>
</section>

<section data-ch="III / IX" data-title="How tequila is made" class="pad alt" id="process-steps">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><div class="label line">How tequila is made</div><h2 class="sp">We stand at every stage<br><span class="g">from the field to the bottle</span></h2></div>
      <p class="lead rv">Real footage from the fields and distilleries of Los Altos de Jalisco, where we work every day</p>
    </div>
    {process_html()}
  </div>
</section>
<div class="dia"></div>
<section data-ch="IV / IX" data-title="Quality" class="pad">
  <div class="wrap split">
    <div class="rv">
      <div class="label line">Why it matters</div>
      <h2 class="sp">Know where<br><span class="g">your tequila comes from</span></h2>
      <div class="rule"></div>
      <p class="lead">Many brands buy bulk tequila from different distilleries with no single quality standard. The taste of tequila depends on every stage: the agave, the cooking, the yeast, fermentation, distillation and filtration</p>
      <p class="lead">Tequila may only be made in five Mexican states, and the highlands of Los Altos give the sweetest agave. We work with distilleries there, where we know the origin of the agave and how the liquid was made. <em>That is how quality stays the same from batch to batch</em></p>
    </div>
    <div class="media frame mask" style="aspect-ratio:4/5"><img src="img/ceo_68.jpg" alt="Cooked agave piña"></div>
  </div>
  <div class="wrap">{facts_html()}</div>
</section>

<section data-ch="V / IX" data-title="Services" class="pad alt" id="services">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><div class="label line">What we do</div><h2 class="sp">Five ways<br><span class="g">to work with us</span></h2></div>
      <p class="lead rv">Distributors, spirits producers and private clients come to us to create their own tequila or to source it in Mexico</p>
    </div>
    {cards_html()}
  </div>
</section>

<div class="film"><img src="img/field_sunset.jpg" alt=""><div class="cap"><span>Los Altos de Jalisco</span><small>Highland agave · 2000 m</small></div></div>
<section data-ch="VI / IX" data-title="Founder" class="pad ceo">
  <div class="wrap split rev">
    <div class="media mask"><img src="img/ceo_main.jpg" alt="Anastasia Strizheva, Founder and CEO of Agave Advisory"></div>
    <div class="rv">
      <div class="label line">Founder &amp; CEO</div>
      <div class="name">Anastasia Strizheva</div>
      <div class="role">Founder &amp; CEO · Agave Advisory Agency</div>
      <div class="ceo-stats"><div><strong>19 years</strong>in tequila</div><div><strong>Since 2007</strong>in the industry</div><div><strong>Jalisco</strong>home base</div></div>
      <p class="lead">Anastasia has worked in the tequila industry since 2007. She knows production from the agave field to the bottling line and has built sales of tequila across international markets</p>
      <a href="about.html" class="link">About the agency</a>
    </div>
  </div>
</section>

<section data-ch="VII / IX" data-title="How we work" class="pad alt" id="process">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><div class="label line">How we work</div><h2 class="sp">A clear path<br><span class="g">from brief to delivery</span></h2></div>
      <p class="lead rv">One team manages every stage of your project, so you deal with one partner and one point of responsibility</p>
    </div>
    {steps_html()}
  </div>
</section>
<div class="dia"></div>
<section data-ch="VIII / IX" data-title="Where we are" class="pad">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:0">
      <div class="rv"><div class="label line">Where we are</div><h2 class="sp">Rooted in Jalisco<br><span class="g">Working worldwide</span></h2></div>
      <p class="lead rv">Offices in Guadalajara and in Los Altos de Jalisco, next to the distilleries we work with</p>
    </div>
    {maps_html()}
    {client_map_html()}
  </div>
</section>

<div class="film"><img src="img/arches.jpg" alt=""><div class="cap"><span>Mexico to the world</span><small>Since 2007</small></div></div>
<section data-ch="IX / IX" data-title="Clients" class="pad alt" id="clients">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><div class="label line">Clients &amp; partners</div><h2 class="sp">Trusted by<br><span class="g">our partners</span></h2></div>
      <p class="lead rv">Distributors, retail chains and producers we work with</p>
    </div>
    {logos_html()}
    {reviews_html()}
  </div>
</section>

<section class="quote" style="background-image:url(img/ceo_50.jpg)">
  <div class="wrap rv"><span class="mark">“</span>
    <blockquote>We stand where your tequila is made, <span class="g">so you do not have to</span></blockquote>
    <cite class="label">Anastasia Strizheva · Founder &amp; CEO</cite>
  </div>
</section>
"""
page("index.html", "Agave Advisory", "", home, "Agave Advisory Agency: one partner for creating and sourcing tequila products, from concept to global delivery. Los Altos de Jalisco, Mexico")

# внутренние страницы собираются из build/inner_pages.py
exec(open(os.path.join(ROOT, "build", "inner_pages.py"), encoding="utf-8").read())
