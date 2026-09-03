# -*- coding: utf-8 -*-
"""Verified business facts for Alfa Plumbing Services (source: alfaplumbingservices.com)."""

ORG = {
    "name": "Alfa Plumbing Services",
    "founded": "2003",
    "owner": "Servando Perez",
    "phone_display": "(713) 992-9257",
    "phone_tel": "+17139929257",
    "email": "info@alfaplumbingservices.com",
    "street": "508 Scott St",
    "city": "Baytown",
    "state": "TX",
    "zip": "77520",
    "logo": "https://alfaplumbingservices.com/wp-content/uploads/2018/04/cropped-ALFA-PLUBING-B-1.jpeg",
    "favicon": "https://alfaplumbingservices.com/wp-content/uploads/2018/10/1.ALFA-PLUBING-fava.png",
    "servando": "https://alfaplumbingservices.com/wp-content/uploads/2020/04/servando.png",
    "gmaps": "https://www.google.com/maps/place/?q=place_id:ChIJrSWt2KxdP4YRqwnd8Jxnvac",
    "yelp": "https://www.yelp.com/biz/alfa-plumbing-services-baytown",
}

UP = "https://alfaplumbingservices.com/wp-content/uploads"
IMG = {
    "servicing": f"{UP}/2018/04/baytown-tx-plumber-services.jpg",
    "heater_repl": f"{UP}/2018/04/baytown-tx-water-heater-replacement.jpg",
    "repair247": f"{UP}/2018/04/baytown-tx-plumbing-repair-247.jpg",
    "drain": f"{UP}/2018/04/baytown-tx-drain-cleaning.jpg",
    "repiping": f"{UP}/2018/11/ed35b70628f21c22d2524518b7494097e377ffd41cb5134697f6c67ea2_640.jpg",
    "install": f"{UP}/2018/09/3250CC2F-BF55-41B9-9939-41B5CDD0A8E3.jpeg",
    "fixture": f"{UP}/2018/09/shutterstock_143795752-1024x599.jpg",
    "sewer": f"{UP}/2018/04/sewer-line-repair-baytown.jpg",
    "commercial": f"{UP}/2018/04/commercial-plumbing-baytown.jpg",
    "newhome": f"{UP}/2018/11/20181115_112209-e1542290227574-300x137.jpg",
    "remodel": f"{UP}/2018/11/92689291_10157326473737130_5873527871549440000-n-e1542294079961-300x137.jpg",
    "favi": f"{UP}/2018/10/1.ALFA-PLUBING-fava.png",
    "team": f"{UP}/2018/04/baytown-tx-plumber-team.jpg",
    "truck": f"{UP}/2018/04/baytown-tx-plumber-truck.jpg",
    "heater_fix": f"{UP}/2018/04/baytown-tx-water-heater-repair.jpg",
}

# --- navigation (label, href, kind) ------------------------------------------------
NAV = [
    ("Services", "services.html", "mega"),
    ("Water Heaters", "water-heaters.html", "plain"),
    ("Drains & Sewer", "drains-sewer.html", "plain"),
    ("Leaks, Gas & Repairs", "leaks-gas-repairs.html", "plain"),
    ("Repiping & Remodels", "repiping-remodels.html", "plain"),
    ("Projects", "projects.html", "plain"),
]
NAV_MAIN = [
    ("About", "about.html"),
    ("Team", "team.html"),
    ("Reviews", "reviews.html"),
    ("Service Areas", "service-areas.html"),
    ("What It Costs", "pricing.html"),
    ("DIY Guides", "guides.html"),
    ("Contact", "contact.html"),
]

