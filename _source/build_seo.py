"""Build the GitHub Pages site (RU root, /uz/, /en/) with full SEO head, robots.txt, sitemap.xml."""
import json, os, re, shutil

SITE = "https://aquadiamond.uz"
TODAY = "2026-11-17"
OUT = "site"
PHONE = "+998 99 369 07 70"
_cfg = open("page.html", encoding="utf-8").read()
def _cv(key):
    m = re.search(key + r': "([^"]*)"', _cfg)
    return m.group(1) if m else ""
INN, LEGAL_ADDR, TG = _cv("inn"), _cv("legalAddress"), _cv("telegram")
PHONE_E164 = "+998993690770"

src = open("page.html", encoding="utf-8").read()
i = src.index('<header class="top">')
head_src, body = src[:i], src[i:]
# drop artifact-only bits from the head; keep fonts and the stylesheet
head_src = re.sub(r"<title>.*?</title>\n", "", head_src)
head_src = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n', "", head_src)
head_src = re.sub(r'<meta name="description"[^>]*>\n', "", head_src)

LANGS = {
    "ru": {
        "path": "/", "locale": "ru_RU", "name": "Русский",
        "title": "AQUADIAMOND — Производство напитков в Узбекистане",
        "desc": "AQUADIAMOND — производитель безалкогольных напитков в Узбекистане. Контрактный розлив энергетиков, лимонадов и газированных напитков. Производство Private Label, разработка рецептур и упаковки.",
        "kw": "Aqua Diamond, Aquadiamond, производитель напитков Узбекистан, производство напитков Ташкент, контрактный розлив напитков, производство энергетиков, производство лимонадов, Private Label Uzbekistan",
        "service": "Контрактный розлив напитков (Private Label)",
        "service_desc": "Розлив энергетиков, лимонадов и газированных напитков в алюминиевую банку 0,33 л, 0,33 л slim и 0,45 л под торговой маркой заказчика: рецептура, дизайн банки, сырьё и тара, розлив, маркировка Asl belgisi, отгрузка.",
        "water": "Розлив питьевой воды в бутыли 5, 10 и 19 л",
        "addr": "Ташкент", "home": "Главная", "og_alt": "AQUADIAMOND: контрактный розлив напитков в банку, Ташкент",
    },
    "uz": {
        "path": "/uz/", "locale": "uz_UZ", "name": "O'zbekcha",
        "title": "AQUADIAMOND — O'zbekistonda ichimliklar ishlab chiqarish",
        "desc": "AQUADIAMOND — O'zbekistondagi alkogolsiz ichimliklar ishlab chiqaruvchi korxona. Energetik, limonad va gazli ichimliklarni shartnoma asosida quyish, Private Label ishlab chiqarish, retsept va qadoq ishlab chiqish.",
        "kw": "Aqua Diamond, Aquadiamond, ichimlik ishlab chiqarish, ichimliklar ishlab chiqaruvchi korxona, ichimliklar zavodi Toshkent, shartnoma asosida quyish, energetik ishlab chiqarish, limonad ishlab chiqarish, Private Label Uzbekistan",
        "service": "Ichimliklarni shartnoma asosida quyish (Private Label)",
        "service_desc": "Energetik, limonad va gazli ichimliklarni buyurtmachi savdo belgisi ostida 0,33 l, 0,33 l slim va 0,45 l alyuminiy bankaga quyish: retsept, banka dizayni, xomashyo va idish, quyish, Asl belgisi markirovkasi, jo'natish.",
        "water": "Ichimlik suvini 5, 10 va 19 l idishlarga quyish",
        "addr": "Toshkent", "home": "Bosh sahifa", "og_alt": "AQUADIAMOND: ichimliklarni bankaga shartnoma asosida quyish, Toshkent",
    },
    "en": {
        "path": "/en/", "locale": "en_US", "name": "English",
        "title": "AQUADIAMOND — Beverage Manufacturer in Uzbekistan",
        "desc": "AQUADIAMOND is a soft drink manufacturer in Uzbekistan offering beverage contract manufacturing: energy drinks, lemonades and sodas, private label production, recipe and packaging development.",
        "kw": "Aqua Diamond, Aqua Diamond Uzbekistan, Aquadiamond, beverage manufacturer Uzbekistan, beverage contract manufacturing, private label Uzbekistan, energy drink manufacturer, soft drink co-packer",
        "service": "Beverage contract manufacturing (private label)",
        "service_desc": "Filling of energy drinks, lemonades and sodas in 0.33 L, 0.33 L slim and 0.45 L aluminium cans under the client's brand: recipe, can design, ingredients and packaging, filling, Asl belgisi marking, shipping.",
        "water": "Drinking water filling in 5, 10 and 19 L bottles",
        "addr": "Tashkent", "home": "Home", "og_alt": "AQUADIAMOND: contract beverage filling in cans, Tashkent",
    },
}
COUNTRY_NAMES = ["Uzbekistan", "Kazakhstan", "Kyrgyzstan", "Tajikistan", "Turkmenistan", "Russia", "Germany", "France", "Sweden", "Lithuania", "Latvia", "South Korea", "United States"]

