"""Экспорт в Тильду: из собранных страниц делает по одному блоку кода (T123) на страницу.
Файлы сайта (стили, скрипты, шрифты, картинки, видео) остаются на внешнем хостинге BASE.
Запуск после build.py и i18n.py: python3 build/tilda.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://yurasnegovoy-hash.github.io/agave-advisory/"
PAGES = ["index", "about", "private-label", "bulk-tequila", "brand-market-advisory", "rtd", "barrel-aging", "how-we-work", "clients", "contact", "privacy"]
LANGS = ["en", "es", "ru"]
# приёмники заявок проекта 56941609 (Настройки сайта → Формы). Новый приёмник: добавить его ключ сюда и перезалить страницы.
# Ключ виден в редакторе любой родной формы: Контент → значение галочки сервиса (черновая страница page400817209)
FORM_SERVICES = [
    "84a04eb14732414162335bcb400d3e94",  # Tilda CRM «Agave Advisory: заявки с сайта»
    "9b182517268ede3eb7640f20b58edb07",  # Telegram, группа app-id -5320058829
]
OUT = f"{ROOT}/tilda"; os.makedirs(OUT, exist_ok=True)
ASSET = r"(?:img/|video/|vendor/|fonts/|fx\.js|map\.js|style\.css|fonts\.css|fx\.css|favicon)"

def url_of(lang, page):
    p = "" if page == "index" else page
    return "/" + "/".join(x for x in (("" if lang == "en" else lang), p) if x)

def link(m):
    lang = (m.group(1) or "en/").rstrip("/"); page = m.group(2); frag = m.group(3) or ""
    return f'href="{url_of(lang, page)}{frag}" data-page="1"'

def block(lang, page):
    src = open(f"{ROOT}/{'' if lang == 'en' else lang + '/'}{page}.html", encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", src).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', src).group(1)
    css = re.findall(r'<link rel="stylesheet" href="([^"]+)">', src)
    body = src[src.index("<body>") + 6:src.index("</body>")]
    k = body.index('<script>\nwindow.agaveTilda'); markup, scripts = body[:k], body[k:]
    fix = lambda t: re.sub(r'((?:src|poster|data-hd|data-sd|href)=")(' + ASSET + ")", r"\1" + BASE + r"\2", t).replace("url(img/", f"url({BASE}img/").replace("url(video/", f"url({BASE}video/")
    markup, scripts = fix(markup), fix(scripts)
    markup = re.sub(r'href="(es/|ru/)?(' + "|".join(PAGES) + r')\.html(#[^"]*)?"', link, markup)
    head = "".join(f'<link rel="stylesheet" href="{BASE}{h}">\n' for h in css)
    boot = ('<script>window.AGAVE_BASE="' + BASE + '";window.AGAVE_TILDA=1;document.documentElement.lang="' + lang + '";'
            '(function(){var r=document.getElementById("agave-root"),a=document.getElementById("allrecords")||r;'
            'while(r.firstChild)document.body.insertBefore(r.firstChild,a);document.body.classList.add("agave");})();</script>')
    # скрытая родная форма Тильды: наша форма передаёт в неё поля, заявки идут в приёмники сайта (Настройки сайта → Формы)
    inp = lambda n, t="text": f'<div class="t-input-group" data-field-name="{n}"><div class="t-input-block"><input type="{t}" name="{n}" class="t-input" value=""></div><div class="t-input-error"></div></div>'
    errs = "".join(f'<li class="t-form__errorbox-item js-rule-error js-rule-error-{r}"></li>' for r in ("all", "req", "email", "name", "phone", "minlength", "string"))
    tform = ('<div id="agave-tform-wrap" aria-hidden="true"><form id="agave-tform" name="agave-tform" role="form" action="" method="POST" data-formactiontype="2" '
             'data-inputbox=".t-input-group" class="t-form js-form-proccess" data-success-callback="agaveFormOk">'
             + "".join(f'<input type="hidden" name="formservices[]" value="{s}" class="js-formaction-services">' for s in FORM_SERVICES) +
             '<div class="js-successbox t-form__successbox" style="display:none;"></div><div class="t-form__inputsbox">'
             + inp("Name") + inp("Company") + inp("Email", "email") + inp("Phone", "tel") + inp("Service") + inp("Message") + inp("Language") + inp("Page")
             + f'<div class="t-form__errorbox-middle"><div class="js-errorbox-all t-form__errorbox-wrapper" style="display:none;"><ul class="t-form__errorbox-text">{errs}</ul></div></div>'
             '<div class="t-form__submit"><button class="t-submit" type="submit" tabindex="-1">Send</button></div></div></form></div>\n'
             '<script src="https://static.tildacdn.pub/js/tilda-forms-1.0.min.js" charset="utf-8"></script>\n')
    html = (f"<!-- Agave Advisory · {lang.upper()} · {page} · вставить в блок T123 «HTML-код» -->\n{head}"
            "<style>body.agave #allrecords{min-height:0!important;height:0;overflow:hidden}body.agave{margin:0}</style>\n"
            f'<div id="agave-root">{markup}</div>\n{tform}{boot}\n{scripts}')
    return title, desc, html

rows = []
for lang in LANGS:
    for page in PAGES:
        title, desc, html = block(lang, page)
        fn = f"{lang}_{page}.txt"; open(f"{OUT}/{fn}", "w", encoding="utf-8").write(html)
        rows.append((fn, url_of(lang, page), title, desc, len(html)))
        if (lang, page) in (("ru", "index"), ("en", "clients")):  # проверочная страница, похожая на Тильду
            t = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                 '<style>#allrecords a{color:#ff8562;text-decoration:none}#allrecords *{box-sizing:content-box}#allrecords{font-family:Arial;min-height:100vh;background:#fff}</style></head>'
                 f'<body class="t-body"><div id="allrecords" class="t-records"><div class="t-rec"><div class="t123"><div class="t-container_100"><div class="t-width t-width_100">{html}</div></div></div></div></div></body></html>')
            open(f"{OUT}/_test_{lang}_{page}.html", "w", encoding="utf-8").write(t)
man = ["СТРАНИЦЫ ДЛЯ ТИЛЬДЫ: файл с кодом → адрес страницы → заголовок и описание для настроек страницы", ""]
for fn, u, t, d, n in rows:
    man += [f"{fn}", f"  Адрес страницы: {u if u != '/' else '/  (главная, адрес не задаётся)'}", f"  Заголовок: {t}", f"  Описание: {d}", ""]
open(f"{OUT}/_СПИСОК_СТРАНИЦ.txt", "w", encoding="utf-8").write("\n".join(man))
print(len(rows), "blocks, max", max(r[4] for r in rows), "chars")
