# -*- coding: utf-8 -*-
"""The journal: index plus long-form posts."""
from common import (BIZ, breadcrumbs, crumb_html, cta_final, img, page, _j)

POSTS = []


def post(slug, title, h1, desc, date, read, cat, lead, body, toc=None, og="/assets/og/og-default.jpg"):
    POSTS.append(dict(slug=slug, title=title, h1=h1, desc=desc, date=date, read=read,
                      cat=cat, lead=lead, body=body, toc=toc or [], og=og))


# ---------------------------------------------------------------------------
post(
    slug="event-security-cost-toronto",
    title="What Event Security Actually Costs in Toronto (2026 Rates) | Swarm",
    h1="What event security<br>actually costs in<br>Toronto.",
    desc="Real 2026 hourly rates for licensed security guards, event staff and close protection in Toronto and the "
         "GTA — plus what a suspiciously cheap quote is hiding.",
    date="2026-09-02", read="7 min", cat="Money",
    og="/assets/og/og-default.jpg",
    lead="Everybody asks the price first and almost nobody asks what is inside it. Here are the real numbers for "
         "the GTA in 2026, what moves them, and the four things a cheap quote has quietly removed.",
    toc=[("The going rate", "rates"), ("What moves the number", "moves"),
         ("What a cheap quote is hiding", "cheap"), ("Worked examples", "examples"),
         ("Questions to ask before you sign", "ask")],
    body="""
<h2 id="rates">The going rate in the GTA, 2026</h2>
<p>Security pricing in Ontario is not a mystery, it is just badly published. Across the market this year, licensed
unarmed guards run roughly <strong>$28–$45 per hour</strong>, with Toronto sitting toward the upper half of that
because of wages, parking and the simple fact that downtown shifts start late and end later. Specialised event
work — where an officer needs to run access control, manage a barrier or handle a VIP route — sits nearer
<strong>$35–$60</strong>. Close protection is a different product entirely, generally <strong>$80–$150 per hour
per agent</strong>.</p>

<table>
<thead><tr><th>Service</th><th>GTA market range</th><th>Typical minimum</th></tr></thead>
<tbody>
<tr><td>Licensed guard, venue or door</td><td>$28–$45/hr</td><td>4 hours</td></tr>
<tr><td>Event security guard</td><td>$35–$60/hr</td><td>4 hours</td></tr>
<tr><td>Supervisor or named lead</td><td>$45–$70/hr</td><td>4 hours</td></tr>
<tr><td>Overnight site and equipment watch</td><td>$32–$50/hr</td><td>8–12 hours</td></tr>
<tr><td>Close protection agent</td><td>$80–$150/hr</td><td>8 hours</td></tr>
</tbody>
</table>

<p>Those are market ranges, not a price list. We quote from a site plan rather than a phone call, because a
300-capacity room with one exit and a 300-capacity room with six are not the same job at the same number.
What you should insist on from anyone you ask is a written figure with a named lead attached to it.</p>

<h2 id="moves">What actually moves the number</h2>
<p>Six things, roughly in order of impact.</p>
<ul>
<li><strong>How many officers, for how long.</strong> A 10-officer, two-day festival is cheaper per hour than two
officers for one six-hour shift. Fixed costs — the lead's planning time, the site visit, scheduling, reporting —
spread across more hours.</li>
<li><strong>When.</strong> Overnight, statutory holidays and New Year's Eve cost more because staff cost more. Any
agency quoting you the same rate for a Tuesday at 18:00 and December 31st at 01:00 is either mistaken or is not
paying somebody properly.</li>
<li><strong>Alcohol.</strong> Licensed premises need more officers per head and more experienced ones, because the
work is refusal, over-service management and capacity rather than standing at a rope.</li>
<li><strong>How predictable the crowd is.</strong> A ticketed corporate dinner and a free public event with the
same headcount are not the same job.</li>
<li><strong>Notice.</strong> A Thursday call for a Saturday can be covered, but the pool of people available
shrinks and the cost of covering it rises.</li>
<li><strong>Whether it recurs.</strong> Weekly bookings should be on a flat rate. If you are staffing the same two
nights every week and paying casual rates, you are paying for flexibility you are not using.</li>
</ul>

<h2 id="cheap">What a suspiciously cheap quote has removed</h2>
<p>When a quote comes in well under $28/hr in this market, something has been taken out. In our experience it is
one of four things, and all four end up on your side of the ledger.</p>

<h3>1. The licence</h3>
<p>Every security guard working in Ontario must hold a current licence under the <em>Private Security and
Investigative Services Act</em> — 40 hours of ministry-approved training, a provincial exam, a Criminal Record and
Judicial Matters Check, and emergency first aid. Licences are digital now and must be carried on shift. An
unlicensed guard is not cheap security; it is an unlicensed person on your premises who your insurer does not know
about.</p>

<h3>2. WSIB</h3>
<p>If the person working your door is not covered and gets hurt on your property, the question of who is
responsible gets interesting quickly. Ask for a WSIB clearance certificate. It takes an agency thirty seconds to
produce and tells you a great deal about the ones that hesitate.</p>

<h3>3. The insurance</h3>
<p>$5M commercial general liability is the standard a venue's landlord and insurer will expect. Some agencies
carry $1M or $2M, which is fine until it is not. Ask for the certificate before the first shift, not after the
first incident.</p>

<h3>4. Supervision and reporting</h3>
<p>The cheapest possible model is to send bodies and never look at them again. No site visit, no post orders, no
named lead, no report. It works right up until the night something happens and you discover there is no written
record of what anybody did.</p>

<blockquote><p>The cheap quote is not cheaper. It is the same price with the paperwork removed, and the paperwork
is the part you are actually buying.</p></blockquote>

<h2 id="examples">Three worked examples</h2>

<h3>A 250-capacity bar, Friday and Saturday</h3>
<p>Three officers — one on ID, one on door, one on floor — 21:00 to 03:00, both nights. That is twelve
officer-shifts of six hours. At the market rates above it lands in the low four figures per weekend, and for a
room doing that volume it is a smaller line item than your bar spill. Recurring bookings should be quoted as a
flat monthly rate so you can budget.</p>

<h3>A 300-guest wedding at a banquet hall</h3>
<p>Four suited officers from 17:00 to 01:00 — two on the entrance and gift table, two on the floor and parking
lot at the end. Thirty-two officer-hours, plus a supervisor if the guest list is complicated. Ask for the
supervisor to be priced separately so you can see what you are paying for.</p>

<h3>A one-day outdoor event, 1,500 attendees</h3>
<p>Ten officers plus a lead, 10:00 to 23:00 including set-up and clear, with overnight equipment watch. The
number of gates, whether alcohol is served and whether the site needs holding overnight move this more than the
attendee count does — which is why a quote given over the phone without a site plan is a guess.</p>

<h2 id="ask">Five questions to ask before you sign anything</h2>
<ol>
<li>What is your Ontario security agency licence number? (Not the guards' — the company's.)</li>
<li>Can I see a WSIB clearance certificate and a $5M certificate of insurance?</li>
<li>Will it be the same officers each week, and who is the named lead?</li>
<li>Do I get a written incident report, and when?</li>
<li>Do you subcontract any part of this to another agency?</li>
</ol>
<p>A good agency answers all five in one email. If any of them produce hesitation, you have learned what you needed
to learn for free.</p>
""",
)

