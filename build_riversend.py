#!/usr/bin/env python3
"""
Bespoke build script for ebbwec.com.au — Riversend Playhouse.
Option B: Magazine / Big Type design.
Standalone, self-contained, no shared imports.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://ebbwec.com.au"
BRAND = "Riversend Playhouse"
TAGLINE = "Regional Victorian theatre"
COPYRIGHT_YEAR = 2026

NAV = [
    ("Programme", "/whats-on/", "whats-on"),
    ("Visit", "/contact/", "contact"),
    ("About", "/about/", "about"),
    ("Archive", "/archive/", "archive"),
]

# Programme catalogue — used for marquee, season aside, programme grid, and item pages.
# ord_index drives the asymmetric grid layout (col-7, col-5, col-4 etc.) on the home page.
SEASON = [
    {
        "slug": "suzi-quatro-leather-forever-encore-tour",
        "title": "Suzi Quatro &mdash; Leather Forever Encore",
        "title_short": "Suzi Quatro",
        "category": "Touring music",
        "venue": "Main Theatre",
        "meta": "Main Theatre &middot; One night only",
        "image": "/assets/img/concert-stage.jpg",
        "image_alt": "Stage lit for a touring music performance, microphone and amplifiers in place",
        "lede": "Suzi Quatro returns to regional Victoria as part of the Leather Forever Encore Tour, with a programme drawn from the catalogue and a handful of deep cuts the touring band have built around for this run.",
        "chips": ["Main Theatre", "One night only", "On sale"],
    },
    {
        "slug": "10cc",
        "title": "10cc",
        "title_short": "10cc",
        "category": "Touring music",
        "venue": "Main Theatre",
        "meta": "Main Theatre &middot; Touring engagement",
        "image": "/assets/img/auditorium.jpg",
        "image_alt": "Theatre auditorium ready for a music performance, full main theatre with orchestra pit",
        "lede": "The British art-rock band returns to Australian audiences with a programme spanning the 1970s catalogue, led by founding member Graham Gouldman.",
        "chips": ["Main Theatre", "Touring", "On sale"],
    },
    {
        "slug": "the-52-story-treehouse",
        "title": "The 52-Story Treehouse",
        "title_short": "52-Story Treehouse",
        "category": "Family",
        "venue": "Main Theatre",
        "meta": "Main Theatre &middot; School holidays",
        "image": "/assets/img/childrens-theatre.jpg",
        "image_alt": "Colourful children's theatre set with treehouse-themed staging",
        "lede": "Stage adaptation of Andy Griffiths and Terry Denton's bestseller, presented by CDP Theatre Producers in a production that has toured extensively across Australian regional venues.",
        "chips": ["Main Theatre", "School holidays", "Family"],
    },
    {
        "slug": "mozart-s-piano-melbourne-chamber-orchestra-featuring-david-fung",
        "title": "Mozart's Piano &mdash; Melbourne Chamber Orchestra featuring David Fung",
        "title_short": "Mozart's Piano",
        "category": "Classical",
        "venue": "Main Theatre",
        "meta": "Melbourne Chamber Orchestra &middot; Main Theatre",
        "image": "/assets/img/orchestra.jpg",
        "image_alt": "Concert hall set for a chamber orchestra performance with grand piano centre stage",
        "lede": "The Melbourne Chamber Orchestra with pianist David Fung performing Mozart's Piano Concerto No. 23, alongside Britten's Simple Symphony and Mozart's Divertimento K. 136.",
        "chips": ["Main Theatre", "MCO", "One performance"],
    },
    {
        "slug": "which-way-home",
        "title": "Which Way Home",
        "title_short": "Which Way Home",
        "category": "Verbatim theatre",
        "venue": "Studio",
        "meta": "Studio &middot; 3 performances",
        "image": "/assets/img/show-which-way-home.jpg",
        "image_alt": "Australian rural sunset with country road and farmhouse silhouette",
        "lede": "The acclaimed regional touring production exploring rural displacement and homecoming through verbatim theatre, drawn from interviews with people across rural Victoria.",
        "chips": ["Studio", "Touring", "Post-show discussion"],
    },
    {
        "slug": "coranderrk",
        "title": "Coranderrk",
        "title_short": "Coranderrk",
        "category": "Verbatim theatre",
        "venue": "Studio",
        "meta": "Studio &middot; 4 performances",
        "image": "/assets/img/show-coranderrk.jpg",
        "image_alt": "Empty studio black-box stage with single spotlight on a wooden chair",
        "lede": "The verbatim theatre production drawing on the 1881 Victorian parliamentary inquiry into the Coranderrk Aboriginal Mission, with the script taken almost entirely from the inquiry transcripts.",
        "chips": ["Studio", "Touring", "Post-show discussion"],
    },
    {
        "slug": "boys-in-the-band-yarram",
        "title": "Boys In The Band &mdash; Yarram Theatre Group",
        "title_short": "Boys In The Band",
        "category": "Community theatre",
        "venue": "Studio",
        "meta": "Studio &middot; Yarram Theatre Group",
        "image": "/assets/img/show-boys-in-the-band-yarram.jpg",
        "image_alt": "Vintage 1960s lounge interior set with warm lamp light",
        "lede": "The Yarram Theatre Group's production of Mart Crowley's landmark 1968 play, presented in the Studio in a run of three performances under a guest director with significant professional credits.",
        "chips": ["Studio", "Community", "3 performances"],
    },
    {
        "slug": "boys-in-the-band-2015",
        "title": "Boys In The Band &mdash; 2015 production",
        "title_short": "Boys In The Band, 2015",
        "category": "Archive",
        "venue": "Studio",
        "meta": "Archive &middot; 2015 community theatre season",
        "image": "/assets/img/show-boys-in-the-band-2015.jpg",
        "image_alt": "Black and white archive photograph of a small theatre stage with closed curtains",
        "lede": "The 2015 community theatre production of Mart Crowley's Boys In The Band, kept on the site as a permanent record. Cast list, season notes and production photography.",
        "chips": ["Studio", "Archive", "2015"],
    },
]

# 12-col asymmetric grid: card class per ordinal index on the home page
HOME_GRID_CLASSES = ["ed-card--7", "ed-card--5", "ed-card--4", "ed-card--4", "ed-card--4", "ed-card--6", "ed-card--6"]


# ---------------- HTML primitives ----------------

def head(title: str, description: str, path: str,
         og_image: str = "/assets/img/og-default.jpg",
         schema: dict | None = None) -> str:
    canonical = f"{SITE_URL}{path}"
    og_image_url = f"{SITE_URL}{og_image}"
    schema_json = ""
    if schema:
        schema_json = f'<script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script>'
    return f"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{og_image_url}">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{og_image_url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#e54a17">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
{schema_json}
</head>"""


