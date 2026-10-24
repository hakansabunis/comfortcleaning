"""Static generator for groupcomfortcleaning.com.

Run from anywhere with `python _build/build.py`. Writes az/, ru/, en/ pages and sitemap.xml.
The underscore folder is not published by GitHub Pages.
"""
import html
import json
import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content_az import C as AZ  # noqa: E402
from content_en import C as EN  # noqa: E402
from content_ru import C as RU  # noqa: E402

SITE = "https://groupcomfortcleaning.com"
PHONE_DISPLAY = "+994 55 278 27 78"
PHONE_TEL = "+994552782778"
WA_NUMBER = "994552782778"
EMAIL = "comfortdivanyuma@gmail.com"
INSTAGRAM = "https://www.instagram.com/comfort__cleaning/"
IG_HANDLE = "@comfort__cleaning"
CSS_V = 9
JS_V = 5
IMG_V = 3
CDN = "https://cdn.jsdelivr.net/npm"
GSAP = "gsap@3.15.0"
LENIS = "lenis@1.3.17"
# Cloudflare Web Analytics, cookieless. The token is public by design.
CF_BEACON = """<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{"token": "353b17cf12604256abd2ad62a50cb3b7"}'></script>"""

LANGS = {"az": AZ, "ru": RU, "en": EN}
ORDER = ["az", "ru", "en"]

SERVICE_KEYS = ["home_clean", "office", "sofa", "curtain", "carpet", "mattress"]
SERVICE_ICONS = {
    "home_clean": "home",
    "office": "building",
    "sofa": "sofa",
    "curtain": "curtain",
    "carpet": "carpet",
    "mattress": "bed",
}

SLUGS = {
    "az": {
        "home": "", "services": "xidmetler", "packages": "paketler", "about": "haqqimizda", "contact": "elaqe",
        "home_clean": "ev-temizliyi", "office": "ofis-temizliyi", "sofa": "divan-temizliyi",
        "curtain": "perde-temizliyi", "carpet": "xalca-temizliyi", "mattress": "dosek-temizliyi",
    },
    "ru": {
        "home": "", "services": "uslugi", "packages": "pakety", "about": "o-nas", "contact": "kontakty",
        "home_clean": "uborka-doma", "office": "uborka-ofisa", "sofa": "chistka-divanov",
        "curtain": "chistka-shtor", "carpet": "chistka-kovrov", "mattress": "chistka-matrasov",
    },
    "en": {
        "home": "", "services": "services", "packages": "packages", "about": "about", "contact": "contact",
        "home_clean": "home-cleaning", "office": "office-cleaning", "sofa": "sofa-cleaning",
        "curtain": "curtain-cleaning", "carpet": "carpet-cleaning", "mattress": "mattress-cleaning",
    },
}
PAGE_KEYS = ["home", "services", "packages", "about", "contact"] + SERVICE_KEYS

# Real Google reviews, complete visible sentences only. Spelling normalised, wording unchanged.
REVIEWS = [
    ("Nuray T.", "Comfort Cleaning şirkətinin xidmətindən çox razı qaldım! İşlərini çox səliqəli, diqqətli və peşəkar şəkildə yerinə yetirirlər. Hər şey təmiz və gözəl oldu."),
    ("Ayan", "Çox razı qaldım. Təmizlik işləri çox səliqəli və diqqətlə görülüb. Mebellərin təmizlənməsi yüksək səviyyədə oldu."),
    ("Məhəmməd M.", "Xidmətləri gözlədiyimdən də yaxşı oldu."),
]

ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "building": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4"/><path d="M10 10h4"/><path d="M10 14h4"/><path d="M10 18h4"/>',
    "sofa": '<path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 11v5a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v2H6v-2a2 2 0 0 0-4 0Z"/><path d="M4 18v2"/><path d="M20 18v2"/><path d="M12 4v9"/>',
    "curtain": '<path d="M2 3h20"/><path d="M4 3v18h4c-1.2-5.5 0.5-11 3-18"/><path d="M20 3v18h-4c1.2-5.5-0.5-11-3-18"/>',
    "carpet": '<rect x="5" y="3.5" width="14" height="17" rx="1.5"/><rect x="8.5" y="7" width="7" height="10" rx="1"/><path d="M7.5 20.5V22M10.5 20.5V22M13.5 20.5V22M16.5 20.5V22M7.5 2v1.5M10.5 2v1.5M13.5 2v1.5M16.5 2v1.5"/>',
    "bed": '<path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M4 10V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v4"/><path d="M12 4v6"/><path d="M2 18h20"/>',
    "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    "tag": '<path d="M12 2H2v10l9.29 9.29a2.41 2.41 0 0 0 3.42 0l6.58-6.58a2.41 2.41 0 0 0 0-3.42L12 2Z"/><path d="M7 7h.01"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "quote": '<path d="M3 21c3 0 7-1 7-8V5c0-1.25-.76-2-2-2H4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .01-1 1.03V20c0 1 0 1 1 1z"/><path d="M15 21c3 0 7-1 7-8V5c0-1.25-.76-2-2-2h-4c-1.25 0-2 .75-2 1.97V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"/>',
    "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "layers": '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "sparkle": '<path d="M12 3l1.9 5.8a2 2 0 0 0 1.3 1.3L21 12l-5.8 1.9a2 2 0 0 0-1.3 1.3L12 21l-1.9-5.8a2 2 0 0 0-1.3-1.3L3 12l5.8-1.9a2 2 0 0 0 1.3-1.3z"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
}
WHATSAPP_PATH = (
    "M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164"
    "-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297"
    "-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075"
    "-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372"
    "-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306"
    " 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173"
    "-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982"
    ".998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03"
    " 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815"
    " 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882"
    " 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413Z"
)


