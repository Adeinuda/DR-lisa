#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collate every route into ONE html file: alfa-plumbing-site/all-routes.html.

The site stays multi-page (that is the architecture the client asked for); this is a
review artifact - the whole website in a single document, so it can be opened, scrolled,
sent to someone or dropped on a staging folder without the folder tree.

How it works
  * takes <main> from each generated page (shared header/footer are emitted once),
  * prefixes every id with `rt-<route>__` so 35 pages of ids cannot collide,
  * rewrites every internal link to that in-file anchor (`services.html` -> #rt-services,
    `water-heaters.html#gas-line-repair` -> #rt-water-heaters__gas-line-repair),
  * leaves tel:/sms:/mailto:, outbound review links and hot-linked images exactly as they are,
  * adds a route index, a per-route banner with a link to the standalone page, and an
    optional "one route at a time" mode (progressive: with no script everything just scrolls).

Run after build.py:  python3 build.py && python3 preview_all.py && python3 validate.py
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = "all-routes.html"

# nav order first, then the guide library - matches the real navigation
TOP = [
    ("index.html", "Home", "the landing route: hero, triage, wayfinder, proof, booking form"),
    ("services.html", "Services", "all 20 services as a wayfinder"),
    ("water-heaters.html", "Water heaters", "cluster route"),
    ("drains-sewer.html", "Drains, sewer & septic", "cluster route"),
    ("leaks-gas-repairs.html", "Leaks, gas & repairs", "cluster route"),
    ("repiping-remodels.html", "Repiping & remodels", "cluster route"),
    ("about.html", "About", "the company, the guarantee, the five steps"),
    ("team.html", "Team", "who answers and who turns up"),
    ("projects.html", "Projects", "eleven jobsite photographs"),
    ("reviews.html", "Reviews", "5.0 on 40 Google reviews, linked to source"),
    ("service-areas.html", "Service areas", "twelve cities, town by town"),
    ("pricing.html", "What it costs", "published ranges and how a quote is built"),
    ("faq.html", "FAQ", "eleven answers + FAQPage schema"),
    ("guides.html", "DIY guides", "the 20-post library preview with category filters"),
    ("contact.html", "Contact", "the booking form, map and what happens next"),
]


def stem(rel):
    base = os.path.basename(rel)
    return base[:-5] if base.endswith(".html") else base


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def main_of(src):
    i = src.index('<main id="main">')
    j = src.index("</main>", i)
    return src[i + len('<main id="main">'):j]


def strip_scripts(fragment):
    return re.sub(r"<script\b.*?</script>", "", fragment, flags=re.S)


def unescape_tags(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text))).strip()


def collect_guide_routes():
    """guides/*.html, in the same newest-first order the hub uses."""
    out = []
    for name in sorted(os.listdir(os.path.join(ROOT, "guides"))):
        if not name.endswith(".html"):
            continue
        rel = "guides/" + name
        src = read(rel)
        m = re.search(r"<time datetime=\"([^\"]+)\">([^<]+)</time>", src)
        out.append((rel, m.group(1) if m else "", m.group(2) if m else ""))
    out.sort(key=lambda r: r[1], reverse=True)
    return [(rel, date, label) for rel, date, label in out]


# ids the production script looks up by name site-wide; keep them addressable
KEEP = {"gcount"}
# the mobile sticky bar tracks the booking band - let the homepage own that anchor
KEEP_ON = {"index.html": {"book"}}
IDREF = ("for", "aria-controls", "aria-labelledby", "aria-describedby", "aria-owns", "list")


def route_ids(text, rel, slug):
    """Namespace every id - and every reference to one - so 35 pages cannot collide."""
    keep = KEEP | KEEP_ON.get(rel, set())

    def ns(attr, value, slug=slug, keep=keep):
        if value in keep or value.startswith("rt-"):
            return '%s="%s"' % (attr, value)
        return '%s="rt-%s__%s"' % (attr, slug, value)

    text = re.sub(r'\bid="([^"]+)"', lambda m: ns("id", m.group(1)), text)
    for attr in IDREF:
        text = re.sub(r'\b%s="([^"]+)"' % attr, lambda m: ns(attr, m.group(1)), text)
    def anchor(m):
        frag = m.group(1)
        if frag.startswith("rt-") or frag in keep:
            return 'href="#%s"' % frag
        return 'href="#rt-%s__%s"' % (slug, frag)

    return re.sub(r'href="#([^"]+)"', anchor, text)


