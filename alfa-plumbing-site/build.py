#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alfa Plumbing Services — multi-page build generator.

Run:  python3 build.py
Writes index.html, the company pages, four service-cluster pages, services.html and
20 guide pages under guides/. Everything shares assets/alfa.css + assets/alfa.js.

Content policy: only facts published on alfaplumbingservices.com are used. Nothing here
invents hours, licence numbers, reviews, prices or services.
"""
import json, os, re, html, datetime
from content import (ORG, IMG, CLUSTERS, TRIAGE, PRICING, OFFER, FAQS,
                     REVIEWERS, REVIEW_THEMES, AREAS, TEAM, PROJECTS)
from guides import GUIDES

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://alfaplumbingservices.com"
PHONE_TEL = "tel:" + ORG["phone_tel"]
SMS = "sms:" + ORG["phone_tel"]
MAIL = "mailto:" + ORG["email"]
PLACE = "ChIJrSWt2KxdP4YRqwnd8Jxnvac"
TODAY = "2026-09-03"

SERVICES = [(n, a, file) for c in CLUSTERS for (a, n, _d) in c["services"] for file in [c["file"]]]
BY_GUIDE = {g["slug"]: g for g in GUIDES}


# ---------------------------------------------------------------- nav / chrome
CLUSTER_BY_ID = {c["id"]: c for c in CLUSTERS}
COMPANY = [
    ("About Alfa", "about.html", "The company, the guarantee and the licence"),
    ("Our team", "team.html", "Who shows up with the truck"),
    ("Projects", "projects.html", "Real jobs, real photos, from the shop"),
    ("Reviews", "reviews.html", "What Baytown says about us"),
    ("Service areas", "service-areas.html", "Baytown and twelve surrounding cities"),
    ("What it costs", "pricing.html", "Published ranges and free estimates"),
    ("FAQ", "faq.html", "Straight answers, no sales copy"),
    ("Contact & book", "contact.html", "Call, text or send the request form"),
]


def nav_html(active):
    mega = []
    for i, c in enumerate(CLUSTERS, 1):
        rows = ['<span class="grp">%s</span>' % c["name"]]
        rows.append('<a href="%s"%s><i>&rarr;</i>Open the %s page</a>'
                    % (c["file"], ' class="on" aria-current="page"' if active == c["file"] else "", c["name"].lower()))
        for j, (sid, sname, _d) in enumerate(c["services"], 1):
            rows.append('<a href="%s#%s"><i>%d%d</i>%s</a>' % (c["file"], sid, i, j, sname))
        mega.append("\n".join(rows))
    mega_html = "\n".join(mega)

    def on(href):
        return ' class="on" aria-current="page"' if href == active else ""

    # Reviews / Areas / Costs / Contact already own a top-level slot — no duplicates in the dropdown
    top_level = {"reviews.html", "service-areas.html", "pricing.html", "contact.html"}
    comp = ['<span class="grp">The company</span>']
    comp += ['<a href="%s"%s><i>&raquo;</i>%s</a>' % (h, on(h), n) for n, h, _d in COMPANY if h not in top_level]
    guides = ['<span class="grp">Browse the guides</span>',
              '<a href="guides.html"%s><i>&raquo;</i>All 20 guides</a>' % on("guides.html")]
    for cat in ["DIY Tutorial", "Plumbing Tips", "Emergency", "Services"]:
        n = len([g for g in GUIDES if g["cat"] == cat])
        guides.append('<a href="guides.html#%s"><i>&raquo;</i>%s <em>%d</em></a>' % (cat_key(cat), cat, n))
    guides.append('<a href="guides/how-to-fix-a-leaky-faucet.html"><i>&raquo;</i>Fix a leaky faucet</a>')

    items = [
        ('<li class="drop"><button class="mtop"%s id="svcbtn" aria-expanded="false" aria-controls="svcpanel">Services</button>'
         '<div class="panel" id="svcpanel" role="region" aria-label="All plumbing services">%s'
         '</div></li>' % (' class="on"' if active in ("services.html",) + tuple(c["file"] for c in CLUSTERS) else "", mega_html)),
        '<li class="drop drop--narrow"><button class="mtop"%s aria-expanded="false" aria-controls="comppanel">About</button>'
        '<div class="panel" id="comppanel" role="region" aria-label="Company">%s</div></li>'
        % (' class="on"' if active in [h for _n, h, _d in COMPANY] else "", "\n".join(comp)),
        '<li><a href="reviews.html"%s>Reviews</a></li>' % on("reviews.html"),
        '<li><a href="service-areas.html"%s>Service Areas</a></li>' % on("service-areas.html"),
        '<li><a href="pricing.html"%s>What It Costs</a></li>' % on("pricing.html"),
        '<li class="drop drop--narrow"><button class="mtop"%s aria-expanded="false" aria-controls="gdpanel">DIY Guides</button>'
        '<div class="panel" id="gdpanel" role="region" aria-label="DIY guides">%s</div></li>'
        % (' class="on"' if active.startswith("guides/") or active == "guides.html" else "", "\n".join(guides)),
        '<li><a href="contact.html"%s>Contact</a></li>' % on("contact.html"),
    ]

    drawer = []
    for c in CLUSTERS:
        drawer.append('<span class="grp">%s</span>' % c["name"])
        drawer.append('<a class="svc" href="%s">%s</a>' % (c["file"], c["tagline"]))
        for sid, sname, _d in c["services"]:
            drawer.append('<a class="svc" href="%s#%s">&middot; %s</a>' % (c["file"], sid, sname))
    drawer.append('<span class="grp">Guides</span>')
    drawer.append('<a href="guides.html">All 20 DIY guides &amp; plumbing tips</a>')
    drawer.append('<span class="grp">Company</span>')
    for n, h, d in COMPANY:
        drawer.append('<a href="%s"%s>%s</a>' % (h, on(h), n))
    return """
<div class="util">
  <div class="wrap">
    <a href="{tel}" aria-label="Call Alfa Plumbing Services at 713 992 9257">&#9742; 713-992-9257</a>
    <span class="sep" aria-hidden="true">/</span>
    <a href="{sms}">Text us</a>
    <span class="sep" aria-hidden="true">/</span>
    <a class="hide-s" href="{mail}">{email}</a>
    <span class="tag">Baytown &middot; Family-owned since {since} &middot; Licensed TX Master Plumber</span>
  </div>
</div>
<header class="hd">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Alfa Plumbing Services — home">
      <img src="{logo}" alt="Alfa Plumbing Services logo" width="550" height="124" onerror="this.style.display='none'">
      <span><span class="lw">Alfa Plumbing<br>Services</span>
      <span class="ls">Baytown, TX &middot; Since {since}</span></span>
    </a>
    <nav class="main" aria-label="Primary">
      <ul>
        {items}
      </ul>
    </nav>
    <div class="cta">
      <a class="btn btn--call" href="{tel}">Call {phone}</a>
      <a class="btn btn--ghost" href="contact.html#book">Book</a>
    </div>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="mobnav" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="mobnav" id="mobnav">
    <div class="wrap">
      {drawer}
    </div>
  </div>
</header>
""".format(tel=PHONE_TEL, sms=SMS, mail=MAIL, email=ORG["email"], since=ORG["founded"],
           logo=ORG["logo"], phone=ORG["phone_display"], items="\n".join(items), drawer="\n".join(drawer))


def cat_key(cat):
    return re.sub(r"[^a-z0-9]+", "-", cat.lower())


FOOTER = """
<footer class="ft" id="legal">
  <div class="wrap">
    <div class="ft-grid">
      <div>
        <div class="brandline">
          <img src="{logo}" alt="Alfa Plumbing Services logo" width="550" height="124" onerror="this.style.display='none'">
          <div class="n">Alfa Plumbing<br>Services</div>
        </div>
        <p class="about">Family-owned plumbing company in Baytown since {since}. Owner-operated by {owner},
        licensed and insured Texas Master Plumber, with a 100% workmanship guarantee on the work we do.</p>
        <div class="entity">
          <div><b>Founded</b> &mdash; {since}, Baytown, Texas</div>
          <div><b>Owner</b> &mdash; {owner}</div>
          <div><b>Address</b> &mdash; {street}, {city}, {state} {zip}</div>
          <div><b>Phone</b> &mdash; {phone} &middot; <b>Email</b> &mdash; {email}</div>
        </div>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          {svc_links}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          {co_links}
          <li><a href="guides.html">DIY guides &amp; plumbing tips</a></li>
        </ul>
      </div>
      <div>
        <h4>Reach us</h4>
        <ul>
          <li class="ft-phone"><a href="{tel}">{phone}</a></li>
          <li><a href="{sms}">Text a photo of the problem</a></li>
          <li><a href="{mail}">{email}</a></li>
          <li><a href="contact.html#book">Book an appointment</a></li>
          <li><a href="https://search.google.com/local/writereview?placeid={place}" target="_blank" rel="noopener nofollow">Leave a Google review &#8599;</a></li>
        </ul>
        <h4 style="margin-top:22px">Visit</h4>
        <p class="about" style="max-width:none">{street}<br>{city}, {state} {zip}</p>
        <p class="mono-note" style="color:rgba(255,255,255,.45);margin-top:8px">Call or text to reach the shop &mdash; phone is the fastest way to us.</p>
      </div>
    </div>
    <div class="bot">
      <div>&copy; {since}&ndash;2026 Alfa Plumbing Services &middot; {city}, {state} &middot; Design prototype for review</div>
      <div class="legal">
        <a href="faq.html">FAQ</a>
        <a href="pricing.html">Pricing</a>
        <a href="service-areas.html">Service areas</a>
        <a href="contact.html">Contact</a>
        <a href="index.html">Home</a>
      </div>
    </div>
  </div>
</footer>
<div class="mbar">
  <a class="btn btn--call" href="{tel}">&#9742; Call now</a>
  <a class="btn" href="contact.html#book">Request service</a>
</div>
""".format(logo=ORG["logo"], since=ORG["founded"], owner=ORG["owner"], street=ORG["street"],
           city=ORG["city"], state=ORG["state"], zip=ORG["zip"], phone=ORG["phone_display"],
           email=ORG["email"], tel=PHONE_TEL, sms=SMS, mail=MAIL, place=PLACE,
           svc_links="\n".join('<li><a href="%s#%s">%s</a></li>' % (f, a, n) for n, a, f in SERVICES),
           co_links="\n".join('<li><a href="%s">%s</a></li>' % (h, n) for n, h, _d in COMPANY))


def head(title, desc, fname, extra_schema=None, og=None):
    desc = meta_desc(DESCS.get(fname, desc))
    title = meta_title(TITLES.get(fname, title)).replace("&", "&amp;")
    canon = "%s/%s" % (SITE, fname)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": SITE + "/#website", "name": "Alfa Plumbing Services",
             "url": SITE + "/", "inLanguage": "en-US",
             "publisher": {"@id": SITE + "/#business"}},
            {"@type": "WebPage", "@id": canon, "url": canon, "name": title,
             "description": desc, "isPartOf": {"@id": SITE + "/#website"}, "datePublished": TODAY,
             "publisher": {"@id": SITE + "/#business"}},
        ],
    }
    graph = schema["@graph"]
    if extra_schema:
        graph.extend(extra_schema)
    js = json.dumps(schema, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return """<!DOCTYPE html>
