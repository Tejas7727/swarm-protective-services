/* Swarm — "One Night". Scroll is the clock.
   One RAF: GSAP's ticker drives Lenis, Lenis feeds ScrollTrigger.
   Every scene is a pinned, scrubbed timeline; every gap between pins carries its own cut. */
(() => {
  'use strict';
  const root = document.documentElement;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  let reduce = root.classList.contains('reduced');
  let lenis = null;
  const scenes = {};   // declared first: begin() can run synchronously when images are cached

  /* ------------------------------------------------------------------ basics */
  $$('[data-yr]').forEach((el) => { el.textContent = new Date().getFullYear(); });

  /* ------------------------------------------------------------ quote dialog */
  const dialog = $('#quote');
  const openQuote = () => {
    if (!dialog || dialog.open) return;
    closeMenu();
    lenis && lenis.stop();
    dialog.showModal();
    setTimeout(() => $('input', dialog)?.focus(), 60);
  };
  dialog?.addEventListener('close', () => {
    lenis && lenis.start();
    if (location.hash === '#quote') history.replaceState(null, '', location.pathname + location.search);
  });
  dialog?.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
  $('[data-quote-close]')?.addEventListener('click', () => dialog.close());
  $$('[data-quote]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); openQuote(); }));

  const form = $('[data-form]');
  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (form.querySelector('[name="company"]').value) return;
    const endpoint = form.getAttribute('data-endpoint');
    const done = () => { form.classList.add('sent'); };
    if (!endpoint) return done();
    fetch(endpoint, { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then((r) => { if (!r.ok) throw new Error(r.status); done(); })
      .catch(() => { const err = $('[data-senderr]', form); if (err) err.hidden = false; });
  });

  /* -------------------------------------------------------------------- menu */
  const menu = $('#menu');
  const menuBtn = $('[data-menu]');
  function closeMenu() {
    if (!menu?.classList.contains('open')) return;
    menu.classList.remove('open');
    menuBtn?.setAttribute('aria-expanded', 'false');
    lenis && lenis.start();
  }
  menuBtn?.addEventListener('click', () => {
    menu.classList.add('open');
    menuBtn.setAttribute('aria-expanded', 'true');
    lenis && lenis.stop();
    $('a', menu)?.focus();
  });
  $('[data-menu-close]')?.addEventListener('click', closeMenu);
  addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

  /* ------------------------------------------------------------ the swarm */
  function swarm(canvas) {
    const pts = window.BEE_POINTS || [];
    const n = pts.length / 3;
    const ctx = canvas.getContext('2d');
    const start = new Float32Array(n * 2);
    const delay = new Float32Array(n);
    let seed = 7;
    const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    for (let i = 0; i < n; i++) {
      const a = rnd() * Math.PI * 2;
      const r = 0.55 + rnd() * 0.9;
      start[i * 2] = Math.cos(a) * r;
      start[i * 2 + 1] = Math.sin(a) * r * 0.75;
      delay[i] = rnd() * 0.32;
    }
    let w = 0, h = 0, dpr = 1, p = 0, raf = 0;
    const resize = () => {
      dpr = Math.min(devicePixelRatio || 1, 1.5);
      const r = canvas.getBoundingClientRect();
      w = r.width; h = r.height;
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      draw();
    };
    const draw = () => {
      raf = 0;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, w, h);
      const size = Math.min(h * 0.46, w * 0.62);
      const cx = w / 2, cy = h * 0.4;
      const spread = Math.max(w, h) * 0.75;
      const dot = Math.max(1.2, size / 170);
      for (const colour of [0, 1]) {
        ctx.fillStyle = colour ? '#E7E4D3' : '#D6B274';
        ctx.beginPath();
        for (let i = 0; i < n; i++) {
          if (pts[i * 3 + 2] !== colour) continue;
          const t = Math.min(1, Math.max(0, (p - delay[i]) / 0.62));
          const e = 1 - Math.pow(1 - t, 3);
          const tx = pts[i * 3] * size, ty = pts[i * 3 + 1] * size;
          const sx = start[i * 2] * spread, sy = start[i * 2 + 1] * spread;
          let x = sx + (tx - sx) * e, y = sy + (ty - sy) * e;
          const spin = (1 - e) * 2.1;
          const c = Math.cos(spin), s = Math.sin(spin);
          const rx = x * c - y * s, ry = x * s + y * c;
          ctx.rect(cx + rx, cy + ry, dot, dot);
        }
        ctx.globalAlpha = 0.35 + 0.65 * Math.min(1, p * 1.4);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      canvas.dataset.frame = String(Math.round(p * 200));
    };
    addEventListener('resize', resize);
    resize();
    return { set(v) { p = v; if (!raf) raf = requestAnimationFrame(draw); } };
  }

  /* --------------------------------------------------- preload, then begin */
  const pre = $('[data-pre]');
  const prePath = pre && $('path', pre);
  const pct = pre && $('.pct', pre);
  const loads = $$('img[data-load]');
  let loaded = 0, started = false;
  const progress = () => {
    const pc = loads.length ? loaded / loads.length : 1;
    if (prePath) prePath.style.strokeDashoffset = String(1 - pc);
    if (pct) pct.textContent = `LOADING ${Math.round(pc * 100)}%`;
    if (pc >= 1) begin();
  };
  loads.forEach((img) => {
    const ok = () => { loaded++; progress(); };
    if (img.complete && img.naturalWidth) ok();
    else { img.addEventListener('load', ok, { once: true }); img.addEventListener('error', ok, { once: true }); }
  });
  progress();
  setTimeout(begin, 5000);

  function begin() {
    if (started) return;
    started = true;
    if (!window.gsap || !window.ScrollTrigger || !window.Lenis) { reduce = true; root.classList.add('reduced'); }
    if (reduce) {
      pre?.classList.add('done');
      const c = $('[data-swarm]');
      if (c) c.style.display = 'none';
      const hdr = $('.hdr');
      const tone = () => {
        const hit = document.elementFromPoint(innerWidth / 2, 60);
        const sec = hit && hit.closest('[data-tone]');
        hdr.dataset.tone = sec && sec !== hdr ? sec.dataset.tone : 'dark';
      };
      addEventListener('scroll', tone, { passive: true });
      tone();
      handleHash();
      return;
    }
    init();
    requestAnimationFrame(() => {
      gsap.to($('svg', pre), { scale: 1.6, opacity: 0, duration: 0.8, ease: 'power3.in' });
      setTimeout(() => pre.classList.add('done'), 420);
    });
  }

  /* ================================================================ SCENES */

  function init() {
    gsap.registerPlugin(ScrollTrigger);
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    window.lenis = lenis;

    const stacked = ['#promises', '#cover', '#story', '#truth', '#report', '#coverage', '#answers'];
    const setOverlap = () => stacked.forEach((sel) => { const el = $(sel); if (el) el.style.marginTop = `${-innerHeight}px`; });
    setOverlap();
    ScrollTrigger.addEventListener('refreshInit', setOverlap);

    const mm = gsap.matchMedia();
    mm.add({ desk: '(min-width: 761px)', mob: '(max-width: 760px)' }, (ctx) => {
      const mob = ctx.conditions.mob;
      const pinPct = {};
      const len = (d, m, key) => { if (key) pinPct[key] = mob ? m : d; return `+=${mob ? m : d}%`; };
      // a sheet arriving over the pinned scene beneath it
      const sheet = (sel) => gsap.fromTo(sel, { scale: 0.9, borderRadius: 26, yPercent: 4 },
        { scale: 1, borderRadius: 0, yPercent: 0, ease: 'power1.out' });
      const inHandoff = (trigger, tl) =>
        gsap.timeline({ scrollTrigger: { trigger, start: 'top bottom', end: 'top top', scrub: true } }).add(tl);

      /* ---------- A. 19:40 the mark → 20:15 the crew ---------------------- */
      {
        const stage = $('#top .stage');
        const photo = $('[data-op-photo]');
        const emblem = $('[data-emblem]');
        const ap = [0.3854, 0.3807];
        const shield = [[.17, .17], [.5, .11], [.83, .17], [.83, .52], [.73, .73], [.5, .86], [.27, .73], [.17, .52]];
        const proxy = { s: 1 };
        let box = null;
        // unscaled geometry from layout, not getBoundingClientRect: GSAP folds the CSS translate
        // into its transform, so reading the painted box mid-scene or with transform removed lies
        const measure = () => {
          const w = emblem.offsetWidth, h = emblem.offsetHeight;
          const top = parseFloat(getComputedStyle(emblem).top);
          box = { x: stage.clientWidth / 2 - w * 0.5, y: top - h * 0.46, w, h };
        };
        const aperture = () => {
          if (!box) measure();
          const s = proxy.s;
          const ax = box.x + box.w * ap[0], ay = box.y + box.h * ap[1];
          if (s * box.w * 0.5 > Math.max(innerWidth, innerHeight) * 2.2) { photo.style.clipPath = 'none'; return; }
          photo.style.clipPath = 'polygon(' + shield.map(([fx, fy]) => {
            const px = box.x + box.w * fx, py = box.y + box.h * fy;
            return `${(ax + (px - ax) * s).toFixed(1)}px ${(ay + (py - ay) * s).toFixed(1)}px`;
          }).join(',') + ')';
        };
        ScrollTrigger.addEventListener('refreshInit', () => { box = null; });

        const crewScale = mob ? 1.2 : 1.32;
        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: {
            trigger: '#top', start: 'top top', end: len(440, 320, 'op'), pin: stage, scrub: true, anticipatePin: 1,
            onRefresh: () => { measure(); aperture(); },
            onUpdate: (self) => { scenes.op.p = self.progress; },
          },
        });
        scenes.op = { st: tl.scrollTrigger, p: 0, tone: () => 'dark' };

        tl.set('.op__plate', { opacity: 1 }, 0)
          .set('.op__lines .op__line', { opacity: 0 }, 0)
          .set('.op__chips li', { opacity: 0, y: 30 }, 0)
          .to('.op__copy, .op__cta', { opacity: 0, y: 40, duration: 0.9, ease: 'power1.in' }, 0)
          .to('.op__kick', { opacity: 0, y: -30, duration: 0.8 }, 0.1)
          .to(proxy, { s: 22, duration: 4, ease: 'power2.in', onUpdate: aperture }, 0)
          .fromTo(emblem, { scale: 1 }, { scale: 22, transformOrigin: `${ap[0] * 100}% ${ap[1] * 100}%`, duration: 4, ease: 'power2.in' }, 0)
          .to(emblem, { opacity: 0, duration: 0.5 }, 3.4)
          .to('.op__type .l1', { yPercent: -140, scale: 1.7, opacity: 0, duration: 2.6, ease: 'power2.in' }, 0.2)
          .to('.op__type .l2', { yPercent: 140, scale: 1.7, opacity: 0, duration: 2.6, ease: 'power2.in' }, 0.2)
          .fromTo('.op__photo img', { scale: 1.18 }, { scale: 1, duration: 4, ease: 'power2.out' }, 0)
          .fromTo('.op__shade', { opacity: 0.35 }, { opacity: 1, duration: 3 }, 1)
          // the advance: the room falls away, the crew steps toward you
          .to('.op__plate', { opacity: 0, duration: 0.9 }, 4.7)
          .to('.op__bg', { scale: 0.86, duration: 3.6 }, 4.7)
          .to('.op__crew', { scale: crewScale, duration: 3.6, ease: 'power1.inOut' }, 4.7)
          .fromTo('[data-line="a"]', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.8 }, 4.9)
          .to('.op__chips li', { opacity: 1, y: 0, stagger: 0.18, duration: 0.5 }, 5.3)
          .to('[data-line="a"]', { opacity: 0, y: -50, duration: 0.5 }, 6.5)
          .fromTo('[data-line="b"]', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.8 }, 6.8)
          // the sign blooms and floods the frame to bone — no seam into 21:00
          .to('.op__glow', { opacity: 1, duration: 1.2 }, 8)
          .to('.op__chips li, [data-line="b"]', { opacity: 0, duration: 0.5 }, 8.8)
          .to({}, { duration: 0.2 });
      }

      /* ---------- B. 21:00 the four promises ------------------------------ */
      {
        const claims = $$('.pr__claims li');
        const cards = $$('.proof');
        inHandoff('#promises', gsap.timeline({ defaults: { ease: 'none' } })
          .add(sheet('#promises .stage'), 0)
          .fromTo('#promises .ghost-time', { scale: 0.55, yPercent: 60, opacity: 0 }, { scale: 1, yPercent: 0, opacity: 1 }, 0)
          .fromTo(claims, { yPercent: 120, scale: 1.4 }, { yPercent: 0, scale: 1, stagger: 0.08 }, 0)
          .fromTo(cards[0], { y: 260, rotation: -8, scale: 0.8, opacity: 0 }, { y: 0, rotation: -1.2, scale: 1, opacity: 1 }, 0.2));
        gsap.set(cards.slice(1), { opacity: 0, y: 120, scale: 0.9 });

        const tl = gsap.timeline({
          defaults: { ease: 'power2.out' },
          scrollTrigger: {
            trigger: '#promises', start: 'top top', end: len(320, 240, 'pr'), pin: '#promises .stage', scrub: true,
            onUpdate: (self) => {
              const i = Math.min(claims.length - 1, Math.floor(self.progress * claims.length * 0.999));
              claims.forEach((c, k) => { c.classList.toggle('on', k === i); });
            },
          },
        });
        scenes.pr = { st: tl.scrollTrigger, tone: () => 'light' };
        tl.fromTo(cards[0], { scale: 0.86, rotation: -6 }, { scale: 1, rotation: -1.2, duration: 0.7 }, 0)
          .fromTo('.pr__claims', { xPercent: -6 }, { xPercent: 0, duration: 0.8 }, 0);
        cards.forEach((card, i) => {
          if (i === 0) return;
          const at = i * 0.9 - 0.15;
          tl.to(cards[i - 1], { y: -90, scale: 0.88, rotation: i % 2 ? -5 : 5, opacity: 0, duration: 0.45, ease: 'power2.in' }, at)
            .fromTo(card, { y: 160, rotation: i % 2 ? 6 : -6, scale: 0.9, opacity: 0 },
              { y: 0, rotation: i % 2 ? 1.2 : -1.2, scale: 1, opacity: 1, duration: 0.55 }, at + 0.05);
        });
        tl.fromTo('#promises .ghost-time', { xPercent: 0 }, { xPercent: -30, ease: 'none', duration: 4 }, 0)
          .to('#promises .stage > div:first-of-type', { yPercent: -8, duration: 4, ease: 'none' }, 0);
      }

      /* ---------- C. 22:30 portal → the rooms ----------------------------- */
      {
        const portal = $('[data-portal]');
        const track = $('[data-track]');
        const rooms = $$('.room');
        const shieldPoly = mob ? 'polygon(22% 32%, 78% 32%, 78% 56%, 50% 70%, 22% 56%)'
          : 'polygon(30% 20%, 70% 20%, 70% 62%, 50% 82%, 30% 62%)';
        const fullPoly = 'polygon(0% 0%, 100% 0%, 100% 100%, 50% 100%, 0% 100%)';
        inHandoff('#cover', gsap.timeline({ defaults: { ease: 'none' } })
          .add(sheet('#cover .stage'), 0)
          .fromTo(portal, { clipPath: 'polygon(49% 49%, 51% 49%, 51% 51%, 50% 52%, 49% 51%)', rotation: -14, scale: 0.6 },
            { clipPath: shieldPoly, rotation: 0, scale: 1 }, 0));

        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: {
            trigger: '#cover', start: 'top top', end: len(520, 420, 'cv'), pin: '#cover .stage', scrub: true, invalidateOnRefresh: true,
          },
        });
        tl.fromTo(portal, { clipPath: shieldPoly }, { clipPath: fullPoly, duration: 1.4, ease: 'power2.inOut' }, 0)
          .fromTo('.room:first-child .room__img img', { scale: 1.6 }, { scale: 1, duration: 1.8, ease: 'power2.out' }, 0)
          .fromTo('[data-cv-head]', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5 }, 1.1)
          .to('[data-cv-head]', { opacity: 0, y: -40, duration: 0.5 }, 1.9)
          .fromTo($$('.room__copy > *', rooms[0]), { opacity: 0, y: 50 }, { opacity: 1, y: 0, stagger: 0.12, duration: 0.5 }, 1.8)
          .fromTo($('.room__big', rooms[0]), { xPercent: 30 }, { xPercent: -10, duration: 3.4 }, 0);
        // dolly to each room, then HOLD while its copy lands: a pan that never rests leaves
        // every headline half off-screen
        const arrive = [1.9];
        let t = 3.2;
        const MOVE = 1.6, HOLD = 1.5;
        for (let i = 1; i < rooms.length; i++) {
          const room = rooms[i];
          tl.to(track, { x: () => -innerWidth * i, duration: MOVE, ease: 'power2.inOut' }, t)
            .to($$('.room__copy > *', rooms[i - 1]), { opacity: 0, x: -80, stagger: 0.05, duration: 0.6, ease: 'power1.in' }, t)
            .fromTo($('.room__img img', room), { xPercent: -30, scale: 1.25 }, { xPercent: 0, scale: 1, duration: MOVE, ease: 'power2.out' }, t)
            .fromTo($('.room__img', room), { clipPath: 'inset(12% 0% 12% 35%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: MOVE, ease: 'power2.inOut' }, t)
            .fromTo($('.room__big', room), { xPercent: 45 }, { xPercent: -10, duration: MOVE + HOLD }, t)
            .fromTo($$('.room__copy > *', room), { opacity: 0, y: 60 }, { opacity: 1, y: 0, stagger: 0.12, duration: 0.7 }, t + MOVE * 0.75);
          arrive.push(t + MOVE + 0.4);
          t += MOVE + HOLD;
        }
        // the last room stays lit: 01:15 slides over it
        tl.to({}, { duration: 0.6 });
        const dur = tl.duration();
        scenes.cv = { st: tl.scrollTrigger, tone: (p) => (p < 1.2 / dur ? 'light' : 'dark'),
          roomAt: arrive.map((a) => a / dur), openAt: 1.6 / dur };
      }

      /* ---------- D. 01:15 the table -------------------------------------- */
      {
        inHandoff('#story', gsap.timeline({ defaults: { ease: 'none' } })
          .add(sheet('#story .stage'), 0)
          .fromTo('.st__photo img', { scale: 1.45 }, { scale: 1.12 }, 0));
        const beats = $$('.st__beat');
        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: { trigger: '#story', start: 'top top', end: len(320, 240, 'st'), pin: '#story .stage', scrub: true },
        });
        scenes.st = { st: tl.scrollTrigger, tone: () => 'dark' };
        tl.to('.st__plate', { scale: 1.02, duration: 10 }, 0)
          .to('.st__crew', { scale: mob ? 1.22 : 1.3, duration: 10, ease: 'power1.in' }, 0)
          .fromTo('#story .ghost-time', { yPercent: 0 }, { yPercent: -60, duration: 10 }, 0)
          .fromTo(beats[0], { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 1 }, 0.2)
          .to(beats[0], { opacity: 0, y: -60, duration: 0.6 }, 3)
          .fromTo('.st__sweep', { xPercent: -45 }, { xPercent: 45, duration: 3.2, ease: 'power1.inOut' }, 3)
          .fromTo('.st__vig', { opacity: 0.55 }, { opacity: 1, duration: 1.4 }, 3)
          .fromTo(beats[1], { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 1 }, 3.5)
          .to(beats[1], { opacity: 0, y: -60, duration: 0.6 }, 6.4)
          .to('.st__vig', { opacity: 0.6, duration: 1.4 }, 6.4)
          .fromTo(beats[2], { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 1 }, 6.9)
          .fromTo('.st__cap', { opacity: 0 }, { opacity: 1, duration: 0.8 }, 7.8)
          // headlights flare as the truth arrives over it
          .fromTo('.st__sweep', { scale: 1, opacity: 0.75 }, { scale: 3, opacity: 1, duration: 1.2 }, 8.8)
          .to({}, { duration: 0.2 });
      }

      /* ---------- E. 02:20 the truth -------------------------------------- */
      {
        gsap.fromTo('[data-row="a"]', { xPercent: mob ? 0 : 3 }, { xPercent: mob ? -16 : -8, ease: 'none',
          scrollTrigger: { trigger: '#truth', start: 'top bottom', end: 'bottom top', scrub: true } });
        gsap.fromTo('[data-row="b"]', { xPercent: -20 }, { xPercent: -4, ease: 'none',
          scrollTrigger: { trigger: '#truth', start: 'top bottom', end: 'bottom top', scrub: true } });
        inHandoff('#truth', gsap.timeline({ defaults: { ease: 'none' } })
          .add(sheet('#truth .stage'), 0)
          .fromTo('.tr__rows', { scale: 2.6, yPercent: 30, opacity: 0.25, transformOrigin: '0% 0%' }, { scale: 1, yPercent: 0, opacity: 1, ease: 'power2.out' }, 0)
          .fromTo('[data-truth]', { y: () => innerHeight * 0.9, opacity: 0 }, { y: () => innerHeight * 0.75, opacity: 0 }, 0));
        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: { trigger: '#truth', start: 'top top', end: len(240, 190, 'tr'), pin: '#truth .stage', scrub: true, invalidateOnRefresh: true },
        });
        scenes.tr = { st: tl.scrollTrigger, tone: () => 'light' };
        tl.fromTo('.tr__strike', { scaleX: 0 }, { scaleX: 1, duration: 2.4, ease: 'power2.inOut' }, 0)
          .fromTo('.tr__row--b', { opacity: 0.15 }, { opacity: 1, duration: 1.6 }, 1.2)
          .to('[data-truth]', { y: 0, opacity: 1, duration: 2.4, ease: 'power3.out' }, 2.4)
          .fromTo('[data-truth] h2 em', { opacity: 0.2 }, { opacity: 1, duration: 1 }, 3.8)
          .to({}, { duration: 1.4 });
      }

      /* ---------- F. 03:05 the report ------------------------------------- */
      {
        inHandoff('#report', gsap.timeline({ defaults: { ease: 'none' } })
          .add(sheet('#report .stage'), 0)
          .fromTo('[data-paper]', { y: 360, rotation: -9, scale: 0.8 }, { y: 60, rotation: -3, scale: 0.95 }, 0)
          .fromTo('.rp__side', { y: 120, opacity: 0 }, { y: 0, opacity: 1 }, 0.3));
        const rows = $$('.paper__row');
        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: { trigger: '#report', start: 'top top', end: len(260, 200, 'rp'), pin: '#report .stage', scrub: true },
        });
        scenes.rp = { st: tl.scrollTrigger, tone: () => 'dark' };
        tl.to('[data-paper]', { y: 0, rotation: -1.5, scale: 1, duration: 1.5, ease: 'power2.out' }, 0)
          .fromTo(rows, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', stagger: 0.9, duration: 0.8 }, 0.6)
          .fromTo('[data-sign]', { strokeDashoffset: 1, strokeDasharray: 1 }, { strokeDashoffset: 0, duration: 1.4, ease: 'power1.inOut' }, 5.2)
          .fromTo('[data-stamp]', { scale: 2.6, opacity: 0, rotation: -30 }, { scale: 1, opacity: 0.85, rotation: -12, duration: 0.6, ease: 'power4.in' }, 6.6)
          .to({}, { duration: 0.8 });
      }

      /* ---------- G. the swarm spreads ------------------------------------ */
      {
        const routes = $$('.gm__route');
        const dots = $$('.gm__dot');
        const lbls = $$('.gm__lbl');
        const count = $('[data-count]');
        inHandoff('#coverage', gsap.timeline({ defaults: { ease: 'none' } })
          .add(sheet('#coverage .stage'), 0)
          .fromTo('.gm__map svg', { scale: 3.2, opacity: 0 }, { scale: 1.5, opacity: 0.6 }, 0)
          .fromTo('.gm__copy', { y: 140, opacity: 0 }, { y: 0, opacity: 1 }, 0.3));
        gsap.set(routes, { strokeDasharray: 1, strokeDashoffset: 1 });
        gsap.set(dots, { scale: 0, transformOrigin: '50% 50%', transformBox: 'fill-box' });
        gsap.set(lbls, { opacity: 0 });
        const n = { v: 1 };
        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: { trigger: '#coverage', start: 'top top', end: len(220, 170, 'gm'), pin: '#coverage .stage', scrub: true },
        });
        scenes.gm = { st: tl.scrollTrigger, tone: () => 'dark' };
        tl.to('.gm__map svg', { scale: 1, opacity: 1, duration: 1.4, ease: 'power2.out' }, 0)
          .fromTo('.gm__ring', { scale: 0.2, opacity: 1, transformOrigin: '50% 50%', transformBox: 'fill-box' },
            { scale: 7, opacity: 0, duration: 2 }, 0.4)
          .to(routes, { strokeDashoffset: 0, stagger: 0.25, duration: 1.1 }, 1.2)
          .to(dots, { scale: 1, stagger: 0.25, duration: 0.4, ease: 'back.out(3)' }, 2)
          .to(lbls, { opacity: 1, stagger: 0.25, duration: 0.4 }, 2.1)
          .fromTo(n, { v: 1 }, { v: 18, duration: 4.5, onUpdate: () => { count.textContent = String(Math.round(n.v)); } }, 1.2)
          .fromTo('.gm__count', { scale: 0.7, opacity: 0.3 }, { scale: 1, opacity: 1, duration: 4.5 }, 1.2)
          .to({}, { duration: 1 });
      }

      /* ---------- H. answers: the intermission still travels -------------- */
      $$('.qa details').forEach((d, i) => {
        gsap.fromTo(d, { x: (i % 2 ? 1 : -1) * (mob ? 70 : 200), opacity: 0.05, scale: 0.94 }, { x: 0, opacity: 1, scale: 1, ease: 'none',
          scrollTrigger: { trigger: d, start: 'top 100%', end: 'top 45%', scrub: true } });
      });
      gsap.fromTo('.qa__head h2', { xPercent: -30, opacity: 0.2 }, { xPercent: 0, opacity: 1, ease: 'none',
        scrollTrigger: { trigger: '.qa', start: 'top bottom', end: 'top 30%', scrub: true } });

      /* ---------- the stack: answers slide over the map too ---------------- */
      inHandoff('#answers', gsap.timeline({ defaults: { ease: 'none' } }).add(sheet('#answers'), 0));

      /* ---------- covered tail: the last viewport of every pin is spent UNDER the
         next sheet, so each scene's own story must finish before it, and the scene
         beneath dims as it is covered ------------------------------------------- */
      for (const key of ['op', 'pr', 'cv', 'st', 'tr', 'rp', 'gm']) {
        const sc = scenes[key]; if (!sc) continue;
        const tl = sc.st.animation;
        const stage = sc.st.pin;
        let veil = stage.querySelector(':scope > .veil');
        if (!veil) { veil = document.createElement('div'); veil.className = 'veil'; stage.appendChild(veil); }
        const c = Math.min(0.6, 100 / pinPct[key]);
        const pad = tl.duration() * c / (1 - c);
        tl.fromTo(veil, { opacity: 0 }, { opacity: 0.72, duration: pad, ease: 'power1.in' }, tl.duration())
          .fromTo(stage, { scale: 1 }, { scale: 0.94, duration: pad, ease: 'power1.in' }, '<');
      }

      /* ---------- J. sign-off: the footer assembles under scroll ----------- */
      gsap.timeline({ defaults: { ease: 'none' }, scrollTrigger: { trigger: '.ft', start: 'top bottom', end: 'bottom bottom', scrub: true } })
        .fromTo('.ft__sign span:first-child', { xPercent: 30, opacity: 0.2 }, { xPercent: 0, opacity: 1 }, 0)
        .fromTo('.ft__sign span:last-child', { xPercent: -30, opacity: 0.2 }, { xPercent: 0, opacity: 1 }, 0)
        .fromTo('.ft__grid > *', { y: 80, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.12 }, 0.2);

      /* ---------- I. call the swarm --------------------------------------- */
      {
        const sw = swarm($('[data-swarm]'));
        const pr = { v: 0 };
        inHandoff('#call', gsap.timeline({ defaults: { ease: 'none' } })
          .fromTo('#call .stage', { clipPath: 'inset(30% 8% 0% 8%)' }, { clipPath: 'inset(0% 0% 0% 0%)' }, 0)
          .fromTo(pr, { v: 0 }, { v: 0.18, onUpdate: () => sw.set(pr.v) }, 0));
        const tl = gsap.timeline({
          defaults: { ease: 'none' },
          scrollTrigger: { trigger: '#call', start: 'top top', end: len(180, 140), pin: '#call .stage', scrub: true },
        });
        scenes.cl = { st: tl.scrollTrigger, tone: () => 'dark' };
        tl.fromTo(pr, { v: 0.18 }, { v: 1, duration: 6, onUpdate: () => sw.set(pr.v) }, 0)
          .fromTo('[data-call]', { scale: 1.8, opacity: 0.06 }, { scale: 1, opacity: 1, duration: 5, ease: 'power2.out' }, 1.5)
          .fromTo('.cl__copy p, .cl__btns', { y: 60, opacity: 0 }, { y: 0, opacity: 1, stagger: 0.3, duration: 1.2 }, 5.4)
          .to({}, { duration: 1.4 });
      }

      return () => {};
    });

    /* ------------------------------------------- rail, header tone, nav */
    const rail = $('.rail');
    const hdr = $('.hdr');
    const railLinks = $$('.rail a');
    const order = ['#top', '#crew', '#promises', '#cover', '#story', '#truth', '#report', '#coverage', '#answers', '#call'];

    const positionOf = (sel) => {
      const vh = innerHeight;
      const span = (s) => s.st.end - s.st.start;
      switch (sel) {
        case '#top': return 0;
        case '#crew': return scenes.op ? scenes.op.st.start + span(scenes.op) * 0.56 : 0;
        case '#promises': return scenes.pr ? scenes.pr.st.start + 2 : 0;
        case '#cover': return scenes.cv ? scenes.cv.st.start + span(scenes.cv) * scenes.cv.openAt : 0;
        case '#venues': case '#events': case '#protection': case '#high-risk': {
          const i = ['#venues', '#events', '#protection', '#high-risk'].indexOf(sel);
          const c = scenes.cv; if (!c) return 0;
          return c.st.start + span(c) * c.roomAt[i];
        }
        case '#story': return scenes.st ? scenes.st.st.start + span(scenes.st) * 0.08 : 0;
        case '#truth': return scenes.tr ? scenes.tr.st.start + span(scenes.tr) * 0.75 : 0;
        case '#report': return scenes.rp ? scenes.rp.st.start + span(scenes.rp) * 0.6 : 0;
        case '#coverage': return scenes.gm ? scenes.gm.st.start + span(scenes.gm) * 0.8 : 0;
        case '#answers': { const el = $('#answers'); return el.getBoundingClientRect().top + scrollY - vh * 0.08; }
        case '#call': return scenes.cl ? scenes.cl.st.end - 2 : document.body.scrollHeight;
        default: { const el = $(sel); return el ? el.getBoundingClientRect().top + scrollY : 0; }
      }
    };
    window.__swarmGo = positionOf;
    window.__swarmScenes = scenes;   // read-only handle for scripts/verification

    $$('[data-go]').forEach((a) => a.addEventListener('click', (e) => {
      e.preventDefault();
      closeMenu();
      lenis.scrollTo(positionOf(a.dataset.go), { duration: 1.6 });
    }));

    const keyOf = { top: 'op', promises: 'pr', cover: 'cv', story: 'st', truth: 'tr', report: 'rp', coverage: 'gm', call: 'cl' };
    const toneAt = (y) => {
      const hit = document.elementFromPoint(innerWidth / 2, innerHeight / 2);
      const sec = hit && hit.closest('main > section, main > .qa');
      if (!sec) return 'dark';
      const sc = scenes[keyOf[sec.id]];
      if (sc && y >= sc.st.start && y <= sc.st.end) return sc.tone((y - sc.st.start) / Math.max(1, sc.st.end - sc.st.start));
      return sec.dataset.tone || 'dark';
    };
    const onScroll = () => {
      const y = scrollY;
      const tone = toneAt(y);
      rail.dataset.tone = tone; hdr.dataset.tone = tone;
      const pos = order.map(positionOf);
      let on = 0;
      pos.forEach((p, i) => { if (y + innerHeight * 0.35 >= p - 4) on = i; });
      railLinks.forEach((l, i) => {
        l.classList.toggle('on', i === on);
        const next = i + 1 < pos.length ? pos[i + 1] : document.body.scrollHeight;
        const pr = Math.min(1, Math.max(0, (y - pos[i]) / Math.max(1, next - pos[i])));
        l.querySelector('i').style.setProperty('--p', pr.toFixed(3));
      });
    };
    lenis.on('scroll', onScroll);
    ScrollTrigger.addEventListener('refresh', onScroll);

    document.fonts?.ready.then(() => ScrollTrigger.refresh());
    addEventListener('load', () => ScrollTrigger.refresh());
    setTimeout(() => { ScrollTrigger.refresh(); handleHash(); onScroll(); }, 120);
  }

  function handleHash() {
    const h = location.hash;
    if (!h) return;
    if (h === '#quote') return openQuote();
    if (!reduce && window.__swarmGo && lenis) {
      lenis.scrollTo(window.__swarmGo(h), { immediate: true, force: true });
    } else {
      $(h)?.scrollIntoView();
    }
  }
})();
