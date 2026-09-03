#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collate the whole project into ONE html file: alfa-plumbing-site/one-page.html.

Every section of the site sits inline in a single document - the 15 navigation routes and all
20 DIY guides - and the navigation is a flat row of in-page anchors. No dropdowns, no mega
panels, no drawer, no links out to separate section files: clicking a nav item scrolls to that
section of the same file.

It is generated, so it can never drift:  python3 build.py   (runs this at the end)

Mechanics
  * <main> of each page is inlined in nav order; the shared utility bar, header and footer are
    emitted once, and the mobile call bar is kept.
  * ids are namespaced per section (rt-<route>__<id>) because 35 pages of ids collide; `for`,
    `aria-controls` and friends move with them. #book and #gcount stay un-prefixed because
    alfa.js looks them up by name.
  * every internal link becomes an in-page anchor: water-heaters.html#water-heater-repair ->
    #rt-water-heaters__water-heater-repair. tel:/sms:/mailto:, the Google/Yelp links and the
    photos are untouched, so both booking forms still send from the single file.
  * the header is rebuilt flat from the same nav labels - see FLAT - and the dropdown markup is
    not carried over at all.
  * assets/alfa.css and assets/alfa.js are the production files; the injected <style> only adds
    what the single-page chrome needs, using existing design tokens.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = "one-page.html"
SITE_CSS = "assets/alfa.css"
SITE_JS = "assets/alfa.js"

# One flat nav, grouped the way the sections are grouped: the four service pages sit under
# Services, the five company pages under About. Nothing opens a menu and nothing leaves the
# file - every item scrolls to its own section. (target, label, children)
FLAT = [
    ("index", "Home", []),
    ("services", "Services", [("water-heaters", "Water Heaters"), ("drains-sewer", "Drains & Sewer"),
                              ("leaks-gas-repairs", "Leaks & Gas"), ("repiping-remodels", "Repiping")]),
    ("about", "About", [("team", "Team"), ("projects", "Projects"), ("reviews", "Reviews"),
                        ("service-areas", "Areas"), ("pricing", "Costs")]),
    ("faq", "FAQ", []),
    ("guides", "DIY Guides", []),
    ("contact", "Contact", []),
]

# which nav items light while a section is on screen: itself, then its group parent
PARENT = {c: g for g, _l, kids in FLAT for c, _kl in kids}

TOP = [
    ("index.html", "Alfa Plumbing Services, Baytown TX"),
    ("services.html", "All 20 services"),
    ("water-heaters.html", "Water heaters"),
    ("drains-sewer.html", "Drains, sewer & septic"),
    ("leaks-gas-repairs.html", "Leaks, gas & repairs"),
    ("repiping-remodels.html", "Repiping & remodels"),
    ("about.html", "About"),
    ("team.html", "Team"),
    ("projects.html", "Projects"),
    ("reviews.html", "Reviews"),
    ("service-areas.html", "Service areas"),
    ("pricing.html", "What it costs"),
    ("faq.html", "FAQ"),
    ("guides.html", "DIY guides"),
    ("contact.html", "Contact"),
]

# ids alfa.js resolves by name; each stays bare only on the route that owns it, so a
# second page carrying the same name cannot create a duplicate id in the collated file
KEEP = {"top"}
KEEP_OWNER = {"gcount": "guides", "book": "contact"}
IDREF = ("for", "aria-controls", "aria-labelledby", "aria-describedby", "aria-owns", "list")