# ---- owner settings: leave empty until real IDs exist (see SEO-SETUP.md) ----
GSC_VERIFY = ""      # Google Search Console: content="..." of the HTML-tag method
YANDEX_VERIFY = ""   # Яндекс Вебмастер: content="..." of the meta-tag method


def jsonld(code, L):
    url = SITE + L["path"]
    ORG = SITE + "/#org"
    graph = [
        {
            "@type": "Organization", "@id": ORG,
            "name": "AQUADIAMOND", "alternateName": ["Aqua Diamond", "Aquadiamond", "AQUA DIAMOND", "ООО «AQUADIAMOND»"],
            "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/img/brand/logo-512.jpg", "width": 512, "height": 512},
            "image": SITE + "/og-image.png",
            "description": L["desc"],
            "telephone": PHONE_E164,
            **({"taxID": INN} if INN else {}),
            "address": {"@type": "PostalAddress", "addressLocality": L["addr"], "addressCountry": "UZ", **({"streetAddress": LEGAL_ADDR} if LEGAL_ADDR else {})},
            "areaServed": [{"@type": "Country", "name": c} for c in COUNTRY_NAMES],
            "brand": [
                {"@type": "Brand", "name": "Moxito", "sameAs": ["https://www.instagram.com/moxito_uzz/"]},
                {"@type": "Brand", "name": "ZAM ZAM", "sameAs": ["https://www.instagram.com/zamzam.aquadiamond/"]},
            ],
            "sameAs": ["https://www.instagram.com/moxito_uzz/", "https://www.facebook.com/people/Moxito-Uzbekistan/61558806222763/", *([f"https://t.me/{TG}"] if TG else [])],
            "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_E164, "contactType": "sales", "areaServed": "UZ", "availableLanguage": ["ru", "uz", "en"]},
            "knowsAbout": ["contract beverage manufacturing", "private label beverages", "energy drinks", "lemonades", "carbonated soft drinks", "aluminium can filling", "bottled drinking water"],
        },
        {"@type": "WebSite", "@id": SITE + "/#website", "name": "AQUADIAMOND", "alternateName": "Aqua Diamond", "url": SITE + "/", "publisher": {"@id": ORG}, "inLanguage": ["ru", "uz", "en"]},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": L["title"], "description": L["desc"], "inLanguage": code,
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": ORG}, "primaryImageOfPage": SITE + "/og-image.png", "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": L["home"], "item": url}]},
        {"@type": "Service", "@id": url + "#contract-filling", "name": L["service"], "description": L["service_desc"], "serviceType": "Contract beverage manufacturing",
         "provider": {"@id": ORG}, "areaServed": [{"@type": "Country", "name": c} for c in COUNTRY_NAMES],
         "offers": {"@type": "Offer", "priceCurrency": "UZS",
                    "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": 700, "priceCurrency": "UZS", "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitText": "can"}},
                    "eligibleQuantity": {"@type": "QuantitativeValue", "minValue": 12000, "unitText": "cans"}}},
        {"@type": "Service", "@id": url + "#water-filling", "name": L["water"], "serviceType": "Bottled water filling", "provider": {"@id": ORG}, "areaServed": {"@type": "Country", "name": "Uzbekistan"}},
    ]
    return f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>\n<!--FAQ_JSONLD-->'