def e(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s, quote=True)


def icon(name, cls="icon"):
    if name == "whatsapp":
        return f'<svg class="{cls} icon--fill" viewBox="0 0 24 24" aria-hidden="true"><path d="{WHATSAPP_PATH}"/></svg>'
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def wa_url(C, key):
    return f"https://wa.me/{WA_NUMBER}?text={urllib.parse.quote(C['wa'][key], safe='')}"


def href(lang, key, current_lang):
    slug = SLUGS[lang][key]
    if lang == current_lang:
        return slug or "./"
    return f"../{lang}/{slug}"


def abs_url(lang, key):
    return f"{SITE}/{lang}/{SLUGS[lang][key]}"


def wa_btn(C, key, cls="btn btn--gold", label=None):
    return (
        f'<a class="{cls}" href="{attr(wa_url(C, key))}" target="_blank" rel="noopener">'
        f'{icon("whatsapp")}<span>{e(label or C["ui"]["cta"])}</span></a>'
    )


def checklist(items, cls="checklist"):
    lis = "".join(f'<li>{icon("check")}<span>{e(t)}</span></li>' for t in items)
    return f'<ul class="{cls}">{lis}</ul>'


# Page chrome

def head(C, key, title, desc, graph):
    lang = C["lang"]
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{abs_url(l, key)}">' for l in ORDER
    )
    og_alt = "\n".join(
        f'<meta property="og:locale:alternate" content="{LANGS[l]["locale"]}">' for l in ORDER if l != lang
    )
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{attr(desc)}">
<link rel="canonical" href="{abs_url(lang, key)}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{abs_url('az', key)}">
<meta name="theme-color" content="#0d1d30">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Comfort Cleaning">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:url" content="{abs_url(lang, key)}">
<meta property="og:image" content="{SITE}/assets/img/favicon-512.png?v={IMG_V}">
<meta property="og:locale" content="{C['locale']}">
{og_alt}
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/img/favicon-32.png?v={IMG_V}">
<link rel="icon" type="image/png" sizes="192x192" href="../assets/img/favicon-192.png?v={IMG_V}">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png?v={IMG_V}">
<script>
(function (d) {{
  d.classList.add("js");
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{
    d.classList.add("motion");
    setTimeout(function () {{ if (!window.__motionReady) d.classList.remove("motion"); }}, 3500);
  }}
}})(document.documentElement);
</script>
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Display:ital,wght@0,400;0,500;1,400&family=Onest:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="../assets/css/style.css?v={CSS_V}">
<script type="application/ld+json">
{ld}
</script>
</head>
"""


def nav_links(C, key):
    out = []
    for k, label in C["ui"]["nav"]:
        if k == key:
            extra = ' aria-current="page"'
        elif k == "services" and key in SERVICE_KEYS:
            extra = ' class="is-section"'
        else:
            extra = ""
        out.append(f'<a href="{href(C["lang"], k, C["lang"])}"{extra}>{e(label)}</a>')
    return "".join(out)


def lang_links(C, key):
    out = []
    for l in ORDER:
        cur = ' aria-current="true"' if l == C["lang"] else ""
        out.append(f'<a href="{href(l, key, C["lang"])}" hreflang="{l}" lang="{l}"{cur}>{l.upper()}</a>')
    return "".join(out)


def header(C, key, wa_key):
    ui = C["ui"]
    return f"""<body>
