# Внутренние страницы: About, How We Work, Clients и 5 услуг. Исполняется из build.py, переменные общие.

def hero(label, h1, lead, video=None, img=None, cta=True, pos="center"):
    bg = (f'<video class="hero-video" src="video/{video}.mp4" poster="video/{video}.jpg" muted loop playsinline autoplay></video>' if video
          else f'<div class="hero-bg" style="background-image:url(img/{img});background-position:{pos}"></div>')
    btn = '<div class="hero-cta rv"><a href="#contact" class="btn fill">Discuss your project</a></div>' if cta else ""
    return f"""<section class="hero sub">
  <div class="hero-bg">{bg}</div>
  <div class="wrap"><div class="label rv">{label}</div><h1 class="sp">{h1}</h1>
  <p class="lead rv">{lead}</p>{btn}</div>
</section>"""

def media(src, ratio="5/4"):
    if src.startswith("video:"):
        v = src[6:]
        return f'<div class="media frame mask" style="aspect-ratio:{ratio}"><video src="video/{v}.mp4" poster="video/{v}.jpg" muted loop playsinline autoplay preload="metadata" style="width:100%;height:100%;object-fit:cover"></video></div>'
    return f'<div class="media frame mask" style="aspect-ratio:{ratio}"><img src="img/{src}" alt=""></div>'

