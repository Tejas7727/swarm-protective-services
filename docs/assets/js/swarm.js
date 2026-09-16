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

  /* --- dispatch clock ------------------------------------------------------ */
  var clock = document.querySelector('[data-clock]');
  if (clock) {
    var tick = function () {
      try {
        clock.textContent = new Intl.DateTimeFormat('en-CA', {
          timeZone: 'America/Toronto', hour: '2-digit', minute: '2-digit', hour12: false
        }).format(new Date()) + ' Toronto';
      } catch (err) { clock.textContent = 'Toronto'; }
    };
    tick();
    setInterval(tick, 30000);
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

  /* --- quote form ---------------------------------------------------------- */
  var form = document.querySelector('form[data-quote]');
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

      if (!endpoint) { done(); return; }

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

  /* --- year ---------------------------------------------------------------- */
  var yr = document.getElementById('yr');
  if (yr) { yr.textContent = new Date().getFullYear(); }
})();