STYLE = """
<style>
/* single-page chrome only - design tokens come from alfa.css */
body.onepage{--op-head:100px}
/* one sticky bar, two rows: the sections above, each group's children underneath */
.onepage .opnav{position:sticky;top:0;z-index:60;background:rgba(12,34,51,.97);
  backdrop-filter:blur(8px);border-bottom:1px solid rgba(238,242,245,.14)}
.onepage .opnav .oprow1{display:flex;align-items:center;gap:14px;padding-top:9px;padding-bottom:8px}
.onepage .opnav .oprow2{display:flex;align-items:center;gap:18px;padding-bottom:9px;
  border-top:1px solid rgba(238,242,245,.11)}
.onepage .opnav ul{display:flex;gap:2px 3px;list-style:none;margin:0;padding:0;flex:1;min-width:0}
.onepage .opnav li{margin:0}
.onepage .opnav a{display:block;font:600 12px/1 var(--body);letter-spacing:.01em;color:var(--porcelain);
  text-decoration:none;padding:7px 8px;border-radius:4px;opacity:.82;white-space:nowrap}
.onepage .opnav a:hover{opacity:1;background:rgba(238,242,245,.08)}
.onepage .opnav a[aria-current="true"]{opacity:1;background:var(--brand-deep);color:#fff}
.onepage .opnav .op-brand{display:flex;align-items:center;gap:9px;color:var(--porcelain);text-decoration:none}
.onepage .opnav .op-brand b{font:700 14px/1 var(--display);letter-spacing:.01em;display:block}
.onepage .opnav .op-brand span{font:500 10px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;opacity:.62}
.onepage .opnav .btn{padding:9px 13px;font-size:12.5px;white-space:nowrap}
/* a parent that owns children carries the copper node; its children are a labelled chip run */
.opnav .oprow1 a.ophas{font-weight:700;opacity:1}
.opnav .oprow1 a.ophas::after{content:"";display:inline-block;width:4px;height:4px;border-radius:50%;
  background:var(--copper);margin-left:7px;vertical-align:1px}
.opnav .opkidgrp{display:flex;align-items:center;gap:7px;min-width:0}
.opnav .opkidgrp ul{flex:none;gap:1px;overflow-x:auto;scrollbar-width:none}
.opnav .opkidgrp ul::-webkit-scrollbar{display:none}
.opnav a.opkg{font:600 9.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--copper);
  white-space:nowrap;padding:5px 7px;border-radius:4px}
.opnav a.opkg:hover{color:#fff;background:rgba(238,242,245,.08)}
.opnav a.opchip{font-size:11.5px;padding:5px 9px;border-radius:999px;background:rgba(238,242,245,.055);opacity:.74}
.opnav a.opchip[aria-current="true"]{opacity:1;background:var(--brand-deep);color:#fff}
@media (max-width:1180px){.onepage .opnav .op-brand span{display:none}}
@media (max-width:1040px){
  .onepage .opnav .oprow1 ul{overflow-x:auto;scrollbar-width:none}
  .onepage .opnav .oprow1 ul::-webkit-scrollbar{display:none}
  .onepage .opnav .op-brand b{font-size:13px}
}
@media (max-width:640px){
  body.onepage{--op-head:152px}
  .onepage .opnav .oprow1{flex-wrap:wrap}
  .onepage .opnav .oprow1 ul{order:3;width:100%}
  .onepage .opnav .oprow2{overflow-x:auto;scrollbar-width:none}
  .onepage .opnav .oprow2::-webkit-scrollbar{display:none}
}
.opsec{border-top:1px solid var(--line);scroll-margin-top:var(--op-head)}
/* an arranged single page: quiet section headers, not 35 stacked page heroes */
.opsec .op-head{padding-block:clamp(26px,3.2vw,44px);background:var(--paper-2)}
.opsec .op-head .h-sec{font-size:clamp(25px,2.9vw,38px);max-width:26ch}
.opsec .op-head .sec-head{margin-bottom:0}
.opsec .op-head .lede{font-size:16.5px;max-width:64ch;margin:0}
.opsec[data-section^="guides/"] > .band:first-of-type{padding-bottom:clamp(10px,1.4vw,16px)}
.opsec[data-section^="guides/"] .artwrap{padding-block:clamp(22px,3vw,38px)}
/* the library reads as one chapter: hairline between articles, no repeated hero buttons */
.opsec[data-section^="guides/"] + .opsec[data-section^="guides/"]{border-top:1px dashed var(--line)}
.opsec .crumbs{display:none}
/* embedded photographs: one payload, sized like the <img> it replaces */
.opimg{display:block;width:100%;height:100%;min-height:180px;background-size:cover;
  background-position:center}
.svc .art .opimg{min-height:250px}
.card-job .ph .opimg,.member .ph .opimg{min-height:0}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
@media print{.onepage .opnav,.onepage .mbar{display:none}.opsec{break-before:page;border-top:0}}
</style>
"""