def head(code, L):
    url = SITE + L["path"]
    alts = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{SITE + X["path"]}">' for c, X in LANGS.items())
    og_alts = "\n".join(f'<meta property="og:locale:alternate" content="{X["locale"]}">' for c, X in LANGS.items() if c != code)
    verify = (f'<meta name="google-site-verification" content="{GSC_VERIFY}">\n' if GSC_VERIFY else "") + (f'<meta name="yandex-verification" content="{YANDEX_VERIFY}">\n' if YANDEX_VERIFY else "")
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{L["title"]}</title>
<meta name="description" content="{L["desc"]}">
<meta name="keywords" content="{L["kw"]}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta name="theme-color" content="#08798a">
<meta name="format-detection" content="telephone=yes">
<meta name="geo.region" content="UZ-TK">
<meta name="geo.placename" content="Tashkent">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" as="image" href="/img/mustang-classic.webp" type="image/webp">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AQUADIAMOND">
<meta property="og:title" content="{L["title"]}">
<meta property="og:description" content="{L["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{L["og_alt"]}">
<meta property="og:locale" content="{L["locale"]}">
{og_alts}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{L["title"]}">
<meta name="twitter:description" content="{L["desc"]}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="twitter:image:alt" content="{L["og_alt"]}">
{verify}{jsonld(code, L)}
<script src="/analytics.js" defer></script>
"""


def page(code, L):
    base = "./" if L["path"] == "/" else "../"
    h = (head(code, L).replace('href="/favicon', f'href="{base}favicon').replace('href="/apple-touch-icon', f'href="{base}apple-touch-icon')
         .replace('href="/site.webmanifest', f'href="{base}site.webmanifest').replace('href="/img/', f'href="{base}img/').replace('src="/analytics.js"', f'src="{base}analytics.js"'))
    bod = body.replace('src="img/', f'src="{base}img/').replace('srcset="img/', f'srcset="{base}img/').replace(', img/brand/', f', {base}img/brand/')
    for c, p in (("ru", ""), ("uz", "uz/"), ("en", "en/")):
        bod = bod.replace(f'href="{p or "./"}" hreflang="{c}"', f'href="{base}{p}" hreflang="{c}"')
    return f'<!DOCTYPE html>\n<html lang="{code}" data-lang="{code}" data-base="{base}">\n<head>\n{h}{head_src}</head>\n<body>\n{bod}</body>\n</html>\n'


if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)
for code, L in LANGS.items():
    d = os.path.join(OUT, L["path"].strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(code, L))

open(os.path.join(OUT, "robots.txt"), "w").write(f"""# AQUADIAMOND: весь публичный контент открыт для поисковых и AI-роботов
User-agent: *
Allow: /

# AI-поиск и ассистенты (явно разрешены)
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""")

# ---------- privacy policy pages ----------
import privacy_content as PC
PRIV_CSS = """:root{--bg:#eef5f5;--surface:#fff;--ink:#0b2629;--muted:#4b6669;--line:#cfdfe0;--accent:#08798a}
@media (prefers-color-scheme:dark){:root{--bg:#051719;--surface:#0c2427;--ink:#e4f2f1;--muted:#93b3b2;--line:#1b3c3f;--accent:#3cc9d9;color-scheme:dark}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:400 17px/1.65 "Golos Text",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:780px;margin:0 auto;padding:28px max(20px,env(safe-area-inset-right,0px)) 64px max(20px,env(safe-area-inset-left,0px))}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding-bottom:20px;border-bottom:1px solid var(--line);margin-bottom:32px}
header a{color:var(--accent);font-weight:600;text-decoration:none}nav.l{display:flex;gap:12px;font:500 13px/1 "JetBrains Mono",monospace}
nav.l a[aria-current]{color:var(--ink)}
h1{font:800 italic clamp(40px,7vw,64px)/.9 "Sofia Sans Extra Condensed","Arial Narrow",Impact,sans-serif;text-transform:uppercase;margin:0 0 12px;text-wrap:balance}
.ver{font:500 13px/1.4 "JetBrains Mono",monospace;color:var(--muted);margin:0 0 32px}
h2{font-size:20px;margin:36px 0 10px}p{margin:0 0 12px;color:var(--ink)}a{color:var(--accent)}
footer{margin-top:48px;padding-top:20px;border-top:1px solid var(--line);font-size:14px;color:var(--muted)}"""
def privacy(code):
    base = "../" if code == "ru" else "../../"
    home = {"ru": base, "uz": base + "uz/", "en": base + "en/"}[code]
    inn = {"ru": f", ИНН {INN}", "uz": f", STIR {INN}", "en": f", TIN {INN}"}[code] if INN else ""
    addr = LEGAL_ADDR or {"ru": "г. Ташкент, Республика Узбекистан", "uz": "Toshkent sh., O'zbekiston Respublikasi", "en": "Tashkent, Republic of Uzbekistan"}[code]
    op = {"ru": "ООО «AQUADIAMOND»", "uz": "«AQUADIAMOND» MChJ", "en": "AQUADIAMOND LLC"}[code]
    tg = f'<a href="https://t.me/{TG}">@{TG}</a>' if TG else ""
    fill = dict(op=op, inn_ru=inn, inn_uz=inn, inn_en=inn, addr=addr, phone=PHONE, tg=tg)
    body = "".join(f"<h2>{h}</h2>{t.format(**fill)}" for h, t in PC.SECTIONS[code])
    path = {"ru": "/privacy/", "uz": "/uz/privacy/", "en": "/en/privacy/"}[code]
    alts = "".join(f'<link rel="alternate" hreflang="{c}" href="{SITE}{p}">' for c, p in (("ru", "/privacy/"), ("uz", "/uz/privacy/"), ("en", "/en/privacy/")))
    langs = "".join(f'<a href="{base}{p}privacy/"{" aria-current=page" if c == code else ""}>{c.upper()}</a>' for c, p in (("ru", ""), ("uz", "uz/"), ("en", "en/")))
    return f"""<!DOCTYPE html>
<html lang="{code}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{PC.TITLE[code]} | AQUADIAMOND</title><meta name="description" content="{PC.DESC[code]}">
<link rel="canonical" href="{SITE}{path}">{alts}<link rel="icon" href="{base}favicon-32.png" sizes="32x32" type="image/png">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;600&family=JetBrains+Mono:wght@500&family=Sofia+Sans+Extra+Condensed:ital,wght@1,800&display=swap">
<style>{PRIV_CSS}</style>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": [
  {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": PC.TITLE[code], "inLanguage": code, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#org"}},
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": {"ru": "Главная", "uz": "Bosh sahifa", "en": "Home"}[code], "item": SITE + {"ru": "/", "uz": "/uz/", "en": "/en/"}[code]},
    {"@type": "ListItem", "position": 2, "name": PC.TITLE[code], "item": SITE + path}]}]}, ensure_ascii=False)}</script></head>