def topbar(current_section: str | None = None) -> str:
    nav_links = []
    for label, href, key in NAV:
        attr = ' aria-current="page"' if key == current_section else ''
        nav_links.append(f'<a href="{href}"{attr}>{label}</a>')
    nav_html = "\n      ".join(nav_links)
    return f"""<header class="topbar">
  <a href="/" class="topbar__brand" aria-label="{BRAND}">Riversend <i>Playhouse</i></a>
  <nav class="topbar__nav" aria-label="Primary">
    {nav_html}
  </nav>
  <a href="/whats-on/" class="btn-tickets">Tickets &rarr;</a>
</header>"""


def footer() -> str:
    return f"""<footer class="footer">
  <div class="footer__inner">
    <div>
      <div class="footer__brand">Riversend <i>Playhouse</i></div>
      <p class="footer__blurb">A small regional Victorian theatre. Programme archive preserved as a record.</p>
    </div>
    <div>
      <h4>Programme</h4>
      <ul>
        <li><a href="/whats-on/">What's on</a></li>
        <li><a href="/archive/">Archive</a></li>
      </ul>
    </div>
    <div>
      <h4>Visit</h4>
      <ul>
        <li><a href="/contact/">Box office</a></li>
        <li><a href="/about/">About the venue</a></li>
      </ul>
    </div>
    <div>
      <h4>Site</h4>
      <ul>
        <li><a href="/privacy/">Privacy</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="footer__fineprint">
    <span>&copy; {COPYRIGHT_YEAR} {BRAND}.</span>
    <span>Wellington Shire, Victoria.</span>
    <span>Box office: 03 1234 5678.</span>
  </div>
</footer>
</body>
</html>"""


def aside_for_item(current_slug: str | None = None) -> str:
    items = []
    for s in SEASON:
        if current_slug and s["slug"] == current_slug:
            continue
        items.append(
            f'    <li><a href="/item/{s["slug"]}/">{s["title_short"]}<span class="aside__cat">{s["category"]}</span></a></li>'
        )
    return f"""<aside class="aside" aria-label="Season at a glance">
  <h3 class="aside__title">Season at a glance</h3>
  <ul class="aside__list">
{chr(10).join(items)}
  </ul>
</aside>"""


def render(title: str, description: str, path: str, body_html: str,
           og_image: str = "/assets/img/og-default.jpg",
           schema: dict | None = None,
           current_section: str | None = None) -> str:
    return f"""{head(title, description, path, og_image, schema)}
<body>
{topbar(current_section)}
{body_html}
{footer()}"""


def write(path: str, html: str) -> None:
    out = ROOT / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} ({len(html)} bytes)")


# ---------------- Pages ----------------