# ---------------------------------------------------------------------------
post(
    slug="how-many-security-guards-event",
    title="How Many Security Guards Do You Need for an Event? | Swarm",
    h1="How many guards<br>does your event<br>actually need?",
    desc="A practical method for sizing event security in Ontario — ratios by event type, the positions you must "
         "cover regardless of headcount, and the mistakes that leave a gap.",
    date="2026-08-19", read="6 min", cat="Planning",
    lead="Headcount is where the conversation starts and it is the least useful number in it. Here is how a "
         "staffing plan is actually built — and why two events with 500 guests can need four officers or fourteen.",
    toc=[("Start with positions, not ratios", "positions"), ("Ratios that hold up", "ratios"),
         ("What pushes the number up", "up"), ("The four gaps we see most", "gaps"),
         ("A worked plan", "plan")],
    body="""
<h2 id="positions">Start with positions, not ratios</h2>
<p>Ontario does not publish a guard-to-guest ratio for private events, and the ones circulating online are
imported from American jurisdictions with different licensing regimes. The number that matters is not a ratio; it
is the list of positions that must be physically occupied for your site to be controlled.</p>
<p>Work through your floor plan and count the things that need a person:</p>
<ul>
<li>Every public entrance, while it is open</li>
<li>Every point where a ticket, wristband or ID is checked</li>
<li>Back of house, loading and any door that can be pushed open from inside</li>
<li>The bar or cash area, if either exists</li>
<li>Each distinct area you cannot see from another — patio, mezzanine, green room, parking</li>
<li>One roving lead who holds none of the above and can go anywhere</li>
</ul>
<p>That list is your floor. Ratios only tell you how much to add on top of it.</p>

<h2 id="ratios">Ratios that hold up in practice</h2>
<table>
<thead><tr><th>Event type</th><th>Working ratio</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Corporate, ticketed, no alcohol</td><td>1 per 150–200</td><td>Access control does most of the work</td></tr>
<tr><td>Private function with bar</td><td>1 per 100</td><td>Plus a gift-table or cash position</td></tr>
<tr><td>Wedding</td><td>1 per 75–100</td><td>Suits; departures matter as much as arrivals</td></tr>
<tr><td>Licensed venue, late night</td><td>1 per 75–100</td><td>Plus dedicated ID once a line forms</td></tr>
<tr><td>Concert or club night</td><td>1 per 50–75</td><td>Barrier and artist route are separate positions</td></tr>
<tr><td>Free public / outdoor event</td><td>1 per 75–125</td><td>Perimeter length often drives it, not headcount</td></tr>
</tbody>
</table>
<p>Use the ratio to sanity-check the position count, not to replace it. If the ratio says six and the positions say
nine, the answer is nine — you cannot leave a fire exit unwatched because the maths said so.</p>

<h2 id="up">What pushes the number up</h2>
<ul>
<li><strong>Alcohol, and how late it runs.</strong> The last ninety minutes of a licensed event generates most of
its incidents. Staffing has to be heaviest at the point people assume it can wind down.</li>
<li><strong>A crowd that arrives without tickets.</strong> If the artist has a local following, people will turn up
regardless. That is a perimeter problem, and perimeter problems are staffing problems.</li>
<li><strong>Multiple access points.</strong> Every additional open door is a full position for the whole event, not
a fraction of one.</li>
<li><strong>Cash on site.</strong> A cash bar or door take needs a position of its own and a plan for moving it.</li>
<li><strong>Anything that has happened before.</strong> A barred patron, an ongoing dispute, a previous incident at
the same event — tell your agency. It changes the plan and it is the single most useful thing you can say.</li>
</ul>

<h2 id="gaps">The four gaps we see most</h2>
<h3>Nobody owns the exit</h3>
<p>Entrances get staffed because they are visible. The exit that people use at 01:00, the one that opens onto a
side street with no lighting, gets forgotten — and that is where the event's worst five minutes usually happen.</p>
<h3>The lead is also holding a post</h3>
<p>If your supervisor is standing on the door, you do not have a supervisor. You have a fourth guard with a title.
Someone has to be free to move.</p>
<h3>Set-up and clear are unstaffed</h3>
<p>Equipment walks during load-in and load-out, not during the show. If the quote starts when doors open, it is
missing the two windows where your gear is actually exposed.</p>
<h3>No written post orders</h3>
<p>Without them, every officer improvises, and their improvisation becomes your liability. Post orders should say
what each position does, what it never does, and the exact point at which police or EMS are called rather than
discussed.</p>

<h2 id="plan">A worked plan: 600-guest ticketed event, licensed bar, two entrances</h2>
<ul>
<li>2 × entrance and ticket check (both entrances, whole event)</li>
<li>1 × ID position at the main door during the first two hours</li>
<li>2 × floor, split by area</li>
<li>1 × bar and cash</li>
<li>1 × back of house and loading</li>
<li>1 × roving lead, no fixed post</li>
<li>+2 for the final ninety minutes and the clear</li>
</ul>
<p>That is eight for most of the night, ten at the end — against a ratio that would have suggested six to eight.
The extra two are the ones that stop the night ending badly, and they are the first two a cheap quote deletes.</p>
""",
)