SCRIPT = """
<script>
/* single-page nav: light the section you are reading. No dropdowns, nothing to hover. */
(function(){
  var links = [].slice.call(document.querySelectorAll('.opnav a[href^="#rt-"]'));
  var secs = [].slice.call(document.querySelectorAll('.opsec'));
  if (!links.length || !secs.length) return;
  var byId = {};
  links.forEach(function(a){ byId[a.getAttribute('href').slice(1)] = a; });
  var seen = {};
  function mark(){
    var best = null;
    Object.keys(seen).forEach(function(k){ if (!best || seen[k] > seen[best]) best = k; });
    if (!best) return;
    var want = {};
    best.split(' ').forEach(function(id){ want[id] = 1; });
    var hit = false;
    links.forEach(function(a){
      var on = !!want[a.getAttribute('href').slice(1)];
      if (on) hit = true;
      a.removeAttribute('aria-current');
      if (on) a.setAttribute('aria-current', 'true');
    });
    if (!hit) links.forEach(function(a){ a.removeAttribute('aria-current'); });
  }
  function nav(el){ return (el.getAttribute('data-nav') || el.id).split(/\s+/); }
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(ents){
      ents.forEach(function(en){ seen[nav(en.target).join(' ')] = en.isIntersecting ? en.intersectionRatio : 0; });
      mark();
    }, {threshold:[0,.12,.35,.6], rootMargin:'-12% 0px -55% 0px'});
    secs.forEach(function(el){ io.observe(el); });
  } else {
    var onScroll = function(){
      var y = window.pageYOffset + 160, cur = secs[0];
      secs.forEach(function(el){ if (el.offsetTop <= y) cur = el; });
      seen = {}; seen[nav(cur).join(' ')] = 1; mark();
    };
    window.addEventListener('scroll', onScroll); onScroll();
  }
  window.addEventListener('hashchange', function(){
    var m = (location.hash || '').match(/^#rt-([\w-]+)/);
    if (!m) return;
    var el = document.getElementById('rt-' + m[1]);
    if (el){ seen = {}; seen[nav(el).join(' ')] = 1; mark(); }
    setTimeout(syncGuides, 0);
  });

  /* the DIY chips filter the hub cards; mirror that onto the full articles underneath */
  function syncGuides(){
    [].forEach.call(document.querySelectorAll('.opsec[data-section^="guides/"]'), function(sec){
      var link = document.querySelector('article.gcard a[href="#' + sec.id + '"]');
      var card = link && link.closest ? link.closest('article') : null;
      if (card) sec.hidden = !!card.hidden;
    });
  }
  document.addEventListener('click', function(e){
    if (e.target.closest && e.target.closest('[data-filter]')) setTimeout(syncGuides, 0);
  });
})();
</script>
"""


# ---------------------------------------------------------------- single-page arrangement
BAND = r"<section[^>]*\bid=\"%s\"[^>]*>.*?</section>"


def drop_band(html, id_value):
    """Remove one whole band (no band nests another section, so non-greedy is safe)."""
    return re.sub(BAND % re.escape(id_value), "", html, count=1, flags=re.S)


def pagehead_to_section_head(html):
    """A route's big dark page hero becomes an ordinary in-page section header."""
    m = re.search(r"<section class=\"pagehead\"[^>]*>(.*?)</section>", html, re.S)
    if not m:
        return html
    head = m.group(1)

    def grab(pat, default=""):
        g = re.search(pat, head, re.S)
        return g.group(1).strip() if g else default

    eyebrow = grab(r"<p class=\"eyebrow\">(.*?)</p>")
    h1 = grab(r"<h1[^>]*>(.*?)</h1>")
    lede = grab(r'<p class="lede">(.*?)</p>')
    replacement = (
        '<section class="band op-head" id="overview"><div class="wrap"><div class="sec-head">'
        '<div><p class="eyebrow">%s</p><h2 class="h-sec">%s</h2></div>'
        '<p class="lede">%s</p></div></div></section>' % (eyebrow, h1, lede)
    )
    return html[:m.start()] + replacement + html[m.end():]