<html lang="en" class="no-js">
<script>document.documentElement.className="js";</script>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0C2233">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Alfa Plumbing Services">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og}">
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Sans+3:ital,wght@0,300..700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/alfa.css">
<script type="application/ld+json">
{js}
</script>
</head>
<body id="top">
<a class="skip" href="#main">Skip to main content</a>
""".format(title=title, desc=desc.replace('"', "&quot;"), canon=canon, og=og or IMG["servicing"],
           fav=ORG["favicon"], pre=pre(fname), js=js)


TITLES = {
 "index.html": "Baytown Plumber, TX | Alfa Plumbing Services, Since 2003",
 "services.html": "All 20 Plumbing Services in Baytown | Alfa Plumbing",
 "water-heaters.html": "Water Heater Repair &amp; Install, Baytown | Alfa Plumbing",
 "drains-sewer.html": "Drain, Sewer &amp; Septic Services, Baytown | Alfa Plumbing",
 "leaks-gas-repairs.html": "Gas Line, Leak Detection &amp; Repairs | Alfa Plumbing",
 "repiping-remodels.html": "Repiping, Remodel &amp; New Build Plumbing | Alfa Plumbing",
 "about.html": "About Alfa Plumbing Services, Baytown Since 2003",
 "team.html": "The Alfa Plumbing Crew in Baytown, Texas",
 "projects.html": "Baytown Plumbing Projects, Real Jobsite Photos | Alfa",
 "reviews.html": "Alfa Plumbing Services Reviews, Baytown TX &mdash; 5.0",
 "service-areas.html": "Baytown Plumbing Service Areas, 12 Cities | Alfa Plumbing",
 "pricing.html": "Baytown Plumber Prices: What a Job Costs | Alfa Plumbing",
 "faq.html": "Plumbing FAQ, Answered by a Baytown Master Plumber",
 "guides.html": "20 Free Plumbing DIY Guides, Baytown Master Plumber",
 "contact.html": "Contact Alfa Plumbing Services, Baytown &mdash; Book a Visit",
}


DESCS = {
 "index.html": "Baytown plumbing since 2003: water heaters, drains, sewer, gas lines, leak detection and repipes. Licensed &amp; insured, same-day service. Call (713) 992-9257.",
 "services.html": "All 20 Alfa Plumbing services in one place, with what each visit includes and the prices the company publishes. Baytown, TX &middot; call (713) 992-9257.",
 "water-heaters.html": "Water heater repair, replacement, annual flush and tankless installs in Baytown. Same-day diagnostics, published price ranges, guaranteed workmanship.",
 "drains-sewer.html": "Drain cleaning, sewer camera and trenchless repair, and septic service with county permits filed. Camera first, then the right machine. Baytown, TX.",
 "leaks-gas-repairs.html": "Gas line repair, underground water leak detection, water line repair, faucet, toilet and disposal work, plus 24-hour emergency response in Baytown.",
 "repiping-remodels.html": "Whole-house repiping in PEX or copper, bath and kitchen remodel rough-ins, new construction and light commercial plumbing around Baytown, Texas.",
 "about.html": "Family-owned in Baytown since 2003 by Servando Perez: a licensed, insured Texas Master Plumber, a 100% workmanship guarantee and free walk-through estimates.",
 "team.html": "Who answers the phone and who turns up: owner and Texas Master Plumber Servando Perez, the licensed crew and the shop on Scott Street, Baytown.",
 "projects.html": "Eleven real Baytown jobsite photographs &mdash; water heaters, repipes, drain and sewer work, remodels and after-hours repairs, shot by the crew.",
 "reviews.html": "Alfa Plumbing Services holds 5.0 across 40 Google reviews as a Baytown plumber. Names, job types and the profile link &mdash; the words stay the customer's.",
 "service-areas.html": "Baytown plus Deer Park, La Porte, Pasadena, South Houston, Jacinto City, Galena Park, Houston, Channelview, Crosby, Mont Belvieu and Anahuac.",
 "pricing.html": "Baytown plumbing prices as published: $526 average visit, $201-$850 typical, $45-$150 an hour, tankless $1,000-$3,000, plus 10% off a first visit.",
 "faq.html": "Eleven honest answers from a Baytown master plumber: repair or replace a heater, free estimates, hydro jetting on old lines, septic permits, 24-hour calls.",
 "guides.html": "Twenty free plumbing guides from a Baytown master plumber: faucets, running toilets, heater flushes, putty, Teflon tape, bills, drains and gas safety.",
 "contact.html": "Call (713) 992-9257, text a photo, or send the request form to info@alfaplumbingservices.com. Shop at 508 Scott St, Baytown, TX 77520.",
}


def meta_title(title, brand="Alfa Plumbing", limit=60):
    """Titles get pixel-clipped near 60 characters, and the brand should appear exactly once."""
    t = re.sub(r"\s+", " ", html.unescape(title)).strip()
    branded = bool(re.search(r"\|\s*Alfa\b|\bAlfa Plumbing\b", t))
    if branded:
        if t.count("Alfa Plumbing") > 1:  # caller plus an auto-appended tail
            t = re.sub(r"\s*\|\s*Alfa Plumbing(?: Services)?\s*$", "", t).strip()
        return t if len(t) <= limit else t[:limit].rsplit(" ", 1)[0].rstrip(" ,.;:")
    with_brand = "%s | %s" % (t, brand)
    if len(with_brand) <= limit:
        return with_brand
    return t if len(t) <= limit else t[:limit].rsplit(" ", 1)[0].rstrip(" ,.;:")


def meta_desc(text, limit=158):
    """Safety net only: whole sentences inside 158 characters, never half a clause."""
    def out(x):
        return x.replace("&", "&amp;")

    t = re.sub(r"\s+", " ", html.unescape(text)).strip()
    if len(out(t)) <= limit:
        return out(t)
    acc = ""
    for sent in re.split(r"(?<=[.!?]) +", t):
        cand = (acc + " " + sent).strip()
        if len(out(cand)) <= limit:
            acc = cand
        elif not acc:
            acc = sent[: limit - 1].rsplit(" ", 1)[0]
            break
        else:
            break
    return out(acc.rstrip(" ,.;:") + ".")


def pre(fname):
    """Relative prefix from the page file back to the build root."""
    return "" if "/" not in fname else "../"


TOP_FILES = ["index.html", "services.html", "water-heaters.html", "drains-sewer.html",
             "leaks-gas-repairs.html", "repiping-remodels.html", "about.html", "team.html",
             "projects.html", "reviews.html", "service-areas.html", "pricing.html", "faq.html",
             "guides.html", "contact.html"]


def shell(fname, title, desc, crumbs, body_html, active, extra_schema=None, og=None, tail_scripts=True):
    out = head(title, desc, fname, extra_schema, og)
    out += nav_html(active)
    out += '<main id="main">\n' + body_html + "\n</main>\n"
    out += FOOTER
    if tail_scripts:
        out += '<script src="%sassets/alfa.js"></script>\n' % pre(fname)
    out += "</body>\n</html>\n"
    if "/" in fname:  # pages inside guides/ reach the rest of the build one level up
        for f in TOP_FILES:
            out = out.replace('href="%s' % f, 'href="../%s' % f)
        out = out.replace('href="../guides/', 'href="')
    write(fname, out)


def write(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)


def crumbs(items, dark=True):
    parts = ['<a href="index.html">Home</a>']
    for label, href in items:
        if href:
            parts.append('<a href="%s">%s</a>' % (href, label))
        else:
            parts.append("<b>%s</b>" % label)
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % " / ".join(parts)


def pagehead(eyebrow, h1, lede, image, alt, crumb, actions=None, side=None):
    acts = actions or """
      <a class="btn btn--call" href="{tel}">&#9742; Call {phone}</a>
      <a class="btn btn--onDark" href="contact.html#book">Request service</a>
      <a class="btn btn--onDark" href="{sms}">Text a photo</a>""".format(tel=PHONE_TEL, phone=ORG["phone_display"], sms=SMS)
    media = side or '<div class="ph">%s</div>' % (
        '<img src="%s" alt="%s" width="1000" height="700" loading="eager">' % (image, alt))
    return """
<section class="pagehead" id="overview">
  <span class="blueprint" aria-hidden="true"></span>
  <div class="wrap">
    <div>
      {crumb}
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <div class="acts">{acts}</div>
    </div>
    {media}
  </div>
</section>""".format(crumb=crumb, eyebrow=eyebrow, h1=h1, lede=lede, acts=acts, media=media)


def cta(note=None):
    return """
<section class="ctaband" id="next">
  <div class="wrap">
    <div>
      <h2>One call usually closes it.</h2>
      <p>{note}</p>
    </div>
    <div class="acts">
      <a class="btn btn--call btn--lg" href="{tel}">&#9742; {phone}</a>
      <a class="btn btn--onDark btn--lg" href="contact.html#book">Book online <span class="ar">&rarr;</span></a>
    </div>
  </div>
</section>""".format(tel=PHONE_TEL, phone=ORG["phone_display"],
                     note=note or "Tell us the symptom and the address; we tell you the likely cause, what it costs and when we can be there.")


def book_form(compact=False):
    opts = "".join('<option>%s</option>' % n for n, _a, _f in SERVICES)
    rows = """
      <div class="row">
        <div class="field"><label for="fn">First name</label><input id="fn" name="First name" type="text" autocomplete="given-name" required><span class="emsg">Please add your first name.</span></div>
        <div class="field"><label for="ln">Last name</label><input id="ln" name="Last name" type="text" autocomplete="family-name" required><span class="emsg">Please add your last name.</span></div>
      </div>
      <div class="row">
        <div class="field"><label for="ph">Phone</label><input id="ph" name="Phone" type="tel" autocomplete="tel" placeholder="(713) 555-0123" required><span class="emsg">We need a number to call you back on.</span></div>
        <div class="field"><label for="em">Email</label><input id="em" name="Email" type="email" autocomplete="email" placeholder="you@example.com" required><span class="emsg">Check the email address.</span></div>
      </div>
      <div class="row">
        <div class="field"><label for="ad">Service address</label><input id="ad" name="Address" type="text" autocomplete="street-address" placeholder="Street, Baytown TX" required><span class="emsg">Which address is the job at?</span></div>
        <div class="field"><label for="sv">What do you need?</label><select id="sv" name="Service">%s</select></div>
      </div>""" % opts
    if not compact:
        rows += """
      <div class="row">
        <div class="field"><label for="wh">When do you need it?</label><select id="wh" name="Timing">
          <option>Today &mdash; urgent</option><option>Within 48 hours</option><option>This week</option><option>Getting quotes</option>
        </select></div>
        <div class="field"><label for="dt">Preferred date</label><input id="dt" name="Date" type="date"></div>
      </div>"""
    rows += """
      <div class="field"><label for="ms">Describe the problem</label><textarea id="ms" name="Message" rows="4" placeholder="No hot water since this morning; Rheem gas 50 gal, about 12 years old."></textarea></div>"""
    return """
<div class="formcard">
  <div class="fh">
    <h3>Request service</h3>
    <p class="fnote">Goes straight to {email}. For anything active &mdash; water on the floor, gas smell, sewage &mdash; call or text instead; the phone is faster than the inbox.</p>
  </div>
  <form class="book" action="mailto:{email}" method="post" enctype="text/plain" name="Alfa plumbing request">
    {rows}
    <button class="btn btn--lg" type="submit">Send request <span class="ar">&rarr;</span></button>
    <p class="formnote">Submitting opens your email app with the request already addressed to us &mdash; press send and it is on its way. If nothing opens, call {phone} or text {phone}.</p>
  </form>
</div>""".format(email=ORG["email"], phone=ORG["phone_display"], rows=rows)


# ---------------------------------------------------------------- shared bands
def triage_band(headline=None, sub=None, id="triage", only=None):
    cards = []
    for tri_idx, row in enumerate(TRIAGE):
        if only is not None and tri_idx not in only:
            continue
        q, a, cta_label = row[0], row[1], row[2]
        urgent = row[3] if len(row) > 3 else False
        href = PHONE_TEL if cta_label.startswith("Call") else "contact.html#book"
        if "camera" in cta_label.lower() or "drain visit" in cta_label.lower():
            href = "drains-sewer.html"
        if "water heater" in cta_label.lower():
            href = "water-heaters.html"
        if "bill" in cta_label.lower():
            href = "guides/why-is-my-water-bill-so-high.html"
        if "project" in cta_label.lower():
            href = "repiping-remodels.html"
        cards.append("""
      <a class="symp{urgent}" href="{href}">
        {hot}<span class="q">{q}</span><span class="a">{a}</span><span class="go">{c} &rarr;</span>
      </a>""".format(urgent=" urgent" if urgent else "", hot='<span class="hot">Act now</span>' if urgent else "",
                     q=q, a=a, c=cta_label, href=href))
    return """
<section class="band paper" id="{sid}">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Start here</p><h2 class="h-sec">{h}</h2></div>
      <p class="lede">{s}</p>
    </div>
    <div class="triage">{cards}</div>
  </div>
</section>""".format(sid=id, h=headline or "What is going wrong?", s=sub or "Pick the symptom closest to yours. It routes you to the right page, the right crew and the right price range.",
                     cards="".join(cards))


def guide_cards(items, cols="ggrid"):
    out = []
    for g in items:
        out.append("""
    <article class="gcard rv" data-cat="{cat_key}">
      <div class="ph"><img src="{img}" alt="{alt}" width="600" height="400" loading="lazy"></div>
      <div class="b">
        <p class="m"><span class="c">{cat}</span><span>&middot;</span><time datetime="{date}">{pretty}</time><span>&middot;</span>{mins} min</p>
        <h3><a href="guides/{slug}.html">{title}</a></h3>
        <p>{lede_short}</p>
        <a class="lk" href="guides/{slug}.html">Read the guide <span aria-hidden="true">&rarr;</span></a>
      </div>
    </article>""".format(cat=g["cat"], cat_key=cat_key(g["cat"]), img=g["img"], alt=g["title"], date=g["date"],
                          pretty=pretty(g["date"]), mins=g["mins"], slug=g["slug"], title=g["title"],
                          lede_short=shorten(g["lede"])))
    return '<div class="%s">%s</div>' % (cols, "\n".join(out))


def shorten(t, n=118):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "&hellip;"


def pretty(d):
    y, m, day = d.split("-")
    return "%s %s, %s" % (["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1], day, y)


def review_band(limit=None, title="Reviews", cap=None, offset=0):
    rv = REVIEWERS[offset: offset + limit] if limit else REVIEWERS[offset:]
    glink = "https://search.google.com/local/reviews?placeid=" + PLACE
    quotes = "".join("""
      <figure class="rev rv">
        <div class="st" aria-label="Five out of five">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="txt"><b>{n}</b> &middot; {job}</p>
        <figcaption class="who"><a class="src" href="{glink}" target="_blank" rel="noopener nofollow">Read it on the Google profile &#8599;</a></figcaption>
      </figure>""".format(n=n, job=job, glink=glink) for n, job in rv)
    return """
<section class="band tint" id="reviews-strip">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{t}</p><h2 class="h-sec">{h}</h2></div>
      <div class="gbp">
        <p class="big">5.0 <span aria-hidden="true">&#9733;</span></p>
        <p class="lbl">40 Google reviews on the business profile</p>
        <p class="divv"></p>
        <a class="btn btn--ghost" href="https://search.google.com/local/writereview?placeid={place}" target="_blank" rel="noopener nofollow">Write a review &#8599;</a>
      </div>
    </div>
    <div class="rev-grid">{q}</div>
    <p class="mono-note" style="margin-top:20px">{sub}</p>
  </div>