# ---------------------------------------------------------------------------
post(
    slug="ontario-security-guard-powers",
    title="What Security Guards Can and Cannot Do in Ontario | Swarm",
    h1="What a guard<br>may legally do<br>in Ontario.",
    desc="A plain-language guide to the powers and limits of licensed security guards in Ontario — refusals, "
         "ejections, reasonable force and lawful detention.",
    date="2026-08-05", read="8 min", cat="Law",
    lead="Most complaints about door staff come from one gap: the public does not know what a guard may do, and a "
         "surprising number of guards are hazy on it too. Here is the line, drawn clearly.",
    toc=[("The starting point", "start"), ("Refusing entry", "refuse"), ("Asking someone to leave", "eject"),
         ("Reasonable force", "force"), ("Detention and arrest", "arrest"),
         ("Searches, ID and phones", "search"), ("What gets a venue sued", "sued")],
    body="""
<p class="sub">This is general information for venue operators, not legal advice. Get your own counsel to review
your post orders.</p>

<h2 id="start">The starting point: a guard has no special powers</h2>
<p>This surprises people. A licensed security guard in Ontario does not have police powers. What they have is the
authority of the occupier — the venue — plus the same rights any member of the public has, exercised on the
occupier's behalf. That is a narrower set of tools than most patrons assume and, occasionally, than the guard
assumes.</p>
<p>Licensing under the <em>Private Security and Investigative Services Act</em> sets the training and background
standard. It does not grant authority. A uniform is not a warrant.</p>

<h2 id="refuse">Refusing entry</h2>
<p><strong>Allowed.</strong> A venue may refuse admission, and a guard may communicate that refusal. You do not
need to give a reason, and the refusal does not have to be fair in the sense of being deserved.</p>
<p><strong>Not allowed.</strong> Refusal on a ground protected by the <em>Human Rights Code</em> — race, ancestry,
place of origin, colour, ethnic origin, citizenship, creed, sex, sexual orientation, gender identity, gender
expression, age, marital status, family status or disability. This is where door policy most often goes wrong, and
where a complaint has real teeth.</p>
<p>Practically: log every refusal with a time and a reason. A refusal log that shows consistent, stated,
non-discriminatory grounds is the best evidence a venue can have.</p>

<h2 id="eject">Asking someone to leave</h2>
<p>Under Ontario's <em>Trespass to Property Act</em>, an occupier can withdraw permission to be on the premises at
any time. Once that is communicated, the person must leave within a reasonable time. If they do not, they are
trespassing.</p>
<p>The communication matters. "You need to leave now" said clearly to the person, ideally with a second officer
present, is the moment the clock starts. Muttered, or shouted across a room, it is contestable later.</p>

<h2 id="force">Reasonable force</h2>
<p>A guard may use force that is <strong>reasonable in the circumstances</strong> to remove a trespasser. Every
word there is doing work.</p>
<ul>
<li>Force is a last step, after the person has been asked and given the chance to go.</li>
<li>It must be proportionate to the resistance, and no more.</li>
<li>It stops the instant the person is compliant or outside. Force applied to someone who has stopped resisting is
assault, and it is the single most common way a guard and a venue both end up in court.</li>
<li>Strikes, chokes and anything applied to the neck are not removal techniques. There is no circumstance at a bar
door where they are the reasonable option.</li>
</ul>
<p>This is why de-escalation training is not a soft skill. It is the part of the job that keeps the other part from
happening.</p>

<h2 id="arrest">Detention and citizen's arrest</h2>
<p>A guard may arrest someone found committing an indictable offence on the property, under the <em>Criminal
Code</em> citizen's arrest provisions. In practice this is a narrow and risky power, and it comes with hard
obligations: the person must be handed to police as soon as reasonably practicable, and the force used must be
reasonable.</p>
<p><strong>What a guard may not do:</strong> detain someone to "teach them a lesson", hold a person until they pay
a bill, detain over a suspected but unwitnessed offence, or hold somebody simply because a manager wants them
held. Unlawful detention is forcible confinement, and it does not stop being that because the person was being
difficult.</p>
<p>Our standing rule is simple: if the situation calls for an arrest, it calls for police. Guards remove people,
police arrest them.</p>

<h2 id="search">Searches, ID and phones</h2>
<ul>
<li><strong>Searches</strong> require consent, and consent can be a condition of entry — "bags are searched at this
door" is fine. What is not fine is searching someone who has refused, or continuing after consent is withdrawn.</li>
<li><strong>ID</strong> may be required as a condition of entry to a licensed premises, and a guard may examine it.
A guard may not confiscate it. Suspected fraudulent ID is a police matter; seizing someone's driver's licence and
keeping it is not lawful.</li>
<li><strong>Phones and filming.</strong> A patron filming in a public-facing venue is generally allowed to. A guard
may not seize a phone, demand deletion, or use the filming as a reason to escalate. Assume everything is being
recorded and behave accordingly — that is good practice regardless of the law.</li>
</ul>

<h2 id="sued">The four things that actually get a venue sued</h2>
<ol>
<li><strong>Force that continued too long.</strong> Almost never the takedown; almost always the thirty seconds
after it.</li>
<li><strong>An ejection that became a public humiliation.</strong> Walk people out, do not perform at them. The
ones that go viral are the ones with an audience.</li>
<li><strong>A refusal with no stated reason and a protected-ground pattern.</strong> Even where each individual
refusal was defensible, the pattern is the case.</li>
<li><strong>No written record.</strong> Eighteen months later, memory is worthless and the report is everything. A
venue with a contemporaneous incident report is in a completely different position from one without.</li>
</ol>
<blockquote><p>The best-run doors in this city are boring. Nothing is performed, nobody is made an example of, and
the paperwork exists.</p></blockquote>
""",
)