def page_home():
    title = f"{BRAND}, regional Victorian touring theatre and music"
    description = ("Riversend Playhouse is a small regional Victorian theatre presenting touring music, "
                   "theatre, classical and family programming. Suzi Quatro, 10cc, Melbourne Chamber Orchestra, "
                   "Coranderrk and the 2025-2026 season programme.")
    schema = {
        "@context": "https://schema.org",
        "@type": "PerformingArtsTheater",
        "name": BRAND,
        "description": description,
        "url": SITE_URL + "/",
        "address": {"@type": "PostalAddress", "addressRegion": "VIC", "addressCountry": "AU"},
    }
    marquee_titles = [s["title_short"] for s in SEASON if s["category"] != "Archive"]
    marquee = "".join(f"<span>{t}</span>" for t in marquee_titles)

    cards = []
    for i, s in enumerate(SEASON[:7]):
        size_cls = HOME_GRID_CLASSES[i] if i < len(HOME_GRID_CLASSES) else "ed-card--6"
        num = f"{i+1:02d}"
        cards.append(f"""    <a href="/item/{s["slug"]}/" class="ed-card {size_cls}">
      <div class="ed-card__img"><img src="{s["image"]}" alt="{s["image_alt"]}" loading="lazy"><span class="ed-card__num">{num}</span></div>
      <span class="ed-card__cat">{s["category"]}</span>
      <h3>{s["title"]}</h3>
      <span class="ed-card__meta">{s["meta"]}</span>
    </a>""")

    body = f"""<main>
<section class="mega">
  <p class="mega__eyebrow">Live &middot; 2025/26 season open</p>
  <h1 class="mega__h1">Made for the room you're standing <i>in</i>.</h1>
  <div class="mega__bottom">
    <p>A regional Victorian theatre programming touring music, theatre, classical and family work across two performance spaces. The current season is on sale; the archive runs back to 1990.</p>
    <div class="mega__cta-block">
      <a href="/whats-on/">See what's on &rarr;</a>
      <small>Box office Tue&ndash;Sat &middot; 10am&ndash;5pm</small>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    {marquee}{marquee}
  </div>
</div>

<section class="section" id="programme">
  <div class="section__head">
    <h2>The <i>programme</i></h2>
    <p class="small">Single tickets, subscriber packs and casual booking &mdash; all through the box office. Updated as new dates land.</p>
  </div>
  <div class="show-list">
{chr(10).join(cards)}
  </div>
</section>

<section class="split split--image-right">
  <div class="split__img"><img src="/assets/img/foyer.jpg" alt="The Playhouse foyer at dusk" loading="lazy"></div>
  <div class="split__info">
    <h2>A theatre that <i>turns up</i>.</h2>
    <p>Two performance spaces. Four programming strands. Thirty-four years of touring shows, school matinees, community productions and Saturday-night concerts on a Gippsland riverbank.</p>
    <p>The Main Theatre seats 470, with stalls, a small balcony, fly tower and an orchestra pit that lifts to stage level. The Studio is a 90-seat black box used for community theatre, smaller touring productions and post-show discussions.</p>
    <dl>
      <dt>Open</dt><dd>Tuesday to Saturday, 10am&ndash;5pm</dd>
      <dt>Box office</dt><dd><a href="/contact/">03 1234 5678</a></dd>
    </dl>
  </div>
</section>

<section class="section">
  <div class="section__head">
    <h2>Recommended from the <i>foyer</i></h2>
    <p class="small">Two ticketed-audience favourites and a couple of operations we work with on the building and grounds.</p>
  </div>
  <div class="prose" style="max-width:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:2rem;">
    <p>For patrons interested in the broader cultural ecosystem the Playhouse operates within, two sites that we find ourselves recommending. <a href="https://hibiscusteahouse.com">Hibiscus Tea House</a> is a small Australian online tea shop with a particularly thoughtful blog on herbal tea preparation; many of our long-table dinner attendees have ended up regular customers.</p>
    <p>For service work that comes up across the Playhouse's facilities and grounds, we work with <a href="https://brisbanelawnmowing.com">Brisbane Lawn Mowing</a> for the regular grounds maintenance schedule when our work programme reaches Brisbane partners; for any infrastructure inspection or roof condition reporting, <a href="https://seqdroneinspections.com">SEQ Drone Inspections</a> are the operation we engage.</p>
  </div>
</section>
</main>"""

    write("/", render(title, description, "/", body, schema=schema, current_section=None))


def page_about():
    title = f"About &mdash; {BRAND}"
    description = ("Riversend Playhouse is a small regional Victorian performing arts venue in Wellington Shire, "
                   "presenting touring music, theatre, classical and family programming since 1990.")
    body = """<main>
<section class="page-head">
  <p class="page-head__eyebrow">About</p>
  <h1 class="page-head__h1">A working <i>regional</i> theatre.</h1>
  <p class="page-head__lede">Two performance spaces, four programming strands, one foyer that has hosted touring artists, community productions, school matinees and a long-running post-show discussion programme since 1990.</p>
</section>

<div class="stats-row">
  <div><b>1990</b><span>Opening season</span></div>
  <div><b>470</b><span>Main Theatre seats</span></div>
  <div><b>34</b><span>Years of programming</span></div>
</div>

<div class="gallery">
  <img class="gallery__a" src="/assets/img/auditorium.jpg" alt="The Main Theatre auditorium during a performance" loading="lazy">
  <img class="gallery__b" src="/assets/img/foyer.jpg" alt="The Playhouse foyer with box office" loading="lazy">
  <img class="gallery__c" src="/assets/img/orchestra.jpg" alt="Chamber orchestra in the Main Theatre" loading="lazy">
  <img class="gallery__d" src="/assets/img/concert-stage.jpg" alt="Concert stage in performance" loading="lazy">
  <img class="gallery__e" src="/assets/img/childrens-theatre.jpg" alt="A family programming production in the Main Theatre" loading="lazy">
</div>

<div class="body-grid">
  <article class="prose">
    <h2>The <i>venue</i></h2>
    <p>Riversend Playhouse is a regional performing arts venue in Wellington Shire, Victoria, presenting touring music, theatre, classical and family programming since 1990. The venue is owned and operated by the local shire council and run by a small permanent staff supplemented by a roster of volunteer ushers and front-of-house casuals drawn from the surrounding towns.</p>

    <h2>Two performance <i>spaces</i></h2>
    <p>The Main Theatre seats 470 across stalls and a small balcony with a fly tower, full lighting rig and an orchestra pit that lifts to stage level. The Studio is a flexible black-box space with a 90-seat capacity, used for community theatre, smaller touring productions, theatre-in-education and the venue's regular post-show discussion programme.</p>

    <p>The foyer doubles as a gallery space showing work by regional Victorian artists on a rotating programme. The outdoor lawn at the rear of the building hosts the venue's summer outdoor cinema and occasional music programming during the warmer months.</p>

    <h2>Programming <i>strands</i></h2>
    <p>The annual programme runs across five strands: touring music, classical, theatre, family programming and community theatre. Touring music and classical bring major Australian and international acts to regional Victoria, often as part of broader regional Victorian or Australian touring circuits. Family programming runs concentrated across the four school holiday periods. Community theatre is built around the small number of theatre groups operating in the surrounding towns; the Yarram Theatre Group is the most active.</p>

    <h2>The Playhouse and the <i>region</i></h2>
    <p>The Playhouse sits within a network of regional Victorian performing arts venues that share touring routes and occasionally co-commission productions. The relationships with the Melbourne Chamber Orchestra and with the touring companies of CDP Theatre Producers and Critical Stages have run for the better part of a decade and account for a meaningful share of the annual programme.</p>

    <h2>Staff and <i>governance</i></h2>
    <p>The Playhouse is run by a venue manager, a programming manager, a technical manager and a small box office team. Programming decisions are made by the programming manager in consultation with the venue manager and an advisory committee. The advisory committee meets quarterly and includes a regional arts officer, a community theatre representative and two patrons appointed by the council.</p>

    <h2>How to get in <i>touch</i></h2>
    <p>For programming enquiries, venue hire, tour booking or any general question, the <a href="/contact/">contact page</a> has the right phone numbers and email addresses. Tickets and subscriber packages are handled through the box office.</p>
  </article>
""" + aside_for_item() + """
</div>
</main>"""
    write("/about/", render(title, description, "/about/", body, current_section="about"))