# --- the 20 service entries found on the live site, grouped into 4 clusters --------
# name, anchor id, one-line (real scope), where it lives
CLUSTERS = [
    {
        "id": "water-heaters", "file": "water-heaters.html",
        "name": "Water Heaters",
        "tagline": "Tank and tankless — repair, replacement, flush and tune-up.",
        "image": IMG["heater_repl"],
        "blurb": "Same-day no-hot-water calls, element and thermocouple diagnostics, full-replacement quotes, annual flushes and Baytown tankless installs.",
        "services": [
            ("water-heater-repair", "Water heater repair", "No hot water, cold shower, leaking tank"),
            ("water-heater-installation", "Water heater installation", "Like-for-like or upgrade, permits and haul-away"),
            ("water-heater-maintenance", "Water heater maintenance", "Annual flush and tune-up"),
            ("tankless-water-heaters", "Tankless water heaters", "On-demand installs for Baytown homes"),
        ],
    },
    {
        "id": "drains-sewer", "file": "drains-sewer.html",
        "name": "Drains, Sewer & Septic",
        "tagline": "Slow, backed-up or smelly — camera first, then the right machine.",
        "image": IMG["drain"],
        "blurb": "Sink, tub, main-line and laundry drain cleaning, sewer camera inspection, trenchless sewer repair and septic service, replacement and permits.",
        "services": [
            ("drain-cleaning", "Drain cleaning", "Kitchen, bath, laundry, main line"),
            ("sewer-line-services", "Sewer line services", "Camera, spot repair, trenchless"),
            ("septic-tank-services", "Septic tank services", "Pump, inspection, design, permits"),
            ("garbage-disposal-repair", "Garbage disposal repair", "Jams, hums and dead disposals"),
        ],
    },
    {
        "id": "leaks-gas", "file": "leaks-gas-repairs.html",
        "name": "Leaks, Gas & Fixture Repairs",
        "tagline": "Find it, then fix it — including the gas line you should never chase yourself.",
        "image": IMG["repair247"],
        "blurb": "Gas line repair and new appliance lines, underground water leak detection and repair, faucet and toilet repairs, garbage disposals and emergency service.",
        "services": [
            ("gas-line-repair", "Gas line repair", "Leak response and appliance tie-ins"),
            ("water-line-repair", "Water line repair", "Underground service line breaks"),
            ("water-leak-detection", "Water leak detection", "Non-invasive locating before demo"),
            ("faucet-repair", "Faucet repair", "Drips, base leaks, cartridge swaps"),
            ("toilet-repair", "Toilet repair", "Running, weak flush, wax ring, rocking"),
            ("emergency-plumber", "Emergency plumber", "After-hours water-on-the-floor response"),
            ("well-water-filtration", "Well water & filtration", "Iron, sulphur odour and pressure problems"),
        ],
    },
    {
        "id": "repiping-remodels", "file": "repiping-remodels.html",
        "name": "Repiping, Remodels & Commercial",
        "tagline": "Whole-house water and drain layouts, done once and done right.",
        "image": IMG["repiping"],
        "blurb": "Whole-house repipe decisions and installs, rough-in and finish plumbing for bath and kitchen remodels, new construction and light commercial.",
        "services": [
            ("house-repiping", "House repiping", "Copper, PEX and CPVC change-outs"),
            ("bathroom-remodels", "Bathroom remodels", "Move or replace supply and drain lines"),
            ("kitchen-remodels", "Kitchen remodels", "Sink, disposal, ice-maker and dishwasher hookups"),
            ("new-construction", "New construction plumbing", "Rough-in to final tie-off"),
            ("commercial-plumbing", "Commercial plumbing", "Light commercial, 24-hour call dispatch"),
        ],
    },
]

# --- emergency / triage prompts (real service scope only) ---------------------------
TRIAGE = [
    ("Water on the floor right now", "Shut the main, then call. We dispatch same-day, including after hours.", "Call (713) 992-9257", True),
    ("No hot water", "Breaker, pilot and thermostat checks first — many calls are a $20 part, not a new tank.", "Book a water heater diagnostic"),
    ("Sewer smell or slow drains everywhere", "Main line or vent problem. A camera tells us before we dig anything.", "Book a drain visit"),
    ("I smell gas", "Leave, ventilate, then phone from outside. Line locator on the way.", "Call (713) 992-9257", True),
    ("High water bill, nothing dripping", "Flapper, fill valve and irrigation checks — plus a meter test you can run yourself.", "Read the bill checklist"),
    ("Remodel or repipe quote", "Rough-in plan, materials, and a per-room price before the first cut.", "Talk through your project"),
]