# ---------------------------------------------------------------------------
post(
    slug="hiring-door-staff-questions",
    title="9 Questions to Ask Before Hiring Door Staff | Swarm Protective Services",
    h1="Nine questions<br>a real agency<br>answers instantly.",
    desc="A checklist for bar and nightclub owners hiring door staff in Ontario — the questions that separate a "
         "licensed agency from a phone number with a van.",
    date="2026-07-22", read="6 min", cat="Hiring",
    lead="Every one of these can be answered in a single email by an agency that has its house in order. Send them "
         "all nine at once and see what comes back — and how fast.",
    body="""
<h2>1. What is your Ontario security agency licence number?</h2>
<p>Not the guards' licences — the company's. A business cannot lawfully supply security guards in Ontario without
an agency licence, and plenty of operations in this city are effectively brokers with no licence of their own.
Ask for the number, then check it. If the answer is vague, stop there.</p>

<h2>2. Will it be the same officers every week?</h2>
<p>The answer separates two business models. Agencies that staff from a pool will tell you "we guarantee trained
officers", which is not the same thing. You want names, and you want the same names, because a guard who knows
your regulars is a completely different asset from one who does not.</p>

<h2>3. Who is my named lead, and can I have their mobile number?</h2>
<p>A phone number for a person beats a dispatch line for an operator. When a situation is developing at 23:40 you
do not want to explain your venue's layout to somebody who has never been in it.</p>

<h2>4. Can I see a $5M certificate of insurance and a WSIB clearance certificate?</h2>
<p>Both should arrive as attachments within the hour. Your landlord, your insurer and in some cases your licence
conditions will want them anyway. An agency that has to "look into that" is telling you something.</p>

<h2>5. Do you subcontract?</h2>
<p>If the answer is yes, ask who to and whether those officers are covered by the same insurance. Subcontracting is
how a client ends up with an unvetted stranger at their door and an unanswerable question about liability when
something happens.</p>

<h2>6. What do your post orders look like?</h2>
<p>Ask to see a sample. Post orders should specify each position, what that officer does, what they explicitly do
not do, the escalation path, and the point at which police or EMS are called. If an agency does not write post
orders, every officer is improvising your liability.</p>

<h2>7. When do I get the incident report?</h2>
<p>The correct answer is "before we leave your building". Not next day, not on request. A report written the
following afternoon is a reconstruction; a report written at 03:05 is evidence. Ask for a redacted sample so you
can see the standard.</p>

<h2>8. What training do your officers have beyond the licence?</h2>
<p>The Ontario licence requires 40 hours of ministry-approved training, a provincial exam, a Criminal Record and
Judicial Matters Check and emergency first aid. That is the floor. Ask what sits on top: de-escalation refreshers,
use-of-force refreshers, naloxone, Standard First Aid and CPR-C, and how often each is renewed.</p>

<h2>9. What would make you turn down a job?</h2>
<p>This is the question that tells you the most and the one nobody expects. An agency with standards has a ready
answer — unlawful work, intimidation dressed up as security, clients who want presence in order to start something.
An agency that has never considered the question will say something like "we're pretty flexible", which is exactly
what you do not want at your door.</p>

<blockquote><p>The nine answers matter less than how long they take. A serious agency has all of this in a folder
and sends it the same day.</p></blockquote>

<h2>What to do with the answers</h2>
<p>Put them side by side. You will usually find that the cheapest quote is missing three or four of the underlying
items entirely — which means it is not the cheapest quote for the same thing, it is a quote for a different and
much thinner thing.</p>
<p>Then do one more step that almost nobody does: ask for a walk-through before you commit. Twenty minutes in your
room tells you more about how an agency thinks than any document. Watch whether they look at your exits, ask about
your regulars, and notice the corner your cameras do not cover.</p>
""",
)

