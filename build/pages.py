# -*- coding: utf-8 -*-
"""The two pages that cannot live on the single page: privacy and 404."""
from common import BIZ, faq_html, faq_schema, page, plain
from home import FAQS

PRIVACY = page(
    path="/privacy.html", depth=0,
    title="Privacy — Swarm Protective Services",
    desc="How Swarm Protective Services handles enquiry data, incident reports and site "
         "records under Canadian privacy law, what we keep and for how long.",
    og="/assets/og/og-default.jpg",
    body="""<section class="phero">
<div class="wrap">
<div class="crumbs"><a href="index.html">Home</a><i>/</i><span>Privacy</span></div>
<p class="eyebrow">Policy</p>
<h1>Privacy.</h1>
<p class="lede">Short version: we collect what we need to quote and staff your job, we keep
incident records because the law and your insurer require it, and we sell nothing to anyone.</p>
</div>
</section>

<section>
<div class="wrap">
<div class="article__body">
<h2>What we collect</h2>
<p>From the quote form: your name, phone number, email address, the service you asked about, the
date, the location and anything you typed into the notes field. From a booking: billing details,
venue contact details and the operational information needed to write post orders.</p>
<p>On shift, our officers record incident information — times, descriptions, actions taken and
who attended. Where a venue operates CCTV, that footage belongs to the venue, not to us.</p>

<h2>Why we collect it</h2>
<p>To quote your job, staff it, invoice it, and to meet our obligations under Ontario's
<em>Private Security and Investigative Services Act</em> and our insurer's requirements. Incident
records also protect you: they are the document that answers a claim months later.</p>

<h2>What we never do</h2>
<p>We do not sell, rent or trade personal information. We do not add enquiry contacts to
marketing lists without being asked. We do not share incident details with anyone other than
you, lawful requests from affected parties, police, or our insurer where a claim is made.</p>

<h2>How long we keep it</h2>
<p>Enquiries that do not become bookings are deleted within twelve months. Booking, invoicing
and incident records are retained for seven years, which is what our insurer and Ontario
limitation periods require.</p>

<h2>Your rights</h2>
<p>Under PIPEDA you may ask what we hold about you, ask for corrections, and ask us to delete
anything we are not required to keep. Email <a href="mailto:{email}">{email}</a> and we will
respond within thirty days.</p>

<h2>This website</h2>
<p>This site sets no advertising or tracking cookies. Fonts are served by Google Fonts, which
receives the request as part of loading the page. The quote form is submitted directly to us.</p>

<h2>Contact</h2>
<p>{name}, {city}, Ontario. <a href="mailto:{email}">{email}</a> ·
<a href="tel:{tel}">{phone}</a>. Ontario security agency licence {lic}.</p>
<p class="sub">Last updated September 2026. This is a plain-language summary, not legal advice;
have your own counsel review it before launch.</p>
</div>
</div>
</section>""".format(email=BIZ["email"], name=BIZ["name"], city=BIZ["city"],
                    tel=BIZ["phone_tel"], phone=BIZ["phone_ui"], lic=BIZ["licence"]),
)

NOT_FOUND = page(
    path="/404.html", depth=0, noindex=True,
    title="Not found — Swarm Protective Services",
    desc="That page does not exist. Licensed door staff, event security and close protection "
         "across the Greater Toronto Area — dispatch answered 24 hours.",
    og="/assets/og/og-default.jpg",
    body="""<section class="phero" style="min-height:62svh;display:flex;align-items:center;border:0">
<div class="wrap">
<p class="eyebrow">404</p>
<h1>Nothing here.</h1>
<p class="lede">Usually a good sign. Not this time — the page you asked for does not exist.</p>
<div class="hero__cta">
<a class="btn" href="index.html"><span>Back to the front</span></a>
<a class="btn btn--ghost" href="index.html#contact"><span>Request a quote</span></a>
</div>
</div>
</section>""",
)

ANSWERS = page(
    path="/answers.html", depth=0,
    title="Security Questions Answered — Swarm Protective Services",
    desc="Straight answers about hiring security in Toronto and the GTA: licensing, armed "
         "guards, how many officers an event needs, response times and what happens on the night.",
    og="/assets/og/og-default.jpg",
    schema=faq_schema([(q, plain(a)) for q, a in FAQS]),
    body="""<section class="phero">
<div class="wrap">
<div class="crumbs"><a href="index.html">Home</a><i>/</i><span>Answers</span></div>
<p class="eyebrow">Answers</p>
<h1>What people ask before they book.</h1>
<p class="lede">If yours is not here, call {phone} or <a href="index.html#contact">send the date and the place</a>.</p>
</div>
</section>
<section>
<div class="wrap">{faq}</div>
</section>""".format(phone=BIZ["phone_ui"], faq=faq_html(FAQS)),
)

PAGES = {
    "privacy.html": PRIVACY,
    "404.html": NOT_FOUND,
    "answers.html": ANSWERS,
}
