# Alfa Plumbing Services — Reimagined Homepage

Deliverable: **`alfa-plumbing-homepage.html`** (single file, no build step, no dependencies beyond Google Fonts).
Extracted from `https://alfaplumbingservices.com/` on 2026-09-03 (live pages + WordPress REST inventory of
25 pages, 20 posts, 4 categories). Strategy follows the attached audit/blueprint.

## Color system (6 values, grounded in the subject)
Derived from Alfa's real logo mark (azure triangle + water-drop negative space, read from
`2018/04/cropped-ALFA-PLUBING-B-1.jpeg`) and jobsite materials — deliberately not a generic plumber palette.

| Token | Hex | Role |
|---|---|---|
| `--porcelain` | `#EEF2F5` | page ground (cool sanitary porcelain, not warm cream) |
| `--ink` | `#0C2233` | body text, dark dispatch bands, footer |
| `--brand` | `#0E7AC7` | Alfa azure: links, focus rings, live-coupling glow |
| `--brand-deep` | `#0A4E82` | primary buttons, headings on light |
| `--copper` | `#B4622D` | the signature line, eyebrow ticks, service metadata |
| `--ember` | `#D24B2A` | urgency only: emergency band, call CTA |

## Type
- **Display** — `Archivo`, width axis opened to ~112%. Engineered signage voice; reads like a utility
  wordmark, which is exactly what the real logo is.
- **Body** — `Source Sans 3`. High x-height for a phone screen in daylight; a 45+ audience.
- **Utility/mono** — `IBM Plex Mono` for eyebrows, licence/rating chips, city codes, hours, cost figures.
  This is the "work-order / dispatch" voice of the system.

## Layout concept — customer journey
`triage → trust → understand → see proof → determine fit → act`
1. **Triage** — hero states Baytown + family-owned + who answers the phone, then a symptom finder
   ("What's going on right now?") in customer language, not internal taxonomy.
2. **Trust** — factual strip: founded 2003, 5.0/40 as displayed by the site's Google widget, 12 published
   communities, 100% workmanship guarantee.
3. **Understand** — services in 4 clusters mirroring the live site's own grouping, names preserved verbatim.
4. **Proof** — Alfa's real photos, the owner, verbatim Google reviews linking to Google, published cost figures.
5. **Fit** — service areas, pricing honesty, objection-handling FAQ (extractable for AI search), resource hub
   grouped by the site's real categories.
6. **Act** — 5-field booking form mirroring the live form's own fields, delivered by `mailto:` to the verified
   inbox, plus call and text-a-photo.

## Signature element — "the service line" (used with restraint)
One copper line runs down the left gutter of every band like a plumbing run, with a **coupling at each
section joint**. The coupling of the section you are reading turns Alfa azure and gains a halo, so the
scroll position is legible as a route through the job. Decorative only (`aria-hidden`), hidden below
1240px, and static under `prefers-reduced-motion`. It never appears as clip-art, icon grid, or ornament.

## Deliberately avoided
No warm-cream + serif + terracotta; no near-black + single neon accent; no broadsheet hairline-rule grid;
no generic plumbing-icon row (the audit names it as a weakness of the current site). Evidence is carried by
photography, mono data chips and inline "to confirm" notes instead.

---

# PLACEHOLDERS, VERIFICATION STATUS & DIVERGENCES
*Everything below is what the build could not source from the live site as fact, or where the build
intentionally departs from the current site. Six matching flags are also written into the page itself —
search for `data-prelaunch="remove-before-launch"` and delete that markup at build time.*

## Verified from the live site (safe to publish)
- **Phone (713) 992-9257** — used identically in the header, footer, every `tel:` and `sms:` link.
- **Email info@alfaplumbingservices.com** — a live `mailto:` in the top bar of every page, on the contact page, and in the "Message Us" tab.
- **Address** 508 Scott St, Baytown, TX 77520 · **Owner** Servando Perez · **Founded** 2003 · **Guarantees** ("100%… job isn't done until you say it is", "Satisfaction money back guaranteed") · **Offer** 10% off first appointment over $300, new customers · **Audiences** residential, commercial, property managers, industrial, landlords, banks/mortgage companies, realtors · **Cost figures** ($526 avg / $201–$850 / $45–$150 hr / tankless $1,000–$3,000 / 10–15 yr tank life / 120°F) · **Service list** and **all 22 photographs** (each asset URL was probed and returns a real image).