# ---------------------------------------------------------------------------
post(
    slug="armed-bodyguards-canada-legal",
    title="Can You Hire an Armed Bodyguard in Canada? The Honest Answer | Swarm",
    h1="Armed bodyguards<br>in Canada: what<br>is actually legal.",
    desc="The straight answer on armed private security and bodyguards in Ontario — what an Authorization to Carry "
         "covers, what it does not, and what to do if your risk is genuinely serious.",
    date="2026-07-08", read="5 min", cat="Law",
    lead="We get this call most weeks and the answer disappoints people. It is still better than the alternative, "
         "which is hiring somebody who was willing to tell you what you wanted to hear.",
    toc=[("The short answer", "short"), ("What an ATC actually covers", "atc"),
         ("Why firms advertise it anyway", "why"), ("What actually protects a person here", "works"),
         ("If your risk is serious", "serious")],
    body="""
<h2 id="short">The short answer</h2>
<p><strong>You cannot hire an armed bodyguard in Canada.</strong> Not in Ontario, not anywhere in the country, and
not by paying more. Carrying a restricted firearm requires a federal Authorization to Carry issued under the
<em>Firearms Act</em>, and personal protection work is not one of the purposes it is issued for.</p>

<h2 id="atc">What an Authorization to Carry actually covers</h2>
<p>The <em>Authorizations to Carry Restricted Firearms and Certain Handguns Regulations</em> contemplate two
narrow situations. The one that matters commercially is this: a person whose lawful profession involves the
handling, transportation or protection of cash, negotiable instruments or other goods of substantial value, where
a firearm is required to protect life during that activity.</p>
<p>That is armoured car and high-value transport work. It is why you see armed officers moving cash from a bank and
never see one standing behind a CEO.</p>
<p>The second situation — protection of life where police protection is inadequate — is issued so rarely that it is
not a service anyone can sell you. It is not a product; it is an exceptional individual authorization.</p>
<p>Where an authorization does apply, there are obligations on the agency too: under Ontario's <em>Private Security
and Investigative Services Act</em>, the Ministry must be notified in writing within five days of an authorization
being issued to a guard.</p>

<h2 id="why">So why do firms advertise armed protection?</h2>
<p>Three reasons, none of them good for you.</p>
<ul>
<li><strong>They are describing US capability.</strong> Some international firms run armed details in jurisdictions
where it is lawful and do not carve Canada out of the brochure.</li>
<li><strong>They mean "armed-capable" and have not said so.</strong> Meaning they can staff cash-in-transit work
under an ATC, which is true and is a completely different service from protecting you at an event.</li>
<li><strong>They are telling you what closes the sale.</strong> This is the common one, and it is the reason to walk
away. A firm that will misrepresent Canadian firearms law to win a booking will misrepresent other things.</li>
</ul>

<h2 id="works">What actually protects a person in this country</h2>
<p>Nothing about the above means protection work here is weak. It means it is planning-led rather than
equipment-led, which is how good close protection works everywhere anyway.</p>
<ul>
<li><strong>Advance work.</strong> Venues and routes walked before you arrive. Most risk is removed at this stage,
by someone with a clipboard, days before anything could happen.</li>
<li><strong>Positioning.</strong> An agent standing in the right place ends an approach before it becomes one.</li>
<li><strong>Vehicle discipline.</strong> Arrivals and departures are where a principal is most exposed. Almost every
serious incident happens within ten metres of a car.</li>
<li><strong>Presence.</strong> Two large, calm, visibly professional agents change the arithmetic for anyone
considering an approach. This is not a consolation prize — it is the mechanism.</li>
<li><strong>Documentation.</strong> Logging approaches, repeat faces and repeat plates is what turns a vague fear
into something police can act on.</li>
</ul>

<h2 id="serious">If your risk is genuinely serious</h2>
<p>Then the honest advice is that private security is one part of the answer and not the first part. Report it.
Build a documented record of incidents with dates, times, screenshots and witnesses. Speak to a lawyer about a
restraining or peace-bond application. Change what is predictable about your routine. And put coverage in place
while all of that is happening — we will place a detail within 24 hours and run the assessment in parallel rather
than leaving someone uncovered while paperwork is written.</p>
<p>What we will not do is sell you a firearm-shaped fantasy. <a href="../index.html#high-risk">Our high-risk
section</a> sets out exactly what we can and cannot lawfully provide.</p>
""",
)

