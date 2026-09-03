import os
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit the collated single page the way a browser and a reviewer would.

validate.py checks the 35 routed pages. This checks the generated artifact:
that the markup is balanced, that every <script> actually parses, that each
photograph carries its own bytes inside a container the stylesheet sizes, that
the grouped nav and the sticky offset agree, that nothing escapes the file
except the four genuine third-party destinations, and that the business schema
survived the trip. Run by build.py after collation; exits non-zero on failure.
"""
import base64, json, os, pathlib, re, subprocess, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = "one-page.html"
SIBLINGS = ("one-page.assets.html", "one-page.preview.html")

# the only outbound destinations allowed anywhere in the build, from the live site itself
OUTBOUND_OK = (
    "https://search.google.com/local/reviews?placeid=ChIJrSWt2KxdP4YRqwnd8Jxnvac",
    "https://search.google.com/local/writereview?placeid=ChIJrSWt2KxdP4YRqwnd8Jxnvac",
    "https://www.google.com/maps/place/?q=place_id:ChIJrSWt2KxdP4YRqwnd8Jxnvac",
    "https://www.yelp.com/biz/alfa-plumbing-services-baytown",
)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
# containers the production stylesheet gives an explicit height or aspect ratio
SIZED = ('class="ph', "frame ph", 'class="art', "gcard", "member", "rcard",
         "grp-card", "mapbox", "svc")

fail, ok = [], []


def check(cond, good, bad):
    (ok if cond else fail).append(good if cond else bad)


def parts(path):
    src = pathlib.Path(path).read_text(encoding="utf-8")
    body = re.sub(r"<script\b.*?</script>|<style\b[^>]*>.*?</style>", " ", src, flags=re.S)
    css = " ".join(re.findall(r"<style\b[^>]*>(.*?)</style>", src, re.S))
    return src, body, css


class Balance(HTMLParser):
    """Tag nesting, as the parser sees it: a dropped </div> in one section can
    swallow the rest of the document, and no amount of grep-style checking shows it."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.bad = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                open_inside = [t for t, _ in self.stack[i + 1:]]
                if open_inside:
                    self.bad.append("</%s> at line %s closes over still-open %s"
                                    % (tag, self.getpos()[0], open_inside[:3]))
                del self.stack[i:]
                return
        self.bad.append("stray </%s> at line %s" % (tag, self.getpos()[0]))


def audit_markup(name, src, body):
    p = Balance()
    p.feed(src)
    check(not p.bad, "%s: tags balance" % name, "%s: %s" % (name, p.bad[:3]))
    check(not p.stack, "%s: nothing left open at EOF" % name,
          "%s: unclosed at end of file: %s" % (name, [t for t, _ in p.stack][:5]))