<a class="skip-link" href="#main">{e(ui['skip'])}</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="./"><img src="../assets/img/favicon-96.png?v={IMG_V}" alt="" width="40" height="40">Comfort Cleaning</a>
    <nav class="nav" aria-label="{attr(ui['menu'])}">{nav_links(C, key)}</nav>
    <div class="lang" role="group" aria-label="{attr(ui['lang_label'])}">{lang_links(C, key)}</div>
    {wa_btn(C, wa_key, "btn btn--gold btn--sm header-cta")}
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="{attr(ui['menu'])}">{icon("menu", "icon icon-open")}{icon("close", "icon icon-close")}</button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" hidden>
  <nav aria-label="{attr(ui['menu'])}">{nav_links(C, key)}</nav>
  <div class="lang" role="group" aria-label="{attr(ui['lang_label'])}">{lang_links(C, key)}</div>
  {wa_btn(C, wa_key, "btn btn--gold btn--block")}
</div>
<main id="main">
"""


def footer(C, key, wa_key):
    ui = C["ui"]
    lang = C["lang"]
    services = "".join(
        f'<li><a href="{href(lang, k, lang)}">{e(C["services"][k]["short"])}</a></li>' for k in SERVICE_KEYS
    )
    services += f'<li><a href="{href(lang, "packages", lang)}">{e(ui["packages_label"])}</a></li>'
    nav = dict(C["ui"]["nav"])
    company = "".join(
        f'<li><a href="{href(lang, k, lang)}">{e(nav[k])}</a></li>' for k in ["home", "services", "about", "contact"]
    )
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="./"><img src="../assets/img/favicon-96.png?v={IMG_V}" alt="" width="40" height="40" loading="lazy">Comfort Cleaning</a>
        <p>{e(ui['footer_text'])}</p>
        <div class="socials">
          <a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a>
          <a href="{attr(wa_url(C, 'general'))}" target="_blank" rel="noopener" aria-label="WhatsApp">{icon("whatsapp")}</a>
          <a href="tel:{PHONE_TEL}" aria-label="{attr(ui['phone_label'])}">{icon("phone")}</a>
        </div>
      </div>
      <div>
        <h2>{e(ui['footer_cols'][0])}</h2>
        <ul>{services}</ul>
      </div>
      <div>
        <h2>{e(ui['footer_cols'][1])}</h2>
        <ul>{company}</ul>
      </div>
      <div>
        <h2>{e(ui['footer_cols'][2])}</h2>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener">{IG_HANDLE}</a></li>
          <li>{e(ui['city'])}</li>
        </ul>
      </div>
    </div>
    <p class="footer-bottom">{e(ui['copyright'])}</p>
  </div>
</footer>
<div class="mobile-bar">
  <a class="btn btn--line-dark" href="tel:{PHONE_TEL}" aria-label="{attr(ui['call'])}">{icon("phone")}<span>{e(ui['call'])}</span></a>
  {wa_btn(C, wa_key, label=ui['cta_short'])}
</div>
<script src="{CDN}/{GSAP}/dist/gsap.min.js" defer></script>
<script src="{CDN}/{GSAP}/dist/ScrollTrigger.min.js" defer></script>
<script src="{CDN}/{GSAP}/dist/SplitText.min.js" defer></script>
<script src="{CDN}/{LENIS}/dist/lenis.min.js" defer></script>
<script src="../assets/js/main.js?v={JS_V}" defer></script>
<script src="../assets/js/water.js?v={JS_V}" defer></script>
<script src="../assets/js/motion.js?v={JS_V}" defer></script>
{CF_BEACON}
</body>
</html>
"""


# Sections

def section_head(eyebrow, h2, sub=None, center=False, reveal=True):
    cls = "section-head" + (" section-head--center" if center else "") + (" reveal" if reveal else "")
    eb = f'<p class="eyebrow">{e(eyebrow)}</p>' if eyebrow else ""
    sb = f'<p class="section-sub">{e(sub)}</p>' if sub else ""
    return f'<div class="{cls}">{eb}<h2 data-split>{e(h2)}</h2>{sb}</div>'