# ---------------------------------------------------------------------------
post(
    slug="incident-report-that-saves-a-licence",
    title="The Incident Report That Saves Your Liquor Licence | Swarm",
    h1="The document<br>that saves you<br>eighteen months later.",
    desc="What belongs in a security incident report, why it must be written the same night, and how a venue's "
         "records decide the outcome of a claim or an AGCO review.",
    date="2026-06-24", read="6 min", cat="Operations",
    lead="Nobody hires a security agency because of its paperwork. It is, reliably, the thing that matters most "
         "once something has actually happened.",
    toc=[("Why the same night", "night"), ("What belongs in it", "what"),
         ("What must never be in it", "never"), ("The refusal log", "refusals"),
         ("A template you can steal", "template")],
    body="""
<h2 id="night">Why it has to be written the same night</h2>
<p>A report written before the crew leaves is a contemporaneous record. A report written the next afternoon is a
reconstruction, and any competent lawyer will treat it as one.</p>
<p>The practical difference is detail. At 03:05 the officer remembers the exact words that were said, which hand
the glass was in, and that the manager was standing by the till. By Sunday lunchtime that has collapsed into "he
was being aggressive so we walked him out" — which is not evidence of anything.</p>
<p>Limitation periods in Ontario mean a claim can land two years later. An AGCO review can look back further. The
report is the only thing that will still be accurate then.</p>

<h2 id="what">What belongs in it</h2>
<ul>
<li><strong>Date, venue, shift times, and every officer on duty by name and licence number.</strong></li>
<li><strong>Head count at peak</strong> against your licensed occupancy.</li>
<li><strong>Every refusal:</strong> time, stated reason, whether ID was involved.</li>
<li><strong>Every ejection:</strong> time, what prompted it, what was said, who spoke, whether force was used, what
kind, for how long, and how it ended.</li>
<li><strong>First aid:</strong> what was administered, by whom, whether naloxone was used, whether EMS attended and
when they were called.</li>
<li><strong>Police attendance:</strong> time called, time attended, officer badge numbers, incident number.</li>
<li><strong>Anything that nearly happened.</strong> The near miss is the most useful line in the whole document,
because it is the one that tells you what to change next week.</li>
<li><strong>Witnesses,</strong> including your own staff, by name.</li>
</ul>
<p>Times should be specific. "Around midnight" is worth nothing. "00:14" is worth a great deal, particularly when it
matches your CCTV timestamp.</p>

<h2 id="never">What must never be in it</h2>
<ul>
<li><strong>Opinions about character.</strong> "Regular troublemaker" is an invitation for someone to argue the
report is biased. Record behaviour, not verdicts.</li>
<li><strong>Medical conclusions.</strong> An officer can write "unresponsive, breathing, naloxone administered at
01:22". An officer cannot write "overdose".</li>
<li><strong>Legal conclusions.</strong> Not "he assaulted her" — "she stated that he had struck her; I observed
redness to her left cheek".</li>
<li><strong>Anything filled in later without marking it.</strong> If something is added, it is dated and initialled
as an addendum. A silently edited report is worse than no report.</li>
<li><strong>Personal information you do not need.</strong> Record what the incident requires, not everything you
could have written down.</li>
</ul>

<h2 id="refusals">The refusal log is the quiet hero</h2>
<p>If a human rights complaint is ever made about your door, the question will be whether there is a pattern. A
consistent log — time, stated reason, no protected grounds — is the strongest answer available, and it is built
one line at a time on nights when nothing is happening.</p>
<p>It also tells you things. Three refusals a night for the same reason means your door policy is unclear or your
signage is wrong, and that is a cheap fix you would otherwise never have noticed.</p>

<h2 id="template">A template you can use tonight</h2>
<table>
<thead><tr><th>Field</th><th>Example entry</th></tr></thead>
<tbody>
<tr><td>Date / venue / shift</td><td>Sat 14 Sep 2026 · [Venue] · 20:45–03:10</td></tr>
<tr><td>Officers on duty</td><td>Name, licence no., post</td></tr>
<tr><td>Peak count / capacity</td><td>268 / 300 at 23:50</td></tr>
<tr><td>Refusals</td><td>21:40 — intoxication, entry refused, left without incident</td></tr>
<tr><td>Incident time</td><td>01:14</td></tr>
<tr><td>What was observed</td><td>Factual, first person, in order</td></tr>
<tr><td>Action taken</td><td>Who did what, in what order, ending with the outcome</td></tr>
<tr><td>Force used</td><td>Type, duration, by whom, when it stopped</td></tr>
<tr><td>Medical / EMS</td><td>Called 01:19, attended 01:27</td></tr>
<tr><td>Police</td><td>Called, attended, badge, incident number</td></tr>
<tr><td>Witnesses</td><td>Names, roles, contact where given</td></tr>
<tr><td>Near misses</td><td>Anything that could have gone the other way</td></tr>
<tr><td>Signed / time filed</td><td>Lead officer, 03:05</td></tr>
</tbody>
</table>
<p>Every shift we run ends with this in your inbox before the crew is in the car. It is not a value-add and it is
not an upsell. It is the job.</p>
""",
)