def _link(match, known):
    whole, href = match.group(0), match.group(1)
    if href.startswith(("http", "tel:", "sms:", "mailto:", "#")):
        return whole
    path, _, frag = href.partition("#")
    path = path.split("../")[-1].split("/")[-1]
    target = known.get(path)
    if target is None:
        return whole
    return 'href="#rt-%s%s"' % (target, ("__" + frag) if frag else "")


def fix_asset_paths(text):
    return text.replace('href="../', 'href="').replace('src="../', 'src="')


HEAD_CSS = """
<style>
/* preview-only chrome; assets/alfa.css is untouched so what you see here is production */
.route{border-top:4px solid var(--copper);scroll-margin-top:140px}
.route>.route-bar{position:sticky;top:0;z-index:40;background:var(--ink);color:#fff;
  display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;padding:9px max(20px,4vw);
  font:500 12px/1.35 var(--mono);letter-spacing:.02em}
.route-bar .k{color:var(--copper);text-transform:uppercase;letter-spacing:.14em;font-size:10px}
.route-bar .p{color:#fff;opacity:.92}
.route-bar .t{font:600 13px/1.35 var(--body);opacity:.8;flex:1 1 220px;min-width:0}
.route-bar a{color:#fff;text-decoration:underline;text-underline-offset:3px;opacity:.78;font-size:11px}
.route-bar a:hover{opacity:1}
.rail{background:var(--porcelain);border-bottom:1px solid var(--line);padding:16px 0 14px}
.rail .wrap{display:flex;flex-direction:column;gap:10px}
.rail .lab{font:500 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-55)}
.rail .row{display:flex;flex-wrap:wrap;gap:6px}
.rail a{font:500 12px/1 var(--body);text-decoration:none;color:var(--ink);
  border:1px solid var(--line);border-radius:999px;padding:6px 10px;background:var(--paper)}
.rail a:hover{border-color:var(--brand);color:var(--brand-deep)}
.rail a.n{border-color:var(--brand-deep);background:var(--brand-deep);color:#fff}
.rail .modes{display:flex;gap:8px;align-items:center;margin-left:auto}
.rail .modes button{font:500 11px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;
  border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:7px 11px;cursor:pointer}
.rail .modes button[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
body[data-mode="single"] .route{display:none}
body[data-mode="single"] .route.is-active{display:block}
body[data-mode="single"] .route>.route-bar{position:static}
@media (prefers-reduced-motion:no-preference){
  .route:target>.route-bar{animation:flash 1.6s ease-out 1}
}
@keyframes flash{0%,40%{background:var(--brand-deep)}100%{background:var(--ink)}}
@media print{.rail,.route-bar a{display:none}.route{break-before:page}}
</style>
"""

SCRIPT = """
<script>
/* preview-only: optional one-route-at-a-time mode. Content never depends on it. */
(function(){
  var body = document.body, routes = [].slice.call(document.querySelectorAll('.route'));
  if (!routes.length) return;
  var bAll = document.getElementById('mode-all'), bOne = document.getElementById('mode-one');
  var nav = document.getElementById('routenav');
  function active(){
    var m = (location.hash || '').match(/^#rt-([\\w-]+?)(?:__|$)/);
    return m ? m[1] : routes[0].getAttribute('data-slug');
  }
  function apply(){
    var id = active();
    routes.forEach(function(r){ r.classList.toggle('is-active', r.getAttribute('data-slug') === id); });
    var cur = document.getElementById('mode-cur');
    if (cur) cur.textContent = routes.filter(function(r){return r.getAttribute('data-slug')===id;})
      .map(function(r){return r.getAttribute('data-path');})[0] || '';
    if (nav) nav.textContent = (routes.map(function(r){return r.getAttribute('data-slug');}).indexOf(id) + 1)
      + ' / ' + routes.length;
  }
  function setMode(single){
    body.setAttribute('data-mode', single ? 'single' : 'all');
    if (bAll) bAll.setAttribute('aria-pressed', single ? 'false' : 'true');
    if (bOne) bOne.setAttribute('aria-pressed', single ? 'true' : 'false');
    apply();
    if (single) window.scrollTo(0, document.querySelector('.rail').offsetHeight);
  }
  if (bAll) bAll.addEventListener('click', function(){ setMode(false); });
  if (bOne) bOne.addEventListener('click', function(){ setMode(true); });
  [].slice.call(document.querySelectorAll('[data-step]')).forEach(function(btn){
    btn.addEventListener('click', function(){
      var i = routes.map(function(r){return r.getAttribute('data-slug');}).indexOf(active());
      var n = (i + (btn.getAttribute('data-step') === 'next' ? 1 : -1) + routes.length) % routes.length;
      location.hash = 'rt-' + routes[n].getAttribute('data-slug');
      if (body.getAttribute('data-mode') !== 'single') setMode(true);
      routes[n].scrollIntoView({block:'start'});
    });
  });
  window.addEventListener('hashchange', apply);
  apply();
})();
</script>
"""


