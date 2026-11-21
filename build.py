#!/usr/bin/env python3
"""Agro Center saytını yığır: content/ qovluğundakı fayllardan _site/ qovluğuna hazır HTML.

Heç bir əlavə paket lazım deyil (yalnız Python 3). İşə salmaq:  python3 build.py
Məzmunu dəyişmək üçün bu fayla toxunmayın: content/ qovluğunu və ya admin paneli istifadə edin.
"""
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "_site"

LANGS = ["az", "en", "ru"]
LANG_NAMES = {"az": "AZ", "en": "EN", "ru": "RU"}
PREFIX = {"az": "", "en": "/en", "ru": "/ru"}
SLUGS = {
    "products": {"az": "mehsullar", "en": "products", "ru": "produkty"},
    "about": {"az": "haqqimizda", "en": "about", "ru": "o-nas"},
    "contact": {"az": "elaqe", "en": "contact", "ru": "kontakt"},
}

T = {
    "home": {"az": "Ana səhifə", "en": "Home", "ru": "Главная"},
    "products": {"az": "Məhsullar", "en": "Products", "ru": "Продукты"},
    "about": {"az": "Haqqımızda", "en": "About", "ru": "О нас"},
    "contact": {"az": "Əlaqə", "en": "Contact", "ru": "Контакты"},
    "call": {"az": "Zəng edin", "en": "Call us", "ru": "Позвонить"},
    "write_wa": {"az": "WhatsApp-a yazın", "en": "Message on WhatsApp", "ru": "Написать в WhatsApp"},
    "all_products": {"az": "Bütün məhsullar", "en": "All products", "ru": "Все продукты"},
    "featured": {"az": "Seçilmiş məhsullar", "en": "Featured products", "ru": "Избранные продукты"},
    "categories": {"az": "Kateqoriyalar", "en": "Categories", "ru": "Категории"},
    "price_on_request": {"az": "Qiymət üçün zəng edin", "en": "Call for price", "ru": "Цена по запросу"},
    "ask_product": {"az": "Bu məhsulu soruşun", "en": "Ask about this product", "ru": "Спросить о продукте"},
    "details": {"az": "Ətraflı", "en": "Details", "ru": "Подробнее"},
    "benefits": {"az": "Faydaları", "en": "Benefits", "ru": "Преимущества"},
    "package": {"az": "Qablaşdırma", "en": "Packaging", "ru": "Упаковка"},
    "price": {"az": "Qiymət", "en": "Price", "ru": "Цена"},
    "category": {"az": "Kateqoriya", "en": "Category", "ru": "Категория"},
    "phone": {"az": "Telefon", "en": "Phone", "ru": "Телефон"},
    "email": {"az": "E-poçt", "en": "Email", "ru": "Эл. почта"},
    "address": {"az": "Ünvan", "en": "Address", "ru": "Адрес"},
    "hours": {"az": "İş saatları", "en": "Opening hours", "ru": "Часы работы"},
    "map": {"az": "Xəritədə aç", "en": "Open in maps", "ru": "Открыть на карте"},
    "form_title": {"az": "Sorğu göndərin", "en": "Send a request", "ru": "Отправить запрос"},
    "form_note": {
        "az": "Forma WhatsApp-ı açır və mesajınızı hazır yazır. Sizə yalnız «Göndər» basmaq qalır.",
        "en": "The form opens WhatsApp with your message ready. You just press Send.",
        "ru": "Форма откроет WhatsApp с готовым сообщением. Останется нажать «Отправить».",
    },
    "f_name": {"az": "Adınız", "en": "Your name", "ru": "Ваше имя"},
    "f_product": {"az": "Hansı məhsul lazımdır?", "en": "Which product do you need?", "ru": "Какой продукт нужен?"},
    "f_qty": {"az": "Miqdar (məs. 10 kisə)", "en": "Quantity (e.g. 10 bags)", "ru": "Количество (напр. 10 мешков)"},
    "f_msg": {"az": "Əlavə qeyd", "en": "Notes", "ru": "Комментарий"},
    "f_send": {"az": "WhatsApp-da göndər", "en": "Send via WhatsApp", "ru": "Отправить в WhatsApp"},
    "wa_hello": {"az": "Salam, Agro Center!", "en": "Hello, Agro Center!", "ru": "Здравствуйте, Agro Center!"},
    "wa_product": {"az": "Bu məhsulla maraqlanıram", "en": "I'm interested in", "ru": "Меня интересует"},
    "contact_lead": {
        "az": "Ən tez cavabı telefonla və ya WhatsApp-da alırsınız.",
        "en": "The fastest way to reach us is by phone or WhatsApp.",
        "ru": "Быстрее всего — по телефону или в WhatsApp.",
    },
    "cta_title": {
        "az": "Hansı məhsul lazım olduğunu bilmirsiniz?",
        "en": "Not sure which product you need?",
        "ru": "Не знаете, какой продукт нужен?",
    },
    "cta_text": {
        "az": "Bitkinizi və sahənizi danışın, uyğun variantı birlikdə seçək.",
        "en": "Tell us about your crop and field, and we’ll choose together.",
        "ru": "Расскажите о культуре и участке — подберём вместе.",
    },
    "menu": {"az": "Menyu", "en": "Menu", "ru": "Меню"},
    "rights": {"az": "Bütün hüquqlar qorunur.", "en": "All rights reserved.", "ru": "Все права защищены."},
    "not_found": {"az": "Səhifə tapılmadı", "en": "Page not found", "ru": "Страница не найдена"},
    "back_home": {"az": "Ana səhifəyə qayıt", "en": "Back to home", "ru": "На главную"},
    "products_lead": {
        "az": "Qiymət və mövcudluq üçün zəng edin və ya WhatsApp-a yazın.",
        "en": "Call or message us on WhatsApp for prices and availability.",
        "ru": "О ценах и наличии узнавайте по телефону или в WhatsApp.",
    },
    "skip": {"az": "Məzmuna keç", "en": "Skip to content", "ru": "К содержимому"},
}

