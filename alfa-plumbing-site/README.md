# ALFA PLUMBING — MULTI-PAGE REFACTOR (this pass)

Everything above describes the single-file prototype (`alfa-plumbing-homepage.html`, now removed from the
tree — recoverable at commit `48a8b80`). This pass turns that into a real route-per-navigation-item build.

## What changed

| Ask | Done |
|---|---|
| Dedicated routes/pages per nav item instead of one long homepage | 15 top-level pages + 20 guide pages, all generated, all sharing one stylesheet |
| Preview for **all** DIY content | `guides.html` lists all 20 published posts (real titles, dates, categories, images) with a working category filter; each has its own page with the extracted body |
| Remove unnecessary text | Audit/placeholder prose deleted from the pages, duplicate service copy cut, homepage bands are now summaries that route out |
| Fix all bugs | See the bug log below |
| Founding year | **2003 everywhere** — the stray "Since '94" and "16/18 years" copy is gone, including from schema |

## Route map

```
index.html                    hero · trust facts · symptom wayfinder · 4 service clusters · why-us ·
                              founder · jobs · reviews · areas · 6 guides · pricing · 4 FAQs · booking form
services.html                 all 20 services, grouped, each row deep-links into its cluster page
water-heaters.html            repair · install · maintenance · tankless
drains-sewer.html             drain cleaning · sewer line · septic · disposal
leaks-gas-repairs.html        gas line · water line · leak detection · faucet · toilet · emergency · well water
repiping-remodels.html        repipe · bath · kitchen · new construction · commercial
about.html  team.html  projects.html  reviews.html  service-areas.html  pricing.html  faq.html  contact.html
guides.html                   the 20-post library, filterable
guides/<slug>.html            one page per published guide (20 files)
```

Each page carries: breadcrumbs, its own `<title>`/description/canonical/OG, a `WebPage` node, a
`BreadcrumbList`-friendly structure, a closing CTA band and the sticky mobile call bar. Nav items route
to real pages (no page renders another page's content). FAQ accordion answers + `FAQPage` schema live on
`faq.html` only, so the homepage and cluster pages cannot drift from the markup.

## Content integrity — decisions made in this pass

- **Review text is not republished.** The Google widget on the live site shows reviewer names, 5-star
  ratings and the job type; the wording belongs to the reviewer on the profile. The build therefore shows
  *name · subject · ★★★★★* with a "read it in the customer's own words" link, and adds four themes written
  as Alfa's own summary (`REVIEW_THEMES`). Nothing is quoted that was not verified verbatim.
- **Project captions describe the service, not a fake case history.** The 11 gallery images are real Alfa
  photos; their captions say what that type of job includes. No invented dollar figures, streets or
  before/after narratives.
- **Team page is only what is published**: Servando Perez (owner, Texas Master Plumber, founded 2003), the
  crew as a unit, and the shop. The live reviews name *Marcos* and *Jose* — if the client wants them on the
  page with portraits and roles, that needs their approval first (photo permission + title), which is why
  they are not asserted here.
- **Hours are still not printed anywhere** (including schema) because they are published nowhere. Licence
  number still omitted (MPL 36649 vs 41752 conflict).
- Guide bodies are the site's own procedures (Delta rebuild steps, the water-heater flush, putty rules,
  Teflon wrap rules and the MIL-T-27730A / A-A-58092 grades, the seven cold-water causes, the five
  high-bill causes, gas-smell response, brown-water triage, septic five-year pumping). Advice that was not
  Alfa's own — third-party plumbing-blog text, the solar-heater scrape, the "Gas Safe" line — stayed out.

## Bugs fixed this pass

1. **Broken asset paths on every page** — the generator emitted `assets/assets/alfa.css`; guide pages also
   needed `../`. Fixed (`pre()` returns a directory prefix) and the validator now checks `<link>`/`<script>`
   targets, not just `<a>`.
2. **`<details open="false">`** — invalid; a boolean attribute with any value is *open*. Now the attribute is
   omitted unless the first item should be expanded.