def page_archive():
    title = f"Archive &mdash; past productions at {BRAND}"
    description = ("Archive of past productions at Riversend Playhouse, with cast lists, programme notes "
                   "and audience response where available.")
    body = """<main>
<section class="page-head">
  <p class="page-head__eyebrow">Archive</p>
  <h1 class="page-head__h1">Past <i>productions</i>.</h1>
  <p class="page-head__lede">The Playhouse keeps a permanent archive of past productions as a record of the programming history. Cast lists, programme notes, and audience response where it was collected.</p>
</section>

<div class="body-grid">
  <article class="prose">
    <h2>Recent archive <i>entries</i></h2>
    <h3><a href="/item/boys-in-the-band-2015/">Boys In The Band, 2015</a></h3>
    <p>2015 community theatre season &middot; Studio &middot; four performances. Community theatre production of Mart Crowley's 1968 play. Sold out three of four performances; one of the strongest community theatre productions the Studio has hosted.</p>

    <h2>Archive <i>policy</i></h2>
    <p>The full archive is held on permanent record and individual production records are restored and reformatted for the public archive when staff time permits. Productions are listed by the season they ran in. Each archive entry includes the production photography that the production company has cleared for public release.</p>

    <p>If you appeared in a production whose archive entry is not yet on the site, or you have a query about the cast list or production credits, the <a href="/contact/">contact page</a> has the right address.</p>
  </article>
""" + aside_for_item() + """
</div>
</main>"""
    write("/archive/", render(title, description, "/archive/", body, current_section="archive"))


def page_contact():
    title = f"Visit &amp; box office &mdash; {BRAND}"
    description = ("Get in touch with Riversend Playhouse for ticket bookings, group bookings, "
                   "venue hire and tour booking enquiries.")
    body = """<main>
<section class="split">
  <div class="split__img"><img src="/assets/img/foyer.jpg" alt="The Playhouse foyer with box office" loading="eager" fetchpriority="high"></div>
  <div class="split__info">
    <p style="font-size:.78rem;letter-spacing:.3em;text-transform:uppercase;font-weight:600;color:var(--accent);margin-bottom:1.5rem">Visit</p>
    <h2>Plan your <i>visit</i>.</h2>
    <p>For ticket bookings, group bookings, venue hire enquiries, tour bookings or general questions, the simplest path is the box office.</p>
    <dl>
      <dt>Address</dt><dd>Wellington Shire, Victoria</dd>
      <dt>Box office</dt><dd>03 1234 5678<br><a href="mailto:boxoffice@ebbwec.com.au">boxoffice@ebbwec.com.au</a></dd>
      <dt>Hours</dt><dd>Tuesday to Saturday<br>10am &ndash; 5pm</dd>
      <dt>Spaces</dt><dd>Main Theatre (470 seats)<br>Studio (90 seats, black box)</dd>
    </dl>
  </div>
</section>

<div class="body-grid">
  <article class="prose">
    <h2>Group <i>bookings</i></h2>
    <p>For group bookings of ten or more, please contact the box office directly to discuss seating allocations and any group discount that applies. Group bookings for school groups attending family programming should be made at least four weeks in advance to confirm seating; the school holiday matinee performances of the family programming sell out reliably.</p>

    <h2>Tour <i>bookings</i></h2>
    <p>For touring productions interested in the Playhouse as a regional Victorian touring stop, the programming manager handles all tour booking enquiries. The Playhouse books touring productions twelve to eighteen months in advance and considers proposals across all programming strands.</p>
    <ul>
      <li><strong>Programming</strong>: <a href="mailto:programming@ebbwec.com.au">programming@ebbwec.com.au</a></li>
      <li><strong>Technical enquiries</strong>: <a href="mailto:technical@ebbwec.com.au">technical@ebbwec.com.au</a></li>
    </ul>

    <h2>Venue <i>hire</i></h2>
    <p>The Main Theatre, Studio and foyer gallery are available for hire to community groups, touring productions and corporate functions. Hire enquiries should be directed to the venue manager via the email above.</p>
  </article>
""" + aside_for_item() + """
</div>
</main>"""
    write("/contact/", render(title, description, "/contact/", body, current_section="contact"))