# ---------------------------------------------------------------------------
def _fmt_date(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%d %B %Y").lstrip("0")


def post_page(p):
    toc = ""
    if p["toc"]:
        items = "".join('<li><a href="#%s">%s</a></li>' % (a, t) for t, a in p["toc"])
        toc = '<nav class="toc" aria-label="On this page"><h4>On this page</h4><ol>%s</ol></nav>' % items

    others = [q for q in POSTS if q["slug"] != p["slug"]][:3]
    more = "".join(
        '<article class="post"><span class="post__meta">%s</span>'
        '<h3><a href="/journal/%s.html">%s</a></h3><p>%s</p>'
        '<span class="post__read">%s read</span></article>'
        % (q["cat"], q["slug"], q["h1"].replace("<br>", " "), q["desc"], q["read"]) for q in others)

    body = """<section class="phero">
<div class="wrap">
{cr}
<p class="hero__kicker">{cat} · {date} · {read} read</p>
<h1>{h1}</h1>
</div>
</section>

<section>
<div class="wrap">
<div class="rail rail--wide">
<div class="rail__label">Field notes
<span>Written for venue owners, event managers and anyone who has to make a staffing decision this week.</span>
<span style="margin-top:18px"><a class="tlink" href="../index.html#quote"><span>Get a quote</span></a></span></div>
<article class="article__body">
<p class="article__lead">{lead}</p>
{toc}
{body}
<hr style="margin:3em 0">
<p class="sub">Swarm Protective Services staffs licensed venues, events and protection details across the Greater
Toronto Area. Dispatch is answered 24 hours on <a href="tel:{tel}">{phone}</a>.</p>
</article>
</div>
</div>
</section>

<section class="alt">
<div class="wrap">
<h2>More from the journal</h2>
<div class="posts" style="margin-top:34px">{more}</div>
</div>
</section>

{cta}""".format(cr=crumb_html([("Home", "../index.html"), ("Journal", "index.html"),
                               (p["h1"].replace("<br>", " "), "/journal/%s.html" % p["slug"])]),
                cat=p["cat"], date=_fmt_date(p["date"]), read=p["read"], h1=p["h1"],
                lead=p["lead"], toc=toc, body=p["body"], more=more,
                tel=BIZ["phone_tel"], phone=BIZ["phone_ui"],
                cta=cta_final(1, "Need this handled rather than read about?",
                              "Tell us the night and we will send a number and a named lead, usually the same day."))

    schema = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"BlogPosting",'
              '"headline":%s,"description":%s,"datePublished":"%s","dateModified":"%s",'
              '"author":{"@type":"Organization","name":%s,"url":"%s/"},'
              '"publisher":{"@id":"%s/#org"},'
              '"mainEntityOfPage":{"@type":"WebPage","@id":"%s/journal/%s.html"},'
              '"image":"%s%s","articleSection":%s,"inLanguage":"en-CA"}</script>'
              % (_j(p["h1"].replace("<br>", " ")), _j(p["desc"]), p["date"], p["date"],
                 _j(BIZ["name"]), BIZ["base"], BIZ["base"], BIZ["base"], p["slug"],
                 BIZ["base"], p["og"], _j(p["cat"])))

    return page(path="/journal/%s.html" % p["slug"], title=p["title"], desc=p["desc"],
                body=body, depth=1, og=p["og"], ogtype="article",
                ogtitle=p["h1"].replace("<br>", " "),
                schema=schema + breadcrumbs([("Home", "/"), ("Journal", "/journal/"),
                                             (p["h1"].replace("<br>", " "),
                                              "/journal/%s.html" % p["slug"])]))