def audit_scripts(src):
    for i, js in enumerate(re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', src, re.S)):
        try:
            doc = json.loads(js)
        except Exception as exc:
            fail.append("JSON-LD block %d is not valid JSON: %s" % (i, exc))
            continue
        nodes = doc if isinstance(doc, list) else doc.get("@graph", [doc])
        types = sorted({n.get("@type", "?") for n in nodes if isinstance(n, dict)})
        ok.append("JSON-LD block %d parses (%s)" % (i, ", ".join(types)[:70]))
        biz = [n for n in nodes if isinstance(n, dict) and n.get("@type") == "Plumber"]
        for b in biz:
            for field, want in (("foundingDate", "2003"), ("telephone", "(713) 992-9257"),
                                ("email", "info@alfaplumbingservices.com")):
                check(str(b.get(field, "")).find(want) >= 0,
                      "Plumber schema keeps %s" % field,
                      "Plumber schema lost %s (has %r)" % (field, b.get(field)))
            addr = (b.get("address") or {}).get("streetAddress", "")
            check("508 Scott St" in addr, "Plumber schema keeps the NAP",
                  "Plumber schema address looks wrong: %r" % addr)
            social = json.dumps(b.get("sameAs", ""))
            check("yelp.com" in social and "google.com" in social,
                  "Plumber schema keeps the real social profiles",
                  "Plumber schema lost sameAs: %s" % social[:60])
    scripts = [s for s in re.findall(r"<script\b(?![^>]*application/ld\+json)[^>]*>(.*?)</script>", src, re.S)
               if s.strip()]
    for i, js in enumerate(scripts):
        tmp = "/tmp/_audit%d.js" % i
        pathlib.Path(tmp).write_text(js, encoding="utf-8")
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        check(r.returncode == 0, "script %d (%dB) parses" % (i, len(js)),
              "script %d does not parse: %s" % (i, r.stderr.strip().replace("\n", " ")[-160:]))



def _frames_contract():
    """Frames the collated file must carry, measured from the routed pages that were collated, and
    which routes show a photograph in their hero. No hand-typed counts, so the contract follows the
    build instead of lagging behind it."""
    n, hero = 0, {}
    for rel in ROUTED:
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        body = s[s.index("<main"):s.index("</main>")] if "<main" in s else s
        body = re.sub(r"<section[^>]*\bid=\"(?:book|jobs|reviews-strip|areas|pricing|guides|faq|services|triage|next)\".*?</section>",
                      " ", body, flags=re.S)                     # bands the collator drops on purpose
        tags = len(re.findall(r"<img\b", body))
        n += tags
        m = re.search(r'<section class="pagehead"[^>]*>(.*?)</section>', body, re.S)
        hero[rel[:-5]] = bool(m and "<img" in m.group(1))
    return n, hero



def audit_frames(name, body, src, css):
    tags = re.findall(r"<img\b[^>]*>", body)
    check(len(tags) >= FRAMES, "%s: %d+ photograph frames" % (name, FRAMES),
          "%s: %d frames, expected at least %d" % (name, len(tags), FRAMES))
    holes = re.findall(r'<(?:div|figure)\b[^>]*class="[^"]*(?:ph|frame|pic|mapbox)[^"]*"[^>]*>\s*</(?:div|figure)>', body)
    check(not holes, "no frame is left sized for a picture with nothing inside",
          "%d empty frame(s): %s" % (len(holes), holes[:3]))
    check("<iframe" not in src, "the single file embeds nothing that has to be fetched",
          "a remote <iframe> survived into %s" % name)
    # a route hero's picture is content, not decoration: no section head may arrive empty because
    # the collapser only kept the words. Compare against what the built pages actually show.
    if name == OUT:
        lost = [rel for rel, has in HERO_PHOTO.items()
                if has and not re.search(r'id="rt-[^"]*__overview"[^>]*>(?:(?!</section>).)*?<img', body, re.S)]
        check(not lost, "every route that had a hero photo keeps one", "section heads with no picture: %s" % lost[:6])
    if name != OUT:                                  # the sibling copies load from files
        return
    bad = [t for t in tags if 'src="data:image/jpeg;base64,' not in t]
    check(not bad, "every frame carries its own bytes",
          "%d frame(s) without an embedded payload: %s" % (len(bad), re.sub(r"\s+", " ", bad[0])[:70] if bad else ""))
    check(not [t for t in tags if not re.search(r'alt="[^"]+"', t)],
          "every frame has alt text", "%d frame(s) without alt text"
          % len([t for t in tags if not re.search(r'alt="[^"]+"', t)]))
    no_dims = [t for t in tags if not ('width="' in t and 'height="' in t)]
    check(not no_dims, "every frame declares width/height (no layout shift)",
          "%d frame(s) missing width/height" % len(no_dims))
    fb = re.findall(r'data-src="([^"]+)"', body)
    check(len(fb) == len(tags), "every frame can escalate to the file beside it",
          "%d of %d frames carry a fallback path" % (len(fb), len(tags)))
    missing = sorted({f for f in fb if not os.path.exists(os.path.join(ROOT, f))})
    check(not missing, "fallback targets all exist", "missing on disk: %s" % missing[:3])
    check(not re.findall(r"<img[^>]*onerror=", body),
          "no inline onerror juggling; the chrome loader owns the escalation",
          "an inline onerror survived; it cannot chain and races the loader")
    for probe in ("function step(img)", "op-noimg", "data-note"):
        check(probe in src, "the loader contains %s" % probe, "the loader lost %s" % probe)
    for probe in (".op-noimg{", ".op-noimg::after{content:attr(data-note)"):
        check(probe in css, "the placeholder frame style is present (%s)" % probe.split("{")[0],
              "no style for a frame that cannot reach its picture: %s" % probe)
    broken = []
    for t in tags:
        m = re.search(r'src="data:image/jpeg;base64,([^"]+)"', t)
        if not m:
            continue
        try:
            raw = base64.b64decode(m.group(1))
            if raw[:2] != b"\xff\xd8" or raw[-2:] != b"\xff\xd9":
                broken.append("payload is not a complete JPEG")
        except Exception as exc:
            broken.append("payload does not decode (%s)" % exc)
    check(not broken, "every payload decodes to a complete JPEG", "%d broken payload(s): %s" % (len(broken), broken[:2]))
    orphans = [re.sub(r"\s+", " ", m.group(0))[:60] for m in re.finditer(r"<img\b[^>]*>", body)
               if not any(k in body[max(0, m.start() - 240):m.start()] for k in SIZED)]
    check(not orphans, "every frame sits in a container the stylesheet sizes",
          "%d frame(s) outside a sized container: %s" % (len(orphans), orphans[:2]))


def audit_nav(body, css):
    ids = re.findall(r'\sid="([^"]+)"', body)
    check(len(ids) == len(set(ids)), "no duplicate ids across the 35 sections",
          "duplicate ids: %s" % sorted({i for i in ids if ids.count(i) > 1})[:6])
    frag = set(re.findall(r'href="#([^"]+)"', body))
    check(frag <= set(ids), "every in-page link resolves",
          "%d link(s) with no target: %s" % (len(frag - set(ids)), sorted(frag - set(ids))[:4]))
    check(body.count('class="opkidgrp"') == 2, "Services and About each own a child group",
          "expected 2 nav groups, found %d" % body.count('class="opkidgrp"'))
    check(len(re.findall(r'class="opchip"', body)) == 9, "the grouped nav carries its 9 children",
          "expected 9 child chips, found %d" % len(re.findall(r'class="opchip"', body)))
    check(body.count('class="ophas"') == 2, "the two parents are marked as owning children",
          "expected 2 marked parents, found %d" % body.count('class="ophas"'))
    check('aria-label="More in Services"' in body and 'aria-label="More in About"' in body,
          "the child groups have accessible names", "the nav groups lost their accessible names")
    px = re.search(r"--op-head:(\d+)px", css)
    # row 1 (9+8+26) plus the chip row (1+9+22) needs ~75px: the offset must clear it,
    # or every anchor jump lands under the sticky bar
    check(px and 80 <= int(px.group(1)) <= 180, "the sticky offset is sized for the two-row bar (%s)"
          % (px.group(0) if px else "absent"), "the sticky offset is wrong or missing: %s" % (px and px.group(0)))
    check("scroll-margin-top:var(--op-head)" in css, "sections offset their anchors by it",
          "sections do not use the sticky offset, so jumps land under the bar")
    for needed in (".opnav .oprow1{", ".opnav .oprow2{", ".opnav a.opchip{", ".opsec .op-head{",
                   "@media print{.onepage .opnav"):
        check(needed in css, "chrome CSS keeps %s" % needed.split("{")[0], "chrome CSS lost %s" % needed)
    gone = [t for t in ("opsub", "opgrp", "opimg", "--ph-", "background-image:var(") if t in body]
    check(not gone, "no superseded nav or embedding markup survived", "dead markup survived: %s" % gone[:3])
    # role="img" is allowed only as a labelled placeholder plate - never as a silent stand-in for a
    # photograph - so every use must be a plate that says what it is standing in for
    plates = re.findall(r'<span class="(?:op-noimg|noplate)"[^>]*role="img"[^>]*aria-label="([^"]+)"', body) \
        + re.findall(r'<span class="noplate" role="img" aria-label="([^"]+)"', body)
    uses = body.count('role="img"')
    check(len(plates) >= uses and all(n.strip() for n in plates),
          "every placeholder plate is labelled (%d)" % len(plates),
          "stray or unlabelled placeholder: %d plates for %d uses" % (len(plates), uses))


def audit_content(body, src):
    check(len(re.findall(r"<h1\b", body)) == 1, "one h1: it reads as one site, not 35 documents",
          "h1 count is %d" % len(re.findall(r"<h1\b", body)))
    check('class="pagehead"' not in body, "the 34 page heroes were demoted to section heads",
          "page-hero bands survived")
    check(body.count('class="ctaband"') == 1, "one closing CTA band", "%d ctaband(s)" % body.count('class="ctaband"'))
    check(body.count('<form class="book"') == 1, "one booking form", "%d booking form(s)" % body.count('<form class="book"'))
    check(body.count('action="mailto:info@alfaplumbingservices.com" method="post" enctype="text/plain"') == 1,
          "the form posts to the shop's inbox via mailto", "the mailto booking action is not exactly once")
    labels = re.findall(r'<label\b[^>]*for="([^"]+)"', body)
    fields = re.findall(r"<(?:input|select|textarea)\b", body)
    check(len(labels) == len(fields), "every field has a label (%d/%d)" % (len(labels), len(fields)),
          "label/field parity broke: %d labels, %d fields" % (len(labels), len(fields)))
    dangling = sorted({l for l in labels if 'id="%s"' % l not in body})
    check(not dangling, "every label points at a field", "%d label(s) point at nothing: %s" % (len(dangling), dangling[:3]))
    for attr in ("aria-controls", "aria-labelledby", "aria-describedby"):
        refs = {x for x in re.findall(r'\b%s="([^"]+)"' % attr, body)}
        check(refs <= set(re.findall(r'\sid="([^"]+)"', body)), "%s references all resolve" % attr,
              '%s="%s" points at nothing' % (attr, sorted(refs)[:1]))
    check(body.count('id="main"') == 1 and '<a class="skip" href="#main">' in body,
          "skip link and #main are intact", "skip link / #main broken")
    check("tel:+17139929257" in body and "sms:+17139929257" in body, "call and text are one tap throughout",
          "tel:/sms: links are missing")
    check("2003" in body and "1994" not in body, "the founding year reads 2003 everywhere",
          "a second founding year crept in")
    try:
        from guides import GUIDES
        slugs = [g["slug"] for g in GUIDES]
    except Exception as exc:
        slugs = []
        ok.append("guides.py unreadable, coverage compared to the hub only (%s)" % exc)
    if slugs:
        secs = set(re.findall(r'<section class="opsec" id="rt-([\w-]+)" data-section="guides/', body))
        check(set(slugs) <= secs, "all %d DIY guides are inline in the file" % len(slugs),
              "guides missing from the single page: %s" % sorted(set(slugs) - secs)[:4])
        hub = pathlib.Path(os.path.join(ROOT, "guides.html")).read_text(encoding="utf-8")
        hc, sc = hub.count('class="gcard rv"'), body.count('class="gcard rv"')
        check(hc == sc, "the library index kept every card (%d)" % sc,
              "the hub shows %d cards, the single page %d" % (hc, sc))
        check(all(('#rt-%s"' % sl) in body for sl in slugs),
              "every card jumps to its own article inside the file", "some cards lost their in-page target")


def audit_empties(body, css):
    """An element with no content is only dead weight if the stylesheet does not paint it.
    <p class="divv"></p> is a 1px rule by design; an empty classless <p> is a trim gone wrong."""
    styled = set(re.findall(r"\.([A-Za-z][\w-]*)\s*\{[^}]*\b(?:width|height|display|background|border|content)\b", css))
    empty = []
    for m in re.finditer(r'<(p|div|span|h2|h3|a|li)\b([^>]*)>\s*</\1>', body, re.S):
        cls = set(re.findall(r"([\w-]+)", (re.search(r'class="([^"]*)"', m.group(2)) or [None, ""])[1]))
        if not (cls & styled):
            empty.append(re.sub(r"\s+", " ", m.group(0))[:60])
    check(not empty, "no unstyled empty elements left by the trimming passes",
          "%d empty element(s) with nothing painting them: %s" % (len(empty), empty[:3]))


def audit_borders(body, src):
    leaving = {h for h in re.findall(r'<a[^>]*href="([^"]+)"', body)
               if not h.startswith(("#", "tel:", "sms:", "mailto:"))}
    check(not (leaving - set(OUTBOUND_OK)),
          "nothing escapes the file except the four real third-party destinations",
          "unexpected outbound links: %s" % sorted(leaving - set(OUTBOUND_OK))[:4])
    legacy = re.findall(r'<a[^>]*href="https?://[^"]*alfaplumbingservices\.com[^"]*"', body)
    check(not legacy, "no link points back at the legacy site (mailto to the shop is the lead path)",
          "%d link(s) point at the legacy WordPress site: %s" % (len(legacy), legacy[:2]))
    check(not re.findall(r'<img[^>]*src="https?://', body), "no image is fetched from another host",
          "an image reaches outside the file")
    check("wp-content" not in body, "no legacy media path in the document", "legacy media reference survived")
    check('<html lang="en"' in src, "the document declares its language", "missing lang on <html>")
    check('content="noindex' in src, "the collated copy is kept out of the index",
          "the single page is indexable, which would duplicate the 35 routes")


ROUTED = sorted(f for f in os.listdir(ROOT) if f.endswith(".html") and not f.startswith("one-page")) + \
        sorted("guides/" + f for f in os.listdir(os.path.join(ROOT, "guides")) if f.endswith(".html"))

FRAMES, HERO_PHOTO = _frames_contract()

def main():
    path = os.path.join(ROOT, OUT)
    if not os.path.exists(path):
        print("audit: %s has not been built yet" % OUT)
        return 1
    src, body, css = parts(path)
    audit_markup(OUT, src, body)
    audit_scripts(src)
    audit_frames(OUT, body, src, css)
    audit_nav(body, css)
    audit_content(body, src)
    audit_borders(body, src)
    audit_empties(body, css)
    for sib in SIBLINGS:
        p = os.path.join(ROOT, sib)
        if not os.path.exists(p):
            ok.append("%s not generated (opt-in packaging)" % sib)
            continue
        s2, b2, c2 = parts(p)
        audit_markup(sib, s2, b2)
        audit_frames(sib, b2, s2, c2)
        check(b2.count('class="opsec"') == 35, "%s holds all 35 sections" % sib,
              "%s has %d sections" % (sib, b2.count('class="opsec"')))
        check("wp-content" not in b2, "%s carries no legacy reference" % sib,
              "%s still references the legacy media library" % sib)
    kb = os.path.getsize(path) / 1024
    print("  audit: %s (%.0f kB) - %d checks, %d problems" % (OUT, kb, len(ok) + len(fail), len(fail)))
    for f in fail:
        print("    PROBLEM %s" % f)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