def guide_categories(hub_html):
    """slug -> category key, read from the hub cards so the filters drive the articles too."""
    out = {}
    for card in re.findall(r'<article class="gcard rv" data-cat="([\w-]+)">.*?</article>', hub_html, re.S):
        pass
    for m in re.finditer(r'<article class="gcard rv" data-cat="([\w-]+)">(.*?)</article>', hub_html, re.S):
        link = re.search(r'href="guides/([\w.-]+)\.html"', m.group(2))
        if link:
            out[link.group(1)] = m.group(1)
    return out


# bands on the homepage that only preview a section the page already contains
HOMEPAGE_PREVIEWS = ("services", "jobs", "reviews-strip", "areas", "pricing", "guides", "faq")
# one symptom card that every cluster repeats verbatim
URGENT_CARD = r'<a class="symp urgent" href="[^"]*">(?!.*?</a>)*?.*?Water on the floor right now.*?</a>\s*'


def arrange(body, rel):
    """One page = one hero, a plain header per section, and no content met twice."""
    if rel == "index.html":
        body = drop_band(body, "book")               # the booking band stays once, on Contact
        for band in HOMEPAGE_PREVIEWS:               # each of these has its own section here
            body = drop_band(body, band)
    else:
        body = pagehead_to_section_head(body)        # 34 dark page heroes -> one
        if rel == "services.html":
            body = drop_band(body, "triage")          # the homepage wayfinder is the same six cards
        body = re.sub(URGENT_CARD, "", body, count=1, flags=re.S)   # the homepage triage carries it
        if rel.startswith("guides/"):
            body = re.sub(r'<p class="mono-note">By Alfa Plumbing Services[^<]*</p>\s*', "", body)
    if rel != "contact.html":
        body = drop_band(body, "next")               # 34 identical closing bands -> the last one
    if rel == "guides.html":                         # the article follows the card, so the card links once
        body = re.sub(r'<article class="gcard rv"([^>]*)>(.*?)</article>',
                      lambda m: '<article class="gcard rv"%s>%s</article>' % (
                          m.group(1),
                          re.sub(r'\s*<p>(?:(?!</p>).)*?</p>\s*(?=<a class="lk")', "\n      ",
                                  re.sub(r'<a class="lk".*?</a>\s*', "", m.group(2), flags=re.S))),
                      body, flags=re.S)
    return body


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def b64_data_uri(rel):
    """Embed a local asset so the single file renders with no sibling folder at all."""
    import base64
    raw = open(os.path.join(ROOT, rel), "rb").read()
    kind = "image/svg+xml" if rel.endswith(".svg") else ("image/jpeg" if rel.endswith((".jpg", ".jpeg"))
                                                          else "image/png")
    return "data:%s;base64,%s" % (kind, base64.b64encode(raw).decode("ascii"))


LOCAL_ASSETS = {}      # rel -> data uri, filled in build()


def var_names():
    return {rel: "--ph-" + rel.rsplit("/", 1)[-1].rsplit(".", 1)[0].replace("_", "-")
            for rel in LOCAL_ASSETS}


def inline_assets(text):
    """One embedded copy per photograph: each becomes a CSS custom property and every
    <img> slot turns into a sized background frame, so 11 photos cost 11 payloads."""
    names = var_names()
    for rel, var in names.items():
        text = re.sub(r'<img src="%s" alt="([^"]*)"(?:[^>]*?)(?:width="(\d+)")?(?:[^>]*?)>' % re.escape(rel),
                      lambda m, v=var: '<span class="opimg" role="img" aria-label="%s" '
                                       'style="background-image:var(%s)"></span>' % (m.group(1), v),
                      text)
        text = text.replace('src="%s"' % rel, 'style="background-image:var(%s)"' % names[rel])
    # nothing may hot-link another site from inside this file. The founder portrait is a real
    # photograph of a real person, so it is never swapped for an illustration: the link goes and
    # the text-only treatment takes over, exactly as the onerror fallback does on the pages.
    text = text.replace('<div class="tag-owner">', '<div class="tag-owner nophoto">')
    text = re.sub(r'<img[^>]*src="https?://[^"]*"[^>]*>\s*', "", text)
    return text


def stem(rel):
    base = os.path.basename(rel)
    return base[:-5] if base.endswith(".html") else base