</section>""".format(t=title, h="Baytown homeowners, in their words.",
                     place=PLACE, q=quotes,
                     sub=cap or "Names and job types are what the profile shows; the wording stays on Google, so nobody has to take our version of it.")


# ---------------------------------------------------------------- page: home
def page_home():
    svc_cards = []
    for i, c in enumerate(CLUSTERS, 1):
        svc_cards.append("""
    <article class="svc rv">
      <div class="art ph"><img src="{img}" alt="{name} work by Alfa Plumbing in Baytown" width="800" height="640" loading="lazy"><span class="num">{n:02d}</span></div>
      <div class="body">
        <p class="eyebrow">{tag}</p>
        <h3>{name}</h3>
        <p class="desc">{blurb}</p>
        <ul>{rows}</ul>
        <div class="foot">
          <a class="lnk" href="{file}">Open {name_lower} <span class="ar">&rarr;</span></a>
          <span class="est">Free walk-through estimates</span>
        </div>
      </div>
    </article>""".format(img=c["image"], name=c["name"], name_lower=c["name"].lower(), n=i,
                          tag=c["tagline"], blurb=c["blurb"], file=c["file"],
                          rows="".join('<li><a href="%s#%s">%s</a></li>' % (c["file"], sid, sname)
                                       for sid, sname, _d in c["services"])))

    why = [
        ("One owner, one standard", "{o} still takes service calls. The person who quotes your job is accountable for it.".format(o=ORG["owner"])),
        ("Guaranteed workmanship", "100% satisfaction on the labour we do, with the money-back clause the company publishes."),
        ("Licensed and insured", "Texas Master Plumber, insured, family-owned in Baytown since {since}.".format(since=ORG["founded"])),
        ("Diagnose, then fix", "Camera, pressure test or continuity check before parts are replaced. We show you what we found."),
        ("Same-day and after hours", "Water on the floor does not wait; neither do we. 24-hour dispatch for real emergencies."),
        ("Honest about the small jobs", "Faucets, flappers and hoses get booked too, and {o}.".format(o=OFFER.lower().rstrip("."))),
    ]
    why_html = "".join("""
        <div class="wrow"><h3>{h}</h3><p>{p}</p></div>""".format(h=h, p=p) for h, p in why)

    facts = [("Founded", "%s in Baytown by %s" % (ORG["founded"], ORG["owner"])),
             ("Guarantee", "100% satisfaction on workmanship, money-back per published terms"),
             ("Licence", "Licensed and insured Texas Master Plumber"),
             ("Reviews", "5.0 out of 40 on the Google Business Profile"),
             ("Offer", OFFER),
             ("Audience", "Residential, commercial, property managers, restoration and new builds")]
    facts_html = "".join('<div class="fc"><span class="k">{k}</span><span class="v">{v}</span></div>'.format(k=k, v=v) for k, v in facts)

    body = """
<section class="hero" id="hero">
  <span class="blueprint" aria-hidden="true"></span>
  <div class="wrap">
    <div class="hero-copy">
      <p class="eyebrow">Baytown, Texas &middot; licensed &amp; insured Master Plumber</p>
      <h1>Hot water, clear drains and a plumber who <em>tells you the truth</em> about both.</h1>
      <p class="lede">Water heaters, drains, sewer lines, gas lines, leak detection and repipes across Baytown and the Houston ship channel. Same-day service, free estimates on new work, and {offer}.</p>
      <div class="acts">
        <a class="btn btn--call btn--lg" href="{tel}">&#9742; Call {phone}</a>
        <a class="btn btn--lg" href="#book">Request service <span class="ar">&rarr;</span></a>
        <a class="btn btn--ghost btn--lg" href="guides.html">Fix it yourself first</a>
      </div>
    </div>
    <div class="hero-art">
      <figure class="frame ph">
        <img src="{img}" alt="Alfa Plumbing technician working under a water heater in a Baytown home" width="1200" height="900">
        <figcaption class="cap"><b>508 Scott St, Baytown</b>Owner-operated plumbing company &middot; {since}</figcaption>
        
      </figure>
      <div class="tag-owner">
        <span class="k">Owner</span>
        <img class="face" src="{servando}" alt="Portrait of {owner}" width="120" height="120" onerror="this.parentNode.classList.add('nophoto')">
        <span class="s">{owner}<br>Texas Master Plumber</span>
      </div>
    </div>
  </div>
</section>

<section class="band dark" id="facts">
  <div class="wrap">
    <div class="fc-grid">{f}</div>
  </div>
</section>

{triage}

<section class="band tint" id="services">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Services</p><h2 class="h-sec">Four ways we get called. Twenty things we actually do.</h2></div>
      <p class="lede">Every service below has its own page with the diagnostics we run, what the visit includes and what it costs. Nothing hidden behind a contact form.</p>
    </div>
    {cards}
    <p style="margin-top:26px"><a class="btn btn--ghost" href="services.html">All services in one list <span class="ar">&rarr;</span></a></p>
  </div>
</section>

<section class="band paper" id="why">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Why Alfa</p><h2 class="h-sec">Why people call us back for the next house.</h2></div>
      <p class="lede">No stock-photo awards. The reasons are specific, and the detail is on the <a href="about.html">About page</a>.</p>
    </div>
    <div class="wgrid">{w}</div>
  </div>
</section>

{founder}

<section class="band tint" id="jobs">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">From the truck</p><h2 class="h-sec">Recent Baytown jobs, photographed on site.</h2></div>
      <p class="lede">Real installs and repairs, photographed by the crew that did them. No stock imagery.</p>
    </div>
    {gal}
    <p style="margin-top:24px"><a class="btn btn--ghost" href="projects.html">See all projects <span class="ar">&rarr;</span></a></p>
  </div>
</section>

{reviews}

{areas}

<section class="band paper" id="guides">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">DIY guides</p><h2 class="h-sec">Twenty guides from a master plumber who is happy if you fix it yourself.</h2></div>
      <p class="lede">Written for Baytown water. Read one before you pay for a service call.</p>
    </div>
    {gcards}
    <p style="margin-top:24px"><a class="btn" href="guides.html">Browse all 20 guides <span class="ar">&rarr;</span></a></p>
  </div>
</section>

<section class="band tint" id="pricing">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">What it costs</p><h2 class="h-sec">Published ranges, not a mystery.</h2></div>
      <p class="lede">Estimates for replacement work are free, and we quote before we start. These are the figures we publish.</p>
    </div>
    <div class="price">{pcards}</div>
    <p style="margin-top:22px"><a class="btn btn--ghost" href="pricing.html">Pricing in full <span class="ar">&rarr;</span></a></p>
  </div>
</section>

<section class="band paper" id="faq">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">FAQ</p><h2 class="h-sec">The questions we answer every week.</h2></div>
      <p class="lede">Eleven more on the <a href="faq.html">full FAQ page</a>, with the schema Google needs to show them.</p>
    </div>
    <div class="faq">{faqs}</div>
  </div>
</section>

<section class="band dark" id="book">
  <div class="wrap">
    <div class="book">
      <div class="dialer">
        <p class="eyebrow">Book an appointment</p>
        <h2 class="h-sec">Tell us the symptom. We will tell you the cause.</h2>
        <p class="lede">Fill this in and it arrives in the shop inbox at {email}. Or skip it and call &mdash; the phone gets answered by a plumber, not a call centre.</p>
        <div class="dcard">
          <span class="k">Call or text</span>
          <span class="v"><a href="{tel}">{phone}</a></span>
          <span class="s">24-hour dispatch for emergencies</span>
        </div>
        <div class="dcard">
          <span class="k">Shop</span>
          <span class="v"><a href="{maps}" target="_blank" rel="noopener">{street}, {city}</a></span>
          <span class="s">{state} {zip}</span>
        </div>
      </div>
      {form}
    </div>
  </div>
</section>
""".format(since=ORG["founded"], phone=ORG["phone_display"], offer=OFFER, tel=PHONE_TEL,
           img=IMG["servicing"], servando=ORG["servando"], owner=ORG["owner"],
           f=facts_html, triage=triage_band(), cards="\n".join(svc_cards), w=why_html,
           founder=founder_block(), gal=gal_block(3), reviews=review_band(limit=3),
           areas=areas_block(teaser=True), gcards=guide_cards(sorted(GUIDES, key=lambda g: g["date"], reverse=True)[:6]),
           email=ORG["email"], street=ORG["street"], city=ORG["city"], state=ORG["state"], zip=ORG["zip"],
           maps=ORG["gmaps"], form=book_form(compact=True),
           pcards="".join('<div class="pcard{hot}"><span class="k">{k}</span><span class="v">{v}</span><span class="s">{s}</span></div>'
                          .format(hot=" hot" if i < 2 else "", k=k, v=v, s=s) for i, (k, v, s) in enumerate(PRICING[:4])),
           faqs=faq_items(FAQS[:4]))
    extra = [plumber_schema()]
    shell("index.html",
          "Baytown Plumber, TX | Alfa Plumbing Services — Family-Owned Since %s" % ORG["founded"],
          "Family-owned Baytown plumbers since %s. Water heaters, drains, sewer, gas lines, leak detection and repiping. Licensed &amp; insured. Call %s." % (ORG["founded"], ORG["phone_display"]),
          None, body, "index.html", extra, og=IMG["servicing"])


def plumber_schema():
    return {
        "@type": "Plumber", "@id": SITE + "/#business",
        "name": ORG["name"], "alternateName": "Alfa Plumbing Services LLC",
        "description": "Family-owned plumbing company in Baytown, Texas, established in %s by %s." % (ORG["founded"], ORG["owner"]),
        "foundingDate": ORG["founded"], "founder": {"@type": "Person", "name": ORG["owner"]},
        "url": SITE + "/", "logo": ORG["logo"], "image": ORG["servando"],
        "telephone": ORG["phone_display"], "email": ORG["email"],
        "address": {"@type": "PostalAddress", "streetAddress": ORG["street"], "addressLocality": ORG["city"],
                    "addressRegion": ORG["state"], "postalCode": ORG["zip"], "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 29.7355, "longitude": -94.9774},
        "areaServed": [{"@type": "City", "name": n} for n, _c, _d in AREAS],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n, _a, _f in SERVICES],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "40",
                            "bestRating": "5", "worstRating": "1"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Plumbing services",
                            "itemListElement": [{"@type": "Offer", "description": OFFER,
                                                 "itemOffered": {"@type": "Service", "name": "New-customer discount"}}]},
        "sameAs": ["https://www.google.com/maps/place/?q=place_id:" + PLACE, ORG["yelp"]],
        "slogan": "Real plumbers, real jobsite photos, 100% workmanship guarantee.",
    }


def founder_block():
    return """
<section class="band paper" id="founder">
  <div class="wrap">
    <div class="founder">
      <div class="pic ph"><img src="{s}" alt="{owner}, founder of Alfa Plumbing Services" width="480" height="480" loading="lazy"></div>
      <div>
        <p class="eyebrow">The founding promise</p>
        <h2 class="h-sub">Show up when you say you will. Explain what broke. Price it before it starts.</h2>
        <blockquote>The rule the company was founded on in {since}, still printed on the estimate &mdash; and the reason the workmanship guarantee is offered by the licence holder rather than a subcontractor.
        <cite>Alfa Plumbing Services &middot; founded {since} by {owner}, Texas Master Plumber</cite></blockquote>
        <div class="facts" style="display:block">
          <p>Started in {since} with one truck and a rule that still runs the shop: show up when you say you will, fix what is actually broken, and leave the house cleaner than you found it.</p>
          <p><a class="lnk" href="about.html">Read the company story <span class="ar">&rarr;</span></a> &middot; <a class="lnk" href="team.html">Meet the crew <span class="ar">&rarr;</span></a></p>
        </div>
      </div>
    </div>
  </div>
</section>""".format(s=ORG["servando"], owner=ORG["owner"], since=ORG["founded"])


def gal_block(n):
    cards = []
    for name, src, meta, desc in PROJECTS[:n]:
        cards.append("""
      <a class="card-job rv" href="projects.html">
        <span class="ph"><img src="{src}" alt="{name} by Alfa Plumbing" width="700" height="480" loading="lazy"></span>
        <span class="m">
          <span class="t">{name}</span>
          <span class="d">{d}</span>
          <span class="meta">{meta}</span>
        </span>
      </a>""".format(src=src, name=name, meta=meta, d=shorten(desc, 96)))
    return '<div class="gal">%s</div>' % "\n".join(cards)


def areas_block(teaser=False):
    items = AREAS[:8] if teaser else AREAS
    cells = "".join('<a class="city{core}" href="contact.html#book"><span class="pin" aria-hidden="true"></span>{n}{z}</a>'
                    .format(core=" core" if core else "", n=n, z="" if teaser else '<span class="z">%s</span>' % d)
                    for n, core, d in items)
    return """
<section class="band {cls}" id="areas">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Service areas</p><h2 class="h-sec">{h}</h2></div>
      <p class="lede">Twelve cities around the shop, and the east Houston neighbourhoods inside an hour of it. Outside this list, call anyway &mdash; if we cannot get there we will tell you who can.</p>
    </div>
    <div class="citylist">{cells}</div>
    <p style="margin-top:22px"><a class="btn btn--ghost" href="service-areas.html">Where we work, town by town <span class="ar">&rarr;</span></a></p>
  </div>