# --- pricing facts published on the live site ---------------------------------------
PRICING = [
    ("Average Baytown plumber visit", "$526", "Range $201 – $850, per the live site's cost guide"),
    ("Hourly rate", "$45 – $150/hr", "Project pricing is more common here than straight hourly"),
    ("Water heater thermocouple / pilot part", "~$20 part", "Frequently the whole repair on a gas tank"),
    ("Tankless water heater install", "$1,000 electric – $3,000 gas", "Baytown average, including the unit"),
    ("Tank water heater lifespan", "10 – 15 years", "Flush yearly; 120°F is the set point we work to"),
]
OFFER = "10% off your first visit over $300"

# --- FAQ (answers drawn only from published Alfa pages) -----------------------------
FAQS = [
    ("Do you charge for estimates?",
     "No. Walk-through estimates for repipes, remodels, sewer repairs and water heater replacements are free — you only pay for work you approve.",
     "Do Alfa Plumbing Services in Baytown provide free estimates for new work?"),
    ("Should I repair or replace my water heater?",
     "If the tank is leaking, it is a replacement — a leaking tank cannot be repaired. If a 10-to-15-year-old tank needs both an element and a thermostat, replace it: the repair money usually ends up in the new tank anyway. Anything under ten years is usually repaired.",
     "When should I repair a water heater instead of replacing it?"),
    ("Why did my hot water run out so fast?",
     "Four usual causes: an undersized tank for the household, a burned-out lower element, a broken dip tube, or a gas pilot that dropped out. Sediment is the silent one — it kills heating efficiency long before the tank starts leaking.",
     "Why am I running out of hot water quickly?"),
    ("How do I know which valve shuts off my house?",
     "Follow the pipe from the water meter to where it enters the wall; that is the main. If you cannot find it or it will not turn, we will locate and service it for you — and if you cannot shut water off, a burst pipe becomes a much larger job.",
     "Where is the main water shut-off valve in my house?"),
    ("Do you handle septic permits?",
     "Yes. Alfa pulls the county permit and files the as-built on replacement systems, so the paperwork is done before the tank goes in.",
     "Do you pull permits for septic replacement?"),
    ("Do you do emergency plumbing at night?",
     "For real emergencies we dispatch 24 hours. Call (713) 992-9257; if the line is busy, text the same number and we call back.",
     "Do you offer 24-hour emergency plumbing in Baytown?"),
    ("Can I use a toilet that won't flush or won't stop running?",
     "A running toilet is usually a flapper that needs replacing and is safe to use while you wait. A toilet that will not drain is a different problem: if multiple drains in the house are slow or gurgling, stop running water and call, because it points to the main line.",
     "Is it safe to keep using a clogged toilet?"),
    ("Will hydro jetting damage old pipes?",
     "It is safe on cast iron, clay and PVC in good shape. If the line is already collapsed or badly offset, jetting makes it worse, so we camera first and only jet what the camera says can take it.",
     "Is hydro jetting safe for older sewer lines?"),
    ("Are you licensed and insured?",
     "Yes — a Texas Master Plumber, licensed and insured, family-owned since 2003.",
     "Is Alfa Plumbing Services licensed and insured in Texas?"),
    ("Do you do small repairs like a leaky faucet?",
     "Yes. Drips, running toilets, wobbly fixtures, disposal jams and hose-bib leaks all count — no job is too small to be worth a call.",
     "Will a Baytown plumber do small repairs?"),
    ("Do you work with insurance restoration and property managers?",
     "Yes. We scope, photograph and price water damage work for restoration and property management accounts, and dispatch after hours for tenants.",
     "Do you handle plumbing for property managers and restoration work?"),
]

# Names and subjects exactly as the current site's Google review widget displays them. The review
# *text* is not republished here — reading it happens on the profile itself, which is what the links do.
REVIEWERS = [
    ("Mike", "Water heater replacement"),
    ("Rosa V.", "Main line clog"),
    ("D. Nguyen", "Tankless install"),
    ("Karen L.", "Bathroom remodel rough-in"),
    ("Tom", "Whole-house repipe"),
    ("J. Alvarez", "Gas line service call"),
]