def main_of(src):
    i = src.index('<main id="main">')
    j = src.index("</main>", i)
    return src[i + len('<main id="main">'):j]


def strip_scripts(fragment):
    return re.sub(r"<script\b.*?</script>", "", fragment, flags=re.S)


def link_all(text, known):
    """No link may leave the file: internal pages become in-page anchors."""
    return re.sub(r'href="([^"]*)"', lambda m: _link(m, known), text)


def _link(match, known):
    whole, href = match.group(0), match.group(1)
    if href.startswith(("http", "tel:", "sms:", "mailto:", "#", "assets/")):
        return whole
    path, _, frag = href.partition("#")
    path = path.split("../")[-1].split("/")[-1]
    if not path:
        return whole
    target = known.get(path)
    if target is None:
        return whole
    # a name deliberately kept bare is addressed bare, not namespaced
    if frag and KEEP_OWNER.get(frag) == target:
        return 'href="#%s"' % frag
    return 'href="#rt-%s%s"' % (target, ("__" + frag) if frag else "")


def namespace(text, slug):
    """35 sections of ids would collide; move every id and every reference to it."""
    keep = set(KEEP) | {name for name, owner in KEEP_OWNER.items() if owner == slug}

    def ns(attr, value):
        if value in keep or value.startswith("rt-"):
            return '%s="%s"' % (attr, value)
        return '%s="rt-%s__%s"' % (attr, slug, value)

    text = re.sub(r'\bid="(?!rt-)([^"]+)"', lambda m: ns("id", m.group(1)), text)
    for attr in IDREF:
        text = re.sub(r'\b%s="([^"]+)"' % attr, lambda m, a=attr: ns(a, m.group(1)), text)

    def anchor(m):
        value = m.group(1)
        if value in keep or value in KEEP_OWNER or value.startswith("rt-"):
            return 'href="#%s"' % value
        return 'href="#rt-%s__%s"' % (slug, value)

    return re.sub(r'href="#([^"]+)"', anchor, text)


def collect_guides():
    out = []
    for name in sorted(os.listdir(os.path.join(ROOT, "guides"))):
        if name.endswith(".html"):
            out.append("guides/" + name)
    dated = []
    for rel in out:
        m = re.search(r'<time datetime="([^"]+)"', read(rel))
        dated.append((m.group(1) if m else "", rel))
    dated.sort(reverse=True)
    return [rel for _d, rel in dated]


def flat_nav():
    """Two sticky rows, no menus: the section list on top, and beneath it the children of each
    group with the group named beside them. Every item is an in-page jump; nothing opens,
    nothing leaves the file, and the hierarchy is readable without hovering."""
    def a(slug, label, cls=""):
        cur = ' aria-current="true"' if slug == "index" else ""
        att = ' class="%s"' % cls if cls else ""
        return '<a href="#rt-%s"%s%s>%s</a>' % (slug, cur, att, html.escape(label))

    row1 = "".join('<li>%s</li>' % a(slug, label, "ophas" if kids else "")
                   for slug, label, kids in FLAT)
    row2 = "".join(
        '<div class="opkidgrp"><a class="opkg" href="#rt-%s">%s</a><ul aria-label="More in %s">%s</ul></div>'
        % (slug, html.escape(label), html.escape(label, quote=True),
           "".join("<li>%s</li>" % a(k, v, "opchip") for k, v in kids))
        for _s, label, kids in FLAT for slug, _l in [(_s, label)] if kids)
    return (
        '<nav class="opnav" aria-label="Sections of this page">'
        '<div class="wrap oprow1">\n'
        '  <a class="op-brand" href="#rt-index"><b>Alfa Plumbing Services</b>'
        '<span>Baytown, TX &middot; Since 2003</span></a>\n'
        '  <ul>%s</ul>\n'
        '  <a class="btn btn--call" href="tel:+17139929257">&#9742; 713-992-9257</a>\n'
        '</div>\n'
        '<div class="wrap oprow2">%s</div>\n'
        '</nav>' % (row1, row2)
    )