3. **Guide filter never matched** — cards were tagged `data-cat="DIY Tutorial"` while chips filtered on
   `diy-tutorial`; values are now both slugged, and `[hidden]` is forced to `display:none!important` so
   flex/grid cards actually hide.
4. **White-on-white inside dark bands** — the step lists and review cards inherited `color:#fff` on white
   cards; explicit `.band.dark` child colours added.
5. **Duplicated offer sentence** ("10% off your first visit over $300 off your first visit over $300") from
   interpolating the offer twice.
6. **Audit vocabulary leaking into customer copy** — "as published on the current site", "media library at
   launch" (now a short photo credit that only shows if the hot-linked asset 404s), "rebuild prototype"
   reduced to one footer phrase.
7. **Duplicate triage block** repeated on every cluster page; each page now shows only its own symptoms.
8. Mega-menu had a redundant 21st "Urgent" entry and a `00` index; counts now honestly total 20 services.
9. Cross-page anchors (`#fixture-repair`) that did not exist; validation enforces every `href` target and
   fragment, and tag-balance checks run over all 35 pages.
10. **Photo cards were mis-nested** — `.card-job` carried the `ph` class itself, so `display:flex` centre
    rules laid the image, tag, title and description side by side. Gallery cards (home, About, Projects) now
    use a `.ph` image block plus a padded text block, and `.ph` is block-flow with `min-height` so a blocked
    asset still holds its frame.
11. **`validate.py` never captured `<script>` bodies**, so every JSON-LD block was silently skipped. Fixed;
    it now reports the count (35 blocks parsed) and fails on literal HTML entities or unresolved fields
    inside schema. Guide `HowTo`/`Article` strings are entity-decoded, so `T&P valve` reaches schema as text,
    not `T&amp;P`.
12. **The homepage ended with a CTA band duplicating its own booking band** — the redundant band is gone; the
    page now ends on the form. Cluster pages likewise dropped a lede that repeated the homepage card copy.
13. **90 fallback captions** ("Alfa Plumbing photo") were printing wherever a hot-linked image was blocked.
    Removed from the markup — the hatched frame stays, and the media-library instruction lives only here.