</section>""".format(cls="tint" if teaser else "paper",
                     h="Baytown and the ship channel corridor." if teaser else "Where we work.", cells=cells)


def faq_items(items):
    out = []
    for i, (q, a, _k) in enumerate(items):
        out.append("""
    <details%s>
      <summary><span>%s</span></summary>
      <div class="a">%s</div>
    </details>""" % (" open" if i == 0 else "", q, a))
    return "".join(out)


# ---------------------------------------------------------------- pages: clusters
def cluster_page(c, extra_bands="", faq_ids=()):
    rows = []
    for i, (sid, sname, sshort) in enumerate(c["services"], 1):
        detail = SERVICE_DETAIL.get(sid, {})
        rel = detail.get("guides", [])
        rel_html = "".join('<a href="guides/%s.html"><span class="k">Guide</span><span class="t">%s</span></a>'
                           % (s, BY_GUIDE[s]["title"]) for s in rel if s in BY_GUIDE)
        rows.append("""
    <div class="svcrow" id="{sid}">
      <span class="idx">{i:02d}</span>
      <div>
        <h3>{name}</h3>
        <p>{what}</p>
        <div class="tags">{tags}</div>
        <div class="go">
          <a class="btn btn--ghost" href="contact.html#book">Book {name}</a>
          <a class="btn btn--call" href="{tel}">&#9742; Call now</a>
        </div>
      </div>
      <div class="side">
        <span class="lbl">What the visit includes</span>
        <ul>{inc}</ul>
        {price}
      </div>
      {rel}
    </div>""".format(sid=sid, i=i, name=sname, what=detail.get("what", sshort),
                    tags="".join("<span>%s</span>" % t for t in detail.get("tags", [])),
                    inc="".join("<li>%s</li>" % x for x in detail.get("include", ["Standard visit: diagnostics, the fix, and what we checked while we were in there."])),
                    price=('<span class="lbl" style="margin-top:12px">Published price facts</span><ul>%s</ul>'
                           % "".join("<li>%s</li>" % p for p in detail.get("price", []))) if detail.get("price") else "",
                    tel=PHONE_TEL,
                    rel=('<div style="grid-column:1/-1"><span class="lbl" style="font:600 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--copper);display:block;margin-bottom:8px">Read before you call</span><div class="relstrip">%s</div></div>' % rel_html) if rel_html else ""))

    faqs = [f for f in FAQS if f[2] in faq_ids]
    faq_band = ""
    if faqs:
        faq_band = """
<section class="band tint" id="faq">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Asked before you call</p><h2 class="h-sec">{h}</h2></div>
      <p class="lede">The full list, with FAQ schema, is on the <a href="faq.html">FAQ page</a>.</p></div>
    <div class="faq">{items}</div>
  </div>
</section>""".format(h="Straight answers about %s." % c["name"].lower(), items=faq_items(faqs))

    body = pagehead(c["name"], c["h1"], c["lead"], c["image"], c["img_alt"],
                    crumbs([(c["name"], None)], True),
                    side=c.get("side")) + (triage_band("Which of these is it?", c["triage_sub"], id="triage", only=c["triage_idx"]) if c.get("triage_idx") else "") + """
<section class="band paper" id="work">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">{name}</p><h2 class="h-sec">{h2}</h2></div>
      <a class="btn btn--ghost" href="contact.html#book" aria-label="Request a {name} visit from Alfa Plumbing">Book a visit <span class="ar">&rarr;</span></a>
    </div>
    {rows}
  </div>
</section>
{extra}
{faq}
{cta}""".format(name=c["name"], h2=c["h2"], rows="\n".join(rows),
               extra=extra_bands, faq=faq_band, cta=cta(c["cta_note"]))
    shell(c["file"], c["title"], c["desc"], None, body, c["file"],
          [{"@type": "Service", "name": c["name"], "provider": {"@id": SITE + "/#business"},
            "areaServed": ORG["city"], "description": c["desc"],
            "serviceType": [s for _a, s, _f in c["services"]]}], og=c["image"])


CLUSTER_COPY = {
 "water-heaters": dict(
   triage_idx=[1, 0],
   h1="Hot water, fixed the first time.",
   h2="What we do on a water heater call.",
   lead="No hot water is the most common call in Baytown, and it is the one where an honest diagnosis saves the most money. We check the cheap things first, then tell you whether the tank is worth keeping.",
   triage_sub="Element, thermostat, pilot, dip tube or sediment — four of those five are a repair, not a replacement.",
   title="Water Heater Repair, Installation & Maintenance in Baytown, TX | Alfa Plumbing",
   desc="Baytown water heater repair, tank and tankless installation, annual flush and tune-up. Same-day diagnostics, published price ranges, 100% workmanship guarantee. Call (713) 992-9257.",
   img_alt="Baytown plumber replacing a water heater for Alfa Plumbing Services",
   cta_note="Gas or electric, tank or tankless — describe the symptom and we will bring the parts for the two most likely causes.",
   faq_ids=("When should I repair a water heater instead of replacing it?",
            "Why am I running out of hot water quickly?"),
 ),
 "drains-sewer": dict(
   triage_idx=[2, 0],
   h1="We camera it before we dig it.",
   h2="What a drain, sewer or septic visit looks like.",
   lead="Slow drains are usually simple. Repeated clogs, sewage smells or several fixtures acting up together are the main line's problem, and guessing at that costs money in concrete. So we look first.",
   triage_sub="Sink, tub, laundry, main line, sewer lateral or septic field — all of them are ours to deal with.",
   title="Drain Cleaning, Sewer Line Repair & Septic Service in Baytown, TX | Alfa Plumbing",
   desc="Baytown drain cleaning, sewer camera inspection, trenchless sewer repair and septic pumping, replacement and county permits. Licensed and insured. Call (713) 992-9257.",
   img_alt="Alfa Plumbing clearing a Baytown home's main drain line",
   cta_note="Tell us which fixtures are slow and what you can smell; we bring the cable, the jet or the camera accordingly.",
   faq_ids=("Is hydro jetting safe for older sewer lines?",
            "Is it safe to keep using a clogged toilet?"),
 ),
 "leaks-gas": dict(
   triage_idx=[3, 0, 4],
   h1="Find it, then fix it — including the gas.",
   h2="How leak and repair calls are run.",
   lead="Gas and buried water are the two places where guessing is expensive or dangerous. Both get located properly before any wall, slab or yard gets opened.",
   triage_sub="Gas smell, spiked water bill, wet lawn, dripping faucet or a toilet that will not stop running.",
   title="Gas Line Repair, Water Leak Detection & Fixture Repair in Baytown, TX | Alfa Plumbing",
   desc="Baytown gas line repair and appliance tie-ins, underground water leak detection, water line repair, faucet, toilet and disposal repairs, plus 24-hour emergency plumbing. Call (713) 992-9257.",
   img_alt="Alfa Plumbing technician repairing a water line in a Baytown yard",
   cta_note="If you smell gas: leave, ventilate, and phone from outside. Everything else can wait for a text message.",
   faq_ids=("Do you offer 24-hour emergency plumbing in Baytown?",
            "Will a Baytown plumber do small repairs?"),
 ),
 "repiping-remodels": dict(
   triage_idx=[5, 4],
   h1="New pipe where the old pipe gave up.",
   h2="What a repipe, remodel or new-build job involves.",
   lead="Big jobs get a walk-through, a drawing and a number that holds. Whether it is a whole-house change-out, moving a wall of plumbing for a bath remodel or a rough-in on a slab, you know the scope before the first cut.",
   triage_sub="Rusty water, pressure loss, multiple pinhole leaks, or plans for a bathroom, kitchen or new build.",
   title="House Repiping, Remodel & New Construction Plumbing in Baytown, TX | Alfa Plumbing",
   desc="Baytown whole-house repipe in copper, PEX or CPVC, bathroom and kitchen remodel rough-ins, new construction plumbing and light commercial service. Free walk-through estimates. Call (713) 992-9257.",
   img_alt="Whole-house repipe in progress by Alfa Plumbing in Baytown",
   cta_note="Send the plans or the room dimensions and we will quote the rough-in and the fixtures separately, so you can choose.",
   faq_ids=("Do Alfa Plumbing Services in Baytown provide free estimates for new work?",
            "Do you handle plumbing for property managers and restoration work?"),
 ),
}

SERVICE_DETAIL = {
 "water-heater-repair": dict(
   guides=["7-reasons-hot-water-goes-cold-quickly", "why-do-i-run-out-of-hot-water-so-fast"],
   what="We come for the no-hot-water call with the parts for the two most likely causes, so one visit is normally the whole job. Element, thermostat, thermocouple, pilot, dip tube, T&P valve and the leaking seam you were afraid of.",
   tags=["Electric & gas", "Same-day", "Tank & tankless"],
   include=["Power, breaker, element and thermostat checks on electric tanks",
            "Pilot, thermocouple and gas-valve checks on gas tanks",
            "T&amp;P valve, pan and drain-line inspection while we are in there",
            "Sediment assessment — flush recommendation if it is early, replacement if it is late",
            "Written note of what failed, so a future plumber is not guessing"],
   price=["A thermocouple or pilot part runs about $20 in parts",
          "Tanks are rated for 10–15 years; age drives the repair-vs-replace call",
          "Set point we work to: 120°F"]),
 "water-heater-installation": dict(
   guides=["baytown-tankless-water-heater", "how-to-fix-a-leaky-faucet"],
   what="Like-for-like swaps and deliberate upgrades: capacity, efficiency, venting and gas supply. We size the tank to the household, not to what is cheapest to stock, and haul the old unit away in the same visit.",
   tags=["Permits where required", "Haul-away included", "Code-correct venting"],
   include=["Capacity and fuel-size conversation before we quote",
            "New pan, drain line, flex connections and expansion tank where the system needs one",
            "Combustion-air and venting checked to current code",
            "Startup, temperature set to 120°F, and a walkthrough of the warranty",
            "Old unit removed from the house, not left in the yard"],
   price=["Average Baytown plumbing visit: $526, with the typical range $201–$850",
          "Gas tankless installs run to about $3,000, unit included",
          "Free walk-through estimate on replacements"]),
 "water-heater-maintenance": dict(
   guides=["water-heater-knocking-easy-5-min-fix", "the-complete-plumbing-guide"],
   what="An annual flush and a safety check. In Baytown water, the sediment is the whole story: it is why tanks knock, why recovery slows, and why they leak at year nine instead of year fifteen.",
   tags=["Annual", "Under 60 minutes", "Plan-friendly"],
   include=["Full drain and flush until the water runs clear, including the stir-and-refill cycle",
            "Anode rod inspection and replacement quote if it is spent",
            "Element, thermostat, T&P valve, gas pressure and burner condition",
            "Leak check on the tank, connections and drain valve",
            "Written report of what you have and roughly how long is left on it"]),
 "tankless-water-heaters": dict(
   guides=["baytown-tankless-water-heater", "7-reasons-hot-water-goes-cold-quickly"],
   what="On-demand installs for Baytown homes that are tired of running out, or that want the closet back. Gas conversions get a proper vent and gas line; point-of-use electric units get the circuit they need.",
   tags=["Energy Star models", "Retrofit or new build", "Descale service"],
   include=["Demand calculation so the unit is not under-sized for two bathrooms at once",
            "Vent material, intake and exhaust routing sized to the model",
            "Gas line, meter and pressure checks where a conversion needs more fuel",
            "Soft-side filtration advice and a descale schedule",
            "Recirculation option so nobody runs the tap for a minute"],
   price=["Baytown average: $1,000 for electric point-of-use, up to $3,000 for a gas whole-house install",
          "Installs since 2003 behind the sizing conversation"]),
 "drain-cleaning": dict(
   guides=["how-to-keep-drains-clear-naturally", "kitchen-sink-leaking-from-drain-5-min-fix"],
   what="Sink, tub, shower, laundry and main line. Plunger and hand auger where they will do, sectional cabling or a hydro jet where they will not, and a camera when the clog keeps coming back.",
   tags=["Kitchen & bath", "Main line", "Hydro jetting"],
   include=["Which fixtures are affected, so we know whether it is a branch or the main",
            "Cable or jet sized to the pipe, not a one-nozzle-fits-all blast",
            "Camera look at the walls of the pipe after cleaning, with the video for you",
            "Grease, root and offset findings written up with what to do about them",
            "Advice on what changed — usually hair, grease or wipes"]),
 "sewer-line-services": dict(
   guides=["how-to-keep-drains-clear-naturally", "septic-tank-services"],
   what="The lateral from the house to the main. Camera first, then the shortest honest repair: a spot fix, a cured-in-place liner, or a replacement when the pipe has given up.",
   tags=["Camera inspection", "Trenchless lining", "Spot repair"],
   include=["Cleanout entry and camera run with the video and measurements",
            "Root, grease, offset and belly findings separated out",
            "Repair option priced per foot versus replacement, so you can see the trade-off",
            "Trenchless lining where the pipe can take it; two pits instead of a trench",
            "Restoration scope written clearly if your yard gets opened"]),
 "septic-tank-services": dict(
   guides=["septic-tank-services", "how-you-can-stop-a-leaky-faucet-yourself"],
   what="For Baytown-area homes off city sewer: pump-outs, inspections, odour and backup diagnostics, replacement design, and the county permit and as-built filed properly.",
   tags=["Pump & inspect", "Replacement design", "Permits handled"],
   include=["Tank pumped, baffles and Tee inspected, sludge and scum depths measured",
            "Field performance signs checked — damp ground, surfacing effluent, slow drains",
            "Written interval for your household size and tank volume (five years is the rule of thumb)",
            "Design and permit package for a new or replacement system",
            "As-built filed so the next owner knows where the tank is"]),
 "garbage-disposal-repair": dict(
   guides=["plumbing-101-diy-10-quick-fixes", "how-to-keep-drains-clear-naturally"],
   what="The hum that means jammed, the dead unit that means reset or motor, and the leak that means the flange. We fix or replace, and we check the air gap and the switch nobody can find.",
   tags=["Reset & jam", "Replacement", "Dishwasher tie-in"],
   include=["Power, air-gap and wall-switch verification before the unit gets blamed",
            "Jam cleared from below, or the unit replaced with the correct horsepower",
            "Flange, sink strainer and drain fittings replaced while it is apart",
            "Dishwasher drain line and high-loop checked so it does not back up",
            "Cold-water habit advice so the new one outlives the last one"]),
 "gas-line-repair": dict(
   guides=["gas-line-repair-baytown", "how-to-apply-teflon-tape"],
   what="Leak response, and new or relocated lines for dryers, ranges, generators, pool heaters, grills and outdoor kitchens. Pressure-tested, sediment-trap fitted, and the utility on the phone when a service has to be isolated.",
   tags=["24-hour response", "Pressure tested", "Appliance tie-ins"],
   include=["Manometer and leak-detection solution on every joint from the meter in",
            "Repair or replace section, with the shut-off and drip leg done properly",
            "Sizing check so the new appliance is not starving for gas",
            "Pressure test held while the utility reconnects, on conversions",
            "Any black-dust or soot findings explained before the wall goes back"]),
 "water-line-repair": dict(
   guides=["water-line-repair-underground-leak-detection", "brown-water-from-your-faucet"],
   what="The service line from the meter to the house, and the supply lines that feed the house. Underground breaks located electronically so the excavation stays the size of the repair.",
   tags=["Underground", "Slab", "Reroute option"],
   include=["Section isolation to prove which line is losing water",
            "Acoustic and electronic tracing to within a foot or two",
            "Repair, replace or reroute options with prices for each",
            "New meter-box stop and house shut-off while the ground is open",
            "Backfill and grading done so the yard is not a second project"]),
 "water-leak-detection": dict(
   guides=["why-is-my-water-bill-so-high", "water-line-repair-underground-leak-detection"],
   what="Water where it should not be, with nothing visible. Non-invasive detection under slab, behind walls and in the attic, so the demolition is a hole, not a wall.",
   tags=["Non-invasive", "Slab", "Insurance-ready report"],
   include=["Meter test and fixture isolation to confirm the house is actually losing water",
            "Acoustic correlation and thermal survey to place the leak",
            "Sewer-camera check when a wet patch could be waste rather than supply",
            "Marked, photographed scope for your insurance claim",
            "Plumbing repair quoted with the access work, not after it"]),
 "faucet-repair": dict(
   guides=["how-to-fix-a-leaky-faucet", "how-you-can-stop-a-leaky-faucet-yourself"],
   what="Drips from the spout, leaks at the base, cartridges that seize, faucets thirty years old with no parts. Repairs first; replacement quoted only when the rebuild is not economic.",
   tags=["Kitchen & bath", "Cartridge or rebuild kit", "Base leaks"],
   include=["Hot and cold isolated, drain protected, aerator and cartridge out",
            "Seats, springs, O-rings and cam assembly replaced as needed",
            "Valve body checked for scoring that would make a rebuild pointless",
            "Supply lines and shut-offs serviced while the cabinet is empty",
            "Full-pressure test before we pack up"]),
 "toilet-repair": dict(
   guides=["how-to-fix-your-toilet-from-running", "why-is-my-water-bill-so-high"],
   what="Running, weak, rocking, leaking at the base or weeping at the shut-off. Often a flapper and a wax ring; occasionally the flange, which is why we look.",
   tags=["Running & weak flush", "Wax ring", "New unit install"],
   include=["Flapper, chain, fill height and float adjustment — the free half of the fix",
            "Food-colouring test to prove the leak before parts get sold",
            "Rocking toilet re-set on a new wax or rubber ring, flange checked",
            "Supply line and angle stop replaced if it is chrome and forty years old",
            "Replacement installation with the shut-off and hose done right"]),
 "emergency-plumber": dict(
   guides=["gas-line-repair-baytown", "brown-water-from-your-faucet"],
   what="Water on the floor, sewage coming up, gas smell, or a burst line at midnight. We talk you through shutting the right valve while the truck is loaded.",
   tags=["24 hours", "Walk-you-through", "Damage control"],
   include=["Phone instruction: main shut-off, water-heater off, breaker, gas — as applicable",
            "Priority dispatch for active water, gas and sewage",
            "Containment and isolation on arrival, before any repair conversation",
            "Permanent repair priced after the risk is handled, never during",
            "Photos and a written scope for the restoration or insurance side"]),
 "house-repiping": dict(
   guides=["should-i-repipe-my-house", "plumbing-101-diy-10-quick-fixes"],
   what="Whole-house supply change-out for galvanized, polybutylene or pinholed copper, and the drain side where it has reached the end. Phased so you have water overnight.",
   tags=["Copper / PEX / CPVC", "2 days typical", "Patching options"],
   include=["Material recommendation for your house and your water, with the trade-offs said out loud",
            "Fixture-by-fixture plan: where the new lines run and what gets opened",
            "New shut-offs, braided hoses and a labelled valve map",
            "Water phased off in stages, not shut down for days",
            "Patching scope written, or your drywall crew briefed before we start"]),
 "bathroom-remodels": dict(
   guides=["how-to-use-plumbers-putty", "how-to-apply-teflon-tape"],
   what="Rough-in and finish plumbing for bath remodels: moving a toilet, relocating a shower drain, re-venting, wall-hung carriers and the fixtures at the end.",
   tags=["Rough-in & finish", "Coordinate with your crew", "Permits"],
   include=["Layout conversation with the tile and cabinet trades so the drain ends up centred",
            "New drain, waste and vent sized and pitched, tested before the wall closes",
            "Carrier or flange relocation, shower pan and flood test",
            "Fixture setting, caulking and shut-offs at the end of the job",
            "Inspection scheduling where the work requires it"]),
 "kitchen-remodels": dict(
   guides=["kitchen-sink-leaking-from-drain-5-min-fix", "how-to-use-plumbers-putty"],
   what="Sink, disposal, dishwasher, ice-maker, pot filler and gas range lines — relocated or added, and pressure-tested before the counters land.",
   tags=["Gas & water", "Under-sink plumbing wall", "Hookups"],
   include=["Sink base cabinet planned so the disposal and the trash pull-out fit",
            "Dedicated hot/cold for the ice maker, with a proper valve",
            "Gas line and sediment trap run for the range, tested",
            "New shut-offs, braided hoses and a drain that clears the bin",
            "Rough-in sign-off photo for the cabinet installer"]),
 "new-construction": dict(
   guides=["the-complete-plumbing-guide", "professional-plumbing-services-10-tips-hiring-local"],
   what="Supply, waste and vent for new builds and additions, from underground under-slab to the final fixtures, inspected at the stages the county asks for.",
   tags=["Under-slab", "Rough-in", "Final tie-off"],
   include=["Underground water and sewer laid and tested before the pour",
            "Rough-in to the plans, with the fixture count checked against the water meter",
            "Water heater, softener and filtration locations resolved early",
            "Final set of fixtures, faucets and appliances, pressure-tested",
            "Inspection coordination at each required stage"]),
 "well-water-filtration": dict(
   guides=["brown-water-from-your-faucet", "water-heater-knocking-easy-5-min-fix"],
   what="Iron staining, sulphur smell, low pressure and a pump that short-cycles. Pressure tanks, softeners, filters and UV — sized to a water test rather than to a brochure.",
   tags=["Test first", "Pressure tank", "Softener & filter"],
   include=["Water test interpretation: iron, manganese, sulphur, pH and hardness",
            "Pressure-switch and tank pre-charge check before anyone sells a new pump",
            "Filtration, softener or UV staged in the order that actually helps",
            "Bypass, service valves and a regeneration drain, installed so it is serviceable later",
            "A maintenance interval written on the equipment, not left to memory"]),
 "commercial-plumbing": dict(
   guides=["professional-plumbing-services-10-tips-hiring-local", "how-to-keep-drains-clear-naturally"],
   what="Light commercial around Baytown: restrooms, kitchen sinks and grease, water heaters and shut-off infrastructure, on an agreement or on a call. After-hours dispatch for tenants.",
   tags=["Service agreements", "After hours", "Restrooms & kitchens"],
   include=["Scheduled flushes, jetting and inspection so the failure finds a weekend we are staffed for",
            "Restroom fixture, valve and supply replacement with minimal downtime",
            "Kitchen hot-water and grease-line servicing",
            "Water on the floor response for property managers, after hours",
            "Photographed scope for restoration and insurance claims"]),
}


# ---------------------------------------------------------------- standalone pages
def page_about():
    body = pagehead(
        "Family-owned in Baytown since %s" % ORG["founded"],
        "A plumbing company built on explaining things.",
        "Alfa Plumbing Services was started in %s by %s and still runs the way it did in the first year: one standard, honest diagnosis, and a truck that shows up when it says it will." % (ORG["founded"], ORG["owner"]),
        IMG["truck"], "Alfa Plumbing Services truck and crew at a Baytown jobsite",
        crumbs([("About", None)])) + """