def water(cls="water"):
    return f'<canvas class="{cls}" aria-hidden="true"></canvas>'


def phone_chat(C):
    h = C["home"]
    c = h["chat"]
    steps = "".join(
        f'<li data-step="{i}">{icon(ic)}<span>{e(t)}</span></li>'
        for i, (ic, t, _d) in enumerate(h["card_steps"], 1)
    )
    tick = '<svg class="ticks" viewBox="0 0 18 12" aria-hidden="true"><path d="M1 6.5 4.5 10 11 2"/><path d="M7 6.5 10.5 10 17 2"/></svg>'
    return f"""<div class="phone-wrap" data-hero-in>
      <ol class="chat-steps" aria-hidden="true">{steps}</ol>
      <div class="phone" role="img" aria-label="{attr(h['card_title'])}">
        <div class="phone-screen">
          <div class="chat-head">
            <img src="../assets/img/favicon-96.png?v={IMG_V}" alt="" width="36" height="36">
            <div><strong>{e(c['name'])}</strong><span>{e(c['status'])}</span></div>
          </div>
          <div class="chat-body">
            <div class="msg msg--out msg--photo" data-msg="1" data-step-on="1">
              <div class="photo-tile">{icon('sofa')}<span>{e(c['photo_label'])}</span></div>
              <p>{e(c['out1'])}</p>{tick}
            </div>
            <div class="typing" data-msg="2"><i></i><i></i><i></i></div>
            <div class="msg msg--in" data-msg="3" data-step-on="2"><p>{e(c['in1'])}</p></div>
            <div class="msg msg--in" data-msg="4"><p>{e(c['in2'])}</p></div>
            <div class="msg msg--out" data-msg="5"><p>{e(c['out2'])}</p>{tick}</div>
            <div class="chat-done" data-msg="6" data-step-on="3">{icon('calendar')}<span>{e(c['done'])}</span></div>
          </div>
        </div>
      </div>
    </div>"""


def hero_home(C):
    h = C["home"]
    return f"""<section class="hero on-dark">
  {water()}
  <div class="container hero-grid">
    <div class="hero-copy">
      <h1 data-split="hero">{e(h['h1'])}</h1>
      <p class="lead" data-hero-in>{e(h['lead'])}</p>
      <div class="hero-actions" data-hero-in>
        {wa_btn(C, 'general', 'btn btn--gold magnetic')}
        <a class="btn btn--line-dark" href="#services">{e(C['ui']['see_services'])}</a>
      </div>
    </div>
    {phone_chat(C)}
  </div>
  <a class="scroll-cue" href="#story" data-hero-in><span>{e(h['scroll_hint'])}</span><i aria-hidden="true"></i></a>
</section>
"""


def page_hero(C, eyebrow, h1, lead, wa_key, eyebrow_href=None):
    if eyebrow_href:
        eb = f'<a class="eyebrow" href="{eyebrow_href}" data-hero-in>{e(eyebrow)}</a>'
    else:
        eb = f'<p class="eyebrow" data-hero-in>{e(eyebrow)}</p>'
    return f"""<section class="page-hero on-dark">
  {water()}
  <div class="container">
    {eb}
    <h1 data-split="hero">{e(h1)}</h1>
    <p class="lead" data-hero-in>{e(lead)}</p>
    <div class="hero-actions" data-hero-in>{wa_btn(C, wa_key, 'btn btn--gold magnetic')}</div>
  </div>
</section>
"""


def sec_marquee(C):
    names = [C["services"][k]["short"] for k in SERVICE_KEYS]
    row = "".join(f"<span>{e(n)}</span><i aria-hidden=\"true\"></i>" for n in names)
    return f"""<div class="marquee" aria-hidden="true">
  <div class="marquee-track"><div class="marquee-row">{row}</div><div class="marquee-row">{row}</div></div>
</div>
"""


def sec_story(C):
    h = C["home"]
    return f"""<section class="story" id="story" aria-label="{attr(h['story_label'])}">
  <div class="container story-stage">
    <p class="eyebrow">{e(h['story_label'])}</p>
    <p class="story-text" data-story>{e(h['story_text'])}</p>
  </div>
</section>
"""