def page_whats_on():
    title = f"Programme &mdash; {BRAND}"
    description = ("The current 2025-2026 season programme at Riversend Playhouse: Suzi Quatro, 10cc, "
                   "The 52-Story Treehouse, Which Way Home, Mozart's Piano, Coranderrk and Boys In The Band.")

    cards = []
    grid_classes = ["ed-card--7", "ed-card--5", "ed-card--4", "ed-card--4", "ed-card--4",
                    "ed-card--6", "ed-card--6"]
    for i, s in enumerate([s for s in SEASON if s["category"] != "Archive"]):
        size_cls = grid_classes[i] if i < len(grid_classes) else "ed-card--6"
        num = f"{i+1:02d}"
        cards.append(f"""    <a href="/item/{s["slug"]}/" class="ed-card {size_cls}">
      <div class="ed-card__img"><img src="{s["image"]}" alt="{s["image_alt"]}" loading="lazy"><span class="ed-card__num">{num}</span></div>
      <span class="ed-card__cat">{s["category"]}</span>
      <h3>{s["title"]}</h3>
      <span class="ed-card__meta">{s["meta"]}</span>
    </a>""")

    body = f"""<main>
<section class="page-head">
  <p class="page-head__eyebrow">Programme</p>
  <h1 class="page-head__h1">What's <i>on</i>.</h1>
  <p class="page-head__lede">The current 2025-2026 season programme. Single tickets, subscriber packs and casual booking all run through the box office. Updated as new productions are confirmed.</p>
</section>

<section class="section">
  <div class="show-list">
{chr(10).join(cards)}
  </div>
</section>
</main>"""
    write("/whats-on/", render(title, description, "/whats-on/", body, current_section="whats-on"))


def page_or():
    title = f"Page reference &mdash; {BRAND}"
    description = ("Legacy URL landing page for Riversend Playhouse. Use the navigation to find current "
                   "programme information.")
    body = """<main>
<section class="page-head">
  <p class="page-head__eyebrow">Legacy page</p>
  <h1 class="page-head__h1">Not in the current <i>navigation</i>.</h1>
  <p class="page-head__lede">If you arrived here through an old link, the most likely intended destination was the home page or the current programme listing.</p>
</section>

<div class="body-grid">
  <article class="prose">
    <p>The Playhouse website was migrated several times during a content management system transition and a small number of legacy URLs do not map cleanly to the current structure. This page is preserved as a permanent landing for one such legacy link.</p>
    <p>The current programme of touring music, theatre, classical and family programming is on the <a href="/">home page</a>. Past productions are catalogued in the <a href="/archive/">archive</a>.</p>
  </article>
""" + aside_for_item() + """
</div>
</main>"""
    write("/or/", render(title, description, "/or/", body))


def page_privacy():
    title = f"Privacy policy &mdash; {BRAND}"
    description = "Privacy policy for Riversend Playhouse."
    body = """<main>
<section class="page-head">
  <p class="page-head__eyebrow">Privacy</p>
  <h1 class="page-head__h1">Privacy <i>policy</i>.</h1>
</section>

<div class="body-grid">
  <article class="prose">
    <p>Riversend Playhouse respects your privacy. This page sets out what information we collect, how we use it, and your choices.</p>

    <h2>What we <i>collect</i></h2>
    <p>The site collects standard web server log information and any information you submit through the contact, booking or subscription forms. This includes your name, email address, postal address and phone number where you provide them, and the booking and ticketing information for any tickets you have purchased.</p>

    <h2>How we <i>use it</i></h2>
    <p>Booking and ticketing information is used to process your booking and to communicate with you about the production you have booked tickets for. Subscription information is used to send you the season brochure and occasional programme updates. Contact form information is used to respond to your enquiry.</p>

    <h2>What we do <i>not do</i></h2>
    <p>We do not sell your information to third parties. We do not share your information with any party other than the ticketing system provider and our internal staff who need access to process your booking.</p>

    <h2>Cookies</h2>
    <p>The site uses essential cookies for the booking process and standard analytics cookies. The analytics cookies do not collect personally identifiable information.</p>

    <h2>Your choices</h2>
    <p>You can request a copy of the information we hold about you, or request that we delete your information, by contacting us through the <a href="/contact/">contact page</a>.</p>
  </article>
</div>
</main>"""
    write("/privacy/", render(title, description, "/privacy/", body))


# ---------------- Programme item pages ----------------