<section class="band paper" id="story">
  <div class="wrap">
    <div class="artwrap">
      <div class="article">
        <h2>What the company was for</h2>
        <p>{owner} started the company in {since} in Baytown with a simple complaint about the trade: plumbers who quoted a new water heater because they had not looked at the $20 part that had failed. The business was built to be the opposite of that — a licensed shop that explains the diagnosis first, prices the work before it starts, and guarantees the labour it does.</p>
        <p>Twenty-plus years later the pattern is the same. Service calls, replacements, repipes, sewer linings, septic permits, remodel rough-ins and after-hours emergencies, mostly for people in {city}, Deer Park, La Porte, Pasadena and the ship-channel neighbourhoods who found us through a neighbour.</p>
        <h2>What “licensed and insured” means here</h2>
        <p>Alfa is a Texas Master Plumber operation, licensed and insured, family-owned. That matters in three specific places: work that needs a county permit (septic replacement, sewer, gas conversions) gets the permit pulled and the as-built filed; insurance-backed crews are in your house; and the 100% satisfaction guarantee comes from the licensed company that did the work, not a subcontractor.</p>
        <aside class="tip"><span class="tag-mono">One number, one team</span><p>{phone} is the shop line and {email} is the inbox. There is no dispatch service in the middle, which is also why the same person who quoted your job can tell you what happened to it.</p></aside>
        <h2>The guarantee, in plain words</h2>
        <p>Alfa offers a 100% satisfaction guarantee with a money-back clause on the work it performs. In practice it means: if the part we replaced is not the reason it is still doing the thing, you do not pay for the wrong guess. New-customer terms currently include {offer} on a first visit over $300.</p>
        <h2>Who we work for</h2>
        <ul class="ticks">
          <li><b>Homeowners</b> — repair, replacement and maintenance on occupied houses.</li>
          <li><b>Buyers, sellers and agents</b> — inspections and repairs between contract and closing, on the clock the transaction sets.</li>
          <li><b>Property managers</b> — tenant calls, after-hours dispatch and documented scopes.</li>
          <li><b>Restoration companies</b> — water-damage scoping, photographs and pricing for the claim.</li>
          <li><b>Builders and remodelers</b> — rough-in and finish plumbing with inspections coordinated.</li>
          <li><b>Commercial accounts</b> — light commercial and small business, 24-hour dispatch.</li>
        </ul>
        <h2>Why the estimate comes before the price</h2>
        <p>Anything that opens a wall, replaces a tank or runs new pipe gets looked at first, because that is the only way the number on the invoice matches the number on the estimate. That is also why the walk-through estimate is free on that work, and why the small stuff — drips, flappers, hoses, jams — gets booked without a sales conversation at all.</p>
      </div>
      <aside class="artside">
        <div class="dcard"><span class="k">Founded</span><span class="v">{since}</span><span class="s">Baytown, Texas</span></div>
        <div class="dcard"><span class="k">Owner</span><span class="v">{owner}</span><span class="s">Texas Master Plumber</span></div>
        <div class="dcard"><span class="k">Guarantee</span><span class="v">100% workmanship</span><span class="s">Money-back clause on published terms</span></div>
        <div class="dcard"><span class="k">Reviews</span><span class="v">5.0 / 40</span><span class="s">Google Business Profile</span></div>
        {cta_card}
      </aside>
    </div>
  </div>
</section>

<section class="band tint" id="timeline">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">How a job runs</p><h2 class="h-sec">Five steps, every time.</h2></div>
    <p class="lede">Same sequence for a $60 flapper and a $12,000 repipe. It is the reason the estimate holds.</p></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="band paper" id="principles">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Principles</p><h2 class="h-sec">Four rules that make the phone call shorter.</h2></div>
    <p class="lede">They also make some jobs smaller than the competition would like. We prefer it that way.</p></div>
    <div class="wgrid">{rules}</div>
  </div>
</section>
{reviews}
{projects}
{cta}""".format(
        owner=ORG["owner"], city=ORG["city"], since=ORG["founded"], phone=ORG["phone_display"],
        email=ORG["email"], offer=OFFER,
        cta_card='<div class="dcard"><span class="k">Talk to us</span><span class="v"><a href="%s">%s</a></span><span class="s"><a href="contact.html">Book online &rarr;</a></span></div>' % (PHONE_TEL, ORG["phone_display"]),
        steps="".join("<li><b>%s</b> %s</li>" % (h, p) for h, p in [
            ("Tell us the symptom.", "Phone, text or the request form. Photographs and a short description cut the diagnosis in half, so send them."),
            ("Diagnosis and a price.", "We test the cheap causes first and show you what we found. New work gets a walk-through estimate, free."),
            ("Approval before tools come out.", "Nothing gets opened, cut or replaced that you have not agreed to and priced."),
            ("The fix, and what else we saw.", "Work done while you are still in the house, plus the honest note about the thing that is not broken yet."),
            ("Guaranteed, and written down.", "100% workmanship guarantee, warranty paperwork left with you, and a record of the parts and settings we used.")]),
        rules="".join("<div class=\"wrow\"><h3>%s</h3><p>%s</p></div>" % (h, p) for h, p in [
            ("Explain before you sell.", "If a $20 part fixes it, that is the repair. The company publishes DIY guides that save customers money on service calls — that is the whole culture of the shop."),
            ("Location before demolition.", "Camera, pressure test or acoustic trace first. Walls and yards get opened once, at the right place."),
            ("One price, agreed in advance.", "Free walk-through estimates on repipes, remodels, sewer repair and water heater replacements, and the invoice matches them."),
            ("Leave it cleaner than we found it.", "Drop cloths, boot covers, haul-away of the old unit and the packaging, and a look at the ceiling below the work before we leave.")]),
        reviews=review_band(limit=3, offset=3),
        projects="""