<body><div class="wrap"><header><a href="{home}" style="display:flex;align-items:center;gap:10px"><img src="{base}img/brand/emblem-96.webp" width="36" height="36" alt="" style="border-radius:9px">{PC.BACK[code]}</a><nav class="l">{langs}</nav></header>
<h1>{PC.TITLE[code]}</h1><p class="ver">{PC.VERSION[code]}</p>{body}
<footer>{op}{inn} · {addr} · {PHONE}</footer></div></body></html>
"""
for code, p in (("ru", "privacy"), ("uz", "uz/privacy"), ("en", "en/privacy")):
    os.makedirs(os.path.join(OUT, p), exist_ok=True)
    open(os.path.join(OUT, p, "index.html"), "w", encoding="utf-8").write(privacy(code))

urls = []
for code, L in LANGS.items():
    links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{c}" href="{SITE + X["path"]}"/>' for c, X in LANGS.items())
    urls.append(f"""  <url>
    <loc>{SITE + L["path"]}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{"1.0" if code == "ru" else "0.8"}</priority>{links}
    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>
  </url>""")
for code, p in (("ru", "/privacy/"), ("uz", "/uz/privacy/"), ("en", "/en/privacy/")):
    urls.append(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>yearly</changefreq>\n    <priority>0.3</priority>\n  </url>")
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")

open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({
    "name": "AQUADIAMOND", "short_name": "AQUADIAMOND", "start_url": "/", "display": "browser",
    "background_color": "#eef5f5", "theme_color": "#08798a",
    "icons": [{"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/favicon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))


open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write("""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Страница не найдена | AQUADIAMOND</title><meta name="robots" content="noindex">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<style>:root{--bg:#eef5f5;--ink:#0b2629;--muted:#4b6669;--accent:#08798a}@media (prefers-color-scheme:dark){:root{--bg:#051719;--ink:#e4f2f1;--muted:#93b3b2;--accent:#3cc9d9}}
body{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--bg);color:var(--ink);font:400 17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;padding:24px}
main{max-width:520px;display:grid;gap:16px}b{font:800 italic 96px/.9 "Arial Narrow",Impact,sans-serif;color:var(--accent)}p{margin:0;color:var(--muted)}a{color:var(--accent);font-weight:600}</style></head>
<body><main><img src="/img/brand/logo-320.webp" width="120" height="120" alt="AQUA DIAMOND" style="border-radius:16px"><b>404</b><p>Такой страницы нет. Bunday sahifa yo'q. Page not found.</p>
<p><a href="/">aquadiamond.uz</a> · +998 99 369 07 70</p></main></body></html>
""")
shutil.copytree("img", os.path.join(OUT, "img"))
print("built", sorted(os.listdir(OUT)))

# favicons from the logo emblem
from PIL import Image as _Im
_em = _Im.open("brand-src/emblem-512.png").convert("RGB")
for _s, _n in [(32, "favicon-32.png"), (192, "favicon-192.png"), (512, "favicon-512.png"), (180, "apple-touch-icon.png")]:
    _em.resize((_s, _s), _Im.LANCZOS).save(os.path.join(OUT, _n), optimize=True)
_em.save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# ---------- llms.txt: short factual profile for AI search ----------
open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(f"""# AQUADIAMOND (Aqua Diamond)

