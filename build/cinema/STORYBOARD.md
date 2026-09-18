# Swarm — the home page

A service page first, with one cinematic section in the middle. The order is the
argument, not the art direction.

| # | Section | id | Job | Proof it does it |
|---|---------|----|-----|------------------|
| 1 | **Hero** | `top` | Five-second test: logo and company name, *Everything under control.*, what we do and where, quote + phone, credentials | A stranger can say what this is and what to do next without scrolling |
| 2 | **What we provide** | `services` | Three services, each with three concrete deliverables and its own quote link | No adjectives — ID checks, capacity, guest lists, advance work, reports |
| 3 | **How we work** | `how` | The objection nobody says out loud: *will the guards be the problem?* | De-escalation refreshers twice a year, licences carried, hands stay down |
| 4 | **How booking works** | `process` | Remove effort: three steps, two of them ours | Tell us the night → walk-through and written plan → shift and report |
| 5 | **One night** | `night` | The signature moment: one camera through four scenes of a Saturday | 22:15 the door · 00:40 the floor · 02:10 the exit · 06:00 the report |
| 6 | **Where we work** | `coverage` | Local relevance for search and for trust | 18 GTA municipalities, plus "ask anyway" |
| 7 | **Clients and crew** | `people` | Proof and faces — placeholders until real ones exist | Honest: "ask us for references" rather than invented quotes |
| 8 | **Answers** | `answers` | Objection handling, including price and the armed-guard question | Eight straight answers, FAQ schema |
| 9 | **Tell us the night** | `book` | The ask, restated with the least friction | Quote, phone, Instagram, TikTok, email |

Always on screen: the header (logo, phone, **Request a quote**) and, on phones, a
bottom bar with **Call dispatch** and **Request a quote**.

## The film, in one section

Four beats of one night. Each scene contains a lit opening and the next scene is
inside it, so the camera pushes through rather than cutting. It lives inside a
sticky stage with four viewport-tall steps of scroll; `scroll-snap-type: proximity`
means a flick lands on a beat but never traps the rest of the page.

Its images are deliberately quiet — desaturated, darkened, contrast eased (see
`assets.py: quiet()`), because the copy is what sells, not the photograph.

If WebGL or motion is unavailable, the four beats become four full-bleed stills with
the same words, and the rest of the page is unchanged.

## Editing

Every string is in [`content.py`](content.py). Anything marked `PLACEHOLDER`
(testimonials, crew) shows only in preview builds — fill it in and it publishes.