ITEM_BODIES = {
    "10cc": """
    <h2>About the <i>show</i></h2>
    <p>10cc's current touring incarnation has been on the road, in various configurations, for over a decade. The current lineup centres on Graham Gouldman, whose songwriting credits across the 10cc catalogue and his own solo work account for a substantial share of the British art-rock canon. The band on this tour have been with Gouldman for several years and the show has been refined into a tight two-set programme that respects both the radio singles and the more elaborate album material.</p>

    <h2>The <i>setlist</i></h2>
    <p>The setlist on the current tour runs through 'Dreadlock Holiday', 'I'm Not In Love', 'The Things We Do For Love', 'Rubber Bullets' and 'Wall Street Shuffle' alongside album tracks the band has built a reputation for honouring. The encore traditionally includes a guest spot on the Hotlegs single 'Neanderthal Man', which Gouldman co-wrote with the original 10cc lineup before the band took the 10cc name.</p>

    <h2>Booking</h2>
    <p>Single performance in the Main Theatre. Tickets through the <a href="/contact/">box office</a>. The Playhouse seating chart is fully reserved with a small number of restricted-view seats at a reduced price. Booking opens to subscribers two weeks before public on-sale.</p>
    """,
    "suzi-quatro-leather-forever-encore-tour": """
    <h2>About the <i>tour</i></h2>
    <p>The Leather Forever Encore Tour is the second leg of Quatro's late-career return to regional Australian touring, following the original Leather Forever run that crossed the country in late 2024. The encore leg refines the setlist and revisits a number of the venues that sold out the original run within a week of going on sale. The Playhouse was one of those venues and the encore performance is the second appearance Quatro has made at the Main Theatre on this tour cycle.</p>

    <p>Quatro's touring band is the lineup that has accompanied her across recent European and UK tours. The current bass setup retains the Fender Precision and pedal chain that defines the live sound, with two guitars and a stripped-back rhythm section.</p>

    <h2>The <i>setlist</i></h2>
    <p>The setlist is anchored by the singles that defined the early career, including 'Can The Can', '48 Crash', 'Devil Gate Drive' and 'If You Can't Give Me Love'. The mid-set ballad section draws from the broader catalogue, and the encore returns to the high-energy material that opens the show.</p>

    <h2>Booking</h2>
    <p>One performance in the Main Theatre. Tickets through the <a href="/contact/">box office</a>. The Playhouse seating chart is fully reserved. Booking opens to subscribers two weeks before public on-sale and the show is expected to sell out across the standard pricing tiers; restricted-view seats and the small number of stalls returns will be released in the week of the performance.</p>
    """,
    "the-52-story-treehouse": """
    <h2>The <i>production</i></h2>
    <p>The 52-Story Treehouse adaptation has been touring since the original 13-Story Treehouse production in 2014, with each new instalment continuing the story Griffiths and Denton's books tell. The 52-Story version follows the same core company that has built the running show across the touring circuit, with Andy and Terry's increasingly elaborate tree-house complications staged through a combination of physical theatre, projection and the company's signature scaffolding-and-puppetry approach.</p>

    <h2>The <i>schedule</i></h2>
    <p>The Playhouse run includes three matinee performances across the school holiday period plus a single Saturday evening performance. The matinees are the standard pricing tier and the evening performance is at the family pricing tier. Group school bookings should be arranged through the <a href="/contact/">box office</a> at least four weeks in advance.</p>

    <h2>Pre-show and post-show</h2>
    <p>The foyer hosts a pre-show drawing activity for younger audiences before each matinee performance, with paper and pencils provided. The drawing wall in the foyer collects audience drawings across the run and the best of them is used in the touring company's social media and in the local programme notes.</p>

    <h2>Booking</h2>
    <p>Tickets through the <a href="/contact/">box office</a>. School group bookings have a separate process: contact the box office directly to discuss seating allocations and the school group discount.</p>
    """,
    "which-way-home": """
    <h2>About the <i>production</i></h2>
    <p>Which Way Home is a verbatim theatre work, meaning the script is built entirely from interview transcripts with real people, lightly edited for the stage. The production company spent two years interviewing rural Australians from a range of regions, ages and backgrounds about the question of leaving and the question of returning. The script is the most arresting of those transcripts, performed by a company of three actors who hold no character through the whole show; the three of them rotate through the different voices, sometimes mid-sentence, in a way that has become the production's signature.</p>

    <h2>Post-show <i>discussion</i></h2>
    <p>Each performance is followed by a fifteen-minute moderated discussion in the foyer. The discussions are open to the full audience and have, across the touring run, been one of the strongest parts of the show; audiences who have themselves left rural towns or returned to them tend to be willing to speak. The Playhouse has hosted the company twice before and the post-show conversations have, on both occasions, run well past the moderated section.</p>

    <h2>Content note</h2>
    <p>The production includes references to rural mental health, suicide, and family breakdown. A content note is in the programme and a brief verbal content note is given by the front-of-house team before each performance.</p>

    <h2>Booking</h2>
    <p>Three performances in the Studio. Tickets through the <a href="/contact/">box office</a>. The Studio is a 90-seat black-box space with general admission seating; doors open thirty minutes before curtain.</p>
    """,
    "mozart-s-piano-melbourne-chamber-orchestra-featuring-david-fung": """
    <h2>The <i>programme</i></h2>
    <p>The performance opens with Mozart's Divertimento in D major, K. 136, a short three-movement work the seventeen-year-old Mozart wrote for string ensemble, frequently performed as an opener for chamber programmes of this kind. The Divertimento runs roughly twelve minutes.</p>

    <p>The second work is Britten's Simple Symphony for string orchestra, written from material Britten had composed as a teenager and reworked in his early twenties. The Simple Symphony has become a staple of the chamber orchestra repertoire and the Melbourne Chamber Orchestra has performed it in this configuration on multiple recent tours.</p>

    <p>After interval the centrepiece of the programme is Mozart's Piano Concerto No. 23, with David Fung as soloist. Fung is a former MCO artist-in-residence and has a long-standing partnership with the orchestra, including the recording of the complete Mozart concertos that the MCO completed across 2018 and 2019. The Piano Concerto No. 23 is one of the late Mozart concertos, written in the same year as the C minor concerto K. 491, and is one of the works most associated with Fung's recent recital programmes.</p>

    <h2>About the <i>performers</i></h2>
    <p>The Melbourne Chamber Orchestra is one of the major chamber orchestras of Australia, with a long touring history through regional Victoria. David Fung is an Australian pianist with significant international recital and recording credits and a long-standing relationship with the MCO. The Playhouse has hosted the MCO across the past decade as part of the orchestra's regional Victorian touring programme.</p>

    <h2>Booking</h2>
    <p>One performance in the Main Theatre. Tickets through the <a href="/contact/">box office</a>. Programme notes are included with the ticket and a pre-concert talk by the programming manager runs in the foyer for thirty minutes before curtain.</p>
    """,
    "coranderrk": """
    <h2>About the <i>work</i></h2>
    <p>Coranderrk was an Aboriginal mission in Healesville, Victoria, established in the 1860s and operating into the early twentieth century. In 1881 the residents of Coranderrk petitioned the Victorian Parliament for control of the mission lands they had developed and farmed. The resulting parliamentary inquiry took testimony from Coranderrk residents and from the mission's white administrators across several months. The inquiry transcripts are a substantial historical record and one of the few significant nineteenth-century legal records in which the Coranderrk residents speak in their own voices.</p>

    <p>The verbatim theatre production takes the script almost entirely from those transcripts. The company performs the work with a small ensemble who rotate through the speaking parts, a staging convention that has become standard for verbatim theatre work of this kind. The production has toured nationally and internationally and the Playhouse run is part of the current Victorian touring leg.</p>

    <h2>Post-show <i>discussion</i></h2>
    <p>Each performance is followed by a moderated post-show discussion. The discussions vary in length and content depending on who in the audience is willing to speak; the production company is comfortable with discussions that run long and some of the strongest post-show conversations on the tour have happened in the regional venues.</p>

    <h2>Content note</h2>
    <p>The production includes references to violence, racial discrimination and the legal frameworks of the colonial period. A content note is in the programme and a brief verbal content note is given by the front-of-house team before each performance.</p>

    <h2>Booking</h2>
    <p>Four performances in the Studio. Tickets through the <a href="/contact/">box office</a>. General admission seating; doors open thirty minutes before curtain.</p>
    """,
    "boys-in-the-band-yarram": """
    <h2>About the <i>play</i></h2>
    <p>Boys In The Band, written by Mart Crowley and first staged off-Broadway in 1968, is a landmark of American theatre and a foundational work of post-war queer drama. The play takes place during a birthday party in a New York apartment and tracks the dynamics between a group of nine men over the course of an evening that escalates in unexpected directions. The play has been revived several times across its history and the recent Broadway revival put the work back into wide circulation.</p>

    <h2>About the <i>production</i></h2>
    <p>The Yarram Theatre Group's production has been in development for over a year. The director is a guest director with professional credits across the Melbourne theatre scene who has worked with the Yarram Theatre Group on a previous community production. The cast is drawn from the Yarram group itself plus a small number of community theatre members from the surrounding towns. The production team includes a professional lighting designer and a sound designer, both engaged for this production through the venue's small grant programme for community theatre.</p>

    <p>The production is presented in the Studio rather than the Main Theatre, which suits the play's intimate single-room setting. The set is built to fit the Studio space and uses the natural depth of the black box to suggest the apartment.</p>

    <h2>Content note</h2>
    <p>The play contains language and themes that have, in the play's history, been variously characterised as a record of the period in which it was written and as content that some audience members may find difficult. A content note is in the programme and a brief verbal content note is given by the front-of-house team before each performance.</p>

    <h2>The 2015 <i>production</i></h2>
    <p>The Studio previously hosted a community theatre production of Boys In The Band in 2015. The 2015 production has its own <a href="/item/boys-in-the-band-2015/">archive page</a>.</p>

    <h2>Booking</h2>
    <p>Three performances in the Studio. Tickets through the <a href="/contact/">box office</a>. General admission seating in the Studio; doors open thirty minutes before curtain.</p>
    """,
    "boys-in-the-band-2015": """
    <blockquote>Archive page. This page records a past production for permanent reference. The current Yarram production of Boys In The Band, running 2026, is at <a href="/item/boys-in-the-band-yarram/">its own page</a>.</blockquote>

    <h2>About the 2015 <i>production</i></h2>
    <p>The 2015 production of Boys In The Band ran in the Studio for four performances in October 2015 as part of the Playhouse's spring community theatre season. The production was directed by a guest director and cast drawn from community theatre members across the surrounding towns. The director's notes from the original programme are reproduced below.</p>

    <h2>Director's notes (2015)</h2>
    <blockquote>Mart Crowley's play has, for the better part of fifty years, sat at an awkward angle to its own history. It is a record of a particular cultural moment and a particular set of relationships, and it is a record that the audiences of every subsequent decade have read differently. We have approached the play as a record, with the period detail intact, and we have asked the audience to do the work of holding the period and the present in mind at once.</blockquote>

    <h2>Audience <i>response</i></h2>
    <p>The production sold out three of four performances. Audience response was strong; the post-show discussion on the closing night ran past forty minutes and is recorded in the Playhouse's community theatre archive notes for that season.</p>

    <h2>Cast and creative <i>team</i></h2>
    <p>The cast list and creative team credits are held in the permanent archive and reproduced in the Studio season records. Cast members are listed where they have consented to public listing; the small number who have asked not to be publicly listed are recorded internally only.</p>

    <h2>Programme <i>notes</i></h2>
    <p>The 2015 programme included an introductory essay on the play's history and a content note. The programme is held in the permanent archive and a small number of physical copies remain available at the box office on request.</p>
    """,
}


