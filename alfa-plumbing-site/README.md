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
   fragment, and `re.sub`/tag-balance checks run over all 35 pages.

## Build & verify

```bash
cd alfa-plumbing-site
python3 build.py       # regenerates every .html, sitemap.xml, robots.txt from content.py + guides.py
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