# Themes the shop hears repeated, written as Alfa's own summary — not quoted customer words.
REVIEW_THEMES = [
    ("Answered the same day", "No hot water, sewage, gas smell and active leaks get fitted in the same day they are called in, including after hours."),
    ("Diagnosis before parts", "Camera video, meter readings, continuity checks and pressure tests first — the recommendation comes after what was found."),
    ("Price agreed before the work", "Walk-through estimates on replacements, repipes, sewer work and remodels, and the invoice matches them."),
    ("House left clean", "Drop cloths, old tanks and packaging removed from the property, and a look at the ceiling below the work before the truck leaves."),
]

AREAS = [
    ("Baytown", True, "Office and shop at 508 Scott St — same-day response across the city."),
    ("Deer Park", False, "Tank, drain and repipe work between Highway 225 and San Jacinto."),
    ("La Porte", False, "Downtown baths and older neighborhoods with original galvanized lines."),
    ("Pasadena", False, "Flood-zone homes: sewer check valves and jetting."),
    ("South Houston", False, "Fixer-upper remodels and service-line repairs."),
    ("Jacinto City", False, "Post-1970 slab homes — leak detection before tile comes up."),
    ("Galena Park", False, "Ship-channel-area drain and sewer service."),
    ("Houston", False, "East-side neighborhoods we can reach the same day."),
    ("Channelview", False, "Industrial and rental properties."),
    ("Crosby", False, "Well and septic properties."),
    ("Mont Belvieu", False, "Rural lots and small businesses."),
    ("Anahuac", False, "Septic systems, docks and camp properties."),
]

TEAM = [
    ("Servando Perez", "Owner / Founder · Texas Master Plumber",
     "Founded the company in 2003 and still takes service calls. Licensed and insured as a Texas Master Plumber, which is what makes the workmanship guarantee the company publishes worth anything: it comes from the licence holder who did the job, not from a subcontractor.",
     ORG["servando"]),
    ("The crew", "Licensed & insured residential and commercial plumbers",
     "Water heaters, drains and sewer, gas lines, leak detection, repipes and remodel rough-ins. The same person who diagnoses the job is the one who does it, so the quote and the work stay attached to one name.",
     IMG["team"]),
    ("The shop", "Scheduling, permits and callbacks",
     "508 Scott St, Baytown. Requests come to the same number and inbox as everything else here, septic and sewer permits are filed by us, and 24-hour dispatch covers the calls that cannot wait until morning.",
     IMG["truck"]),
]

PROJECTS = [
    ("Water heater replacement", IMG["heater_repl"], "Water heaters", "Tank set on a new pan and drain line, connections and venting done to code, old unit removed from the property."),
    ("Whole-house repipe", IMG["repiping"], "Repiping", "Galvanized and polybutylene lines replaced with PEX or copper, with a shut-off at every fixture and a labelled valve map."),
    ("Drain cleaning", IMG["drain"], "Drains", "Cable or hydro jet sized to the pipe, then a camera look so you can see the cleaned wall, not just hear about it."),
    ("Sewer line repair", IMG["sewer"], "Sewer line", "Lined where the pipe can take it, spot-repaired where it cannot, excavated only when the camera says it has to be."),
    ("Fixture and toilet repairs", IMG["fixture"], "Fixtures", "Cartridges, flappers, O-rings, wax rings and angle stops — the small repairs that fix most of what gets called in."),
    ("New construction rough-in", IMG["newhome"], "New build", "Under-slab water and waste laid and tested before the pour, rough-in inspected, fixtures set at the end."),
    ("Bathroom remodel", IMG["remodel"], "Remodel", "Drain, waste and vent relocated with the tile crew, tested before the wall closes, fixtures and caulking at the handover."),
    ("Commercial service", IMG["commercial"], "Commercial", "Restrooms, kitchen hot water and shut-off infrastructure on a service agreement, with after-hours dispatch for tenants."),
    ("Water heater install", IMG["install"], "Water heaters", "Capacity sized to the household, expansion tank where the system needs one, temperature set to 120°F on start-up."),
    ("Emergency response", IMG["repair247"], "24-hour calls", "Active water, sewage and gas get isolation advice on the phone first, then a truck — repair priced after the risk is handled."),
    ("Tankless conversion", IMG["servicing"], "Tankless", "Demand calculated, venting and gas supply sized for the model, filtration discussed before the unit goes on the wall."),
]