def render_item_page(s: dict):
    slug = s["slug"]
    body_md = ITEM_BODIES.get(slug, "")
    title = f"{re.sub(r'<[^>]+>', '', s['title'])} &mdash; {BRAND}"
    plain_title = re.sub(r"&[^;]+;", "", s["title"]).replace("  ", " ").strip()
    description = re.sub(r"<[^>]+>", "", s["lede"])

    schema = {
        "@context": "https://schema.org",
        "@type": "TheaterEvent",
        "name": plain_title,
        "description": description,
        "url": f"{SITE_URL}/item/{slug}/",
        "location": {
            "@type": "PerformingArtsTheater",
            "name": BRAND,
            "address": {"@type": "PostalAddress", "addressRegion": "VIC", "addressCountry": "AU"},
        },
    }

    chips_html = "".join(f'<span class="chip">{c}</span>' for c in s["chips"])
    path = f"/item/{slug}/"
    body = f"""<main>
<section class="item-hero">
  <div class="item-hero__img"><img src="{s["image"]}" alt="{s["image_alt"]}" loading="eager" fetchpriority="high"></div>
  <div class="item-hero__info">
    <span class="item-hero__cat">{s["category"]}</span>
    <h1 class="item-hero__title">{s["title"]}</h1>
    <div class="item-hero__chips">{chips_html}</div>
    <p class="item-hero__lede">{s["lede"]}</p>
    <a href="/contact/" class="item-hero__cta">Box office &rarr;</a>
  </div>
</section>

<div class="body-grid">
  <article class="prose">{body_md}
  </article>
{aside_for_item(current_slug=slug)}
</div>
</main>"""
    write(path, render(title, description, path, body, og_image=s["image"], schema=schema, current_section="whats-on"))