## Unverified — needs the client before launch
1. **Email is verified as *published*, not as *monitored*.** The About page also prints a second address (`Info@alfaplumbing.com`) and a Connecticut number (`203-767-8567`) — both template leftovers. Confirm the inbox actually reaches the office; if it doesn't, the `mailto:` action should switch to the verified number as primary.
2. **Licence number conflicts:** one page says *MPL 36649*, another *MPL 41752*. "Licensed & insured Texas Master Plumber" is published everywhere so that claim is used, but **no number is printed anywhere in this build**.
3. **Business hours are published nowhere** (header, footer, contact page, widget). Third-party listings contradict each other, so hours are shown only as "Confirm before launch" and are **omitted from the LocalBusiness schema** rather than guessed.
4. **Founding year:** 2003 used in all 15 places; the stray "Since '94" badge and the "16/18 years" variants are flagged in-page for correction across the site, GBP and directories.
5. **Team page:** only Marcos and Jose appear by name (in customer reviews). Two of the three portraits are deliberate empty placeholders; confirm names, roles and photo permission.
6. **Reviews:** all six are verbatim from the site's Google widget, but the newest is ~3 years old and the 5.0/40 count is the widget's cached value. Wire a live GBP feed instead of typed-in numbers.
7. **No booking/scheduler API exists** on the current site, so nothing was replaced by a third-party scheduler; requests go via `mailto:` plus `tel:`/`sms:`.

## Nav: what could and could not be extracted
The live header is a JS-rendered ShiftNav off-canvas panel — the menu markup is not in the served HTML, and the WordPress menus REST endpoint is authentication-locked (401). jina/AllOrigins/Codetabs/Wayback renders all returned an empty panel. So the navigation here was **reconstructed from the site's own authoritative page inventory** (WordPress REST: 25 pages + 20 posts + 4 categories), preserving real page/service names verbatim. Consequences to accept or reverse:
- **Flattened:** the 20 service entries are grouped into 4 clusters (Water Heaters · Drains, Sewer & Septic · Gas, Water & Leaks · Fixtures, Property & Urgent) and a mega-menu; the live site is a flat list with no parent/child relationship in the DB (`parent:0`, `menu_order:0` on all 25 pages).
- **Renamed for customers, not for SEO:** "Blog" → "Plumbing Guides"; "About Alfa Plumbing" → "About"; "Check Our Google Reviews" → "Reviews"; "Baytown Water Heater Maintenance" → "Water Heater Maintenance".
- **Dropped:** the `Links` page (a comment-spam/link-farm directory that can cause a penalty), `Sitemap` (a shortcode that never rendered), and the duplicate location pages `/water-heater-repair-houston/` and `/plumbing-company-baytown-tx/`. Their real content was folded into the single services/areas sections instead of kept as separate near-duplicate URLs.
- **Added:** "Why Alfa", "Projects", "What it costs", "Service Areas" as navigation items — no new pages, only anchors to sections built from existing content.

## Structural divergences from the live site
- Single-page prototype, so **every link is an in-page anchor**; there are zero links to the legacy domain (only Google and Yelp, for reviews/proof).
- One homepage replaces the site's **five near-duplicate water-heater pages** (`/water-heaters/`, `/water-heater-repair/`, `/water-heater-installation/`, `/baytown-water-heater-maintenance/`, `/water-heater-repair-houston/`); at launch, keep one canonical hub and redirect the rest — and retitle the two service pages currently published as *blog posts* (`/gas-line-repair/`, `/water-line-repair/`).
- The generic icon grid (`plumber_icon_01–09`, `logo_0*` partner marks) is gone — replaced by photography and the symptom wayfinder, per the audit.
- Scraped/foreign content that was **deliberately not reused**: the solar-water-heater article with its pixabay stock and YouTube embed, the competitor's warranty/quote paragraphs (25-yr / 10-yr, Patrick Middleton) on the repipe page, third-party "Gas Safe registered engineer" (a UK credential) on the gas page, and the blog footer's literal "Lorem Ipsum" block.
- `2003–2026` copyright and the "Rebuild prototype, not yet the live site" line in the footer should be removed at handoff.

---

# ADDENDUM — multi-page refactor (`alfa-plumbing-site/`)

The single-file prototype is superseded. The build is now **one route per navigation item** plus the full
DIY library, generated from two content modules so no page can drift from the design system:

```
alfa-plumbing-site/
  build.py      page shell, nav, footer, schema, all page bodies
  content.py    verified business facts: 20 services in 4 clusters, pricing, FAQ, areas, team, gallery
  guides.py     the 20 published posts (slug, real date, category, image, body)
  validate.py   links · anchors · alt text · JSON-LD · duplicate ids · tag balance · form wiring · assets
  serve.py      preview server (0.0.0.0)
  assets/       alfa.css (design system + multi-page components) · alfa.js (nav, filters, reveals, form)
  index.html · services.html · water-heaters.html · drains-sewer.html · leaks-gas-repairs.html ·
  repiping-remodels.html · about.html · team.html · projects.html · reviews.html · service-areas.html ·
  pricing.html · faq.html · guides.html · contact.html · guides/<20 slugs>.html · sitemap.xml · robots.txt
```

**Design system unchanged** — same tokens (`--porcelain/--ink/--brand/--brand-deep/--copper/--ember`),
Archivo / Source Sans 3 / IBM Plex Mono, the copper service-line pipe run in the left gutter (now per band,
on every page), the symptom wayfinder, no icon grid, none of the three banned aesthetics. New components:
`.pagehead` band with breadcrumbs, `.svcrow` service rows (what it is / what the visit includes / published
price facts / the guide to read first), `.article` + numbered `.steps` for the guides, `.gcard` library grid
with category filter, `.ctaband` closing every page, and a print stylesheet.