<section class="band tint" id="jobs">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Proof</p><h2 class="h-sec">The work, as published.</h2></div>
    <p class="lede">Photographs from our own jobs — the full gallery is on the projects page.</p></div>
    {gal}
    <p style="margin-top:22px"><a class="btn btn--ghost" href="projects.html">Open the projects gallery <span class="ar">&rarr;</span></a></p>
  </div>
</section>""".format(gal=gal_block(3)),
        cta=cta("Questions about the licence, the insurance or the guarantee are answered on the phone in about two minutes — and they should be asked."))
    shell("about.html", "About Alfa Plumbing Services — Family-Owned Baytown Plumber Since %s" % ORG["founded"],
          "Family-owned in Baytown since %s by %s. Licensed and insured Texas Master Plumber with a 100%% workmanship guarantee, and free walk-through estimates on new work. Call %s." % (ORG["founded"], ORG["owner"], ORG["phone_display"]),
          None, body, "about.html", og=IMG["truck"])


def page_team():
    members = "".join("""
    <article class="member rv">
      <div class="ph"><img src="{img}" alt="{name} — {role}" width="600" height="700" loading="lazy"></div>
      <div class="m"><h3 class="nm">{name}</h3><p class="rl">{role}</p><p class="bio">{bio}</p></div>
    </article>""".format(img=img, name=n, role=r, bio=b) for n, r, b, img in TEAM)
    body = pagehead("Who shows up", "Servando, the crew, and the person who answers the phone.",
                    "A small company on purpose: the licence holder runs the shop, the crew that diagnoses your job is the crew that does it, and the owner still takes service calls.",
                    IMG["team"], "Alfa Plumbing Services team at a Baytown jobsite",
                    crumbs([("Team", None)])) + """
<section class="band paper" id="crew">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">The people</p><h2 class="h-sec">Three jobs, one truck roster.</h2></div>
    <p class="lede">Names and roles as the company publishes them. Portraits are the shop's own photographs.</p></div>
    <div class="team">{members}</div>
  </div>
</section>

<section class="band tint" id="how">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">How we behave on site</p><h2 class="h-sec">The five things the crew is briefed on.</h2></div>
    <p class="lede">Written into the crew brief, not left to chance — and the reason the same technician who diagnoses does the work.</p></div>
    <ol class="steps">{beh}</ol>
    <div class="callout">
      <div><h3>Ask for the diagnosis in writing</h3><p>On any Alfa visit you get what failed, what was replaced and what it costs, before the truck leaves. If you cannot get that from a quote, that is the answer.</p></div>
      <div class="acts"><a class="btn btn--onDark" href="{tel}">&#9742; {phone}</a><a class="btn btn--onDark" href="contact.html#book">Request service</a></div>
    </div>
  </div>
</section>
{cta}""".format(
        members=members,
        beh="".join("<li><b>%s</b> %s</li>" % (h, p) for h, p in [
            ("Knock, then floor protection.", "Drop cloths from the door to the work area, and they come back out with us."),
            ("Show, then tell.", "The failed part, the camera video or the meter reading goes in front of the customer before any recommendation."),
            ("Price changes need permission.", "If the job turns out to be bigger, nobody proceeds until the customer has agreed to the new number."),
            ("Clean like a guest.", "Swept, tools out, old unit and packaging gone from the house."),
            ("Follow-up is not optional.", "The owner calls back on the big jobs — repipes, replacements, sewer work — to check it is doing what it should.")]),
        tel=PHONE_TEL, phone=ORG["phone_display"], cta=cta("The person who diagnoses your job is the person who does it — which is why the estimate and the work carry the same name."))
    shell("team.html", "Our Team — Alfa Plumbing Services, Baytown TX",
          "Meet Alfa Plumbing Services in Baytown: owner and Texas Master Plumber %s, the service crew and dispatch. Licensed, insured and family-owned since %s." % (ORG["owner"], ORG["founded"]),
          None, body, "team.html", og=IMG["team"])


def page_projects():
    cards = "".join("""
      <article class="card-job rv">
        <div class="ph"><img src="{src}" alt="{name} by Alfa Plumbing Services" width="800" height="540" loading="lazy"></div>
        <div class="m">
          <p class="t">{name}</p>
          <p class="d">{d}</p>
          <p class="meta">{meta}</p>
        </div>
      </article>""".format(src=src, name=n, meta=meta, d=d) for n, src, meta, d in PROJECTS)
    body = pagehead("Projects", "Real jobs, photographed by the crew that did them.",
                    "Every photograph below was taken by the crew on a real Baytown-area job. Installs, repairs, rough-ins and emergencies — the way the work actually looks, with the service it shows described honestly.",
                    IMG["heater_repl"], "Baytown water heater replacement by Alfa Plumbing",
                    crumbs([("Projects", None)])) + """
<section class="band paper" id="gallery">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Gallery</p><h2 class="h-sec">Eleven photographs from the shop's own archive.</h2></div>
    <p class="lede">Each caption describes the type of work shown and what that work includes.</p></div>
    <div class="gal">{cards}</div>
  </div>
</section>

<section class="band tint" id="whatyouget">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">On any of these</p><h2 class="h-sec">What you get with a job like this.</h2></div>
    <p class="lede">Written on the estimate, not discovered at the door.</p></div>
    <ul class="ticks" style="max-width:74ch">{incl}</ul>
  </div>
</section>
{cta}""".format(
        cards=cards,
        incl="".join("<li>%s</li>" % x for x in [
            "Diagnosis and photographs of what we found, before parts get changed",
            "Free walk-through estimate on replacements, repipes, remodels and sewer work",
            "The 100% workmanship guarantee on our labour, from the licensed company that did it",
            "Haul-away of old tanks, pipes and packaging, out of the house not into the yard",
            "Permit and as-built handling where the county requires it (septic, sewer, gas conversions)",
            "A written record of settings, parts and the next service date"]),
        cta=cta("Want a photo like these for your job? Ask — we photograph replacements, repipes and sewer camera runs as standard."))
    shell("projects.html", "Plumbing Projects in Baytown — Real Jobsite Photos | Alfa Plumbing",
          "Water heater replacements, repipes, sewer lining, remodel rough-ins and commercial service around Baytown, documented with the company's own jobsite photographs.",
          None, body, "projects.html", og=IMG["heater_repl"])


def page_reviews():
    glink = "https://search.google.com/local/reviews?placeid=" + PLACE
    quotes = "".join("""
      <figure class="rev rv">
        <div class="st" aria-label="Five out of five">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
        <p class="txt"><b>{n}</b> &middot; {job}</p>
        <figcaption class="who"><a class="src" href="{glink}" target="_blank" rel="noopener nofollow">Read it on the Google profile &#8599;</a></figcaption>
      </figure>""".format(n=n, job=job, glink=glink) for n, job in REVIEWERS)
    body = pagehead("Reviews", "5.0 out of 40 on Google.",
                    "Each card names the reviewer and the job type, then links to the review on the profile so you can read it at the source.",
                    IMG["team"], "Alfa Plumbing Services crew in Baytown",
                    crumbs([("Reviews", None)]),
                    actions="""
      <a class="btn btn--call" href="{tel}">&#9742; Call {phone}</a>
      <a class="btn btn--onDark" href="https://search.google.com/local/writereview?placeid={place}" target="_blank" rel="noopener nofollow">Write a review &#8599;</a>
      <a class="btn btn--onDark" href="https://www.google.com/maps/place/?q=place_id:{place}" target="_blank" rel="noopener">Open the profile &#8599;</a>""".format(tel=PHONE_TEL, phone=ORG["phone_display"], place=PLACE)) + """
<section class="band paper" id="all">
  <div class="wrap">
    <div class="gbp" style="margin-bottom:30px">
      <p class="big">5.0 <span aria-hidden="true">&#9733;</span></p>
      <p class="lbl">Average rating on the Alfa Plumbing Services Google Business Profile.</p>
      <p class="divv"></p>
      <div class="acts" style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn btn--ghost" href="https://search.google.com/local/reviews?placeid={place}" target="_blank" rel="noopener nofollow">Read them on Google &#8599;</a>
        <a class="btn btn--ghost" href="{yelp}" target="_blank" rel="noopener nofollow">Yelp listing &#8599;</a>
      </div>
    </div>
    <div class="rev-grid">{quotes}</div>
  </div>
</section>

<section class="band tint" id="whyreview">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">The pattern</p><h2 class="h-sec">What the calls are actually about.</h2></div>
    <p class="lede">Four themes the shop hears repeated, in our own words, with the habit behind each one.</p></div>
    <div class="wgrid">{themes}</div>
  </div>
</section>
{cta}""".format(place=PLACE, yelp=ORG["yelp"], quotes=quotes,
        themes="".join('<div class="wrow"><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in REVIEW_THEMES),
        cta=cta("Happy with a job? A Google review from a Baytown address is the most useful thing you can do for the next customer."))
    shell("reviews.html", "Google Reviews for Alfa Plumbing Services, Baytown TX — 5.0",
          "Read what Baytown homeowners say about Alfa Plumbing Services: 5.0 on 40 Google reviews. Same-day water heater, drain, sewer, gas line and repipe work. Call %s." % ORG["phone_display"],
          None, body, "reviews.html", og=IMG["team"])


def page_areas():
    cells = "".join("""
      <a class="city{core}" href="contact.html#book"><span class="pin" aria-hidden="true"></span>{n}{z}</a>"""
                    .format(core=" core" if core else "", n=n,
                            z='<span class="z">Shop, dispatch and staging &mdash; %s</span>' % ORG["street"] if core else "")
                    for n, core, _d in AREAS)
    body = pagehead("Service areas", "Baytown and twelve cities around it.",
                    "The shop is at %s, %s — which is why most of these calls get same-day service. Outside the list, we will still tell you who to call." % (ORG["street"], ORG["city"]),
                    IMG["repair247"], "Alfa Plumbing service van in Baytown, Texas",
                    crumbs([("Service areas", None)])) + """
<section class="band paper" id="cities">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Coverage</p><h2 class="h-sec">The twelve cities on the list, and what changes between them.</h2></div>
    <p class="lede">Coverage is about drive time and housing stock: how far the truck has to roll, and what kind of pipe it will meet when it gets there.</p></div>
    <div class="citylist">{cells}</div>
  </div>
</section>

<section class="band dark" id="map">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">The shop</p><h2 class="h-sec">{street}, {city}</h2></div>
    <p class="lede">Park in front, or call ahead if you are bringing a photo of the problem on your phone.</p></div>
    <div class="mapbox ph"><iframe class="gmap" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map showing Alfa Plumbing Services at {street}, {city}, {state} {zip}" src="https://maps.google.com/maps?q={q}&amp;z=11&amp;output=embed"></iframe><span class="cap"><b>Alfa Plumbing Services</b> &mdash; {street}, {city}, {state} {zip} &middot; the twelve cities above are the working radius</span></div>
    <div class="acts" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px">
      <a class="btn btn--onDark" href="{maps}" target="_blank" rel="noopener">Open in Google Maps &#8599;</a>
      <a class="btn btn--call" href="{tel}">&#9742; {phone}</a>
    </div>
  </div>
</section>

<section class="band tint" id="notes">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Local notes</p><h2 class="h-sec">What changes town to town.</h2></div>
    <p class="lede">Baytown-area plumbing is mostly a question of water, age and what the sewer goes to.</p></div>
    <div class="wgrid">{notes}</div>
  </div>
</section>
{cta}""".format(cells=cells, street=ORG["street"], city=ORG["city"], state=ORG["state"], zip=ORG["zip"],
        q="508%20Scott%20St%2C%20Baytown%2C%20TX%2077520", maps=ORG["gmaps"], tel=PHONE_TEL, phone=ORG["phone_display"],
        notes="".join('<div class="wrow"><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in [
            ("Homes off city sewer", "Crosby, Mont Belvieu and Anahuac run septic. Pumping on a five-year interval is the whole maintenance plan, and replacement work needs the county permit we file."),
            ("Older iron lines", "Deer Park, La Porte and downtown Baytown houses built before about 1970 often still have galvanized supply. Rust-through and pressure loss are repipe conversations, not faucet repairs."),
            ("Slab leaks and flooding", "Pasadena, South Houston and Jacinto City sit on slab with high water tables. Two wet spots under a slab is a reroute discussion, and check valves are worth it in the flood-prone streets."),
            ("Coastal and well water", "Iron and sulphate in well water stain fixtures and eat heaters early. Filtration and a softener protect the tank you just paid for.")]),
        cta=cta("Homes off city sewer need septic service on a schedule rather than in a panic — if that is you, start with the tank, not the drain."))
    shell("service-areas.html", "Plumbing Service Areas — Baytown, Deer Park, La Porte, Pasadena & Near Houston | Alfa Plumbing",
          "Alfa Plumbing Services covers Baytown, Deer Park, La Porte, Pasadena, South Houston, Jacinto City, Galena Park, Houston, Channelview, Crosby, Mont Belvieu and Anahuac. Call %s." % ORG["phone_display"],
          None, body, "service-areas.html", og=IMG["repair247"])


def page_pricing():
    cards = "".join('<div class="pcard{hot}"><span class="k">{k}</span><span class="v">{v}</span><span class="s">{s}</span></div>'
                    .format(hot=" hot" if i < 2 else "", k=k, v=v, s=s) for i, (k, v, s) in enumerate(PRICING))
    faqs = [f for f in FAQS if f[2] in ("Do Alfa Plumbing Services in Baytown provide free estimates for new work?",
                                         "Is it safe to keep using a clogged toilet?")]
    body = pagehead("What it costs", "The numbers the company publishes. No teaser pricing.",
                    "These are the ranges shown on the current Alfa Plumbing site. Final pricing comes from a walk-through, because a water heater is not one price and a repipe is certainly not.",
                    IMG["install"], "Alfa Plumbing water heater installation in Baytown",
                    crumbs([("What it costs", None)])) + """