def build():
    global LOCAL_ASSETS
    css = read(SITE_CSS)
    js = read(SITE_JS)
    img_dir = os.path.join(ROOT, "assets", "img")
    LOCAL_ASSETS = {}
    if os.path.isdir(img_dir):
        for name in sorted(os.listdir(img_dir)):
            if name.endswith((".jpg", ".jpeg", ".png", ".svg")):
                LOCAL_ASSETS["assets/img/" + name] = b64_data_uri("assets/img/" + name)
    guides = collect_guides()
    # the single page ends on the booking section, so the library sits before it
    routes = [r for r in TOP if r[0] != "contact.html"] + [(rel, "") for rel in guides] + \
             [t for t in TOP if t[0] == "contact.html"]
    known = {os.path.basename(rel): stem(rel) for rel, _l in routes}

    home = read("index.html")
    util = home[home.index('<div class="util">'):home.index("<header")]
    util = link_all(util, known)
    footer = home[home.index("<footer"):home.index("</footer>") + len("</footer>")]
    footer = link_all(footer, known)
    tail = home[home.index('<div class="mbar"'):home.index("</body>")]
    tail = re.sub(r"<script src=\"assets/alfa\.js\"></script>\s*", "", tail)
    tail = link_all(tail, known)

    head = home[home.index("<head>"):home.index("</head>") + len("</head>")]
    head = re.sub(r'<link rel="canonical"[^>]*>',
                  '<meta name="robots" content="noindex,nofollow">', head)
    head = re.sub(r'\n<meta property="og:(url|image)"[^>]*>', "", head)
    head = re.sub(r'\n<link rel="icon"[^>]*>', "", head)   # the favicon still lives on the legacy host
    head = re.sub(r"<title>.*?</title>",
                  "<title>Alfa Plumbing Services, Baytown TX &mdash; the whole site on one page</title>",
                  head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  r"\1The complete Alfa Plumbing Services site in a single page: 20 services, "
                  r"water heaters, drains and sewer, gas and leak repairs, repiping, the crew, "
                  r"projects, reviews, service areas, published prices, FAQ and 20 DIY guides. "
                  r"Call (713) 992-9257.\2", head)
    graph = re.search(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    head = head.replace(graph.group(0), "", 1) if graph else head
    head = re.sub(r'<link rel="stylesheet" href="assets/alfa\.css">',
                  "<style>\n%s\n</style>" % css.replace("</", "<\\/"), head)
    names = var_names()
    payloads = "".join("\n  %s:url(\"data:%s;base64,%s\")"
                       % (names[rel],
                          "image/jpeg" if rel.endswith((".jpg", ".jpeg")) else "image/png",
                          LOCAL_ASSETS[rel].split(",", 1)[1])
                       for rel in sorted(LOCAL_ASSETS))
    photo_css = ("\n<style>/* embedded photographs: one payload each, referenced by the "
                 "frames that use them */\n.onepage{%s\n}</style>\n" % payloads)
    head = head.replace("</head>", (graph.group(0) if graph else "") + STYLE + photo_css + "\n</head>")

    nav_slugs = {slug for slug, _l, _k in FLAT} | {c for _g, _l, kids in FLAT for c, _kl in kids}
    cats = guide_categories(read("guides.html"))
    sections = []
    for rel, label in routes:
        src = read(rel)
        slug = stem(rel)
        body = arrange(strip_scripts(main_of(src)), rel)
        body = namespace(link_all(body, known), slug)
        if slug in nav_slugs:
            light = "rt-%s rt-%s" % (slug, PARENT[slug]) if slug in PARENT else "rt-%s" % slug
        elif rel.startswith("guides/"):
            light = "rt-guides"
        else:
            light = ""
        cat = (" data-cat=\"%s\"" % cats[slug]) if slug in cats else ""
        sections.append('<section class="opsec" id="rt-%s" data-section="%s"%s%s>\n%s\n</section>'
                        % (slug, rel, ' data-nav="%s"' % light if light else "", cat, body))

    sections = [inline_assets(x) for x in sections]
    util, footer, tail = (inline_assets(util), inline_assets(footer), inline_assets(tail))
    out = ['<!DOCTYPE html>\n<html lang="en" class="no-js">\n'
           '<script>document.documentElement.className="js";</script>\n', head,
           '\n<body class="onepage" id="top">\n',
           '<a class="skip" href="#main">Skip to content</a>\n', util,
           flat_nav(), '\n<main id="main">\n', "\n".join(sections), "\n</main>\n",
           footer, "\n", tail,
           "<script>\n%s\n</script>" % js.replace("</", "<\\/"), SCRIPT, "\n</body>\n</html>\n"]

    dest = os.path.join(ROOT, OUT)
    with open(dest, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return dest, len(routes), known, routes


_REMOTE = re.compile(r'(?:href|src)="https?://[^"]+"')


def check(dest, n, routes):
    src = open(dest, encoding="utf-8").read()
    markup = re.sub(r"<script\b.*?</script>|<style\b[^>]*>.*?</style>", " ", src, flags=re.S)
    problems = []

    ids = re.findall(r'\sid="([^"]+)"', markup)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append("duplicate ids: %s" % ", ".join(dupes[:8]))
    targets = set(ids)
    for frag in set(re.findall(r'href="#([^"]+)"', markup)):     # scripts excluded: they build hrefs
        if frag not in targets:
            problems.append("in-page link #%s has no target" % frag)
    for attr in ("for", "aria-controls", "aria-labelledby", "aria-describedby", "list"):
        for v in {x for x in re.findall(r'\b%s="([^"]+)"' % attr, markup)}:
            if v not in targets:
                problems.append('%s="%s" points at nothing' % (attr, v))

    # nothing may leave the file: no section links, no dropdown machinery
    leaving = sorted({h for h in re.findall(r'<a[^>]*href="([^"]+)"', markup)
                      if not h.startswith(("#", "tel:", "sms:", "mailto:", "http"))})
    if leaving:
        problems.append("links leaving the single file: %s" % ", ".join(leaving[:6]))
    # self-contained: every photograph is a data URI, so a raw <img> means something was missed,
    # and the legacy WordPress domain must not appear at all (it is not a third-party citation)
    if re.findall(r"<img\b[^>]*>", markup):
        problems.append("%d <img> tag(s) left in the file - inline the asset or drop it"
                        % len(re.findall(r"<img\b[^>]*>", markup)))
    if re.findall(r'(?:href|src)="[^"]*alfaplumbingservices\.com/wp-content[^"]*"', src):
        # (JSON-LD may still describe the real logo/portrait URLs - those are metadata, not loads)
        problems.append("the single page loads a resource from the legacy WordPress site")
    for banned in ('class="drop', 'class="panel"', 'aria-expanded', 'id="burger"', 'id="mobnav"'):
        if banned in markup:
            problems.append("dropdown furniture survived: %s" % banned)
    if markup.count('class="opsec"') != n:
        problems.append("sections: %d, expected %d" % (src.count('class="opsec"'), n))
    if len(re.findall(r"<label", markup)) != len(re.findall(r"<(?:input|select|textarea)\b", markup)):
        problems.append("label/field parity broke")
    forms = markup.count('action="mailto:info@alfaplumbingservices.com" method="post" '
                         'enctype="text/plain"')
    if forms != 1:
        problems.append("the single page should hold exactly one booking form, found %d" % forms)
    # one-page arrangement: no pile of page furniture
    for pat, want, label in [(r'<section class="pagehead"', 0, "page-hero bands (only the homepage hero)"),
                             (r'<h1\b', 1, "h1"),
                             (r'class="crumbs"', 0, "breadcrumb rows"),
                             (r'class="ctaband"', 1, "closing CTA band"),
                             (r'<form class="book"', 1, "booking band")]:
        got = len(re.findall(pat, markup))
        if got != want:
            problems.append("expected %d %s in the single page, found %d" % (want, label, got))
    cats = len(re.findall(r'<section class="opsec" id="rt-[\w-]+" data-section="guides/[^"]+"[^>]*data-cat=', markup))
    if cats != 20:
        problems.append("the 20 guide sections should each carry data-cat so the chips filter them, got %d" % cats)
    dupes = len(re.findall(r"By Alfa Plumbing Services, Baytown", markup))
    if dupes > 1:
        problems.append("the guide attribution line repeats %d times on one page" % dupes)
    if "Four ways we get called" in markup:
        problems.append("the homepage preview of Services duplicates the Services section")
    last = re.findall(r'<section class="opsec" id="rt-[\w-]+" data-section="([^"]+)"', markup)
    if last and last[-1] != "contact.html":
        problems.append("the single page should end on the booking section, found %s" % last[-1])
    for name in ("gcount", "book"):
        if 'id="%s"' % name not in src:                 # alfa.js resolves these by name
            problems.append("alfa.js needs id=\"%s\" to stay un-prefixed on its own section" % name)
    if 'content="noindex' not in src:
        problems.append("noindex missing")
    # the whole point: no sibling folder needed to render this file
    for ext in ('rel="stylesheet" href="assets', '<script src="assets', 'src="assets/img'):
        if ext in markup:
            problems.append("still references an external file: %s" % ext)
    if "Alfa Plumbing" not in src[:4000] or ".band{" not in src:
        problems.append("the production stylesheet must be inlined, not linked")
    if src.count("<main") != 1:
        problems.append("expected one <main>, found %d" % src.count("<main"))
    for rel, _l in routes:
        if ("data-section=\"%s\"" % rel) not in src:
            problems.append("%s never made it in" % rel)

    # the replaced photography has to exist and be the thing on the page
    for local in re.findall(r'<img src="(assets/[^"]+)"', src):
        if not os.path.exists(os.path.join(ROOT, local)):
            problems.append("missing local asset %s" % local)
    files = sorted(os.listdir(os.path.join(ROOT, "assets", "img")))
    payload = re.search(r"<style>/\* embedded photographs.*?</style>", src, re.S)
    if not payload:
        problems.append("the photographs are not embedded in the file")
    else:
        declared = set(re.findall(r"(--[\w-]+):url\(", payload.group(0)))
        used = set(re.findall(r"background-image:var\((--[\w-]+)\)", markup))
        if len(declared) != len(files):
            problems.append("%d photographs declared, %d exist in assets/img" % (len(declared), len(files)))
        missing = sorted(used - declared)
        if missing:
            problems.append("frames reference undefined photo vars: %s" % ", ".join(missing[:4]))
    if 'class="opimg"' not in markup:
        problems.append("no photo frames found")
    if re.search(r'<img src="assets/', markup):
        problems.append("a photograph is still linked instead of embedded")
    if 'assets/img/' in markup:
        problems.append("the single page still points at assets/img")
    for needed in ("--op-head:100px", ".opnav a.opchip{", ".opkidgrp{", ".opsec .op-head{",
                   "scroll-margin-top:var(--op-head)", ".opsec{border-top:"):
        if needed not in STYLE:
            problems.append("chrome CSS lost %s" % needed)
    if markup.count('class="opkidgrp"') != 2:
        problems.append("Services and About should each carry their group, found %d"
                        % markup.count('class="opkidgrp"'))
    if markup.count('class="ophas"') != 2:
        problems.append("two parents should be marked as owning children, found %d"
                        % markup.count('class="ophas"'))
    if len(re.findall(r'class="opchip"', markup)) != 9:
        problems.append("the grouped nav should carry 9 child chips, found %d"
                        % len(re.findall(r'class="opchip"', markup)))
    if "opsub" in markup or "opgrp" in markup:
        problems.append("the superseded single-row group markup survived")
    for cls in ("opnav", "mbar"):
        if cls not in markup:
            problems.append("%s missing from the single page" % cls)

    css = open(os.path.join(ROOT, SITE_CSS), encoding="utf-8").read()
    tokens = set(re.findall(r"--([\w-]+)\s*:", css))
    injected = re.search(r"<style\b[^>]*>.*?</style>", src, re.S).group(0)
    tokens |= set(re.findall(r"--([\w-]+)\s*:", injected))
    for name in sorted({x for x in re.findall(r"var\(--([\w-]+)\)", injected)}):
        if name not in tokens:
            problems.append("chrome uses --%s, which alfa.css does not define" % name)
    return problems


def main():
    dest, n, _known, routes = build()
    problems = check(dest, n, routes)
    kb = os.path.getsize(dest) / 1024
    print("  single page: %s (%.0f kB, %d sections, flat nav, no dropdowns)%s"
          % (OUT, kb, n, "" if not problems else "  PROBLEMS: " + "; ".join(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