> AQUADIAMOND LLC (ООО «AQUADIAMOND», Aqua Diamond, Aquadiamond) is a soft drink manufacturer in Tashkent, Uzbekistan. It offers beverage contract manufacturing (private label): energy drinks, lemonades and carbonated soft drinks filled in aluminium cans under the client's brand, plus drinking water in PET bottles. Own brands: Moxito (non-alcoholic sparkling mojito) and ZAM ZAM (drinking water).

## Company facts
- Legal name: ООО «AQUADIAMOND» (AQUADIAMOND LLC){f"; TIN (ИНН): {INN}" if INN else ""}
- Location: Tashkent, Uzbekistan{f" — {LEGAL_ADDR}" if LEGAL_ADDR else ""}
- Website: {SITE}/ (Russian), {SITE}/uz/ (Uzbek), {SITE}/en/ (English)
- Sales phone: {PHONE}
- Telegram: {"https://t.me/" + TG if TG else "—"}
- Instagram: https://www.instagram.com/moxito_uzz/ (Moxito), https://www.instagram.com/zamzam.aquadiamond/ (ZAM ZAM)

## Production
- 3 filling lines; one line fills more than 300,000 cans per day
- Minimum contract batch: 12,000 cans
- Indicative contract filling price: from 700 UZS per can (final price depends on recipe, can format, design and volume)
- More than 20 million cans produced; more than 50 ready flavours
- Cans: 0.33 L standard, 0.33 L slim, 0.45 L (aluminium)
- Still drinking water: 5 L, 10 L and 19 L PET bottles
- Marking: Asl belgisi (Uzbekistan national digital product marking)

## Services (turnkey)
Recipe development, flavour approval, can design, sourcing of ingredients and packaging, filling, quality control, Asl belgisi marking, documents, pallet shipping in Uzbekistan and for export.

## Export
12 countries: Kazakhstan, Kyrgyzstan, Tajikistan, Turkmenistan, Russia, Germany, France, Sweden, Lithuania, Latvia, South Korea, United States.

## Brands filled on the line (portfolio)
Mustang Energy (Classic, Exotic; 0.45 L), Anarfresh (pomegranate; 0.45 L and 0.33 L), Xurmofresh (date; 0.45 L), Moxito (Lime & Mint, Lime & Strawberry; 0.45 L), ZAM ZAM water (5 L, 10 L).
Clients named on the site: Chernogolovka, Big Beer, La Cuba, Khabeeb, Anar Fresh, Via Life.

## FAQ
- Minimum batch? 12,000 cans per filling run.
- Price? From 700 UZS per can.
- Own recipe possible? Yes, or a flavour developed from 50+ ready ones.
- Private label? Yes: energy drinks, lemonades and sodas under the client's brand.
- Export? Yes, to 12 countries.

## Pages
- [Главная (RU)]({SITE}/): контрактный розлив напитков, производство в Ташкенте
- [Bosh sahifa (UZ)]({SITE}/uz/)
- [Home (EN)]({SITE}/en/)
- [Privacy policy]({SITE}/privacy/)
""")

# ---------- analytics.js: loads GA4 / Yandex Metrika only when real IDs are filled in ----------
open(os.path.join(OUT, "analytics.js"), "w", encoding="utf-8").write("""/* AQUADIAMOND — analytics loader.
 * Впишите реальные идентификаторы и отправьте сайт на GitHub (push.bat).
 * Пока строки пустые, ничего не загружается и никаких cookies не ставится.
 * ВАЖНО: перед включением обновите раздел 2 Политики конфиденциальности —
 * сейчас там написано, что сайт не использует аналитические cookie.
 */
var GA4_ID = "";        // Google Analytics 4: вида "G-XXXXXXXXXX"
var YM_ID  = "";        // Яндекс Метрика: номер счётчика, только цифры

(function () {
  if (GA4_ID) {
    var s = document.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date()); gtag("config", GA4_ID);
  }
  if (YM_ID) {
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date();
      k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })
      (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
    ym(Number(YM_ID), "init", { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false });
  }
})();
""")
shutil.copy("SEO-SETUP.md", os.path.join(OUT, "SEO-SETUP.md"))
