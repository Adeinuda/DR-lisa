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