def service_card(C, k, n):
    lang = C["lang"]
    s = C["services"][k]
    items = checklist(s["items"]) if s["items"] else ""
    text, kind = s["link"]
    if kind == "wa":
        link = f'<a class="link-arrow" href="{attr(wa_url(C, k))}" target="_blank" rel="noopener">{e(text)}{icon("arrow")}</a>'
    else:
        link = f'<a class="link-arrow" href="{href(lang, k, lang)}">{e(text)}{icon("arrow")}</a>'
    return f"""<article class="service-card reveal">
      <div class="card-top"><span class="service-icon">{icon(SERVICE_ICONS[k])}</span><span class="card-num">0{n}</span></div>
      <h3><a href="{href(lang, k, lang)}">{e(s['name'])}</a></h3>
      <p>{e(s['card'])}</p>
      {items}
      <div class="card-foot">{link}</div>
    </article>"""


def sec_services(C, with_head=True):
    b = C["services_block"]
    head_html = section_head(b["eyebrow"], b["h2"], b["sub"]) if with_head else ""
    cards = "\n    ".join(service_card(C, k, n) for n, k in enumerate(SERVICE_KEYS, 1))
    end = f"""<article class="service-card service-card--end on-dark reveal">
      <p class="end-title">{e(C['price']['h2'])}</p>
      {wa_btn(C, 'general', 'btn btn--gold magnetic')}
    </article>"""
    return f"""<section class="section section--mist services" id="services">
  <div class="container">{head_html}</div>
  <div class="services-viewport">
    <div class="services-track">
    {cards}
    {end}
    </div>
  </div>
  <div class="container"><div class="services-progress" aria-hidden="true"><i></i></div></div>
</section>
"""


def sec_packages(C, with_head=True):
    p = C["packages_block"]
    head_html = section_head(p["eyebrow"], p["h2"], p["sub"]) if with_head else ""
    hours = "".join(f"<li>{e(h)}</li>" for h in p["hours"])
    return f"""<section class="section">
  <div class="container">
    {head_html}
    <div class="packages">
      <article class="package reveal">
        <h3>{e(p['full_name'])}</h3>
        <p class="for">{e(p['full_for'])}</p>
        <p class="intro">{e(p['full_intro'])}</p>
        {checklist(p['full_list'])}
        <div>{wa_btn(C, 'full', 'btn btn--line')}</div>
      </article>
      <article class="package package--accent on-dark reveal">
        <h3>{e(p['hourly_name'])}</h3>
        <p class="for">{e(p['hourly_for'])}</p>
        <p class="intro">{e(p['hourly_intro'])}</p>
        <ul class="hours">{hours}</ul>
        <p class="package-note">{e(p['hourly_note'])}</p>
        <div>{wa_btn(C, 'hourly')}</div>
      </article>
    </div>
  </div>
</section>
"""


def sec_emphasis(C):
    m = C["emphasis"]
    lang = C["lang"]
    h = C["home"]
    items = "".join(f'<li>{icon("check")}<span>{e(t)}</span></li>' for t in m["list"])
    return f"""<section class="section section--ocean on-dark emphasis">
  <div class="container emphasis-grid">
    <div>
      <p class="eyebrow reveal">{e(m['eyebrow'])}</p>
      <h2 data-split>{e(m['h2'])}</h2>
      <p class="section-sub reveal">{e(m['sub'])}</p>
      <ul class="emphasis-chips reveal">{items}</ul>
      <div class="section-actions reveal">
        {wa_btn(C, 'sofa', 'btn btn--gold magnetic', label=m['cta'])}
        <a class="link-arrow" href="{href(lang, 'sofa', lang)}">{e(m['link'])}{icon('arrow')}</a>
      </div>
    </div>
    <div class="wipe-card reveal" data-wipe>
      <div class="wipe-clean">
        <span class="wipe-icon">{icon('sofa')}</span>
        <p class="wipe-title">{e(h['wipe_title'])}</p>
      </div>
      <canvas class="wipe-canvas" aria-hidden="true"></canvas>
      <p class="wipe-hint">{icon('sparkle')}<span>{e(h['wipe_hint'])}</span></p>
      <button class="wipe-reset" type="button">{e(h['wipe_reset'])}</button>
    </div>
  </div>
</section>
"""


def sec_why(C, cls="section"):
    w = C["why"]
    items = "".join(
        f'<li class="reveal"><span class="service-icon">{icon(ic)}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
        for ic, t, d in w["items"]
    )
    return f"""<section class="{cls}">
  <div class="container why">
    <div class="why-head">{section_head(w['eyebrow'], w['h2'], w['sub'], reveal=False)}</div>
    <ul class="why-list">{items}</ul>
  </div>
</section>
"""