<section class="band paper" id="ranges">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Published ranges</p><h2 class="h-sec">Baytown plumbing costs, as published.</h2></div>
    <p class="lede">Anything a customer can be quoted honestly on the phone is below. Anything that cannot, we insist on seeing first.</p></div>
    <div class="price">{cards}</div>
    <div class="callout" style="margin-top:26px">
      <div><h3>{offer}</h3><p>Applies to a first visit over $300. Mention it when you book — the discount is on the invoice, not in a coupon email.</p></div>
      <div class="acts"><a class="btn btn--onDark" href="{tel}">&#9742; {phone}</a><a class="btn btn--onDark" href="contact.html#book">Request service</a></div>
    </div>
  </div>
</section>

<section class="band tint" id="howprice">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">How a price gets set</p><h2 class="h-sec">Six things that move a Baytown quote.</h2></div>
    <p class="lede">Knowing which of these applies to you is most of the reason to call before you buy a part online.</p></div>
    <ol class="steps">{six}</ol>
    <div class="wgrid" style="margin-top:26px">{free}</div>
  </div>
</section>

<section class="band paper" id="paying">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Estimates, warranty, payment</p><h2 class="h-sec">The commercial bit, stated plainly.</h2></div>
    <p class="lede">What we commit to, in writing, before the truck leaves.</p></div>
    <ul class="ticks" style="max-width:74ch">{terms}</ul>
  </div>
</section>

<section class="band tint" id="faq">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Money questions</p><h2 class="h-sec">The two we get asked first.</h2></div>
    <p class="lede">The rest are on the <a href="faq.html">FAQ page</a>.</p></div>
    <div class="faq">{f}</div>
  </div>
</section>
{cta}""".format(
        cards=cards, offer=OFFER, tel=PHONE_TEL, phone=ORG["phone_display"],
        six="".join("<li><b>%s</b> %s</li>" % (h, p) for h, p in [
            ("Fuel and type.", "Electric tank, gas tank, electric point-of-use or gas tankless — the equipment and venting differ by hundreds of dollars, not tens."),
            ("Age of the existing unit.", "Under ten years old usually means repair. Ten to fifteen means the repair money is better spent on a replacement that is quoted while we are there."),
            ("Access.", "A heater in a garage corner is one job; one in an attic, a closet with no pan, or a crawlspace is longer work and more hands."),
            ("Code items found on the way.", "Expansion tanks, T&amp;P piping to code, seismic straps, pans, drain lines, fresh air intake. Each is cheap alone and they are quoted as options, not surprises."),
            ("Pipe and material on a repipe.", "Copper, PEX and CPVC differ in cost and in how much wall gets opened; patching is a separate line item by choice, not necessity."),
            ("Depth of the line for underground work.", "A sewer lateral under a driveway and one under turf are different excavations. Camera first — then the right number.")]),
        free="".join('<div class="wrow"><h3>%s</h3><p>%s</p></div>' % (h, p) for h, p in [
            ("Free walk-through estimates", "Replacements, repipes, remodels, sewer repair and septic work are quoted on site at no charge. You only pay for work you approve."),
            ("100% workmanship guarantee", "Published by the company with a money-back clause on the labour Alfa performs — the licensed company that did the work stands behind it.")]),
        terms="".join("<li>%s</li>" % x for x in [
            "Estimates for replacement, repipe, remodel and sewer work are free — walk-through, no charge, no obligation.",
            "Workmanship is covered by the 100% satisfaction guarantee with money-back clause; equipment carries the manufacturer's own warranty, registered at install.",
            "Permits on jobs that require them are pulled by Alfa, including county septic permits and as-builts.",
            "Emergency dispatch is available 24 hours; call the shop line for the after-hours rate rather than assuming a holiday multiplier.",
            "Invoices itemise parts, labour and options declined, so warranty questions later have a paper trail."]),
        f=faq_items(faqs), cta=cta("Send a photo of the nameplate and the installation and we can usually give you a range before a truck is scheduled."))
    shell("pricing.html", "Baytown Plumber Prices — What a Plumbing Job Costs | Alfa Plumbing",
          "Published Baytown plumbing price ranges: average visit $526 (typical $201–$850), $45–$150/hour, tankless installs $1,000–$3,000, plus %s. Free walk-through estimates." % OFFER,
          None, body, "pricing.html", og=IMG["install"])


def page_faq():
    faq_schema = {"@type": "FAQPage", "@id": SITE + "/faq.html#faqpage",
                  "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a, _k in FAQS]}
    body = pagehead("FAQ", "Answers to the questions a Baytown homeowner actually asks.",
                    "Written from the content published by Alfa Plumbing — diagnostics rules, guarantee terms, permit handling and the guidance in the company's own DIY guides. Nothing invented, and if a number is not published we say so instead of guessing.",
                    IMG["fixture"], "Alfa Plumbing technician explaining a repair to a Baytown homeowner",
                    crumbs([("FAQ", None)])) + """
<section class="band paper" id="faq">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">{n} questions</p><h2 class="h-sec">Read this before you call — or before you DIY.</h2></div>
    <p class="lede">Each answer is the one we give on the phone. The page carries FAQPage schema so search engines can show them the same way.</p></div>
    <div class="faq">{f}</div>
  </div>
</section>

<section class="band tint" id="safety">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Before anything else</p><h2 class="h-sec">The three minutes that limit the damage.</h2></div>
    <p class="lede">Do these in this order while someone phones us.</p></div>
    <ol class="steps">{safe}</ol>
    <div class="relstrip" style="margin-top:26px">{rel}</div>
  </div>
</section>
{cta}""".format(
        n=len(FAQS), f=faq_items(FAQS),
        safe="".join("<li><b>%s</b> %s</li>" % (h, p) for h, p in [
            ("Shut the water at the main.", "Follow the pipe from the meter to where it enters the wall and turn it clockwise. If you cannot find it or it will not move, tell us on the phone — that becomes part of the job."),
            ("Kill the power to the heater.", "Breaker off for an electric tank; turn the gas control to Pilot or off if water is near the burner or the tank is leaking."),
            ("Get out if you smell gas.", "No switches, no flames, no doorbells. Ventilate on your way out and phone from outside — utility first, us second."),
            ("Photograph everything.", "The wet ceiling, the label on the tank, the video of the drain. Photos turn a guess into a two-visit job instead of a four-visit one."),
            ("Do not pour drain chemicals on a full clog.", "They sit on top of the blockage, heat up, and damage the pipe and whoever gets their hands in it afterwards.")]),
        rel="".join('<a href="%s"><span class="k">%s</span><span class="t">%s</span></a>' % (href, k, t) for k, href, t in [
            ("Guide", "guides/why-is-my-water-bill-so-high.html", "Why the bill jumped and how to test it yourself"),
            ("Guide", "guides/water-heater-knocking-easy-5-min-fix.html", "The five-minute flush that stops a knocking tank"),
            ("Page", "water-heaters.html#water-heater-repair", "What a water heater visit includes"),
            ("Page", "leaks-gas-repairs.html#gas-line-repair", "Gas line repair and appliance tie-ins")]),
        cta=cta("Not answered here? Call %s — we would rather talk for two minutes than have you guess." % ORG["phone_display"]))
    shell("faq.html", "Plumbing FAQ — Baytown Plumber Questions Answered | Alfa Plumbing Services",
          "Eleven honest answers from a Baytown master plumber: repair or replace a water heater, free estimates, hydro jetting on old lines, septic permits, 24-hour emergency service.",
          None, body, "faq.html", [faq_schema], og=IMG["fixture"])


def page_services():
    groups = []
    for c in CLUSTERS:
        rows = "".join('<a class="srow" href="%s#%s"><span class="n">%s</span><span class="d">%s</span><span class="go" aria-hidden="true">&rarr;</span></a>'
                       % (c["file"], sid, sname, sshort) for sid, sname, sshort in c["services"])
        groups.append("""
      <article class="grp-card rv">
        <div class="ph"><img src="{img}" alt="{name} in Baytown by Alfa Plumbing" width="800" height="420" loading="lazy"></div>
        <div class="b">
          <p class="eyebrow">{tag}</p>
          <h3><a href="{file}">{name}</a></h3>
          <div class="srows">{rows}</div>
          <a class="btn btn--ghost" href="{file}">Open the {lower} page <span class="ar">&rarr;</span></a>
        </div>
      </article>""".format(img=c["image"], name=c["name"], tag=c["tagline"], file=c["file"], rows=rows,
                           lower=c["name"].lower()))
    body = pagehead("All services", "Twenty services, four pages, no hidden menu.",
                   "Everything Alfa Plumbing performs in Baytown and the ship-channel cities, grouped the way the company's own pages group it. Each line goes to the section on its page where the diagnostics, the inclusions and the price facts live.",
                   IMG["servicing"], "Alfa Plumbing Services performing plumbing work in a Baytown home",
                   crumbs([("Services", None)])) + """
<section class="band paper" id="all">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Four clusters</p><h2 class="h-sec">Pick the group, then the service.</h2></div>
    <p class="lede">If you are not sure which one you need, the <a href="index.html#triage">symptom picker</a> on the home page routes you faster.</p></div>
    <div class="grpgrid">{groups}</div>
    <div class="callout">
      <div><h3>Emergency plumber, 24 hours</h3><p>Active water, sewage coming up, or a gas smell is not queued behind the scheduled work. Call {phone} and we dispatch.</p></div>
      <div class="acts"><a class="btn btn--onDark btn--call" href="{tel}">&#9742; Call now</a><a class="btn btn--onDark" href="leaks-gas-repairs.html#emergency-plumber">What an emergency visit includes</a></div>
    </div>
  </div>
</section>
{triage}
{cta}""".format(groups="\n".join(groups), phone=ORG["phone_display"], tel=PHONE_TEL,
               triage=triage_band("Which do you need?", "Six symptoms, six routes. Choose one and you will be on the right page with the right price facts in two clicks."),
               cta=cta("Not on the list? Call anyway — well water, filtration, backflow and repair-for-rental work all come through this office too."))
    shell("services.html", "Plumbing Services in Baytown, TX — All 20 Services | Alfa Plumbing Services",
          "Water heaters, drain and sewer, septic, gas lines, leak detection, repiping, fixtures, remodels, new construction, commercial and 24-hour emergency plumbing in Baytown. Call %s." % ORG["phone_display"],
          None, body, "services.html", og=IMG["servicing"])


def page_guides_index():
    chips = ['<button class="fchip on" id="all-guides" data-filter="all" aria-pressed="true">All <span>(%d)</span></button>' % len(GUIDES)]
    for cat in ["DIY Tutorial", "Plumbing Tips", "Emergency", "Services"]:
        items = [g for g in GUIDES if g["cat"] == cat]
        if items:
            chips.append('<button class="fchip" id="%s" data-filter="%s" aria-pressed="false">%s <span>(%d)</span></button>'
                         % (cat_key(cat), cat_key(cat), cat, len(items)))
    by_date = sorted(GUIDES, key=lambda g: g["date"], reverse=True)
    body = pagehead("DIY guides & plumbing tips", "Twenty guides. Read one before you pay for a call.",
                    "The shop's master plumber publishes these precisely so fewer people pay for a call they could have done in ten minutes — and so nobody attempts the work that needs a licence.",
                    IMG["fixture"], "Homeowner fixing a faucet with an Alfa Plumbing guide",
                    crumbs([("DIY guides", None)])) + """
<section class="band paper" id="library">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">{n} published guides</p><h2 class="h-sec">The whole library, newest first.</h2></div>
    <p class="lede">Written by the shop, dated as published, and each one ends where the licensed work begins.</p></div>
    <div class="filters" role="group" aria-label="Filter guides by category">
      {chips}
      <p class="fcount" id="gcount" aria-live="polite">{n} guides</p>
    </div>
    {cards}
  </div>
</section>

<section class="band dark" id="limits">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Where DIY stops</p><h2 class="h-sec">Four things you should not do yourself.</h2></div>
    <p class="lede">Everything on this page is safe to try. These are the ones where the cheap fix becomes an expensive claim.</p></div>
    <ol class="steps" style="max-width:78ch">{stop}</ol>
  </div>