def index_page():
    cards = "".join(
        '<article class="post"><span class="post__meta">%s · %s</span>'
        '<h3><a href="/journal/%s.html">%s</a></h3><p>%s</p>'
        '<span class="post__read">%s read</span></article>'
        % (p["cat"], _fmt_date(p["date"]), p["slug"], p["h1"].replace("<br>", " "), p["desc"], p["read"])
        for p in POSTS)

    body = """<section class="phero">
<div class="phero__media">{im}</div>
<div class="wrap">
{cr}
<p class="hero__kicker">Journal</p>
<h1>Field notes.</h1>
<p class="lede">What we have learned running doors, events and protection details in this city — written for the
people who have to make the staffing decision, not for search engines.</p>
</div>
</section>

<section>
<div class="wrap">
<div class="posts">{cards}</div>
</div>
</section>

{cta}""".format(im=img("crew-hall", [640, 900, 1200, 1600], "100vw",
                       "Swarm crew on shift in Toronto", ratio=16 / 10, depth=1),
                cr=crumb_html([("Home", "../index.html"), ("Journal", "index.html")]),
                cards=cards,
                cta=cta_final(1, "Stop reading. Start covering.",
                              "Tell us the date, the venue and the headcount. Most quotes go out the same day."))

    return page(path="/journal/", depth=1,
                title="Journal — Security Field Notes for Toronto Venues | Swarm",
                desc="Practical writing on event security costs, guard ratios, Ontario security law, incident "
                     "reporting and hiring door staff — from a working GTA security agency.",
                og="/assets/og/og-default.jpg",
                body=body,
                schema=breadcrumbs([("Home", "/"), ("Journal", "/journal/")]))


def pages():
    out = {"journal/index.html": index_page()}
    for p in POSTS:
        out["journal/%s.html" % p["slug"]] = post_page(p)
    return out
