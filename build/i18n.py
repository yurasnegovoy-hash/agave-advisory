"""Испанская и русская версии: берёт собранные английские страницы, переводит тексты через Gemini,
пишет копии в es/ и ru/. Переводы кешируются в build/i18n_<lang>.json, их можно править руками.
Запуск после build.py: python3 build/i18n.py"""
import os, re, json, urllib.request, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index", "about", "how-we-work", "clients", "private-label", "bulk-tequila", "brand-market-advisory", "rtd", "barrel-aging", "contact", "privacy"]
LANGS = {"es": "Spanish (Mexico). Always formal usted, never tú. Always correct accents and ñ (decisión, línea, producción, añejo)", "ru": "Russian (business register, вежливое «вы»)"}
KEY = os.environ.get("GEMINI_API_KEY")
SKIP = re.compile(r"^(AGAVE|ADVISORY|EN|ES|RU|EN · ES · RU|LinkedIn|Instagram|agaveadvisoryagency@gmail\.com|\+52 33 1420 1317|©.*|[\d\s/·.,%°+–-]+|I|II|III|IV|V|VI|VII|VIII|IX)$")
ATTR = re.compile(r'(\s(?:alt|placeholder|aria-label|data-title|data-cap|content)=")([^"]*)(")')
TAG = re.compile(r"(<[^>]+>)")

def pieces(html):
    """Делит страницу на теги и текст; текст внутри script/style/svg не трогаем"""
    out, skip = [], 0
    for part in TAG.split(html):
        if part.startswith("<"):
            low = part.lower()
            if re.match(r"<(script|style|svg)\b", low) and not low.endswith("/>"):
                skip += 1
            elif re.match(r"</(script|style|svg)>", low):
                skip = max(0, skip - 1)
            out.append(("tag", part))
        else:
            out.append(("txt" if not skip else "raw", part))
    return out

def need(t):
    s = t.strip()
    return bool(s) and re.search(r"[A-Za-z]", s) and not SKIP.match(s)

def collect():
    seen, order = set(), []
    for p in PAGES:
        for kind, part in pieces(open(f"{ROOT}/{p}.html", encoding="utf-8").read()):
            items = []
            if kind == "txt" and need(part):
                items.append(part.strip())
            if kind == "tag":
                for m in ATTR.finditer(part):
                    if 'name="robots"' in part or 'name="viewport"' in part or 'charset' in part:
                        continue
                    if need(m.group(2)):
                        items.append(m.group(2))
            for s in items:
                if s not in seen:
                    seen.add(s); order.append(s)
    return order

def gemini(strings, lang):
    prompt = (f"Translate these website strings from English into {LANGS[lang]}. The site belongs to Agave Advisory Agency, "
              "a tequila export and private label agency in Jalisco, Mexico. Tone: restrained luxury, B2B, confident. "
              "Strings are in page order; some are fragments of one heading split by styling, translate them so they read naturally together. "
              "Keep brand and proper names (Agave Advisory, Los Altos de Jalisco, Guadalajara, IMPI, CRT, Blue Weber, EXW, FOB, CIF, HACCP) unchanged. "
              "Keep tequila categories (blanco, reposado, añejo, extra añejo, cristalino) as is. Keep the same capitalisation style. "
              "No em dashes, no trailing periods where the source has none. "
              "Input is a JSON object id → English string. Return a JSON object with the same ids → translation, every id present.\n\n" + json.dumps({str(i): t for i, t in enumerate(strings)}, ensure_ascii=False))
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}}
    import time
    res = None
    for attempt in range(8):
        model = ["gemini-flash-latest", "gemini-flash-lite-latest"][attempt % 2]
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}",
                                     data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        try:
            res = json.load(urllib.request.urlopen(req, timeout=600)); break
        except Exception as e:
            print("retry", model, e, flush=True); time.sleep(20)
    if res is None:
        raise SystemExit("gemini unavailable")
    obj = json.loads(res["candidates"][0]["content"]["parts"][0]["text"])
    return {t: obj[str(i)] for i, t in enumerate(strings) if str(i) in obj and isinstance(obj[str(i)], str)}

def translate(lang, strings):
    cache_f = f"{ROOT}/build/i18n_{lang}.json"
    cache = json.load(open(cache_f, encoding="utf-8")) if os.path.exists(cache_f) else {}
    todo = [s for s in strings if s not in cache]
    for rnd in range(3):  # недостающие строки догоняем повторными проходами
        todo = [s for s in strings if s not in cache]
        for i in range(0, len(todo), 60):
            cache.update(gemini(todo[i:i + 60], lang))
            json.dump(cache, open(cache_f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(lang, "cached", len(cache), "/", len(strings), flush=True)
        if not [s for s in strings if s not in cache]:
            break
    return cache

def localize(html, lang, tr, page):
    out = []
    for kind, part in pieces(html):
        if kind == "txt" and need(part):
            s = part.strip(); lead = part[:len(part) - len(part.lstrip())]; trail = part[len(part.rstrip()):]
            out.append(lead + tr.get(s, s) + trail)
        elif kind == "tag":
            part = ATTR.sub(lambda m: m.group(1) + (tr.get(m.group(2), m.group(2)) if need(m.group(2)) else m.group(2)) + m.group(3), part)
            # ссылки на страницы сайта остаются внутри языка
            part = re.sub(r'href="((?:' + "|".join(PAGES) + r')\.html(?:#[^"]*)?)"', lambda m: f'href="{lang}/{m.group(1)}"', part)
            out.append(part)
        else:
            out.append(part)
    html = "".join(out)
    html = html.replace('<html lang="en">', f'<html lang="{lang}">')
    html = html.replace("<head>", '<head>\n<base href="../">', 1)
    return html

def switcher(html, lang, page):
    """Переключатель EN · ES · RU рабочими ссылками и hreflang"""
    base = "" if lang == "en" else ""
    links = {"en": f"{page}.html", "es": f"es/{page}.html", "ru": f"ru/{page}.html"}
    sw = " · ".join((f"<b>{k.upper()}</b>" if k == lang else f'<a href="{v}" data-lang="{k}">{k.upper()}</a>') for k, v in links.items())
    html = re.sub(r'<span class="lang">.*?</span>(?=<a href="#contact")', f'<span class="lang">{sw}</span>', html, count=1)
    alt = "".join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k, v in links.items())
    return html.replace("</head>", alt + "\n</head>", 1)

if __name__ == "__main__":
    strings = collect(); print("strings", len(strings))
    for p in PAGES:
        f = f"{ROOT}/{p}.html"
        src = open(f, encoding="utf-8").read()  # сначала читаем, потом пишем: иначе open("w") обнулит файл
        open(f, "w", encoding="utf-8").write(switcher(src, "en", p))
    for lang in LANGS:
        tr = translate(lang, strings)
        os.makedirs(f"{ROOT}/{lang}", exist_ok=True)
        for p in PAGES:
            src = open(f"{ROOT}/{p}.html", encoding="utf-8").read()
            html = switcher(localize(src, lang, tr, p), lang, p)
            open(f"{ROOT}/{lang}/{p}.html", "w", encoding="utf-8").write(html)
        print(lang, "pages ok")