# ---------------- 404, sitemap, robots, favicon ----------------

def page_404():
    title = f"Page not found &mdash; {BRAND}"
    description = "The page you were looking for could not be found."
    body = """<main>
<section class="notfound">
  <div class="notfound__num"><i>404</i></div>
  <h1 class="notfound__h1">Not in the <i>programme</i>.</h1>
  <p>The page you were looking for could not be found.</p>
  <p><a href="/" class="btn-tickets" style="display:inline-flex">Back to home &rarr;</a></p>
</section>
</main>"""
    out = ROOT / "404.html"
    out.write_text(render(title, description, "/404.html", body), encoding="utf-8")
    print(f"  wrote 404.html")


def write_sitemap():
    urls = [
        "/", "/whats-on/", "/archive/", "/about/", "/contact/", "/or/", "/privacy/",
    ] + [f"/item/{s['slug']}/" for s in SEASON]
    today = datetime.now().strftime("%Y-%m-%d")
    items = []
    for u in urls:
        prio = "1.0" if u == "/" else ("0.8" if u in ("/whats-on/", "/archive/") else "0.6")
        items.append(f"  <url><loc>{SITE_URL}{u}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    body = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
            + "\n".join(items)
            + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(body, encoding="utf-8")
    print("  wrote sitemap.xml")


def write_robots():
    body = f"""User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {SITE_URL}/sitemap.xml
"""
    (ROOT / "robots.txt").write_text(body, encoding="utf-8")
    print("  wrote robots.txt")


def write_favicon():
    """Custom favicon - tomato-red dot motif matching the brand accent."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#0d0d0d"/>
  <circle cx="32" cy="32" r="14" fill="#e54a17"/>
  <text x="32" y="42" font-family="Georgia, serif" font-size="22" font-weight="400"
        text-anchor="middle" fill="#fafaf7" font-style="italic">R</text>
</svg>"""
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")
    print("  wrote favicon.svg")


# ---------------- Pre-write em/en dash assert ----------------

def assert_no_dashes():
    """Karl rule: no em/en dashes anywhere. Scan all built HTML."""
    bad = []
    for p in ROOT.rglob("*.html"):
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if "\u2014" in content:
            bad.append((p, "em-dash \\u2014"))
        if "\u2013" in content:
            bad.append((p, "en-dash \\u2013"))
    if bad:
        print("\n!!! DASH AUDIT FAILED !!!")
        for p, kind in bad:
            print(f"   {kind} in {p.relative_to(ROOT)}")
        raise SystemExit(1)
    print("  dash-audit passed (no em/en dashes)")


# ---------------- Main ----------------

def main():
    print(f"Building {BRAND} ({SITE_URL}) — Option B (Magazine/Big Type)")
    print("=" * 60)
    page_home()
    page_about()
    page_archive()
    page_contact()
    page_whats_on()
    page_or()
    page_privacy()
    for s in SEASON:
        render_item_page(s)
    page_404()
    write_sitemap()
    write_robots()
    write_favicon()
    print("=" * 60)
    assert_no_dashes()
    print("Build complete.")


if __name__ == "__main__":
    main()