def build():
    known = {}
    guides = collect_guide_routes()
    routes = [(rel, label, note) for rel, label, note in TOP]
    routes += [(rel, "", "DIY guide, published %s" % date) for rel, date, _ in guides]

    for rel, _l, _n in routes:
        known[os.path.basename(rel)] = stem(rel)

    pieces, index_html, n = [], [], 0
    for rel, label, note in routes:
        src = read(rel)
        slug = stem(rel)
        if not label:
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S)
            label = unescape_tags(h1.group(1)) if h1 else slug
        body = strip_scripts(main_of(src))
        body = route_ids(link_all(fix_asset_paths(body), known), rel, slug)
        n += 1
        pieces.append(
            '<section class="route" id="rt-%s" data-slug="%s" data-path="/%s">\n'
            '  <div class="route-bar"><span class="k">Route %02d</span>'
            '<span class="p">/%s</span><span class="t">%s</span>'
            '<a href="%s">Open standalone page &#8599;</a><a href="#top">Top &#8593;</a></div>\n'
            '  <div class="route-body">\n%s\n  </div>\n</section>\n'
            % (slug, slug, rel, n, rel, html.escape(note or "", quote=False), rel, body)
        )
        index_html.append('<a href="#rt-%s"%s>%s</a>'
                          % (slug, ' class="n"' if rel == "index.html" else "",
                             html.escape(label)))

    # shared header (utility bar + nav + logo) taken from the homepage, re-linked
    home = read("index.html")
    header = home[home.index('<div class="util">'):home.index('<main id="main">')]
    header = link_all(header, known)
    header = header.replace(' class="on"', "").replace(' aria-current="page"', "")
    footer = home[home.index("<footer"):home.index("</footer>") + len("</footer>")]
    footer = link_all(footer, known)

    head = home[home.index("<head>"):home.index("</head>") + len("</head>")]
    head = re.sub(r"<link rel=\"canonical\"[^>]*>",
                  '<meta name="robots" content="noindex,nofollow">', head)
    head = re.sub(r'\n<meta property="og:(url|image)"[^>]*>', "", head)
    head = re.sub(r"<title>.*?</title>",
                  "<title>Alfa Plumbing Services &mdash; every route in one file (35 routes)</title>", head, flags=re.S)
    head = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  r"\1One file containing all 35 routes of the reimagined Alfa Plumbing Services site: "
                  r"15 navigation pages and 20 DIY guides, with working in-file navigation, "
                  r"tel/sms/mailto lead paths and production CSS.\2", head)
    # keep the site graph once, from the homepage, so the preview still carries the schema
    graph = re.search(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    head = head.replace(graph.group(0), "", 1) if graph else head
    head = head.replace("</head>", (graph.group(0) if graph else "") + HEAD_CSS + "\n</head>")

    rail = (
        '<nav class="rail" aria-label="All routes">\n  <div class="wrap">\n'
        '    <div class="row"><span class="lab">All routes (%d)</span>%s'
        '<span class="modes"><button id="mode-all" aria-pressed="true">Scroll all</button>'
        '<button id="mode-one" aria-pressed="false">One route at a time</button>'
        '<button data-step="prev" aria-label="Previous route">&larr;</button>'
        '<button data-step="next" aria-label="Next route">&rarr;</button>'
        '<code id="routenav"></code><code id="mode-cur"></code></span></div>\n'
        '  </div>\n</nav>\n'
    ) % (n, "\n".join(index_html[:n]))

    out = ["<!DOCTYPE html>\n<html lang=\"en\" class=\"no-js\">\n"
           '<script>document.documentElement.className="js";</script>\n',
           head, "\n<body id=\"top\" data-mode=\"all\">\n",
           '<a class="skip" href="#main">Skip to all routes</a>\n',
           header, rail,
           '\n<main id="main">\n', "\n".join(pieces), "\n</main>\n",
           footer, "\n", SCRIPT, "\n</body>\n</html>\n"]

    dest = os.path.join(ROOT, OUT)
    with open(dest, "w", encoding="utf-8") as f:
        f.write("".join(out))
    return dest, n, known, routes


def link_all(text, known):
    return re.sub(r'href="([^"]*)"', lambda m: _link_full(m, known, "rt-index"), text)


def _link_full(match, known, home_slug):
    whole, href = match.group(0), match.group(1)
    if href.startswith(("http", "tel:", "sms:", "mailto:", "#")):
        return whole
    path, _, frag = href.partition("#")
    path = path.split("../")[-1].split("/")[-1]
    if not path:
        return whole
    target = known.get(path)
    if target is None:
        return whole
    return 'href="#rt-%s%s"' % (target, ("__" + frag) if frag else "")


# ----------------------------------------------------------------- self-checks
def check(dest, n, routes):
    src = open(dest, encoding="utf-8").read()
    problems = []
    ids = re.findall(r'\sid="([^"]+)"', src)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append("duplicate ids in the collated file: %s" % ", ".join(dupes[:8]))
    targets = set(ids)
    for frag in re.findall(r'href="#([^"]+)"', src):
        if frag not in targets:
            problems.append("in-file link #{} has no target".format(frag))
    if src.count('<main') != 1:
        problems.append("expected exactly one <main>, found %d (nested main is invalid)"
                        % src.count("<main"))
    page_links = re.findall(r'<a[^>]*href="([^"]*\.html[^"]*)"', src)
    if len(page_links) != n:
        problems.append("standalone page links: %d, expected %d (one per route)"
                        % (len(page_links), n))
    for h in page_links:
        if "#" in h:
            problems.append("route bar link still carries an anchor: %s" % h)
    if src.count('class="route"') != n:
        problems.append("route sections: %s, expected %d" % (src.count('class="route"'), n))
    for rel, _l, _note in routes:
        if ("/%s" % rel) not in src:
            problems.append("route %s never made it into the file" % rel)
    if "mailto:info@alfaplumbingservices.com" not in src:
        problems.append("mailto lead path lost in the collation")
    if "assets/alfa.css" not in src:
        problems.append("stylesheet not linked")
    # every id reference must still resolve after namespacing
    for attr in ("for", "aria-controls", "aria-labelledby", "aria-describedby", "list"):
        for v in {x for x in re.findall(r'\b%s="([^"]+)"' % attr, src)}:
            if v not in targets:
                problems.append("%s=\"%s\" points at nothing" % (attr, v))
    if len(re.findall(r"<label", src)) != len(re.findall(r"<(?:input|select|textarea)\b", src)):
        problems.append("label/field parity broke in the collation")
    for keep in ("gcount", "book"):                      # looked up by id in alfa.js
        if 'id="%s"' % keep not in src:
            problems.append("id=\"%s\" must survive un-prefixed for alfa.js" % keep)
    if src.count('action="mailto:info@alfaplumbingservices.com" method="post" '
                 'enctype="text/plain"') != 2:
        problems.append("both booking forms must survive the collation")
    if 'content="noindex' not in src:
        problems.append("the preview must not be indexable")
    css = open(os.path.join(ROOT, "assets", "alfa.css"), encoding="utf-8").read()
    tokens = set(re.findall(r"--([\w-]+)\s*:", css))
    injected = re.search(r"<style>.*?</style>", src, re.S).group(0)
    for name in sorted({x for x in re.findall(r"var\(--([\w-]+)\)", injected)}):
        if name not in tokens:
            problems.append("preview style uses --%s, which alfa.css does not define" % name)
    return problems


def main():
    dest, n, _known, routes = build()
    problems = check(dest, n, routes)
    kb = os.path.getsize(dest) / 1024
    print("wrote %s (%.0f kB) · %d routes · %d kB of route content inlined"
          % (OUT, kb, n, sum(len(read(r)) for r, _l, _ in routes) / 1024))
    for p in problems:
        print("  !", p)
    if problems:
        sys.exit(1)
    print("  in-file links resolve, ids unique, one <main>, mailto + stylesheet intact")


if __name__ == "__main__":
    main()