def sec_price(C, wa_key, cls="section section--mist"):
    p = C["price"]
    steps = "".join(f'<li><span class="num">{i}</span><span>{e(t)}</span></li>' for i, t in enumerate(p["steps"], 1))
    return f"""<section class="{cls}">
  <div class="container">
    <div class="price-panel on-dark reveal">
      <div>
        <h2>{e(p['h2'])}</h2>
        <p>{e(p['p'])}</p>
        {wa_btn(C, wa_key)}
      </div>
      <ol class="photo-steps">{steps}</ol>
    </div>
  </div>
</section>
"""


def sec_process(C, cls="section"):
    p = C["process"]
    steps = "".join(
        f'<li class="reveal"><span class="process-num">{i}</span><div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'
        for i, (t, d) in enumerate(p["steps"], 1)
    )
    return f"""<section class="{cls}">
  <div class="container process-wrap">
    <div class="process-head">{section_head(p['eyebrow'], p['h2'], p['sub'])}</div>
    <div class="process-track"><span class="process-line" aria-hidden="true"><i></i></span><ol class="process">{steps}</ol></div>
  </div>
</section>
"""


def sec_reviews(C, cls="section section--mist"):
    r = C["reviews"]
    ui = C["ui"]
    cards = []
    for i, (name, text) in enumerate(REVIEWS):
        tr = ""
        if r["translations"]:
            tr = f'<div class="review-translation" lang="{C["lang"]}"><small>{e(ui["translated"])}</small>{e(r["translations"][i])}</div>'
        cards.append(
            f'<figure class="review reveal">{icon("quote")}'
            f'<blockquote lang="az"><p>{e(text)}</p></blockquote>{tr}'
            f'<figcaption><strong>{e(name)}</strong><span>{e(ui["review_source"])}</span></figcaption></figure>'
        )
    return f"""<section class="{cls}">
  <div class="container">
    {section_head(r['eyebrow'], r['h2'], r['sub'], center=True)}
    <div class="reviews">{''.join(cards)}</div>
  </div>
</section>
"""


def sec_faq(C, ids, h2=None, cls="section"):
    ui = C["ui"]
    items = "".join(
        f'<details name="faq"><summary><span>{e(C["faq"][i][0])}</span>{icon("plus")}</summary>'
        f'<div class="faq-a"><p>{e(C["faq"][i][1])}</p></div></details>'
        for i in ids
    )
    return f"""<section class="{cls}">
  <div class="container">
    {section_head(ui['faq_eyebrow'], h2 or ui['faq_h2'], center=True)}
    <div class="faq reveal">{items}</div>
  </div>
</section>
"""


def sec_final(C, wa_key):
    f = C["final"]
    return f"""<section class="section section--ocean on-dark final">
  {water()}
  <div class="container">
    <h2 data-split>{e(f['h2'])}</h2>
    <p class="section-sub reveal">{e(f['sub'])}</p>
    <div class="section-actions section-actions--center reveal">{wa_btn(C, wa_key, 'btn btn--gold magnetic')}</div>
  </div>
</section>
"""


# Structured data

def business(C):
    return {
        "@type": "LocalBusiness",
        "@id": f"{SITE}/#business",
        "name": "Comfort Cleaning",
        "alternateName": ["Group Comfort Cleaning", "Comfort Cleaning Group"],
        "url": f"{SITE}/{C['lang']}/",
        "logo": f"{SITE}/assets/img/favicon-512.png",
        "image": f"{SITE}/assets/img/favicon-512.png",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": C["ui"]["city"], "addressCountry": "AZ"},
        "areaServed": {"@type": "City", "name": C["ui"]["city"]},
        "sameAs": [INSTAGRAM],
        "description": C["home"]["desc"],
    }


def faq_ld(C, ids):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": C["faq"][i][0], "acceptedAnswer": {"@type": "Answer", "text": C["faq"][i][1]}}
            for i in ids
        ],
    }


# Pages

