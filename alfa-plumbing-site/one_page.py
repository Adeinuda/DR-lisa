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

# flat nav, in the order the sections appear: (anchor target, label)
FLAT = [
    ("index", "Home"),
    ("services", "Services"),
    ("water-heaters", "Water Heaters"),
    ("drains-sewer", "Drains & Sewer"),
    ("leaks-gas-repairs", "Leaks & Gas"),
    ("repiping-remodels", "Repiping"),
    ("about", "About"),
    ("team", "Team"),
    ("projects", "Projects"),
    ("reviews", "Reviews"),
    ("service-areas", "Areas"),
    ("pricing", "Costs"),
    ("faq", "FAQ"),
    ("guides", "DIY Guides"),
    ("contact", "Contact"),
]

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
body.onepage{--op-head:104px}
.onepage .opnav{position:sticky;top:0;z-index:60;background:rgba(12,34,51,.97);
  backdrop-filter:blur(8px);border-bottom:1px solid rgba(238,242,245,.14)}
.onepage .opnav .wrap{display:flex;align-items:center;gap:14px;padding-top:9px;padding-bottom:9px}
.onepage .opnav ul{display:flex;flex-wrap:wrap;gap:2px 3px;list-style:none;margin:0;padding:0;flex:1}
.onepage .opnav li{margin:0}
.onepage .opnav a{display:block;font:600 12px/1 var(--body);letter-spacing:.01em;color:var(--porcelain);
  text-decoration:none;padding:7px 8px;border-radius:4px;opacity:.82;white-space:nowrap}
.onepage .opnav a:hover{opacity:1;background:rgba(238,242,245,.08)}
.onepage .opnav a[aria-current="true"]{opacity:1;background:var(--brand-deep);color:#fff}
.onepage .opnav .op-brand{display:flex;align-items:center;gap:9px;color:var(--porcelain);text-decoration:none}
.onepage .opnav .op-brand b{font:700 14px/1 var(--display);letter-spacing:.01em;display:block}
.onepage .opnav .op-brand span{font:500 10px/1.2 var(--mono);letter-spacing:.1em;text-transform:uppercase;opacity:.62}
.onepage .opnav .btn{padding:9px 13px;font-size:12.5px;white-space:nowrap}
@media (max-width:1180px){.onepage .opnav .op-brand span{display:none}}
@media (max-width:820px){
  .onepage .opnav{--op-head:96px}
  .onepage .opnav .wrap{flex-wrap:wrap}
  .onepage .opnav ul{order:3;width:100%;overflow-x:auto;flex-wrap:nowrap;padding-bottom:4px;
    scrollbar-width:thin}
  .onepage .opnav .op-brand b{font-size:13px}
  body.onepage{--op-head:132px}
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
    if (!best || !byId[best]) return;
    links.forEach(function(a){ a.removeAttribute('aria-current'); });
    byId[best].setAttribute('aria-current', 'true');
  }
  function nav(el){ return el.getAttribute('data-nav') || el.id; }
  if ('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(ents){
      ents.forEach(function(en){ seen[nav(en.target)] = en.isIntersecting ? en.intersectionRatio : 0; });
      mark();
    }, {threshold:[0,.12,.35,.6], rootMargin:'-12% 0px -55% 0px'});
    secs.forEach(function(el){ io.observe(el); });
  } else {
    var onScroll = function(){
      var y = window.pageYOffset + 160, cur = secs[0];
      secs.forEach(function(el){ if (el.offsetTop <= y) cur = el; });
      seen = {}; seen[nav(cur)] = 1; mark();
    };
    window.addEventListener('scroll', onScroll); onScroll();
  }
  window.addEventListener('hashchange', function(){
    var m = (location.hash || '').match(/^#rt-([\w-]+)/);
    if (!m) return;
    var el = document.getElementById('rt-' + m[1]);
    if (el){ seen = {}; seen[nav(el)] = 1; mark(); }
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


def arrange(body, rel):
    """One page = one hero, a plain header per section, one booking form, one closer."""
    if rel != "index.html":
        body = pagehead_to_section_head(body)      # 34 dark page heroes -> one
    else:
        body = drop_band(body, "book")              # the booking band stays once, on Contact
    if rel != "contact.html":
        body = drop_band(body, "next")              # 34 identical closing bands -> the last one
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


def inline_assets(text):
    for rel, uri in LOCAL_ASSETS.items():
        text = text.replace('src="%s"' % rel, 'src="%s"' % uri)
        text = text.replace("src='%s'" % rel, "src='%s'" % uri)
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
    items = "".join('<li><a href="#rt-%s"%s>%s</a></li>'
                    % (slug, ' aria-current="true"' if i == 0 else "", html.escape(label))
                    for i, (slug, label) in enumerate(FLAT))
    return (
        '<nav class="opnav" aria-label="Sections of this page"><div class="wrap">\n'
        '  <a class="op-brand" href="#rt-index"><b>Alfa Plumbing Services</b>'
        '<span>Baytown, TX &middot; Since 2003</span></a>\n'
        '  <ul>%s</ul>\n'
        '  <a class="btn btn--call" href="tel:+17139929257">&#9742; 713-992-9257</a>\n'
        '</div></nav>' % items
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
    head = head.replace("</head>", (graph.group(0) if graph else "") + STYLE + "\n</head>")

    nav_slugs = {slug for slug, _label in FLAT}
    cats = guide_categories(read("guides.html"))
    sections = []
    for rel, label in routes:
        src = read(rel)
        slug = stem(rel)
        body = arrange(strip_scripts(main_of(src)), rel)
        body = namespace(link_all(body, known), slug)
        light = slug if slug in nav_slugs else ("guides" if rel.startswith("guides/") else "")
        cat = (" data-cat=\"%s\"" % cats[slug]) if slug in cats else ""
        sections.append('<section class="opsec" id="rt-%s" data-section="%s"%s%s>\n%s\n</section>'
                        % (slug, rel, ' data-nav="rt-%s"' % light if light else "", cat, body))

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


def check(dest, n, routes):
    src = open(dest, encoding="utf-8").read()
    markup = re.sub(r"<script\b.*?</script>|<style>.*?</style>", " ", src, flags=re.S)
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
    embeds = len(re.findall(r'<img src="data:image/', markup))
    if embeds < 2:
        problems.append("the two replaced photographs must be embedded, not linked (found %d)" % embeds)
    for cls in ("opnav", "mbar"):
        if cls not in markup:
            problems.append("%s missing from the single page" % cls)

    css = open(os.path.join(ROOT, SITE_CSS), encoding="utf-8").read()
    tokens = set(re.findall(r"--([\w-]+)\s*:", css))
    injected = re.search(r"<style>.*?</style>", src, re.S).group(0)
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