14. Pricing copy still said "per the live site's cost guide"; every audit phrase ("current site", "live
    site's", "as published on") is now out of customer-facing pages, and the tankless guide's "18+ years"
    experience line was reworded so nothing competes with the 2003 founding year.
15. **A jobsite photo was captioned as a "map"** on the Service Areas and Contact pages — misleading. Both
    now embed the actual location (`maps.google.com/maps?q=508+Scott+St…&output=embed`, no API key) with an
    address caption and the existing "Open directions" link as fallback.
16. **Four pages were reachable twice** — Reviews, Service Areas, Pricing and Contact sat both at the top
    level of the nav and inside the About dropdown. The dropdown now filters a `top_level` set, and
    `validate.py` fails any route that two nav items point at.
17. The homepage hero carried a row of symptom chips that repeated, one section later, the triage band
    underneath it. The chip row is gone; the triage band is the single place a symptom is offered.
18. **SERP metadata was over budget** — descriptions ran 200-272 characters (Google clips near 158, several
    ended mid-word or on "in the.") and titles reached 77 with a doubled brand tail
    (`... | Alfa Plumbing | Alfa Plumbing`). `build.py` now runs every title through `meta_title()` and every
    description through `meta_desc()`, backed by hand-authored `TITLES` for the 15 company pages, `ttitle`
    per guide (the full real post title stays as the on-page `<h1>`) and `mdesc` per guide, so shortening is
    editorial rather than a cut in half. Titles are 28-60 characters with the brand exactly once;
    descriptions 70-158 ending on a complete sentence; `&` is escaped for `<title>`/`og:title`. All four
    rules are enforced by `validate.py`.
19. 38 dead CSS rules removed (`.chip`, `.emg`, `.stats`, `.rcard`, `.hours-tbl`, `.altact`, `.ph .fb`, the
    orphaned logo rules) - generated markup and stylesheet are now 1:1, verified by diffing every class in
    `alfa.css` against every class emitted by `build.py`.
20. **Reveal animation could blank a page.** `.rv{opacity:0}` applied with no script running, so a blocked
    or failed `alfa.js` left every card invisible. `<html>` now ships `class="no-js"` flipped to `js` by a
    two-line inline script, and the hidden start-state is scoped to `.js .rv` - content-first, animation second.
    `validate.py` fails if the ungated rule ever comes back.
21. **The Reviews route carried the Service Areas route.** An eight-city grid sat mid-page on `reviews.html`
    (heading, lede, city buttons, and a second link to the same page). Cut; the city grid now exists once, on
    `service-areas.html`, with the homepage teaser and footer pointing at it.
22. **The homepage and About page showed the identical three reviewers**, and each card said both "Posted on the
    Alfa Plumbing Google profile" and "Read it in the customer's own words". `review_band()` gained an `offset`
    so About shows the other three names (zero overlap), and each card carries one labelled link. The caption
    "what the current profile widget displays" - build vocabulary, not customer copy - is gone.
23. Mega-menu now marks the cluster you are on (`aria-current="page"` on the active group's own link), and a
    new validator check asserts every page ships the `no-js`/`js` gate.


24. **Two wayfinder images were the wrong picture.** The Water Heaters and Drains/Sewer/Septic cards pulled
    `heater_repl` and `drain` from the old site's 2018 media library, so the two biggest cards on the wayfinder
    showed generic legacy banner art. Both clusters now ship a real photographic asset - `assets/img/water-heaters.jpg`
    (gas tank, copper lines and drain pan in a Gulf Coast garage) and `assets/img/drains-sewer.jpg` (inspection
    cable at a home's PVC cleanout) - used on the home cards, the `services.html` group cards and the cluster
    pageheads, with the absolute URL for `og:image`. **These are generated illustrations, not the shop's own
    jobsite photographs** - see the launch checklist - and their `alt` text says "Illustration:" for that reason.
25. `assets/alfa.js` now matches `main > section[id], main > section.opsec[id] > section[id]`, so the copper
    service line still lights the band you are reading in the collated single page (the bands sit one level
    deeper there). No change in behaviour on the multi-page routes.

## Single page: `one-page.html`

The whole project collated into one HTML file with a **flat nav and no dropdown of any section** - no mega
panels, no burger drawer, no links that leave the file. `python3 build.py` regenerates it after every build
(`one_page.py` does the work).

* **What it holds:** `<main>` from each of the 15 navigation routes and all 20 DIY guide routes, inline in
  nav order (35 sections), plus the shared utility bar, footer and mobile call bar emitted once.
* **It is genuinely one file:** `assets/alfa.css`, `assets/alfa.js` and the two local photographs are
  **inlined** (CSS and JS into `<style>`/`<script>`, the photos as data URIs), so it renders correctly when
  opened directly, emailed, or dropped in a viewer that cannot resolve sibling files - no folder next to it.
  The only external request left is the Google Fonts link, which degrades to the `system-ui` fallback in the
  token stack. ~880 kB on its own; the multi-page site keeps the real 900px JPEG files (~140 kB for both).
* **Navigation:** one sticky row of 15 in-page anchors (Home, Services, the four clusters, About, Team,
  Projects, Reviews, Areas, Costs, FAQ, DIY Guides, Contact) with a call button; the active section lights
  as you scroll. Every internal link in the document was rewritten to an in-page anchor
  (`water-heaters.html#water-heater-repair` -> `#rt-water-heaters__water-heater-repair`), so breadcrumbs,
  cross-sell links, the FAQ jump and the guide category filters all work inside the one file. The
  generator fails the build if any `class="drop"`, `.panel`, `aria-expanded`, `#burger` or `#mobnav`
  survives, or if any `<a>` points at a file.
* **Ids are namespaced** per section (`rt-<route>__<id>`) because 35 sections of ids collide; `for`,
  `aria-controls` and friends move with them. `#book` stays bare on the homepage section (the mobile bar
  tracks it) and `#gcount` on the guides section, because `alfa.js` resolves those by name.
* **Lead paths are untouched:** `tel:`, `sms:`, `mailto:` and the Google/Yelp links are emitted verbatim, so
  both booking forms still send from the single file.
* **It is a variant, not a 36th route:** `noindex,nofollow`, absent from `sitemap.xml`, skipped by
  `validate.py`. The shipped site stays multi-page so each route can be indexed. `one_page.py` self-checks
  the collation (unique ids, every anchor and `for`/`aria-*` reference resolves, label/field parity, both
  mailto forms, one `<main>`, no undefined CSS tokens, **nothing left pointing at `assets/`**).
* **Single-page typesetting:** repeated per-page chrome is suppressed here - breadcrumbs hidden, each
  section header tightened, guide articles drop their duplicate hero buttons (their own CTA band follows)
  and the sections are separated by a hairline instead of looking like 35 stacked pages.

## Build & verify

```bash
cd alfa-plumbing-site
python3 build.py       # regenerates every .html, sitemap.xml, robots.txt from content.py + guides.py
                       # ...and one-page.html, the whole site collated into one flat-nav file
python3 validate.py    # links, anchors, alt text, JSON-LD, duplicate ids, tag balance, form wiring,
                       # asset existence, "no link to the legacy domain", fabricated-year guard
python3 serve.py 8000  # preview server, bound to 0.0.0.0
```

Content lives in two data modules — `content.py` (business facts, clusters, 20 services, pricing, FAQ,
areas, team, gallery) and `guides.py` (the 20 posts: slug, title, real publish date, category, image,
body). Edit those, re-run `build.py`. The chrome (nav, footer, sticky bar, mailto form) is generated once,
so a new page cannot drift from the design system.

## Schema

- `index.html`: `Plumber` with real NAP, `foundingDate: 2003`, founder, 12 `areaServed`, 20 `makesOffer`,
  `aggregateRating 5.0/40`, `sameAs` Google + Yelp. **No hours, no licence number.**
- every page: `WebSite` + `WebPage` with `publisher` by `@id`.
- `faq.html`: `FAQPage` generated from the visible accordions (single source of truth).
- each guide: `Article` (real `datePublished`, Alfa as author) plus a `HowTo` built from the numbered steps
  that actually exist in the body.

## Launch checklist (unchanged items marked ●)

1. ● Copy the 22 hot-linked `wp-content/uploads` images into the new media library and rewrite the URLs in
   `content.py` / `guides.py` (`UP` is the only place the base lives), then delete the `.fb` fallbacks.
2. ● Decide the inbox: keep `mailto:info@alfaplumbingservices.com` or point the form at a real backend/CRM;
   if the address is not monitored, make `tel:` the primary and remove the form.
3. ● Publish real hours (all pages + `openingHoursSpecification`) and settle the licence number.
4. ● Replace the static review block with a live GBP feed; keep the "read it on Google" links.
5. ● 301s: `/water-heaters/` + the four water-heater variants → `water-heaters.html`;
   `/gas-line-repair/`, `/water-line-repair/` (currently *posts*) → the leaks/gas cluster;
   every old blog URL → its `guides/<slug>.html`; `/links/` and the shortcode sitemap → delete, do not
   redirect.
6. Set the canonical/sitemap domain if the site will not live on `alfaplumbingservices.com`, then drop the
   "Design prototype for review" footer phrase.
7. Remove `data-*` nothing — there are no in-page launch flags in this build; the launch notes are all here.
8. Replace the two generated illustrations (`assets/img/water-heaters.jpg`, `assets/img/drains-sewer.jpg`) with
   Alfa's own photos of a water heater change-out and a sewer camera inspection at a cleanout, and drop the
   "Illustration:" prefix from their alt text once they are real.