ICONS = {
    "sack": '<path d="M9 3h6l-1 3h-4z"/><path d="M10 6c-3 2-5 5-5 9a6 6 0 0 0 6 6h2a6 6 0 0 0 6-6c0-4-2-7-5-9"/><path d="M9 13h6M9 16h4"/>',
    "sprout": '<path d="M12 21v-9"/><path d="M12 12c0-4-3-6-7-6 0 4 3 6 7 6z"/><path d="M12 10c0-4 3-7 7-7 0 4-3 7-7 7z"/><path d="M7 21h10"/>',
    "shield": '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="M12 16c0-3 1-5 4-6-3 0-4 2-4 6zM12 16c0-2-1-3-3-4"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "chat": '<path d="M4 20l1.3-3.9A8 8 0 1 1 8 19z"/><path d="M9 10h.01M12 10h.01M15 10h.01"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def e(s):
    return html.escape(str(s or ""), quote=True)


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def tx(d, lang):
    """Mətni dilə görə götürür; boşdursa AZ variantına düşür."""
    if isinstance(d, dict):
        return d.get(lang) or d.get("az") or ""
    return d or ""


def paras(text):
    return "".join(f"<p>{e(p.strip())}</p>" for p in re.split(r"\n\s*\n", text or "") if p.strip())


def fmt_phone(p):
    d = re.sub(r"\D", "", p or "")
    if d.startswith("994") and len(d) == 12:
        return f"+994 {d[3:5]} {d[5:8]} {d[8:10]} {d[10:12]}"
    return p


def url(page, lang, slug=None):
    if page == "home":
        return PREFIX[lang] + "/"
    u = f"{PREFIX[lang]}/{SLUGS[page][lang]}/"
    return u + f"{slug}/" if slug else u


# ---------- data ----------
S = load("settings.json")
HOME = load("home.json")
ABOUT = load("about.json")
CATS = sorted(load("categories.json")["items"], key=lambda c: c.get("order", 99))
CAT_BY = {c["slug"]: c for c in CATS}
PRODUCTS = []
for f in sorted((CONTENT / "products").glob("*.json")):
    p = json.loads(f.read_text(encoding="utf-8"))
    p["slug"] = re.sub(r"[^a-z0-9-]", "-", (p.get("slug") or f.stem).lower()).strip("-")
    if p.get("visible", True):
        PRODUCTS.append(p)
PRODUCTS.sort(key=lambda p: ([c["slug"] for c in CATS].index(p.get("category")) if p.get("category") in CAT_BY else 99,
                             p.get("order", 99), tx(p["name"], "az")))

SITE = (S.get("site_url") or "https://agrocenter.az").rstrip("/")
PHONE = S.get("phone", "")
TEL = "tel:" + re.sub(r"[^\d+]", "", PHONE)
WA_NUM = re.sub(r"\D", "", S.get("whatsapp") or PHONE)


def wa_link(text):
    return f"https://wa.me/{WA_NUM}?text={quote(text)}"


# ---------- layout ----------
def product_visual(p, lang, cls="pv"):
    if p.get("image"):
        return (f'<div class="{cls}"><img src="{e(p["image"])}" alt="{e(tx(p["name"], lang))}" '
                f'loading="lazy" width="570" height="570"></div>')
    cat = CAT_BY.get(p.get("category"), {})
    return f'<div class="{cls} {cls}--empty cat-{e(cat.get("slug", ""))}">{icon(cat.get("icon", "sprout"), "pv-ic")}</div>'


def header(lang, active, alts):
    nav = "".join(
        f'<a href="{url(k, lang)}"{" aria-current=page" if k == active else ""}>{T[k][lang]}</a>'
        for k in ["home", "products", "about", "contact"])
    langs = "".join(
        f'<a href="{alts[l]}" hreflang="{l}" lang="{l}"{" aria-current=true" if l == lang else ""}>{LANG_NAMES[l]}</a>'
        for l in LANGS)
    return f'''<a class="skip" href="#main">{T["skip"][lang]}</a>
<header class="hdr">
  <div class="wrap hdr-in">
    <a class="brand" href="{url("home", lang)}"><img src="/assets/img/logo-sm.png" alt="" width="48" height="48"><span>Agro Center</span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">{icon("menu")}<span>{T["menu"][lang]}</span></button>
    <div class="nav-wrap" id="nav">
      <nav class="nav" aria-label="{T["menu"][lang]}">{nav}</nav>
      <div class="langs">{langs}</div>
      <a class="hdr-call" href="{TEL}">{icon("phone")}<span>{e(fmt_phone(PHONE))}</span></a>
    </div>
  </div>
</header>'''


def footer(lang):
    cats = "".join(f'<li><a href="{url("products", lang)}#{c["slug"]}">{e(tx(c["name"], lang))}</a></li>' for c in CATS)
    contact = [f'<li><a href="{TEL}">{e(fmt_phone(PHONE))}</a></li>',
               f'<li><a href="{wa_link(T["wa_hello"][lang])}">WhatsApp</a></li>']
    if S.get("email"):
        contact.append(f'<li><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></li>')
    addr = tx(S.get("address"), lang)
    if addr:
        contact.append(f"<li>{e(addr)}</li>")
    social = []
    for k, name in [("instagram", "Instagram"), ("facebook", "Facebook")]:
        if S.get(k):
            social.append(f'<li><a href="{e(S[k])}" rel="noopener">{name}</a></li>')
    social_html = f'<div><h2>{ {"az": "Sosial şəbəkələr", "en": "Social", "ru": "Соцсети"}[lang] }</h2><ul>{"".join(social)}</ul></div>' if social else ""
    return f'''<footer class="ftr">
  <div class="wrap ftr-in">
    <div class="ftr-brand"><img src="/assets/img/logo-sm.png" alt="Agro Center" width="72" height="72"><p>{e(tx(ABOUT["lead"], lang))}</p></div>
    <div><h2>{T["products"][lang]}</h2><ul>{cats}</ul></div>
    <div><h2>{T["contact"][lang]}</h2><ul>{"".join(contact)}</ul></div>
    {social_html}
  </div>
  <div class="wrap ftr-base">© {date.today().year} {e(S.get("company", "Agro Center"))}. {T["rights"][lang]}</div>
</footer>
<a class="fab" href="{wa_link(T["wa_hello"][lang])}" aria-label="{T["write_wa"][lang]}">{icon("chat")}</a>'''


def org_jsonld():
    d = {"@context": "https://schema.org", "@type": "Store", "name": "Agro Center",
         "legalName": S.get("company"), "url": SITE + "/", "logo": SITE + "/assets/img/logo.png",
         "image": SITE + "/assets/img/logo.png", "telephone": PHONE}
    if S.get("email"):
        d["email"] = S["email"]
    if tx(S.get("address"), "az"):
        d["address"] = {"@type": "PostalAddress", "streetAddress": tx(S["address"], "az"), "addressCountry": "AZ"}
    same = [S[k] for k in ("instagram", "facebook") if S.get(k)]
    if same:
        d["sameAs"] = same
    return json.dumps(d, ensure_ascii=False)


def page(lang, active, title, desc, body, alts, extra_head=""):
    full_title = f"{title} | Agro Center" if active != "home" else f"Agro Center — {title}"
    alt_links = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{alts[l]}">' for l in LANGS)
    alt_links += f'<link rel="alternate" hreflang="x-default" href="{SITE}{alts["az"]}">'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{alts[lang]}">
{alt_links}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{alts[lang]}">
<meta property="og:image" content="{SITE}/assets/img/logo.png">
<meta name="theme-color" content="#1d3a1a">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&family=Onest:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{org_jsonld()}</script>
{extra_head}
</head>
<body>
{header(lang, active, alts)}
<main id="main">
{body}
</main>
{footer(lang)}
<script src="/assets/main.js" defer></script>
</body>
</html>
'''


def alts_for(page_key, slug=None):
    return {l: url(page_key, l, slug) for l in LANGS}


def contact_buttons(lang, wa_text=None, big=False):
    cls = " btn--lg" if big else ""
    return (f'<div class="btns"><a class="btn btn--call{cls}" href="{TEL}">{icon("phone")}<span>{e(fmt_phone(PHONE))}</span></a>'
            f'<a class="btn btn--wa{cls}" href="{wa_link(wa_text or T["wa_hello"][lang])}">{icon("chat")}<span>{T["write_wa"][lang]}</span></a></div>')


def product_card(p, lang):
    pk = tx(p.get("package"), lang)
    price = p.get("price") or ""
    meta = f'<p class="pc-pack">{e(pk)}</p>' if pk else ""
    price_html = f'<p class="pc-price">{e(price)}</p>' if price else f'<p class="pc-price pc-price--ask">{T["price_on_request"][lang]}</p>'
    return f'''<li class="pc">
  <a href="{url("products", lang, p["slug"])}">
    {product_visual(p, lang)}
    <div class="pc-body"><h3>{e(tx(p["name"], lang))}</h3>{meta}{price_html}</div>
  </a>
</li>'''


def cta_band(lang):
    return f'''<section class="band">
  <div class="wrap band-in">
    <div><h2>{T["cta_title"][lang]}</h2><p>{T["cta_text"][lang]}</p></div>
    {contact_buttons(lang)}
  </div>
</section>'''


# ---------- pages ----------
def build_home(lang):
    feat = [p for p in PRODUCTS if p.get("featured")]
    for p in PRODUCTS:  # 4-dən azdırsa, hər kateqoriyadan bir məhsulla tamamla
        if len(feat) >= 4:
            break
        if p not in feat and p.get("category") not in {q.get("category") for q in feat}:
            feat.append(p)
    feat += [p for p in PRODUCTS if p not in feat][:max(0, 4 - len(feat))]
    hero_p = next((p for p in feat if p.get("image")), None)
    label = ""
    if hero_p:
        specs = "".join(f'<div><dt>{e(tx(s["label"], lang))}</dt><dd>{e(tx(s["value"], lang))}</dd></div>' for s in hero_p.get("specs", []))
        pk = tx(hero_p.get("package"), lang)
        if pk:
            specs += f'<div><dt>{T["package"][lang]}</dt><dd>{e(pk)}</dd></div>'
        label = f'''<a class="tag" href="{url("products", lang, hero_p["slug"])}">
      <img src="{e(hero_p["image"])}" alt="{e(tx(hero_p["name"], lang))}" width="570" height="570">
      <div class="tag-label"><p class="tag-name">{e(tx(hero_p["name"], lang))}</p><dl>{specs}</dl></div>
    </a>'''
    points = "".join(f'<li><h3>{e(tx(pt["title"], lang))}</h3><p>{e(tx(pt["text"], lang))}</p></li>' for pt in HOME.get("points", []))
    cats = "".join(f'''<li><a class="cat cat-{c["slug"]}" href="{url("products", lang)}#{c["slug"]}">
      {icon(c.get("icon", "sprout"), "cat-ic")}<span class="cat-name">{e(tx(c["name"], lang))}</span><span class="cat-desc">{e(tx(c["desc"], lang))}</span>
      <span class="cat-count">{sum(1 for p in PRODUCTS if p.get("category") == c["slug"])}</span></a></li>''' for c in CATS)
    body = f'''<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-text">
      <h1>{e(tx(HOME["hero_title"], lang))}</h1>
      <p class="lead">{e(tx(HOME["hero_text"], lang))}</p>
      {contact_buttons(lang, big=True)}
    </div>
    {label}
  </div>
</section>
<section class="points"><div class="wrap"><ul class="points-list">{points}</ul></div></section>
<section class="sec">
  <div class="wrap">
    <h2 class="sec-title">{T["categories"][lang]}</h2>
    <ul class="cats">{cats}</ul>
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    <div class="sec-head"><h2 class="sec-title">{T["featured"][lang]}</h2><a class="more" href="{url("products", lang)}">{T["all_products"][lang]}</a></div>
    <ul class="grid">{"".join(product_card(p, lang) for p in feat[:8])}</ul>
  </div>
</section>
{cta_band(lang)}'''
    return page(lang, "home", tx(HOME["hero_title"], lang), tx(HOME["hero_text"], lang), body, alts_for("home"))


def build_products(lang):
    chips = "".join(f'<a href="#{c["slug"]}">{e(tx(c["name"], lang))}</a>' for c in CATS)
    sections = ""
    for c in CATS:
        items = [p for p in PRODUCTS if p.get("category") == c["slug"]]
        if not items:
            continue
        sections += f'''<section class="cat-sec" id="{c["slug"]}">
  <div class="cat-sec-head">{icon(c.get("icon", "sprout"), "cat-ic")}<div><h2>{e(tx(c["name"], lang))}</h2><p>{e(tx(c["desc"], lang))}</p></div></div>
  <ul class="grid">{"".join(product_card(p, lang) for p in items)}</ul>
</section>'''
    body = f'''<section class="phead"><div class="wrap">
  <h1>{T["products"][lang]}</h1><p class="lead">{T["products_lead"][lang]}</p>
  <nav class="chips" aria-label="{T["categories"][lang]}">{chips}</nav>
</div></section>
<div class="wrap">{sections}</div>
{cta_band(lang)}'''
    return page(lang, "products", T["products"][lang],
                ", ".join(tx(c["name"], lang) for c in CATS) + ". " + T["products_lead"][lang], body, alts_for("products"))


def build_product(lang, p):
    name = tx(p["name"], lang)
    cat = CAT_BY.get(p.get("category"))
    rows = ""
    if cat:
        rows += f'<div><dt>{T["category"][lang]}</dt><dd><a href="{url("products", lang)}#{cat["slug"]}">{e(tx(cat["name"], lang))}</a></dd></div>'
    for s in p.get("specs", []):
        rows += f'<div><dt>{e(tx(s["label"], lang))}</dt><dd>{e(tx(s["value"], lang))}</dd></div>'
    if tx(p.get("package"), lang):
        rows += f'<div><dt>{T["package"][lang]}</dt><dd>{e(tx(p["package"], lang))}</dd></div>'
    rows += f'<div><dt>{T["price"][lang]}</dt><dd>{e(p.get("price")) or T["price_on_request"][lang]}</dd></div>'
    wa_text = f'{T["wa_hello"][lang]} {T["wa_product"][lang]}: {name}'
    related = [q for q in PRODUCTS if q.get("category") == p.get("category") and q["slug"] != p["slug"]][:4]
    rel_html = (f'<section class="sec"><div class="wrap"><h2 class="sec-title">{e(tx(cat["name"], lang)) if cat else ""}</h2>'
                f'<ul class="grid">{"".join(product_card(q, lang) for q in related)}</ul></div></section>') if related else ""
    desc = tx(p.get("description"), lang)
    feats = [f.strip(" -•✅\t") for f in tx(p.get("features"), lang).splitlines() if f.strip(" -•✅\t")]
    features_html = (f'<h2 class="pd-sub">{T["benefits"][lang]}</h2><ul class="feats">'
                     + "".join(f"<li>{e(f)}</li>" for f in feats) + "</ul>") if feats else ""
    jsonld = {"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc,
              "brand": {"@type": "Brand", "name": "Agro Center"}}
    if p.get("image"):
        jsonld["image"] = SITE + p["image"]
    body = f'''<div class="wrap crumbs"><a href="{url("products", lang)}">{T["products"][lang]}</a>{f' / <a href="{url("products", lang)}#{cat["slug"]}">{e(tx(cat["name"], lang))}</a>' if cat else ""}</div>
<section class="pd"><div class="wrap pd-in">
  {product_visual(p, lang, "pd-v")}
  <div class="pd-text">
    <h1>{e(name)}</h1>
    {paras(desc)}
    {features_html}
    <dl class="specs">{rows}</dl>
    <p class="pd-ask">{T["ask_product"][lang]}</p>
    {contact_buttons(lang, wa_text)}
  </div>
</div></section>
{rel_html}'''
    return page(lang, "products", name, desc[:160], body, alts_for("products", p["slug"]),
                f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>')


def build_about(lang):
    body = f'''<section class="phead"><div class="wrap"><h1>{e(tx(ABOUT["title"], lang))}</h1></div></section>
<section class="sec"><div class="wrap prose">
  <p class="lead">{e(tx(ABOUT["lead"], lang))}</p>
  {paras(tx(ABOUT["body"], lang))}
</div></section>
{cta_band(lang)}'''
    return page(lang, "about", tx(ABOUT["title"], lang), tx(ABOUT["lead"], lang), body, alts_for("about"))


def build_contact(lang):
    items = [f'<li>{icon("phone")}<div><h2>{T["phone"][lang]}</h2><a href="{TEL}">{e(fmt_phone(PHONE))}</a></div></li>',
             f'<li>{icon("chat")}<div><h2>WhatsApp</h2><a href="{wa_link(T["wa_hello"][lang])}">{e(fmt_phone(S.get("whatsapp") or PHONE))}</a></div></li>']
    if S.get("email"):
        items.append(f'<li>{icon("mail")}<div><h2>{T["email"][lang]}</h2><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></div></li>')
    if tx(S.get("address"), lang):
        m = f'<a href="{e(S["map_link"])}" rel="noopener">{T["map"][lang]}</a>' if S.get("map_link") else ""
        items.append(f'<li>{icon("pin")}<div><h2>{T["address"][lang]}</h2><p>{e(tx(S["address"], lang))}</p>{m}</div></li>')
    if tx(S.get("hours"), lang):
        items.append(f'<li>{icon("clock")}<div><h2>{T["hours"][lang]}</h2><p>{e(tx(S["hours"], lang))}</p></div></li>')
    options = "".join(f'<option>{e(tx(p["name"], lang))}</option>' for p in PRODUCTS)
    body = f'''<section class="phead"><div class="wrap"><h1>{T["contact"][lang]}</h1><p class="lead">{T["contact_lead"][lang]}</p></div></section>
<section class="sec"><div class="wrap contact">
  <ul class="clist">{"".join(items)}</ul>
  <form class="form" id="wa-form" data-wa="{WA_NUM}" data-hello="{e(T["wa_hello"][lang])}">
    <h2>{T["form_title"][lang]}</h2>
    <p class="form-note">{T["form_note"][lang]}</p>
    <label>{T["f_name"][lang]}<input name="name" autocomplete="name" required></label>
    <label>{T["f_product"][lang]}<input name="product" list="plist"></label>
    <datalist id="plist">{options}</datalist>
    <label>{T["f_qty"][lang]}<input name="qty"></label>
    <label>{T["f_msg"][lang]}<textarea name="msg" rows="4"></textarea></label>
    <button class="btn btn--wa" type="submit">{icon("chat")}<span>{T["f_send"][lang]}</span></button>
  </form>
</div></section>'''
    return page(lang, "contact", T["contact"][lang], f'{T["contact_lead"][lang]} {fmt_phone(PHONE)}', body, alts_for("contact"))


def build_404():
    lang = "az"
    body = f'''<section class="phead"><div class="wrap"><h1>{T["not_found"][lang]}</h1>
<p class="lead"><a href="/">{T["back_home"][lang]}</a> · <a href="/en/">Home</a> · <a href="/ru/">Главная</a></p></div></section>'''
    return page(lang, "404", T["not_found"][lang], "", body, alts_for("home"))


def redirect(to):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>Agro Center</title>'
            f'<link rel="canonical" href="{SITE}{to}"><meta http-equiv="refresh" content="0; url={to}">'
            f'<meta name="robots" content="noindex"></head><body><a href="{to}">{to}</a></body></html>')


def write(rel, text):
    path = OUT / rel.lstrip("/")
    if rel.endswith("/"):
        path = path / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    urls = []
    for lang in LANGS:
        for key, fn in [("home", build_home), ("products", build_products), ("about", build_about), ("contact", build_contact)]:
            u = url(key, lang)
            write(u, fn(lang))
            urls.append(u)
        for p in PRODUCTS:
            u = url("products", lang, p["slug"])
            write(u, build_product(lang, p))
            urls.append(u)
    write("/404.html", build_404())
    # köhnə saytın linkləri yeni səhifələrə yönəlsin
    old = {"index.html": "/", "mehsullar.html": "/mehsullar/", "haqqimizda.html": "/haqqimizda/", "elaqe.html": "/elaqe/",
           "admin.html": "/", "en/index.html": None, "en/products.html": "/en/products/", "en/about.html": "/en/about/",
           "en/contact.html": "/en/contact/", "ru/index.html": None, "ru/produkty.html": "/ru/produkty/",
           "ru/o-nas.html": "/ru/o-nas/", "ru/kontakt.html": "/ru/kontakt/"}
    # Netlify üçün: köhnə .html linkləri 301 ilə yönləndir (səhifə ilə eyni adlı fayl yaratmırıq ki, döngə olmasın)
    rules = [f"/{src}  {to}  301" for src, to in old.items() if to and not src.endswith("index.html")]
    write("/_redirects", "\n".join(rules) + "\n")
    for src, to in old.items():
        clash = (OUT / src.replace(".html", "")).is_dir()
        if to and not clash and not (OUT / src).exists():
            write("/" + src, redirect(to))
    today = date.today().isoformat()
    sm = "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    domain = re.sub(r"^https?://", "", SITE).split("/")[0]
    write("/CNAME", domain + "\n")
    write("/.nojekyll", "")
    print(f"Hazırdır: {len(urls)} səhifə, {len(PRODUCTS)} məhsul -> {OUT}")


if __name__ == "__main__":
    main()
