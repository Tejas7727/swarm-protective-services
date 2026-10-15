/* Swarm Protective Services — site behaviour. No dependencies.
   Scroll-linked motion lives in CSS scroll timelines; this file only supplies
   the fallback for browsers that lack them, plus the bits CSS cannot do. */
(function () {
  'use strict';

  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasScrollTimeline = CSS.supports && CSS.supports('animation-timeline', 'view()');
  if (!hasScrollTimeline) { document.documentElement.classList.add('js-io'); }

  /* --- masthead: solid once you leave the top ----------------------------- */
  var topbar = document.querySelector('.topbar');
  if (topbar) {
    var stick = function () { topbar.classList.toggle('is-stuck', window.scrollY > 16); };
    stick();
    addEventListener('scroll', stick, { passive: true });
  }

  /* --- mobile drawer ------------------------------------------------------ */
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');
  if (burger && drawer) {
    var setDrawer = function (open) {
      drawer.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) { drawer.querySelector('a').focus({ preventScroll: true }); }
    };
    burger.addEventListener('click', function () {
      setDrawer(burger.getAttribute('aria-expanded') !== 'true');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setDrawer(false); }
    });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        setDrawer(false); burger.focus();
      }
    });
  }

  /* --- reveal fallback + counters ----------------------------------------- */
  var counters = [].slice.call(document.querySelectorAll('[data-count]'));

  var runCount = function (el) {
    if (el.dataset.done) { return; }
    el.dataset.done = '1';
    var target = parseFloat(el.dataset.count);
    var prefix = el.dataset.prefix || '';
    var suffix = el.dataset.suffix || '';
    if (reduced || !isFinite(target)) { el.textContent = prefix + target + suffix; return; }
    var start = performance.now();
    var dur = 1100;
    var step = function (now) {
      var t = Math.min(1, (now - start) / dur);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = prefix + Math.round(target * eased) + suffix;
      if (t < 1) { requestAnimationFrame(step); }
    };
    requestAnimationFrame(step);
  };

  if ('IntersectionObserver' in window) {
    var targets = counters.slice();
    if (!hasScrollTimeline) {
      targets = targets.concat(
        [].slice.call(document.querySelectorAll('.reveal,.night__row,.proof__cell,.step')));
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        var el = entry.target;
        el.classList.add('is-in');
        if (el.hasAttribute('data-count')) { runCount(el); }
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    counters.forEach(runCount);
    document.documentElement.classList.remove('js-io');
  }

  /* --- active section in the nav ------------------------------------------ */
  var navLinks = [].slice.call(document.querySelectorAll('.mast__nav a[href*="#"]'));
  var sections = navLinks
    .map(function (a) {
      var id = a.getAttribute('href').split('#')[1];
      return id ? document.getElementById(id) : null;
    })
    .filter(Boolean);

  if (sections.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        navLinks.forEach(function (a) {
          a.classList.toggle('is-active',
            a.getAttribute('href').split('#')[1] === entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* --- screens: the page moves one screen at a time --------------------------
     Pages built from .scr screens snap to them (html.snap). One spring follows
     the scroll and every animated property reads from it, so motion eases into
     place instead of stepping with the wheel. This only writes CSS variables;
     the styles (html.fx7) turn them into motion. Reduced motion: no snap, no
     motion, every screen still and complete.
       per screen    --d screens away (signed), --ad unsigned, --up leaving
       [data-film]   home: the push into the jacket, the portal (one scroll)
       [data-cov]    coverage: Toronto, out to the GTA, out to Canada
       [data-words]  a sentence lit word by word as its screen arrives
       [data-draw]   routes that draw as their screen arrives
       .phero        journal and plain pages: the title steps back
     Guidance: a rail of the page's screens (desktop) and, at the foot of each
     screen, a quiet cue naming the next one. */
  var all = function (s) { return [].slice.call(document.querySelectorAll(s)); };
  var screens = all('.scr');
  var film = document.querySelector('[data-film]'), cov = document.querySelector('[data-cov]');
  var words = all('[data-words]'), draws = all('[data-draw]'), pheros = all('.phero');
  var html = document.documentElement;
  var DOWN = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M6 13l6 6 6-6"/></svg>';

  var rail = null, railLinks = [];
  var named = screens.filter(function (s) { return s.id && s.getAttribute('data-label'); });
  if (named.length > 1) {
    rail = document.createElement('nav');
    rail.className = 'rail7';
    rail.setAttribute('aria-label', 'On this page');
    rail.innerHTML = named.map(function (s) {
      return '<a href="#' + s.id + '"><span>' + s.getAttribute('data-label') + '</span><i></i></a>';
    }).join('');
    document.body.appendChild(rail);
    railLinks = [].slice.call(rail.querySelectorAll('a'));
    named.forEach(function (s, i) {
      var nx = named[i + 1];
      if (!nx || s.classList.contains('hx')) { return; }     // the welcome screen has its own three ways in
      var a = document.createElement('a');
      a.className = 'next7';
      a.href = '#' + nx.id;
      a.innerHTML = 'Next <b>' + nx.getAttribute('data-label') + '</b>' + DOWN;
      s.appendChild(a);
    });
  }

  if (!reduced && screens.length) { html.classList.add('snap'); }
  if (!reduced && (screens.length || pheros.length)) {
    html.classList.add('fx7');
    var VW = 1, VH = 1, diag = 1, filmTop = 0, covTop = 0, tops = [], hts = [];
    var smooth = function (a, b, x) {
      var t = Math.min(1, Math.max(0, (x - a) / (b - a)));
      return t * t * (3 - 2 * t);
    };
    var set = function (el, k, v) { el.style.setProperty(k, v); };

    // home: where the camera goes in — the dark jacket under the emblem, on
    // whichever plate the browser picked, through the same cover crop the CSS draws
    var shot = film && film.querySelector('.film__hero img');
    var plates = shot ? JSON.parse(shot.getAttribute('data-plates')) : null;
    var origin = function () {
      var src = shot.currentSrc || shot.src;
      var p = plates[/crew-m-/.test(src) ? 'crew-m' : /crew-t-/.test(src) ? 'crew-t' : 'crew'];
      var s = Math.max(VW / p[0], VH / p[1]), dw = p[0] * s, dh = p[1] * s;
      set(film, '--ox', ((VW - dw) * p[4] + p[2] * dw).toFixed(1) + 'px');
      set(film, '--oy', ((VH - dh) * p[5] + p[3] * dh).toFixed(1) + 'px');
    };
    // coverage: Toronto at the centre of the zoom
    var hq = cov && cov.querySelector('#gm-hq'), gta = cov && cov.querySelector('.cov__gta');
    var hqOrigin = function () {
      gta.style.transform = 'none';
      var g = gta.getBoundingClientRect(), h = hq.getBoundingClientRect();
      gta.style.transform = '';
      set(cov, '--hqx', (h.left + h.width / 2 - g.left).toFixed(1) + 'px');
      set(cov, '--hqy', (h.top + h.height / 2 - g.top).toFixed(1) + 'px');
    };
    // a sentence lit word by word: split once into spans that know their place
    words.forEach(function (el) {
      var list = el.textContent.trim().split(/\s+/);
      el.innerHTML = list.map(function (w, i) { return '<span class="w" style="--i:' + i + '">' + w + '</span>'; }).join(' ');
      set(el, '--n', list.length);
    });
    var home = function (el) { return screens.indexOf(el.closest('.scr')); };
    var wordsAt = words.map(home), drawsAt = draws.map(home);

    var paint = function (y) {
      var dist = [], active = 0;
      for (var i = 0; i < screens.length; i++) {
        // arriving: screens below the top edge; leaving: only once its bottom has
        // passed the bottom of the window, so a tall screen never fades while read
        var d = tops[i] > y ? (tops[i] - y) / VH : Math.min(0, (tops[i] + hts[i] - y - VH) / VH);
        d = Math.max(-1.5, Math.min(1.5, d));
        dist[i] = d;
        if (tops[i] <= y + VH * 0.45) { active = i; }
        if (Math.abs(d) > 1.4 && screens[i]._d !== undefined && Math.abs(screens[i]._d) > 1.4) { continue; }
        screens[i]._d = d;
        set(screens[i], '--d', d.toFixed(4));
        set(screens[i], '--ad', Math.abs(d).toFixed(4));
        set(screens[i], '--up', Math.min(1, Math.max(0, -d)).toFixed(4));
      }
      if (film) {
        var t = (y - filmTop) / VH, open = smooth(0.42, 0.95, t);  // 0: welcome, 1: services
        set(film, '--copy', smooth(0, 0.35, t).toFixed(3));
        set(film, '--push', smooth(0, 0.78, t).toFixed(4));
        set(film, '--open', open.toFixed(4));
        set(film, '--r', (open * diag).toFixed(1) + 'px');
        set(film, '--ring', (smooth(0.4, 0.52, t) * (1 - smooth(0.8, 0.97, t))).toFixed(3));
        set(film, '--dim', smooth(0.6, 1, t).toFixed(3));
      }
      if (cov) {
        var c = Math.min(1, Math.max(0, (y - covTop) / (2 * VH)));   // 0 Toronto, .5 the GTA, 1 Canada
        set(cov, '--z', (3 - 2 * smooth(0.04, 0.48, c)).toFixed(4));
        set(cov, '--draw', smooth(0.18, 0.5, c).toFixed(4));
        set(cov, '--gout', smooth(0.55, 0.88, c).toFixed(4));
        set(cov, '--can', smooth(0.6, 0.92, c).toFixed(4));
        set(cov, '--arc', smooth(0.72, 1, c).toFixed(4));
      }
      words.forEach(function (el, k) {
        var d = dist[wordsAt[k]] || 0;
        set(el, '--wp', (1 - smooth(0.04, 0.8, Math.max(0, d))).toFixed(4));
      });
      draws.forEach(function (el, k) {
        var d = dist[drawsAt[k]] || 0;
        set(el, '--draw', (1 - smooth(0.04, 0.85, Math.max(0, d))).toFixed(4));
      });
      pheros.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom > 0) { set(el, '--h', smooth(0, 1, -r.top / (r.height * 0.9)).toFixed(4)); }
      });
      if (rail) {
        var on = named.indexOf(screens[active]);
        if (on < 0) { for (var j = active; j >= 0 && on < 0; j--) { on = named.indexOf(screens[j]); } }
        railLinks.forEach(function (a, k) { a.classList.toggle('is-on', k === on); });
        var cur = screens[active];
        rail.classList.toggle('on-light', !!cur && (cur.classList.contains('px') || cur.classList.contains('std7')));
      }
    };

    // the spring: follows the scroll, critically damped, settles in about half a second
    var cur = window.scrollY, vel = 0, raf = 0, last = 0;
    var spring = function (now) {
      var dt = Math.min(0.033, (now - last) / 1000 || 0.016); last = now;
      var target = window.scrollY, k = 90, damp = 2 * Math.sqrt(k);
      vel += (k * (target - cur) - damp * vel) * dt;
      cur += vel * dt;
      if (Math.abs(target - cur) < 0.4 && Math.abs(vel) < 4) { cur = target; vel = 0; }
      paint(cur);
      raf = (cur !== target || vel) ? requestAnimationFrame(spring) : 0;
    };
    var kick = function () { if (!raf) { last = 0; raf = requestAnimationFrame(spring); } };
    var measure = function () {
      VW = window.innerWidth; VH = window.innerHeight; diag = Math.hypot(VW, VH);
      var y = window.scrollY;
      tops = screens.map(function (s) { return s.getBoundingClientRect().top + y; });
      hts = screens.map(function (s) { return s.offsetHeight; });
      if (film) { filmTop = film.getBoundingClientRect().top + y; origin(); }
      if (cov) { covTop = cov.getBoundingClientRect().top + y; if (hq) { hqOrigin(); } }
      cur = y; vel = 0;
      paint(cur);
    };
    addEventListener('scroll', kick, { passive: true });

    // wheel and trackpad: one gesture moves one screen, in one eased glide.
    // Touch keeps the browser's own snapping; keyboard and links snap natively.
    // A screen taller than the window scrolls normally until its edge, and a
    // trackpad's momentum tail is absorbed instead of skipping a second screen.
    var busy = 0, acc = 0, accAt = 0;
    var ease = function (x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
    var glide = function (to, dur) {
      var from = window.scrollY, t0 = performance.now();
      html.style.scrollSnapType = 'none';
      var step = function (now) {
        var p = Math.min(1, (now - t0) / dur);
        window.scrollTo({ top: from + (to - from) * ease(p), behavior: 'instant' });
        if (p < 1) { requestAnimationFrame(step); } else { html.style.scrollSnapType = ''; }
      };
      requestAnimationFrame(step);
    };
    if (screens.length > 1) {
      addEventListener('wheel', function (e) {
        if (e.ctrlKey || Math.abs(e.deltaX) > Math.abs(e.deltaY) || document.querySelector('.drawer.is-open')) { return; }
        var now = performance.now();
        if (now < busy) { busy = Math.max(busy, now + 180); e.preventDefault(); return; }
        var y = window.scrollY, i = 0;
        for (var k = 0; k < tops.length; k++) { if (tops[k] <= y + 2) { i = k; } }
        if (e.deltaY > 0 && tops[i] + hts[i] > y + VH + 2) { return; }      // still inside a tall screen
        if (e.deltaY < 0 && tops[i] < y - 2) { return; }
        e.preventDefault();
        if (now - accAt > 220) { acc = 0; }
        acc += e.deltaY; accAt = now;
        if (Math.abs(acc) < 24) { return; }                                // a touch, not a gesture yet
        var j = i + (acc > 0 ? 1 : -1);
        var to = j < 0 ? 0 : j >= tops.length ? html.scrollHeight - VH : tops[j];
        acc = 0;
        if (Math.abs(to - y) < 2) { return; }
        // the camera moves (the jacket, the map) take a little longer than a plain step
        var slow = [film, cov].some(function (w) { return w && w.contains(screens[i]) && screens[j] && w.contains(screens[j]); });
        busy = now + (slow ? 1300 : 900);
        glide(to, slow ? 1150 : 760);
      }, { passive: false });
    }
    addEventListener('resize', measure);
    if (shot) { shot.addEventListener('load', measure); }
    if (document.fonts && document.fonts.ready) { document.fonts.ready.then(measure); }
    addEventListener('load', measure);
    measure();
  }

  /* --- quote form ---------------------------------------------------------- */
  // Without the script every step shows at once and the form still works. With
  // it, one step at a time; a visitor who came from a service page arrives with
  // that service picked and starts at step two.
  var form = document.querySelector('form[data-quote]');
  var steps = form ? [].slice.call(form.querySelectorAll('.qf__step')) : [];
  if (form && steps.length) {
    var at = 0;
    var back = form.querySelector('[data-back]'), next = form.querySelector('[data-next]');
    var send = form.querySelector('[data-send]'), prog = form.querySelector('[data-prog]');
    var bar = form.querySelector('.qf__prog');
    var show = function (i, focus) {
      at = i;
      steps.forEach(function (s, k) { s.classList.toggle('is-on', k === i); });
      back.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      send.hidden = i !== steps.length - 1;
      var picked = form.querySelector('[name="service"]:checked');
      prog.textContent = 'Step ' + (i + 1) + ' of ' + steps.length +
        (i > 0 && picked ? ' · ' + picked.value : '');
      bar.style.setProperty('--p', ((i + 1) / steps.length * 100) + '%');
      if (focus) {
        var f = steps[i].querySelector('input:not([type=radio]),select,input:checked,input');
        if (f) { f.focus({ preventScroll: true }); }
      }
    };
    var valid = function (i) {
      var bad = [].slice.call(steps[i].querySelectorAll('input,select,textarea'))
        .filter(function (el) { return !el.checkValidity(); })[0];
      if (bad) { bad.reportValidity(); return false; }
      return true;
    };
    form.classList.add('is-steps');
    next.addEventListener('click', function () { if (valid(at)) { show(at + 1, true); } });
    back.addEventListener('click', function () { show(at - 1, true); });
    // a tap on step one is an answer: move on (arrow keys only move the choice;
    // keyboard users go on with Next)
    var tapped = false;
    steps[0].addEventListener('pointerdown', function () { tapped = true; });
    steps[0].addEventListener('change', function () {
      if (at === 0 && tapped) { setTimeout(function () { show(1, true); }, 180); }
      tapped = false;
    });
    var want = new URLSearchParams(location.search).get('service');
    var pre = want && form.querySelector('[name="service"][data-slug="' + want.replace(/[^a-z-]/g, '') + '"]');
    if (pre) { pre.checked = true; }
    show(pre ? 1 : 0, false);
  }
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) { return; }
      if (form.querySelector('[name="company"]').value) { return; }  /* honeypot */

      var endpoint = form.getAttribute('data-endpoint');
      var done = function () {
        form.classList.add('is-sent');
        var ok = form.querySelector('.form__ok');
        ok.setAttribute('tabindex', '-1');
        ok.focus({ preventScroll: true });
        form.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'center' });
      };

      // no form service yet: the request goes out from the visitor's own mail app
      if (!endpoint) {
        var data = new FormData(form), lines = [];
        data.forEach(function (v, k) { if (k !== 'company' && v) { lines.push(k + ': ' + v); } });
        location.href = 'mailto:' + (form.getAttribute('data-to') || '') +
          '?subject=' + encodeURIComponent('Quote request — ' + (data.get('service') || 'security')) +
          '&body=' + encodeURIComponent(lines.join('\n'));
        done();
        return;
      }

      var btn = form.querySelector('button[type="submit"]');
      var label = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }

      fetch(endpoint, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(form)
      }).then(function (r) {
        if (!r.ok) { throw new Error(r.status); }
        done();
      }).catch(function () {
        if (btn) { btn.disabled = false; btn.textContent = label; }
        var err = form.querySelector('[data-senderr]');
        if (err) { err.hidden = false; }
      });
    });
  }

  /* --- the GTA map: a squarer window on narrow screens --------------------- */
  var gm = document.querySelector('.gm[data-narrow]');
  if (gm) {
    var mq = window.matchMedia('(max-width:899px)');
    var frame = function () { gm.setAttribute('viewBox', gm.getAttribute(mq.matches ? 'data-narrow' : 'data-full')); };
    frame();
    if (mq.addEventListener) { mq.addEventListener('change', frame); }
  }

  /* --- phones: the Call / quote bar steps aside when the form is on screen -- */
  var abar = document.querySelector('.abar'), kx = document.getElementById('contact');
  if (abar && kx && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      abar.classList.toggle('is-away', es[0].isIntersecting);
    }, { rootMargin: '0px 0px -30% 0px' }).observe(kx);
  }

  /* --- year ---------------------------------------------------------------- */
  var yr = document.getElementById('yr');
  if (yr) { yr.textContent = new Date().getFullYear(); }
})();