def page_home(C):
    graph = [
        business(C),
        {
            "@type": "WebSite",
            "@id": f"{SITE}/#website",
            "name": "Comfort Cleaning",
            "alternateName": ["Group Comfort Cleaning", "Comfort Cleaning Group"],
            "url": f"{SITE}/",
            "inLanguage": C["lang"],
            "publisher": {"@id": f"{SITE}/#business"},
        },
        faq_ld(C, list(C["faq"].keys())),
    ]
    body = (
        hero_home(C)
        + sec_marquee(C)
        + sec_story(C)
        + sec_services(C)
        + sec_packages(C)
        + sec_emphasis(C)
        + sec_why(C)
        + sec_price(C, "general")
        + sec_process(C)
        + sec_reviews(C)
        + sec_faq(C, list(C["faq"].keys()))
        + sec_final(C, "general")
    )
    return head(C, "home", C["home"]["title"], C["home"]["desc"], graph) + header(C, "home", "general") + body + footer(C, "home", "general")


def page_services(C):
    p = C["pages"]["services"]
    body = (
        page_hero(C, p["eyebrow"], p["h1"], p["lead"], "general")
        + sec_services(C, with_head=False)
        + sec_packages(C)
        + sec_emphasis(C)
        + sec_price(C, "general", cls="section")
        + sec_final(C, "general")
    )
    return head(C, "services", p["title"], p["desc"], [business(C)]) + header(C, "services", "general") + body + footer(C, "services", "general")


def page_packages(C):
    p = C["pages"]["packages"]
    note = C["packages_block"]["hourly_note"]
    depends = f"""<section class="section section--mist">
  <div class="container split">
    {section_head(None, p['depends_h'], p['depends_sub'])}
    <div class="detail-card reveal">
      {checklist(p['depends'])}
      <p class="notice">{icon('info')}<span>{e(note)}</span></p>
    </div>
  </div>
</section>
"""
    body = (
        page_hero(C, p["eyebrow"], p["h1"], p["lead"], "packages")
        + sec_packages(C, with_head=False)
        + depends
        + sec_faq(C, p["faq"])
        + sec_final(C, "packages")
    )
    return head(C, "packages", p["title"], p["desc"], [business(C)]) + header(C, "packages", "packages") + body + footer(C, "packages", "packages")


def page_about(C):
    p = C["pages"]["about"]
    prose = "".join(f"<p>{e(t)}</p>" for t in p["prose"])
    story = f"""<section class="section">
  <div class="container split">
    <div class="prose reveal"><h2>{e(p['story_h'])}</h2>{prose}</div>
    <aside class="area-card reveal">{icon('pin')}<h3>{e(p['area_h'])}</h3><p>{e(p['area_p'])}</p></aside>
  </div>
</section>
"""
    body = (
        page_hero(C, p["eyebrow"], p["h1"], p["lead"], "general")
        + story
        + sec_why(C, cls="section section--mist")
        + sec_process(C)
        + sec_reviews(C)
        + sec_final(C, "general")
    )
    return head(C, "about", p["title"], p["desc"], [business(C)]) + header(C, "about", "general") + body + footer(C, "about", "general")


def page_contact(C):
    p = C["pages"]["contact"]
    ui = C["ui"]
    grid = f"""<section class="section">
  <div class="container">
    <div class="contact-grid">
      <a class="contact-item contact-item--primary reveal" href="{attr(wa_url(C, 'general'))}" target="_blank" rel="noopener">
        <span class="service-icon">{icon('whatsapp')}</span>
        <span><small>{e(p['wa_small'])}</small><strong>{e(p['wa_strong'])}</strong></span>
      </a>
      <a class="contact-item reveal" href="tel:{PHONE_TEL}">
        <span class="service-icon">{icon('phone')}</span>
        <span><small>{e(ui['phone_label'])}</small><strong>{PHONE_DISPLAY}</strong></span>
      </a>
      <a class="contact-item reveal" href="mailto:{EMAIL}">
        <span class="service-icon">{icon('mail')}</span>
        <span><small>{e(ui['email_label'])}</small><strong>{EMAIL}</strong></span>
      </a>
      <a class="contact-item reveal" href="{INSTAGRAM}" target="_blank" rel="noopener">
        <span class="service-icon">{icon('instagram')}</span>
        <span><small>{e(ui['ig_label'])}</small><strong>{IG_HANDLE}</strong></span>
      </a>
      <div class="contact-item reveal">
        <span class="service-icon">{icon('pin')}</span>
        <span><small>{e(ui['area_label'])}</small><strong>{e(ui['city'])}</strong></span>
      </div>
    </div>
  </div>
</section>
"""
    body = (
        page_hero(C, p["eyebrow"], p["h1"], p["lead"], "general")
        + grid
        + sec_price(C, "general")
        + sec_faq(C, p["faq"])
    )
    return head(C, "contact", p["title"], p["desc"], [business(C)]) + header(C, "contact", "general") + body + footer(C, "contact", "general")