def grid(items, cols=2):
    return f'<div class="svc-grid" style="grid-template-columns:repeat({cols},1fr)">' + "".join(
        f'<div class="rv"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(items)) + "</div>"

def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

def faq_html(items):
    return '<div class="faq rv">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"

def others_html(slug):
    return '<div class="others">' + "".join(f'<a href="{o}.html" class="rv">{ic(oi)}<b>{ot}</b></a>' for o, ot, oi in SERVICES if o != slug) + "</div>"

# ================= ABOUT =================
TIMELINE = [
    ("2007", "First steps in the tequila industry", "Anastasia joins the tequila business in Jalisco and learns production from the inside: agave fields, cooking, fermentation, distillation, bottling"),
    ("2010s", "International sales", "Years of building export sales of tequila to distributors and retail chains on several continents. Documents, forwarders, customs, shelf"),
    ("Today", "Agave Advisory Agency", "An agency that represents foreign companies in Mexico: one partner for creating and sourcing tequila, from concept to delivery"),
]
about = f"""
{hero("About us", 'Nineteen years<br><span class="g">in tequila</span>', "Agave Advisory Agency represents foreign companies in Mexico. We create and source tequila for distributors, retail chains, spirits producers and private clients", video="distill", cta=False)}

<section class="pad ceo">
  <div class="wrap split">
    <div class="media mask"><img src="img/ceo_main.jpg" alt="Anastasia Strizheva at a distillery in Jalisco"></div>
    <div class="rv">
      <div class="label line">Founder &amp; CEO</div>
      <div class="name">Anastasia Strizheva</div>
      <div class="role">Founder &amp; CEO · Agave Advisory Agency</div>
      <div class="ceo-stats"><div><strong><span class="cnt" data-to="19">19</span> years</strong>in tequila</div><div><strong>Since <span class="cnt" data-to="2007">2007</span></strong>in the industry</div><div><strong>Jalisco</strong>home base</div></div>
      <p class="lead">Anastasia has worked in the tequila industry since 2007. She knows production from the agave field to the bottling line and has built sales of tequila across international markets</p>
      <p class="lead">She founded Agave Advisory Agency to give companies abroad what they need most when working with Mexico: a trusted person on the ground who knows production and international trade from the inside</p>
      <div class="hero-cta" style="margin-top:30px"><a href="https://www.linkedin.com/in/anastasia-strizheva-489446122/" target="_blank" rel="noopener" class="btn ghost">LinkedIn</a></div>
    </div>
  </div>
  <div class="wrap strip"><div class="mask"><img src="img/ceo_64.jpg" alt=""></div><div class="mask"><img src="img/ceo_68.jpg" alt=""></div><div class="mask"><img src="img/ceo_17.jpg" alt=""></div></div>
</section>

<section class="pad alt">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><div class="label line">The story</div><h2 class="sp">From the first harvest<br><span class="g">to your market</span></h2></div></div>
    <div class="svc-grid" style="grid-template-columns:repeat(3,1fr)">{"".join(f'<div class="rv"><span class="num" style="font-size:26px">{y}</span><h3>{t}</h3><p>{d}</p></div>' for y, t, d in TIMELINE)}</div>
  </div>
</section>

<section class="pad">
  <div class="wrap split">
    <div class="rv">
      <div class="label line">Why an agency</div>
      <h2 class="sp">What a distillery<br><span class="g">will not do for you</span></h2>
      <div class="rule"></div>
      <p class="lead">A distillery makes tequila. It does not choose your bottle supplier, file your trademark, check your labels with the regulator, stand at your bottling line or book your forwarder. When you are in another country, someone has to</p>
      {checks(["We choose the distillery that fits your product, not the one that answers first", "We know who makes good glass, closures and packaging in Mexico, and at what price", "We stand at the line when your tequila is bottled and send you photo and video reports", "We organise export on EXW, FOB, CIF or any terms your market needs"])}
    </div>
    {media("video:bottling_line", "4/5")}
  </div>
</section>

<section class="pad alt">
  <div class="wrap">
    <div class="sec-head">
      <div class="rv"><div class="label line">How we choose a distillery</div><h2 class="sp">Not every tequila<br><span class="g">is made the same way</span></h2></div>
      <p class="lead rv">In Mexico there are around 200 certified producers and over 3000 registered tequila brands. The difference between them is in the process</p>
    </div>
    {grid([("Agave", "Where it grew, how old it is, how much sugar it holds. Highland agave of Los Altos is larger and sweeter"), ("Cooking and yeast", "Slow cooking and the yeast strain decide the aromas: citrus, fruit, flowers, vanilla"), ("Distillation", "Copper or steel, how heads and tails are cut, how long the spirit is filtered"), ("Consistency", "Whether batch 10 tastes like batch 1. We look for distilleries where it does")], 4)}
    {facts_html()}
  </div>
</section>

<section class="pad">
  <div class="wrap">
    <div class="sec-head" style="margin-bottom:0"><div class="rv"><div class="label line">Where we are</div><h2 class="sp">Guadalajara and<br><span class="g">Los Altos de Jalisco</span></h2></div>
    <p class="lead rv">An office in Guadalajara and an office next to the distilleries we work with. We are at the plant when your tequila is made</p></div>
    {maps_html()}
  </div>
</section>
"""
page("about.html", "About Agave Advisory", "about", about, "Anastasia Strizheva, Founder and CEO of Agave Advisory Agency, has worked in the tequila industry since 2007")

# ================= HOW WE WORK =================
STAGES = [
    ("Brief", "You tell us what you want to create or source, for which market and with which requirements", "A short call or a message. No documents needed yet", "We understand the task and ask the right questions"),
    ("Project assessment", "We review the project: which distilleries fit, which components are needed, which documents your market requires", "Answers to our questions", "An honest view of what is realistic and what it takes"),
    ("Proposal", "You receive a clear plan of work: stages, responsibilities, what happens when", "Your decision", "A plan you can share with your partners"),
    ("Development", "Liquid selection and samples, bottle and packaging, label design coordination, trademark and regulatory work", "Approval of samples and design", "A product ready for production"),
    ("Production", "Components are delivered to the distillery, tequila is bottled under our supervision. Packaging check, quality inspection, final approval", "Nothing. You receive photo and video reports", "Finished goods, checked and approved"),
    ("Delivery", "Export documents, forwarder, port and delivery to your market on the agreed terms. Shipment monitoring until arrival", "Receiving the goods", "Your tequila in your market"),
]
how = f"""
{hero("How we work", 'Six stages<br><span class="g">one responsibility</span>', "From the first call to the delivered pallet, one team manages the project and reports to you at every stage", video="warehouse", cta=False)}
<section class="pad"><div class="wrap">{steps_html()}</div></section>
<section class="pad alt"><div class="wrap">
  <div class="sec-head"><div class="rv"><div class="label line">Stage by stage</div><h2 class="sp">What happens<br><span class="g">and what you get</span></h2></div></div>
  <div class="svc-grid">{"".join(f'<div class="rv"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p><p style="margin-top:14px"><span class="label" style="display:inline">Your part</span><br>{y}</p><p style="margin-top:8px"><span class="label" style="display:inline">You get</span><br>{g}</p></div>' for i, (t, d, y, g) in enumerate(STAGES))}</div>
</div></section>
<section class="pad"><div class="wrap split">
  {media("video:lab", "4/5")}
  <div class="rv"><div class="label line">Reporting</div><h2 class="sp">You see<br><span class="g">what we see</span></h2><div class="rule"></div>
  <p class="lead">At every stage you receive photo and video reports from the field, the distillery and the bottling line. Samples go to you by courier. Nothing is shipped without your final approval</p>
  {checks(["Photo and video from the line on bottling day", "Samples before any commitment", "Shipment tracking until arrival", "One contact person for the whole project"])}</div>
</div></section>
"""
page("how-we-work.html", "How We Work · Agave Advisory", "process", how, "How Agave Advisory works: brief, assessment, proposal, development, production, delivery")

# ================= CLIENTS =================
clients = f"""
{hero("Clients &amp; partners", 'Trusted<br><span class="g">worldwide</span>', "Distributors, retail chains and producers we work with, and the partners behind our projects", img="wl_map.jpg", cta=False)}
<section class="pad"><div class="wrap">{client_map_html()}<div style="height:90px"></div>{logos_html()}{reviews_html()}</div></section>
"""
page("clients.html", "Clients & Partners · Agave Advisory", "clients", clients, "Clients and partners of Agave Advisory Agency")

# ================= УСЛУГИ =================
SVC = {
 "private-label": dict(video="bottling_line", side="video:cooking",
   h1='Private label<br><span class="g">&amp; turnkey development</span>',
   lead="Your own tequila brand, produced in Jalisco and delivered to your market. We coordinate every stage so you work with one team instead of a dozen suppliers",
   who="For distributors, retail chains and private clients who want tequila under their own label. From the first idea to pallets in your warehouse",
   grid=[("Product development", "Category, liquid profile and product concept. Blanco, reposado, añejo or a line. Sweeter or drier, with notes of vanilla or dried fruit. We shape the profile with the master distiller to your brief"),
         ("Distillery selection", "The partner distillery that fits your product and volume. We know who works with highland agave, who has copper stills, who keeps consistency from batch to batch"),
         ("Components and packaging", "Glass bottles, corks and closures, labels, luxury packaging and gift boxes. We negotiate with suppliers, buy and warehouse components when needed"),
         ("Legal and regulatory", "Coordination of the regulatory documentation: trademark registration, label approval with the Tequila Regulatory Council, agreements with the distillery and ongoing compliance"),
         ("Bottling supervision", "We stand at the line: on-site production control, packaging verification, quality inspection, photo and video reporting, final approval before shipment"),
         ("Export and delivery", "Forwarder selection, export coordination, door-to-door delivery on EXW, FOB, CIF or other terms. Shipment monitoring until arrival")],
   why=["You never coordinate a dozen suppliers across time zones","Your brand is registered and your label is approved before the first bottle is filled", "Your tequila comes from a distillery we know, with a profile you approved on samples"],
   need=["Your idea and your market", "Brand name and logo, or we help create them", "Decision on samples and design"],
   result=["Tequila produced under your brand", "Trademark and label approved in Mexico", "Documents prepared for export", "Goods delivered to your market"],
   faq=[("Can you make a brand from zero, without a name or design?", "Yes. Brand strategy, naming and packaging design are part of Brand & Market Advisory. We bring them into the project when needed"),
        ("Who owns the trademark?", "You. The brand and the trademark belong to you"),
        ("Can the liquid be made to my taste?", "Yes. We work with the master distiller on the profile: sweeter or drier, longer or shorter aging, different barrels. You approve samples"),
        ("Do I need to come to Mexico?", "No. We represent you at every stage and send photo and video reports. You are welcome to visit at any time")]),
 "bulk-tequila": dict(video="tanks", side="video:lab",
   h1='Bulk<br><span class="g">tequila supply</span>',
   lead="Tequila selected to your requirements and supplied in bulk from trusted distilleries in Jalisco. Samples first, specification agreed, supply organised",
   who="For bottlers, spirits producers and distributors who need tequila as a liquid, in volumes and with a profile that stays the same from batch to batch",
   grid=[("Selection to your requirements", "Category, profile and character to your brief. 100% agave. Highland agave of Los Altos is larger and sweeter"),
         ("Samples", "You taste and approve samples before any commitment. We send them by courier"),
         ("Specification", "We agree the specification with the distillery and keep it: same agave, same process, same result"),
         ("Quality control", "Laboratory analysis and tasting before every shipment. You know what is in the tank"),
         ("Supply organisation", "Filling, export documents and logistics on the terms you need. Regular supply on a schedule"),
         ("Confidentiality", "Which distillery, which specification, which volume: it all stays between us")],
   why=["Many bulk buyers take tequila from different distilleries with no single standard. We work with distilleries where we know where the agave grew and how the liquid was made", "You approve the liquid on samples, not on a description", "Every batch is checked before it leaves Mexico"],
   need=["Category and target profile", "Volume and frequency", "Market and delivery terms"],
   result=["Approved samples", "Agreed specification", "Organised regular supply", "Export documents for your market"],
   faq=[("Which categories can you supply?", "Blanco, reposado, añejo, extra añejo and cristalino. Other agave spirits on request"),
        ("Is the tequila 100% agave?", "Yes. We work with 100% Blue Weber agave tequila"),
        ("Can you keep the profile consistent over time?", "Yes. That is the point of an agreed specification and a distillery we know"),
        ("On which terms do you deliver?", "EXW, FOB, CIF or other terms your market needs")]),
 "brand-market-advisory": dict(video="warehouse", side="ceo_still.jpg",
   h1='Brand<br><span class="g">&amp; market advisory</span>',
   lead="We help you shape a tequila product that fits your market: positioning, product line, price architecture and preparation for market entry",
   who="For companies preparing a tequila launch or expanding their range, and for brands that want to enter a new market with the right product",
   grid=[("Positioning", "Where your tequila stands in the category and for whom it is made. Against which brands, at which price, on which shelf"),
         ("Product line", "Which expressions to launch and in which order. One hero product or a line from blanco to extra añejo"),
         ("Price architecture", "How the line is priced across channels and markets, from bulk cost to shelf price"),
         ("Bottle and packaging advisory", "Which glass, closure and packaging fit the positioning and the budget. What is available in Mexico and at what cost"),
         ("Tequila profile selection", "Which liquid fits the brand: sweeter, drier, aged, cristalino. We work with the master distiller on the profile"),
         ("Market entry strategy", "Preparation for the markets you have chosen: requirements, documents, distribution channels, partners")],
   why=["We have sold tequila to distributors and chains in different markets and know what works on the shelf", "We know production, so your strategy is realistic and fits the budget", "The same team that advises can also produce and deliver"],
   need=["Your market and your ambition", "Budget range", "Existing brand materials, if any"],
   result=["Clear positioning", "A defined product line", "Price architecture", "A plan for your markets"],
   faq=[("Can you work only on strategy, without production?", "Yes. Brand & Market Advisory is a standalone service"),
        ("Do you help with distribution?", "We advise on distribution channels and partners as part of market entry preparation"),
        ("Do you design labels and packaging?", "We coordinate the design and advise on what works in production and on the shelf")]),
 "rtd": dict(video="ferment", side="video:bottling_line",
   h1='RTD<br><span class="g">development</span>',
   lead="We coordinate the development of tequila-based ready-to-drink products and find the right production and packaging solutions for them",
   who="For brands and producers who want a tequila RTD in their portfolio: cocktails, hard seltzers and mixed drinks for modern markets and new generations",
   grid=[("Concept", "The drink, its profile and the format it comes in. Which tequila, which mixers, which strength"),
         ("Development coordination", "Work with technologists and producers on the recipe and stability of the product"),
         ("Tequila base", "The right tequila for the drink: category, profile, volume and consistent supply"),
         ("Production partners", "Manufacturers in Mexico that fit your product, format and volume"),
         ("Packaging solutions", "Cans, bottles and secondary packaging. Suppliers, prices and lead times"),
         ("Regulatory and export", "Documents for your market and delivery on the terms you need")],
   why=["We know where the tequila comes from, so the base of your drink is consistent", "We know producers and packaging suppliers in Mexico", "One partner from recipe to pallet"],
   need=["Concept of the drink and target market", "Format and volume", "Approval of samples"],
   result=["A developed RTD product", "Production and packaging partners", "Tequila supply for the drink", "A product ready for your market"],
   faq=[("Can the RTD be made with my existing tequila brand?", "Yes. We can build the drink on your tequila or source the base for it"),
        ("Which formats are possible?", "Cans, glass bottles and other formats available with our production partners")]),
 "barrel-aging": dict(video="barrels", side="video:distill",
   h1='Barrel<br><span class="g">&amp; aging advisory</span>',
   lead="The right wood, the right influence, the right character. We select barrels and advise on aging to shape the flavour profile you want",
   who="For distilleries and brands working on reposado, añejo and extra añejo expressions, and for anyone who needs barrels delivered to a distillery in Mexico",
   grid=[("Barrel selection", "American white oak ex-bourbon barrels, 53 gal / 200 L, from leading Kentucky and Tennessee producers. French oak on request"),
         ("Quality of every barrel", "Freshly dumped, used once, checked for leaks and physical damage. Phytosanitary certificates provided"),
         ("Aging recommendations", "How long and in which wood to age: reposado from 2 months, añejo from 1 year, extra añejo from 3 years"),
         ("Flavour profile", "How barrel and time shape the character: vanilla, roasted coffee, chocolate, nuts, coconut"),
         ("Storage conditions", "Barrels rest in rooms with controlled humidity and no light. We advise on the setup"),
         ("Delivery to the distillery", "From the cooperage to your distillery in Mexico. Container quantities and schedule")],
   why=["We know what the barrel does to tequila, not only where to buy it", "Barrels come from leading bourbon producers, checked one by one", "We can advise, supply and oversee the aging together with the distillery"],
   need=["Your tequila and the profile you want", "Volume to be aged", "Where the barrels go"],
   result=["Barrels that fit your profile", "An aging plan with timing and wood", "Barrels delivered to your distillery"],
   faq=[("Which barrels do you supply?", "Classic 53 gal / 200 L ex-bourbon barrels from American white oak, from leading Kentucky and Tennessee producers. French oak on request"),
        ("How are the barrels delivered?", "By container or truck, from the cooperage to your distillery in Mexico. We will propose what fits your project"),
        ("Can you advise without supplying barrels?", "Yes. Aging advisory is available as a standalone service")]),
}

for n, (slug, title, icon) in enumerate(SERVICES):
    s = SVC[slug]
    body = f"""
{hero(f"Service 0{n+1}", s['h1'], s['lead'], video=s['video'])}
<section class="pad">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><div class="label line">What we cover</div><h2 class="sp">{title}</h2></div><p class="lead rv">{s['who']}</p></div>
    {grid(s['grid'])}
  </div>
</section>
<section class="pad alt">
  <div class="wrap split">
    {media(s['side'], '4/5')}
    <div class="rv"><div class="label line">Why with us</div><h2 class="sp">One partner<br><span class="g">on the ground</span></h2><div class="rule"></div>{checks(s['why'])}</div>
  </div>
</section>
<section class="pad">
  <div class="wrap split" style="align-items:start">
    <div class="rv"><div class="label line">What we need from you</div><h2 class="sp">To start</h2>{checks(s['need'])}</div>
    <div class="rv"><div class="label line">What you get</div><h2 class="sp">The result<br><span class="g">in your hands</span></h2>{checks(s['result'])}<p class="tagline">One partner. One process. One responsibility</p></div>
  </div>
</section>
<section class="pad alt">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><div class="label line">How it works</div><h2 class="sp">From brief<br><span class="g">to delivery</span></h2></div><p class="lead rv">Six stages, one team. You receive reports at every stage and approve samples before any commitment</p></div>
    {steps_html()}
  </div>
</section>
<section class="pad"><div class="wrap split" style="align-items:start">
  <div class="rv"><div class="label line">Questions</div><h2 class="sp">Good<br><span class="g">to know</span></h2></div>
  {faq_html(s['faq'] + [("Is my project confidential?", "Yes. Your project, suppliers and specifications stay between us"), ("How do we start?", "Send us a short brief through the form below. We will come back to you with the next steps")])}
</div></section>
<section class="pad alt"><div class="wrap">
  <div class="label line rv" style="margin-bottom:36px">Other services</div>
  {others_html(slug)}
</div></section>
"""
    page(f"{slug}.html", f"{title} · Agave Advisory", "services", body, s["lead"].split(". ")[0])

# ================= CONTACT =================
contact = f"""
{hero("Contact", 'Let us talk<br><span class="g">about your project</span>', "Write to us in English, Spanish or Russian and we will suggest the next steps", img="arches.jpg", cta=False)}
<section class="pad"><div class="wrap">
  <div class="sec-head"><div class="rv"><div class="label line">Where we are</div><h2 class="sp">Guadalajara<br><span class="g">and Los Altos de Jalisco</span></h2></div>
  <p class="lead rv">Our office is in Guadalajara and our work is in the highlands, at the distilleries of Los Altos</p></div>
  {maps_html()}
</div></section>
"""
page("contact.html", "Contact · Agave Advisory", "contact", contact, "Contact Agave Advisory Agency: e-mail, WhatsApp and offices in Guadalajara and Los Altos de Jalisco")

# ================= PRIVACY =================
PRIV = [
    ("Who we are", "Agave Advisory Agency, Guadalajara and Los Altos de Jalisco, Mexico. This notice explains what personal data we collect through this website and how we use it"),
    ("What we collect", "Only what you send through the contact form or by e-mail: your name, company, e-mail address, phone number and the description of your project. The website does not use analytics cookies or advertising trackers"),
    ("Why we collect it", "To answer your request, prepare a proposal and stay in touch about your project. Requests from the form reach us through the FormSubmit e-mail service. We do not send newsletters or sell your data, and we share project details with logistics and production partners only with your consent"),
    ("How long we keep it", "For as long as we work together and for the period required by Mexican law for business records"),
    ("Your rights", "You may ask at any time what data we hold about you, correct it, or ask us to delete it. Write to agaveadvisoryagency@gmail.com"),
    ("Age", "This website contains information about alcoholic beverages and is intended for visitors of legal drinking age in their country"),
]
privacy = f"""
{hero("Privacy notice", 'Your data<br><span class="g">stays between us</span>', "A short and plain explanation of what we collect on this website and what we do with it", img="arches.jpg", cta=False)}
<section class="pad"><div class="wrap">
  <div class="svc-grid">{"".join(f'<div class="rv"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(PRIV))}</div>
  <p class="note rv" style="margin-top:50px">Last updated: November 2026</p>
</div></section>
"""
page("privacy.html", "Privacy Notice · Agave Advisory", "", privacy, "Privacy notice of Agave Advisory Agency")