**Homepage slimmed**: it keeps hero, trust facts, the symptom picker, four cluster cards, why-us, founder,
three photos, three review entries, eight cities, six guides, four price cards, four FAQs and the booking
form — each as a summary that routes to its own page instead of rendering the whole site.

**DIY content fully represented**: all 20 posts appear on `guides.html` (real titles, WordPress categories,
publication dates from the REST API, the company's own images) and each has its own page. Twelve bodies were
recovered in full from the live posts; the rest carry their published lead copy plus their real
procedures/checklists. Nothing is listed that is not on the current site.

**Integrity decisions in this pass** (see `alfa-plumbing-site/README.md` for the full list):
- Review *wording* is no longer reproduced — names, subjects and the 5.0/40 figure only, linked to the
  profile, so no customer words are invented. Themes are labelled as Alfa's own summary.
- Gallery captions describe the type of work shown rather than narrating invented jobs.
- Hours and the licence number remain out of the pages **and** out of the schema; founding year is 2003
  everywhere, including `foundingDate`.
- All in-page launch flags were removed from the pages; every launch note now lives in the README's
  checklist and in this brief.

**Zero links to the legacy domain** remain enforced by `validate.py` (which also fails the build if any
`href`, fragment, `<link>`/`<script>` target, `alt`, or JSON-LD block is broken — currently 35 pages,
0 problems).

### Second audit pass (metadata, navigation, dead copy)

- **2003** is now airtight: 206 occurrences across 35 pages, zero competing founding dates or
  "16/18 years" claims anywhere, including inside the DIY articles.
- **DIY preview** unchanged at 20 of 20 cards (real titles, WordPress dates, categories, read times,
  one-sentence previews) plus 20 routed pages; the chip filter and `#category` deep links work.
- **Unnecessary text**: removed the hero symptom-chip row that duplicated the triage band, removed the
  four pages duplicated between the top-level nav and the About dropdown, and deleted 38 dead CSS rules so
  the stylesheet matches only what the markup uses.
- **Metadata**: every page now ships a 28-60 character title with one brand token and a 70-158 character
  description ending on a complete sentence (previously 200-272 characters, clipped mid-word by Google).
  Company pages use hand-authored `TITLES`/`DESCS`; guides use `ttitle`/`mdesc` while keeping the real post
  title as `<h1>`.
- **Validator** gained four checks (title length, description length, mid-word clipping, duplicated brand,
  duplicated nav route). Green run: `35 pages · 35 JSON-LD blocks parsed · 0 problems`.

## Single page (`one-page.html`)

Requested as "collate all section on the project to a single html, no external dropdown of any section".
Delivered as a generated variant: `python3 build.py` also writes `one-page.html` - all 35 sections inline in
one file with one sticky flat nav (15 in-page anchors + the call button) and **no dropdown machinery at all**:
no mega panel, no About/Guides submenus, no burger drawer, and every internal link rewritten to an in-file
anchor. Per-section ids are namespaced (`rt-<section>__<id>`) so 35 sections cannot collide, lead paths
(`tel:`/`sms:`/`mailto:`) and outbound review links stay verbatim, and the generator fails if a dropdown or a
link that leaves the file survives. `assets/alfa.css` is untouched apart from the band selector widening, so
the single page renders with production styling; it is `noindex`, out of the sitemap, and the shipped site
stays multi-page for indexing.

### Two wayfinder images replaced

The Water Heaters and Drains/Sewer/Septic cards were still pointing at 2018 media-library banners from the old
site, so the two biggest cards on the wayfinder read as stock filler. They now use photographic assets in the
build - `assets/img/water-heaters.jpg` (gas tank, copper supply lines and drain pan in a Gulf Coast garage) and
`assets/img/drains-sewer.jpg` (inspection cable fed into a home's PVC cleanout, monitor and gloves on the grass) -
across the home cards, the `services.html` group cards and the cluster pageheads, with absolute URLs for
`og:image`. Both are generated stand-ins, labelled "Illustration:" in the alt text, and flagged in the launch
checklist for replacement with the shop's own photographs.

### Arrangement pass (why the first single page looked scattered)

Inlining the CSS/JS fixed the missing-stylesheet failure, but the page still read as a pile of pages, because
that is what it was: `<main>` of each route includes that route's own dark page hero, its breadcrumb row, its
three call buttons and its closing CTA band, so the one-pager carried 34 heroes, 34 identical closers, two
booking forms and 35 H1s. `one_page.py` now re-arranges instead of concatenating: hero only on the homepage,
compact section headers elsewhere, one booking form (in Contact, which the retargeted CTAs point at), one
closing CTA at the end, guides grouped as one chapter whose chips filter both the hub cards and the inline
articles, and Contact moved to last so the page ends on the conversion. The build fails if that arrangement
regresses.