</section>
{cta}""".format(
        n=len(GUIDES), chips="".join(chips), cards=guide_cards(by_date),
        stop="".join("<li><b>%s</b> %s</li>" % (h, p) for h, p in [
            ("Anything on the gas line beyond a connection you can reach.", "A fitting you can tighten by hand after an appliance move is fine. Running or repairing pipe is not: pressure test, sediment trap and a leak check are the difference between an appliance and an emergency call."),
            ("A repipe, a sewer line, or any line inside a wall or slab.", "Materials, pitch, venting and permits. It is also why a located leak costs a hole and an unlocated one costs a room."),
            ("Chemical drain openers on a clog that will not move.", "They sit on top of the blockage, heat up, and come back to burn the hands of whoever cables it afterwards — including ours."),
            ("Ignoring a tank that is leaking at the seam.", "There is no repair for that. Shut the water and the gas to it, then call for the replacement quote on the same visit.")]),
        cta=cta("Tried the fix and it is still doing the thing? Send the guide name and a photo — we will tell you honestly whether the next step is a part or a plumber."))
    shell("guides.html", "Free Plumbing DIY Guides & Tutorials from a Baytown Master Plumber | Alfa Plumbing",
          "Twenty published guides: leaky faucets and running toilets, water heater flushes, plumber's putty and Teflon tape, high water bills, drains, brown water, gas smell response and leak detection.",
          None, body, "guides.html", og=IMG["fixture"])


# ---------------------------------------------------------------- guide pages
def page_guide(g, idx):
    prev_g = GUIDES[idx - 1] if idx > 0 else None
    next_g = GUIDES[idx + 1] if idx + 1 < len(GUIDES) else None
    rel_html = "".join('<a href="{href}"><span class="k">{k}</span><span class="t">{t}</span></a>'.format(
        href=href, k=("Guide" if href.split("#")[0][:-5] in BY_GUIDE else "Service"),
        t=t) for t, href in g.get("related", []))
    steps = re.findall(r"<li>(.*?)</li>", g["body"], re.S)
    howto = None
    ol = re.search(r'<ol class="steps">(.*?)</ol>', g["body"], re.S)
    if ol:
        items = re.findall(r"<li>(.*?)</li>", ol.group(1), re.S)
        if 3 <= len(items) <= 14:
            howto = {"@type": "HowTo", "name": html.unescape(g["title"]),
                     "description": html.unescape(g["lede"]), "totalTime": "PT%dM" % max(g["mins"], 3),
                     "step": [{"@type": "HowToStep", "position": i + 1,
                               "name": html.unescape(re.sub(r"<[^>]+>", "", st))[:110].strip(),
                               "itemListElement": [{"@type": "HowToDirection",
                                                    "text": html.unescape(re.sub(r"<[^>]+>", " ", st)).replace("  ", " ").strip()}]}
                              for i, st in enumerate(items)]}
    article = {"@type": "Article", "@id": SITE + "/guides/%s.html#article" % g["slug"],
               "headline": html.unescape(g["title"]), "datePublished": g["date"], "dateModified": g["date"],
               "author": {"@type": "Organization", "name": ORG["name"], "url": SITE + "/about.html"},
               "publisher": {"@id": SITE + "/#business"}, "image": g["img"],
               "mainEntityOfPage": SITE + "/guides/%s.html" % g["slug"],
               "articleSection": g["cat"], "inLanguage": "en-US"}
    extra = [article] + ([howto] if howto else [])
    pager = ""
    if prev_g or next_g:
        cells = []
        if prev_g:
            cells.append('<a href="%s.html"><span class="k">&larr; Newer guide</span><span class="t">%s</span></a>' % (prev_g["slug"], prev_g["title"]))
        if next_g:
            cells.append('<a class="next" href="%s.html"><span class="k">Older guide &rarr;</span><span class="t">%s</span></a>' % (next_g["slug"], next_g["title"]))
        pager = '<nav class="pager" aria-label="More guides">%s</nav>' % "".join(cells)
    body = """
<section class="pagehead" id="overview">
  <span class="blueprint" aria-hidden="true"></span>
  <div class="wrap" style="grid-template-columns:1fr">
    <div>
      {crumb}
      <p class="eyebrow">{cat} &middot; {mins} minute read</p>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
    </div>
  </div>
</section>

<section class="band paper" id="guide">
  <div class="wrap">
    <div class="artwrap">
      <article class="article">
        <div class="meta">
          <span>Published <time datetime="{date}">{pretty}</time></span><span class="dot"></span>
          <span>{cat}</span><span class="dot"></span>
          <span>By {author}, Texas Master Plumber</span>
        </div>
        {body}
        <div class="ph" style="margin:26px 0;border-radius:14px;overflow:hidden">{img}</div>
        <p class="mono-note">By Alfa Plumbing Services, Baytown &middot; Texas Master Plumber. Where a job needs a licence, we say so.</p>
        {pager}
      </article>
      <aside class="artside">
        {call}
        <div class="dcard"><span class="k">Related services</span>
          <ul style="margin:8px 0 0;padding:0;list-style:none;font-size:14.5px;line-height:1.5">{rel}</ul>
        </div>
        <div class="dcard"><span class="k">More guides</span><span class="s"><a href="guides.html">All {n} DIY guides &rarr;</a></span></div>
      </aside>
    </div>
  </div>
</section>
{cta}""".format(
        crumb=crumbs([("DIY guides", "guides.html"), (g["title"], None)]),
        cat=g["cat"], mins=g["mins"], title=g["title"], lede=g["lede"], date=g["date"],
        pretty=pretty(g["date"]), author=ORG["owner"], body=g["body"],
        img='<img src="%s" alt="%s" width="1200" height="640" loading="lazy">' % (g["img"], g["title"]),
        pager=pager, n=len(GUIDES),
        call="""<div class="dcard"><span class="k">Still leaking, cold or clogged?</span>
        <span class="v"><a href="{tel}">{phone}</a></span>
        <span class="s">Same-day service in Baytown &middot; {offer}</span>
        <a class="btn" href="contact.html#book" style="margin-top:10px;justify-content:center">Request a visit</a></div>""".format(tel=PHONE_TEL, phone=ORG["phone_display"], offer=OFFER),
        rel="".join('<li><a href="{href}">{t}</a></li>'.format(href=href, t=t) for t, href in g.get("related", [])),
        cta=cta("If the guide got you most of the way and something is still wrong, that is the point at which a diagnostic call earns its money."))
    shell("guides/%s.html" % g["slug"],
          g.get("ttitle", g["title"]),
          g.get("mdesc") or g.get("ttitle", g["title"]),
          None, body, "guides/%s.html" % g["slug"], extra, og=g["img"])


def page_contact():
    body = """
<section class="pagehead" id="overview">
  <span class="blueprint" aria-hidden="true"></span>
  <div class="wrap">
    <div>
      {crumb}
      <p class="eyebrow">Contact &amp; booking</p>
      <h1>Call, text or send the request.</h1>
      <p class="lede">The phone is answered by a plumber, and text messages with a photo of the problem are usually the fastest way to get a real answer. The form below arrives in the shop inbox.</p>
      <div class="acts">
        <a class="btn btn--call btn--lg" href="{tel}">&#9742; {phone}</a>
        <a class="btn btn--onDark btn--lg" href="{sms}">Text a photo</a>
        <a class="btn btn--onDark btn--lg" href="{mail}">{email}</a>
      </div>
    </div>
    <div class="ph"><img src="{img}" alt="Alfa Plumbing Services truck ready for a Baytown call" width="1000" height="700" loading="eager"></div>
  </div>
</section>

<section class="band dark" id="book">
  <div class="wrap">
    <div class="book">
      <div class="dialer">
        <p class="eyebrow">Request service</p>
        <h2 class="h-sec">Six fields. No account, no portal.</h2>
        <p class="lede">Fill it in and your email app opens with the request addressed to {email}. Press send and it is with us. Texting a photo of the problem is usually the quickest route to a real answer.</p>
        <div class="dcard"><span class="k">Emergency? Skip the form</span>
          <span class="v"><a href="{tel}">{phone}</a></span>
          <span class="s">24-hour dispatch for active water, gas and sewage</span></div>
        <div class="dcard"><span class="k">The shop</span>
          <span class="v"><a href="{maps}" target="_blank" rel="noopener">{street}, {city}</a></span>
          <span class="s">{state} {zip} &middot; {area_note}</span></div>
      </div>
      {form}
    </div>
  </div>
</section>

<section class="band paper" id="after">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">What happens next</p><h2 class="h-sec">From request to fixed, in four steps.</h2></div>
    <p class="lede">No call centre, no “someone from our network”, no surprise second visit to price the work.</p></div>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="band tint" id="where">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Find us</p><h2 class="h-sec">{street}, {city}</h2></div>
    <p class="lede">Serving {areas}. Drive time from the shop is why same-day service works here.</p></div>
    <div class="mapbox ph"><iframe class="gmap" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map showing Alfa Plumbing Services at {street}, {city}, {state} {zip}" src="https://maps.google.com/maps?q={q}&amp;z=11&amp;output=embed"></iframe><span class="cap"><b>Alfa Plumbing Services</b> &mdash; {street}, {city}, {state} {zip}</span></div>
    <div class="acts" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px">
      <a class="btn" href="{maps}" target="_blank" rel="noopener">Open directions &#8599;</a>
      <a class="btn btn--ghost" href="service-areas.html">All service areas</a>
      <a class="btn btn--ghost" href="pricing.html">What a visit costs</a>
    </div>
  </div>
</section>
{cta}""".format(crumb=crumbs([("Contact", None)]), tel=PHONE_TEL, sms=SMS, mail=MAIL,
        phone=ORG["phone_display"], email=ORG["email"], img=IMG["truck"], maps=ORG["gmaps"],
        street=ORG["street"], city=ORG["city"], state=ORG["state"], zip=ORG["zip"],
        area_note="Baytown office — call or text before stopping in",
        areas=", ".join(n for n, _c, _d in AREAS[:6]) + " and six more",
        form=book_form(),
        steps="".join("<li><b>%s</b> %s</li>" % (h, p) for h, p in [
            ("We call back the same day.", "Morning requests get a call back before lunch. Real emergencies get dispatched while you are on the phone."),
            ("We tell you what it probably is.", "Symptom plus age of the equipment usually gives a range over the phone, and we bring the parts for the two likely causes."),
            ("Diagnosis on site, then a price.", "Test the cheap things first; show you what failed. Walk-through estimates on replacements, repipes, remodels and sewer work are free."),
            ("The work, guaranteed.", "Fix it, clean up, haul the old unit away, and write down what was replaced and when it is due again.")]),
        q="508%20Scott%20St%2C%20Baytown%2C%20TX%2077520", cta=cta("If it is water where water should not be, shut the main and call %s before you write anything into a form." % ORG["phone_display"]))
    shell("contact.html", "Contact Alfa Plumbing Services, Baytown TX — Call, Text or Book Online",
          "Call %s, text a photo of the problem, or send the request form to %s. Baytown shop at %s — licensed &amp; insured, family-owned since %s, 24-hour emergency dispatch." % (
              ORG["phone_display"], ORG["email"], ORG["street"], ORG["founded"]),
          None, body, "contact.html", og=IMG["truck"])


# ---------------------------------------------------------------- css for new bands
EXTRA_CSS = """
.fc-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:rgba(255,255,255,.14)}
.fc{background:var(--ink);padding:18px 20px;display:flex;flex-direction:column;gap:6px}
.fc .k{font:600 10.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:#f0a582}
.fc .v{font-size:15.4px;color:rgba(255,255,255,.86);line-height:1.45}
.wgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px 40px}
.wrow h3{font-size:19px;letter-spacing:-.02em;margin-bottom:7px}
.wrow p{margin:0;font-size:15.4px;color:var(--ink-70);line-height:1.55}
@media (max-width:980px){.wgrid{grid-template-columns:repeat(2,minmax(0,1fr))}.fc-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){.wgrid,.fc-grid{grid-template-columns:1fr}}
.grpgrid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.grp-card{background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden;box-shadow:var(--sh-1);display:flex;flex-direction:column}
.grp-card .ph img{height:190px;width:100%;object-fit:cover}
.grp-card .b{padding:20px 22px 22px;display:flex;flex-direction:column;gap:12px;flex:1}
.grp-card h3{font-size:clamp(21px,2.3vw,27px);letter-spacing:-.025em;margin:0}
.grp-card h3 a{color:inherit;text-decoration:none}.grp-card h3 a:hover{color:var(--brand-deep)}
.srows{display:grid;gap:2px;margin:0 0 4px}
.srow{display:grid;grid-template-columns:1fr auto;gap:10px;align-items:baseline;text-decoration:none;color:inherit;padding:9px 10px;border-radius:8px;border-bottom:1px solid var(--line-soft)}
.srow:hover{background:var(--paper-2)}
.srow .n{font-weight:700;font-size:15.4px}
.srow .d{font-size:14.2px;color:var(--ink-55);grid-column:1/2}
.srow .go{color:var(--copper);font-family:var(--mono)}
@media (max-width:900px){.grpgrid{grid-template-columns:1fr}}
.ft-phone a{font:800 22px/1.1 var(--display);letter-spacing:-.02em;color:#fff}
.tag-owner.nophoto img{display:none}
.faq details summary{cursor:pointer}
"""


# ---------------------------------------------------------------- build
def plumber_css():
    p = os.path.join(ROOT, "assets", "alfa.css")
    s = open(p, encoding="utf-8").read()
    marker = "/* == ALFA MULTI-PAGE COMPONENTS =="
    if marker not in s:
        with open(p, "a", encoding="utf-8") as fh:
            fh.write("\n" + marker + " */\n" + EXTRA_CSS)


def build():
    for key, c in CLUSTER_COPY.items():
        cl = CLUSTER_BY_ID[key]
        cl.update(c)
    page_home()
    page_services()
    for c in CLUSTERS:
        cluster_page(c)
    page_about(); page_team(); page_projects(); page_reviews(); page_areas()
    page_pricing(); page_faq(); page_guides_index(); page_contact()
    for i, g in enumerate(GUIDES):
        page_guide(g, i)
    plumber_css()
    write("sitemap.xml", sitemap())
    write("robots.txt", "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)


def sitemap():
    files = ["index.html", "services.html"] + [c["file"] for c in CLUSTERS] + \
            ["about.html", "team.html", "projects.html", "reviews.html", "service-areas.html",
             "pricing.html", "faq.html", "guides.html", "contact.html"] + \
            ["guides/%s.html" % g["slug"] for g in GUIDES]
    pr = {"index.html": "1.0"}
    urls = []
    for f in files:
        pri = pr.get(f, "0.8" if f == "services.html" or f == "guides.html" else "0.7")
        urls.append("  <url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>"
                    % (SITE, "" if f == "index.html" else f, TODAY, pri))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % "\n".join(urls)


if __name__ == "__main__":
    build()
    print("built", len([f for f in os.listdir(ROOT) if f.endswith(".html")]), "top-level pages,",
          len(os.listdir(os.path.join(ROOT, "guides"))), "guide pages")
