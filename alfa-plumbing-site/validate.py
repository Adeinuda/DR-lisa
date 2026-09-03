#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation for the Alfa multi-page build: links, anchors, alt text, JSON-LD, tag balance,
duplicate ids, form wiring, and the no-legacy-links rule. Run after build.py."""
import json, os, re, sys
from html.parser import HTMLParser
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
OUTBOUND_ALLOWED = ("tel:", "sms:", "mailto:", "https://www.google.com/maps", "https://search.google.com",
                    "https://www.yelp.com")

problems = []


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.ids, self.imgs, self.hrefs, self.scripts, self.forms = [], Counter(), [], [], [], []
        self.cur_script, self.in_script = [], False
        self.form_attrs = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))
        if "id" in a:
            self.ids[a["id"]] += 1
        if tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt")))
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "form":
            self.forms.append({k: a.get(k) for k in ("action", "method", "enctype")})
        if tag == "script":
            self.in_script = True
            self.cur_script = []
            self.script_type = a.get("type", "")

    def handle_startendtag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids[a["id"]] += 1
        if tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt")))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                open_tag, pos = self.stack.pop(i)
                return
        problems.append("%s: stray </%s>" % (self.name, tag))
        if tag == "script":
            if self.script_type == "application/ld+json":
                self.scripts.append("".join(self.cur_script))
            self.in_script = False

    def handle_data(self, data):
        if self.in_script:
            self.cur_script.append(data)


files = []
for dirpath, _dirs, names in os.walk(ROOT):
    if "assets" in dirpath:
        continue
    for n in sorted(names):
        if n.endswith(".html"):
            files.append(os.path.relpath(os.path.join(dirpath, n), ROOT))

anchors = {}
parsed = {}
for rel in files:  # pass 1: collect ids so cross-page anchors resolve regardless of file order
    src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    anchors[rel] = set(re.findall(r'\sid="([^"]+)"', src))
for rel in files:
    src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    p = P()
    p.name = rel
    p.feed(src)
    p.close()
    parsed[rel] = p
    ids = set(re.findall(r'\sid="([^"]+)"', src))
    anchors[rel] = ids
    # unclosed tags
    for tag, pos in p.stack:
        if tag in ("html", "body", "head"):
            continue
        problems.append("%s: <%s> opened at %s never closed" % (rel, tag, pos))
    # duplicate ids
    for i, n in p.ids.items():
        if n > 1:
            problems.append("%s: id '%s' used %d times" % (rel, i, n))
    # alt text
    for src_, alt in p.imgs:
        if alt is None or not alt.strip():
            problems.append("%s: <img> without alt (%s)" % (rel, src_[:70]))
    # JSON-LD
    for raw in p.scripts:
        try:
            json.loads(raw.replace("<\\/", "</"))
        except Exception as e:
            problems.append("%s: bad JSON-LD — %s" % (rel, e))
    # links
    for href in p.hrefs:
        if href.startswith("#"):
            if href != "#top" and href[1:] not in anchors[rel]:
                problems.append("%s: dead anchor %s" % (rel, href))
            continue
        if href.startswith(OUTBOUND_ALLOWED):
            continue
        if href.startswith("http"):
            problems.append("%s: disallowed outbound link %s" % (rel, href))
            continue
        path, _, frag = href.partition("#")
        if path.startswith("../"):
            target = os.path.normpath(os.path.join(os.path.dirname(rel), path))
        elif path.startswith("guides/") or "/" in path:
            target = path
        else:
            target = os.path.join(os.path.dirname(rel), path) if "/" in rel else path
        target = os.path.normpath(target)
        if not os.path.exists(os.path.join(ROOT, target)):
            problems.append("%s: broken link %s" % (rel, href))
            continue
        if frag and frag not in anchors.get(target, set()):
            problems.append("%s: missing anchor %s in %s" % (rel, href, target))
    # form wiring
    for f in p.forms:
        if f["action"] and "mailto:" not in f["action"]:
            problems.append("%s: form action is not mailto (%s)" % (rel, f["action"]))
        if f["method"] != "post" or f["enctype"] != "text/plain":
            problems.append("%s: form needs method=post enctype=text/plain (%s)" % (rel, f))
    # local <link>/<script> assets must exist
    for m in re.finditer(r'<(?:link|script)[^>]*(?:href|src)="([^"#]+?)"', src):
        u = m.group(1)
        if u.startswith(("http", "mailto:", "data:")):
            continue
        target = os.path.normpath(os.path.join(os.path.dirname(rel), u))
        if not os.path.exists(os.path.join(ROOT, target)):
            problems.append("%s: missing asset %s" % (rel, u))
    # content rules
    if re.search(r"<a [^>]*href=\"https?://alfaplumbingservices\.com", src):
        problems.append("%s: link back to the legacy site" % rel)
    visible = re.sub(r"<[^>]+>", " ", src)
    for bad in ("Since '94", "since '94", "1994", "Lorem ipsum", "TODO", "placeholder", "[insert", "lorem"):
        if bad in visible:
            problems.append("%s: suspicious legacy copy '%s'" % (rel, bad))
    if '"hours"' in src.lower() or "OpeningHours" in src:
        problems.append("%s: hours present but never published — must stay out" % rel)

# cross-file: every generated page reachable from nav or footer
reachable = set()
for rel in ("index.html",):
    for h in parsed[rel].hrefs:
        reachable.add(os.path.normpath(h.partition("#")[0] or "index.html"))
print("%d pages · %d problems" % (len(files), len(problems)))
for x in problems[:60]:
    print("  !", x)
if len(problems) > 60:
    print("  … %d more" % (len(problems) - 60))
sys.exit(1 if problems else 0)
