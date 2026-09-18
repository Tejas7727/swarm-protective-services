/* Swarm — site behaviour.
 *
 * Three things, in order of importance to the business:
 *   1. the quote dialog and the phone are always one tap away,
 *   2. sections arrive quietly as you scroll,
 *   3. one section — "One night" — is a camera pushing through four scenes,
 *      each one seen through the opening in the one before it.
 *
 * The camera only loads its images when that section is close, and only draws
 * while it is on screen. Nothing else on the page depends on it.
 */
(function () {
  "use strict";
  var D = document, W = window, root = D.documentElement;
  var reduced = W.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------- chrome */
  var mast = D.getElementById("mast");
  var onScroll = function () {
    if (mast) mast.classList.toggle("is-scrolled", (W.scrollY || 0) > 24);
  };
  onScroll();
  W.addEventListener("scroll", onScroll, { passive: true });

  var burger = D.querySelector(".burger");
  var drawer = D.getElementById("drawer");
  if (burger && drawer) {
    var setDrawer = function (open) {
      drawer.hidden = !open;
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      root.classList.toggle("is-locked", open);
    };
    burger.addEventListener("click", function () { setDrawer(drawer.hidden); });
    drawer.addEventListener("click", function (e) {
      if (e.target.tagName === "A") setDrawer(false);
    });
    W.addEventListener("keydown", function (e) { if (e.key === "Escape") setDrawer(false); });
  }

  var yr = D.getElementById("yr");
  if (yr) yr.textContent = String(new Date().getFullYear());

  /* -------------------------------------------------------- quote dialog */
  var dlg = D.getElementById("quote");
  function openQuote() {
    if (!dlg || dlg.open) return;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    var first = dlg.querySelector("input");
    if (first) setTimeout(function () { first.focus(); }, 40);
  }
  [].slice.call(D.querySelectorAll("[data-quote]")).forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); openQuote(); });
  });
  if (location.hash === "#quote") setTimeout(openQuote, 60);
  if (dlg) {
    var close = dlg.querySelector("[data-close]");
    if (close) close.addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    var form = dlg.querySelector("[data-form]");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!form.reportValidity()) return;
        if (form.querySelector('[name="company"]').value) return;      // honeypot
        var data = new FormData(form), endpoint = form.getAttribute("data-endpoint");
        var sent = form.querySelector(".q__sent");
        if (endpoint) {
          fetch(endpoint, { method: "POST", headers: { Accept: "application/json" }, body: data })
            .then(function () { if (sent) sent.hidden = false; })
            .catch(function () { if (sent) sent.hidden = false; });
          return;
        }
        var body = [];
        data.forEach(function (v, k) { if (k !== "company" && v) body.push(k + ": " + v); });
        W.location.href = "mailto:" + (form.getAttribute("data-to") || "dispatch@swarmprotective.ca") +
          "?subject=" + encodeURIComponent("Quote request — " + (data.get("service") || "security")) +
          "&body=" + encodeURIComponent(body.join("\n"));
        if (sent) sent.hidden = false;
      });
    }
  }

  /* ------------------------------------------------------------ reveals */
  var reveals = [].slice.call(D.querySelectorAll(".reveal"));
  if (reduced || !("IntersectionObserver" in W)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------- hero, gently moving */
  var hero = D.querySelector(".hero");
  var pars = [].slice.call(D.querySelectorAll("[data-par]"));
  if (hero && pars.length && !reduced) {
    var px = 0, py = 0, tx = 0, ty = 0, sy = 0, running = false;
    var step = function () {
      px += (tx - px) * 0.08; py += (ty - py) * 0.08;
      for (var i = 0; i < pars.length; i++) {
        var el = pars[i], k = parseFloat(el.getAttribute("data-par")) || 0;
        el.style.transform = "translate3d(" + (-px * k * 90).toFixed(2) + "px," +
          (-py * k * 50 + sy * k * 0.25).toFixed(2) + "px,0) scale(" + (1 + k * 0.5).toFixed(3) + ")";
      }
      running = Math.abs(tx - px) > 0.001 || Math.abs(ty - py) > 0.001;
      if (running) W.requestAnimationFrame(step);
    };
    var kick = function () { if (!running) { running = true; W.requestAnimationFrame(step); } };
    W.addEventListener("pointermove", function (e) {
      if (W.innerWidth < 760) return;
      tx = (e.clientX / W.innerWidth - 0.5) * 2;
      ty = (e.clientY / W.innerHeight - 0.5) * 2;
      kick();
    }, { passive: true });
    W.addEventListener("scroll", function () {
      var r = hero.getBoundingClientRect();
      if (r.bottom < 0) return;
      sy = -r.top;
      kick();
    }, { passive: true });
    kick();
  }

  /* --------------------------------------------------------- one night */
  var film = D.querySelector(".film");
  var canvas = D.getElementById("stage");
  var data = D.getElementById("scene-data");
  if (!film || !canvas || !data) return;

  var beats = [].slice.call(film.querySelectorAll(".beat"));
  var hud = D.getElementById("hud");
  var hudTime = hud && hud.querySelector("[data-time]");
  var hudLabel = hud && hud.querySelector("[data-label]");
  var ticks = [].slice.call(film.querySelectorAll(".tick"));

  // beat navigation works with or without the camera
  ticks.forEach(function (b, i) {
    b.addEventListener("click", function () {
      W.scrollTo({ top: filmTop() + i * stepH(), behavior: reduced ? "auto" : "smooth" });
    });
  });
  function stepH() { return Math.max(1, film.querySelector(".film__step").getBoundingClientRect().height); }

  var gl = null;
  if (!reduced) {
    try {
      gl = canvas.getContext("webgl2", { antialias: false, alpha: false, powerPreference: "high-performance" });
    } catch (e) { gl = null; }
  }
  if (!gl) { root.classList.add("plain"); return; }

  var SCENE = JSON.parse(data.textContent);
  var byId = {};
  SCENE.plates.forEach(function (p) { byId[p.id] = p; });
  // the film's plates, in beat order, with portals re-pointed inside this list
  // (the hero uses a plate this section never draws, so indices differ)
  var ids = beats.map(function (b) { return b.getAttribute("data-plate"); });
  var P = [];
  ids.forEach(function (id) { if (byId[id]) P.push(byId[id]); });
  P.forEach(function (pl, i) {
    if (!pl.portal) return;
    var childId = SCENE.plates[pl.portal.child] && SCENE.plates[pl.portal.child].id;
    var k = ids.indexOf(childId);
    pl._portal = k > i ? { rect: pl.portal.rect, aper: pl.portal.aper, feather: pl.portal.feather,
                           cross: pl.portal.cross, flood: pl.portal.flood, child: k } : null;
  });
  if (!P.length) { root.classList.add("plain"); return; }
  root.classList.add("fx");

  var VS =
    "#version 300 es\n" +
    "in vec2 a;uniform vec4 u_rect;uniform vec2 u_res;out vec2 v;\n" +
    "void main(){vec2 p=u_rect.xy+a*u_rect.zw;vec2 c=(p/u_res)*2.0-1.0;\n" +
    "gl_Position=vec4(c.x,-c.y,0.0,1.0);v=a;}";
  var FS =
    "#version 300 es\nprecision highp float;\n" +
    "in vec2 v;out vec4 o;uniform sampler2D u_tex;\n" +
    "uniform float u_lod,u_alpha,u_exp,u_feather,u_radial,u_dpr;\n" +
    "uniform vec3 u_tint;uniform vec4 u_clip;uniform vec2 u_res;\n" +
    "void main(){vec4 c=texture(u_tex,v,u_lod);\n" +
    " if(u_lod>0.5){float t=exp2(u_lod)/900.0;\n" +
    "  c=0.25*(texture(u_tex,v+vec2(t,0.0),u_lod)+texture(u_tex,v-vec2(t,0.0),u_lod)\n" +
    "        +texture(u_tex,v+vec2(0.0,t),u_lod)+texture(u_tex,v-vec2(0.0,t),u_lod));}\n" +
    " vec2 p=vec2(gl_FragCoord.x/u_dpr,u_res.y-gl_FragCoord.y/u_dpr);\n" +
    " float m;\n" +
    " if(u_radial>0.5){vec2 h=u_clip.zw*0.5;vec2 q=(p-(u_clip.xy+h))/max(h,vec2(1.0));\n" +
    "  m=1.0-smoothstep(0.18,1.0,length(q));}\n" +
    " else{vec2 d=min(p-u_clip.xy,u_clip.xy+u_clip.zw-p);\n" +
    "  m=smoothstep(0.0,1.0,clamp(min(d.x,d.y)/max(u_feather,0.5),0.0,1.0));}\n" +
    " o=vec4(c.rgb*u_tint*u_exp,c.a)*(u_alpha*m);}";

  function shader(t, s) { var x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); return x; }
  var prog = gl.createProgram();
  gl.attachShader(prog, shader(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, FS));
  gl.bindAttribLocation(prog, 0, "a");
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    root.classList.add("plain"); root.classList.remove("fx"); return;
  }
  gl.useProgram(prog);
  var U = {};
  ["u_rect", "u_res", "u_tex", "u_lod", "u_alpha", "u_exp", "u_tint", "u_clip",
   "u_feather", "u_radial", "u_dpr"].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, 0, 1, 0, 0, 1, 1, 1]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
  gl.clearColor(0.031, 0.035, 0.039, 1);
  var WHITE = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, WHITE);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
                new Uint8Array([255, 255, 255, 255]));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

  function pick(sizes, target) {
    var best = sizes[0];
    for (var i = sizes.length - 1; i >= 0; i--) if (sizes[i].w >= target) best = sizes[i];
    return best;
  }
  var textures = {}, pending = {}, lit = false;
  function load(key, sizes, target) {
    if (textures[key] || pending[key]) return;
    pending[key] = 1;
    var img = new Image();
    img.decoding = "async";
    img.src = pick(sizes, target).src;
    img.onload = function () {
      var t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      textures[key] = t;
      if (!lit) { lit = true; film.classList.add("lit"); }
    };
    img.onerror = function () { pending[key] = 0; };
  }

  var VW = 0, VH = 0, mob = false, near = false;
  function cover(pl, focal) {
    var s = Math.max(VW / pl.w, VH / pl.h);
    var x = VW / 2 - focal[0] * pl.w * s, y = VH / 2 - focal[1] * pl.h * s;
    return { s: s, x: Math.min(0, Math.max(VW - pl.w * s, x)), y: Math.min(0, Math.max(VH - pl.h * s, y)) };
  }
  function focalOf(pl) { return mob && pl.focalM ? pl.focalM : pl.focal; }
  function segment(k, f) {
    var pl = P[k], A = cover(pl, focalOf(pl));
    if (!pl._portal) return { T: A, A: A, F: { x: VW / 2, y: VH / 2 }, m: 0, A0: 1 };
    var ch = P[pl._portal.child], Cc = cover(ch, focalOf(ch));
    var R = pl._portal.rect, rx = R[0] * pl.w, ry = R[1] * pl.h, rw = R[2] * pl.w;
    var m = rw / ch.w;
    var Bs = Cc.s / m, Bx = Cc.x - Bs * rx, By = Cc.y - Bs * ry;
    var s = A.s * Math.pow(Bs / A.s, f);
    var px = (Bx - A.x) / (A.s - Bs), py = (By - A.y) / (A.s - Bs);
    var Fx = A.s * px + A.x, Fy = A.s * py + A.y;
    return { T: { s: s, x: Fx - s * px, y: Fy - s * py }, A: A, F: { x: Fx, y: Fy }, m: m, A0: Bs / A.s };
  }
  function drawPlate(tex, pl, T, o) {
    gl.uniform4f(U.u_rect, T.x, T.y, pl.w * T.s, pl.h * T.s);
    gl.uniform1f(U.u_lod, o.lod || 0);
    gl.uniform1f(U.u_alpha, o.alpha == null ? 1 : o.alpha);
    gl.uniform1f(U.u_exp, o.exp == null ? 1 : o.exp);
    gl.uniform3f(U.u_tint, o.tint[0], o.tint[1], o.tint[2]);
    var c = o.clip || [-9e4, -9e4, 1.8e5, 1.8e5];
    gl.uniform4f(U.u_clip, c[0], c[1], c[2], c[3]);
    gl.uniform1f(U.u_feather, o.feather || 0.5);
    gl.uniform1f(U.u_radial, o.radial ? 1 : 0);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  function clipRect(pl, T, aper) {
    return [T.x + T.s * aper[0] * pl.w, T.y + T.s * aper[1] * pl.h,
            T.s * aper[2] * pl.w, T.s * aper[3] * pl.h];
  }
  function intersect(a, b) {
    if (!a) return b; if (!b) return a;
    var x = Math.max(a[0], b[0]), y = Math.max(a[1], b[1]);
    return [x, y, Math.max(0, Math.min(a[0] + a[2], b[0] + b[2]) - x),
            Math.max(0, Math.min(a[1] + a[3], b[1] + b[3]) - y)];
  }
  function ease(f) { return 0.25 * f + 0.75 * (f * f * (3 - 2 * f)); }
  function smooth(a, b, x) { var t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); }

  function render(p, t) {
    var k = Math.min(P.length - 1, Math.floor(p)), f = ease(Math.min(1, Math.max(0, p - k)));
    var seg = segment(k, f), T = { s: seg.T.s, x: seg.T.x, y: seg.T.y };
    var breathe = 1 + Math.sin(t * 0.00031) * 0.004;
    T.s *= breathe;
    T.x = VW / 2 + (T.x - VW / 2) * breathe;
    T.y = VH / 2 + (T.y - VH / 2) * breathe;

    gl.clear(gl.COLOR_BUFFER_BIT);
    var pl = P[k], g = pl.grade, leaving = pl._portal ? f : 0;
    if (textures[pl.id]) {
      drawPlate(textures[pl.id], pl, T, {
        tint: g.tint, exp: g.exp * (1 - 0.12 * smooth(0.55, 1, leaving)),
        lod: 1.3 * smooth(0.55, 1, leaving), alpha: 1 - smooth(0.86, 1, leaving),
      });
    }
    if (pl._portal && textures[P[pl._portal.child].id]) {
      var ch = P[pl._portal.child], R = pl._portal.rect;
      var childT = { s: T.s * seg.m, x: T.x + T.s * R[0] * pl.w, y: T.y + T.s * R[1] * pl.h };
      var op = clipRect(pl, T, pl._portal.aper);
      var e = 1;
      if (seg.A0 > 1.0001) {
        var rest0 = clipRect(pl, seg.A, pl._portal.aper);
        var G = Math.hypot(VW, VH) / Math.max(20, Math.min(rest0[2], rest0[3]));
        e = Math.max(1.05, Math.min(6, Math.log(G) / ((pl._portal.cross || 0.76) * Math.log(seg.A0))));
      }
      var ga = Math.pow(T.s / seg.A.s, e - 1);
      var ocx = op[0] + op[2] / 2, ocy = op[1] + op[3] / 2;
      op = [ocx - op[2] * ga / 2, ocy - op[3] * ga / 2, op[2] * ga, op[3] * ga];
      var clip = intersect(op, [childT.x, childT.y, ch.w * childT.s, ch.h * childT.s]);
      var fe = smooth(0, 0.5, f), soft = 1 - smooth(0.6, 0.98, f);
      if (f < 0.62) {                               // the opening glows before it opens
        var hw = clip[2] * 3.4, hh = clip[3] * 3.4;
        var hcx = clip[0] + clip[2] / 2, hcy = clip[1] + clip[3] / 2;
        gl.blendFunc(gl.ONE, gl.ONE);
        drawPlate(textures[ch.id], ch,
          { s: childT.s * 3.4, x: hcx + (childT.x - hcx) * 3.4, y: hcy + (childT.y - hcy) * 3.4 }, {
            tint: [ch.grade.tint[0] * 1.18, ch.grade.tint[1], ch.grade.tint[2] * 0.8],
            exp: ch.grade.exp * 0.95, lod: 7.5, alpha: 0.3 * (1 - smooth(0.1, 0.5, f)),
            clip: [hcx - hw / 2, hcy - hh / 2, hw, hh], radial: true,
          });
        gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      }
      drawPlate(textures[ch.id], ch, childT, {
        tint: ch.grade.tint, exp: ch.grade.exp * (0.6 + 0.4 * fe),
        lod: 5.0 * (1 - fe), alpha: smooth(0.04, 0.26, f) * (0.86 + 0.14 * fe),
        clip: clip, feather: pl._portal.feather * Math.min(clip[2], clip[3]) * 0.5 * soft,
      });
      if (pl._portal.flood) {                       // night into morning, in light
        var fl = Math.sin(Math.PI * smooth(0.18, 0.95, f)) * 0.92;
        if (fl > 0.002) {
          gl.uniform4f(U.u_rect, 0, 0, VW, VH);
          gl.uniform1f(U.u_lod, 0); gl.uniform1f(U.u_alpha, fl); gl.uniform1f(U.u_exp, 1);
          gl.uniform3f(U.u_tint, pl._portal.flood[0], pl._portal.flood[1], pl._portal.flood[2]);
          gl.uniform4f(U.u_clip, -9e4, -9e4, 1.8e5, 1.8e5);
          gl.uniform1f(U.u_feather, 0.5); gl.uniform1f(U.u_radial, 0);
          gl.bindTexture(gl.TEXTURE_2D, WHITE);
          gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        }
      }
    }
    if (pl.layers && pl.layers.length) {            // someone the camera passes
      for (var i = 0; i < pl.layers.length; i++) {
        var L = pl.layers[i], key = pl.id + "-L" + i;
        if (!textures[key]) continue;
        var lx = T.x + T.s * L.rect[0] * pl.w, ly = T.y + T.s * L.rect[1] * pl.h;
        var gz = Math.pow(T.s / seg.A.s, L.depth - 1);
        var a = 1 - smooth(L.fade[0], L.fade[1], f);
        if (a <= 0.002) continue;
        gl.uniform4f(U.u_rect, seg.F.x + (lx - seg.F.x) * gz, seg.F.y + (ly - seg.F.y) * gz,
                     T.s * L.rect[2] * pl.w * gz, T.s * L.rect[3] * pl.h * gz);
        gl.uniform1f(U.u_lod, 3.4 * smooth(L.fade[0], L.fade[1] + 0.06, f));
        gl.uniform1f(U.u_alpha, a); gl.uniform1f(U.u_exp, g.exp);
        gl.uniform3f(U.u_tint, g.tint[0], g.tint[1], g.tint[2]);
        gl.uniform4f(U.u_clip, -9e4, -9e4, 1.8e5, 1.8e5);
        gl.uniform1f(U.u_feather, 0.5); gl.uniform1f(U.u_radial, 0);
        gl.bindTexture(gl.TEXTURE_2D, textures[key]);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      }
    }
    canvas.dataset.frame = p.toFixed(3);
  }

  var active = -1;
  function paintBeats(p) {
    for (var i = 0; i < beats.length; i++) {
      var d = p - i, ad = Math.abs(d), el = beats[i];
      if (ad > 0.62) {
        if (el.style.visibility !== "hidden") {
          el.style.visibility = "hidden"; el.style.opacity = "0";
          el.classList.remove("in"); el.setAttribute("inert", "");
        }
        continue;
      }
      el.style.visibility = "visible";
      el.removeAttribute("inert");
      el.style.opacity = (1 - smooth(0.08, 0.42, ad)).toFixed(3);
      el.style.transform = "translate3d(0," + (-d * 1.4).toFixed(2) + "vh,0) scale(" +
        (1 + Math.max(-0.05, Math.min(0.16, d * 0.15))).toFixed(4) + ")";
      el.classList.toggle("in", ad < 0.34);
    }
    var a = Math.max(0, Math.min(beats.length - 1, Math.round(p)));
    if (a !== active) {
      active = a;
      if (hudTime) hudTime.textContent = beats[a].getAttribute("data-time") || "";
      if (hudLabel) hudLabel.textContent = beats[a].getAttribute("data-label") || "";
      for (var j = 0; j < ticks.length; j++) ticks[j].setAttribute("aria-current", j === a ? "true" : "false");
    }
  }

  var target = 0, cur = 0, vel = 0, last = 0, fps = 0, raf = 0;
  function measure() {
    var st = film.querySelector(".film__stage").getBoundingClientRect();
    VW = Math.round(st.width); VH = Math.round(st.height);
    mob = VW < 760;
    var dpr = Math.min(W.devicePixelRatio || 1, VW * VH > 1400000 ? 1.5 : 2);
    canvas.width = Math.round(VW * dpr); canvas.height = Math.round(VH * dpr);
    canvas.style.width = VW + "px"; canvas.style.height = VH + "px";
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(U.u_res, VW, VH);                  // every rect here is CSS pixels
    gl.uniform1f(U.u_dpr, canvas.width / Math.max(1, VW));
  }
  // Where the stage starts sticking, in document coordinates. offsetTop is
  // relative to .film (it is the positioned ancestor), and the stage's own rect
  // reads 0 while it is stuck — so measure the scroll track, which never moves.
  function filmTop() {
    return film.querySelector(".film__scroll").getBoundingClientRect().top + W.scrollY;
  }
  function progress() {
    return Math.max(0, Math.min(P.length - 1, (W.scrollY - filmTop()) / stepH()));
  }
  function frame(t) {
    var dt = Math.min(0.033, (t - last) / 1000 || 0.016); last = t;
    target = progress();
    var k = 40, c = 2 * Math.sqrt(k);
    vel += (k * (target - cur) - c * vel) * dt;
    cur += vel * dt;
    if (Math.abs(target - cur) < 0.0004 && Math.abs(vel) < 0.0015) { cur = target; vel = 0; }
    render(cur, t);
    paintBeats(cur);
    fps = fps ? fps * 0.9 + (1 / dt) * 0.1 : 1 / dt;
    W.__push = { p: cur, target: target, stopH: stepH(), fps: Math.round(fps),
                 loaded: Object.keys(textures).length, near: near };
    raf = near ? W.requestAnimationFrame(frame) : 0;
  }

  // load the plates only when the section is close, draw only while it is visible
  var warm = new IntersectionObserver(function (en) {
    if (!en[0].isIntersecting) return;
    warm.disconnect();
    measure();
    var wide = Math.round(VW * Math.min(W.devicePixelRatio || 1, 2));
    P.forEach(function (pl, i) {
      load(pl.id, pl.sizes, i === 0 ? wide : Math.round(wide * 0.8));
      (pl.layers || []).forEach(function (L, j) { load(pl.id + "-L" + j, L.sizes, Math.round(wide * 0.6)); });
    });
  }, { rootMargin: "120% 0px" });
  warm.observe(film);

  var vis = new IntersectionObserver(function (en) {
    near = en[0].isIntersecting;
    if (near && !raf) { measure(); cur = target = progress(); last = 0; raf = W.requestAnimationFrame(frame); }
  }, { rootMargin: "20% 0px" });
  vis.observe(film);

  W.addEventListener("resize", function () { if (near) measure(); }, { passive: true });
  W.addEventListener("orientationchange", function () { if (near) measure(); }, { passive: true });
})();