def page_service(C, k):
    lang = C["lang"]
    ui = C["ui"]
    s = C["services"][k]
    labels = ui["triad"]
    triad = f"""<section class="section">
  <div class="container triad">
    <div class="triad-item reveal"><p class="triad-label">{e(labels[0])}</p><p class="triad-text">{e(s['situation'])}</p></div>
    <div class="triad-item reveal"><p class="triad-label">{e(labels[1])}</p><p class="triad-text">{e(s['we_do'])}</p></div>
    <div class="triad-item triad-item--result reveal"><p class="triad-label">{e(labels[2])}</p><p class="triad-text">{e(s['result'])}</p></div>
  </div>
</section>
"""
    options = "".join(
        f'<div class="option"><strong>{e(t)}</strong>' + (f"<span>{e(d)}</span>" if d else "") + "</div>"
        for t, d in s["options"]
    )
    opt_link = ""
    if s["options_link"]:
        text, target = s["options_link"]
        opt_link = f'<a class="link-arrow" href="{href(lang, target, lang)}">{e(text)}{icon("arrow")}</a>'
    second_items = C["packages_block"]["full_list"] if s["second_list"] == "PACKAGE_LIST" else s["second_list"]
    hint = f'<p class="hint">{e(s["second_hint"])}</p>' if s["second_hint"] else ""
    details = f"""<section class="section section--mist">
  <div class="container detail-grid">
    <div class="detail-card reveal">
      <h2>{e(s['options_h'])}</h2>
      <div class="options">{options}</div>
      {opt_link}
    </div>
    <div class="detail-card reveal">
      <h2>{e(s['second_h'])}</h2>
      {checklist(second_items)}
      {hint}
    </div>
  </div>
</section>
"""
    others = "".join(
        f'<a href="{href(lang, o, lang)}">{icon(SERVICE_ICONS[o])}{e(C["services"][o]["short"])}</a>'
        for o in SERVICE_KEYS if o != k
    )
    others_html = f"""<section class="section section--tight">
  <div class="container">
    <p class="eyebrow">{e(ui['other_services'])}</p>
    <div class="pill-links">{others}</div>
  </div>
</section>
"""
    nav = dict(ui["nav"])
    body = (
        page_hero(C, nav["services"], s["name"], s["lead"], k, eyebrow_href=href(lang, "services", lang))
        + triad
        + details
        + sec_price(C, k, cls="section")
        + sec_faq(C, s["faq"], h2=ui["faq_h2_service"], cls="section section--mist")
        + others_html
        + sec_final(C, k)
    )
    graph = [
        business(C),
        {
            "@type": "Service",
            "name": s["name"],
            "serviceType": s["name"],
            "description": s["desc"],
            "url": abs_url(lang, k),
            "provider": {"@id": f"{SITE}/#business"},
            "areaServed": {"@type": "City", "name": ui["city"]},
        },
    ]
    title = s.get("seo_title") or f"{s['short']} | Comfort Cleaning"
    return head(C, k, title, s["desc"], graph) + header(C, k, k) + body + footer(C, k, k)


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def build_sitemap():
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in PAGE_KEYS:
        for lang in ORDER:
            rows.append("  <url>")
            rows.append(f"    <loc>{abs_url(lang, key)}</loc>")
            for alt in ORDER:
                rows.append(f'    <xhtml:link rel="alternate" hreflang="{alt}" href="{abs_url(alt, key)}"/>')
            rows.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{abs_url("az", key)}"/>')
            rows.append("  </url>")
    rows.append("</urlset>")
    write("sitemap.xml", "\n".join(rows) + "\n")


def main():
    count = 0
    for lang in ORDER:
        C = LANGS[lang]
        pages = {
            "home": page_home(C),
            "services": page_services(C),
            "packages": page_packages(C),
            "about": page_about(C),
            "contact": page_contact(C),
        }
        for k in SERVICE_KEYS:
            pages[k] = page_service(C, k)
        for key, text in pages.items():
            name = SLUGS[lang][key] or "index"
            write(f"{lang}/{name}.html", text)
            count += 1
    build_sitemap()
    print(f"built {count} pages and sitemap.xml")


if __name__ == "__main__":
    main()
