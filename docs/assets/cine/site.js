/* Swarm — site behaviour.
 *
 * The page works without this file. What it adds, when it can:
 *
 *   one camera over five screens — it pushes through one of our officers into
 *   the next scene twice, then pulls back out of the door into the map of the
 *   GTA; the quote and call buttons travel from the first screen into the
 *   header, and from the header down into the form.
 *
 * One scroll clock (the page's own scroll, snapped by CSS), one spring for the
 * camera, one owner for every animated property. Content is never hidden:
 * copy that is off-stage is transparent, not removed, and focusing it brings
 * the camera to it.
 */
(function () {
  "use strict";
  var D = document, W = window, root = D.documentElement;

  /* ----------------------------------------------------------- always on */
  var yr = D.getElementById("yr");
  if (yr) yr.textContent = String(new Date().getFullYear());

  var burger = D.querySelector(".burger"), drawer = D.getElementById("drawer");
  function setDrawer(open) {
    if (!burger || !drawer) return;
    drawer.hidden = !open;                            // state and presentation change together
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    root.classList.toggle("is-locked", open);
  }
  if (burger && drawer) {
    burger.addEventListener("click", function () { setDrawer(drawer.hidden); });
    drawer.addEventListener("click", function (e) { if (e.target.closest("a")) setDrawer(false); });
    W.addEventListener("keydown", function (e) { if (e.key === "Escape") setDrawer(false); });
  }

  var form = D.querySelector("[data-form]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      if (form.querySelector('[name="company"]').value) return;          // honeypot
      var data = new FormData(form), sent = form.querySelector(".form__sent");
      var endpoint = form.getAttribute("data-endpoint");
      if (endpoint) {
        fetch(endpoint, { method: "POST", headers: { Accept: "application/json" }, body: data })
          .then(function () { if (sent) sent.hidden = false; })
          .catch(function () { if (sent) sent.hidden = false; });
        return;
      }
      // no form service yet: hand the request to the visitor's mail app
      var body = [];
      data.forEach(function (v, k) { if (k !== "company" && v) body.push(k + ": " + v); });
      W.location.href = "mailto:" + (form.getAttribute("data-to") || "dispatch@swarmprotective.ca") +
        "?subject=" + encodeURIComponent("Quote request — " + (data.get("service") || "security")) +
        "&body=" + encodeURIComponent(body.join("\n"));
      if (sent) sent.hidden = false;
    });
  }

  /* ------------------------------------------------------- can we film? */
  var reduce = W.matchMedia("(prefers-reduced-motion: reduce)");
  if (reduce.addEventListener) reduce.addEventListener("change", function () { W.location.reload(); });
  if (reduce.matches) return;

  var canvas = D.getElementById("stage"), data = D.getElementById("scene-data");
  if (!canvas || !data) return;
  var gl = null;
  try {
    gl = canvas.getContext("webgl2", { alpha: true, premultipliedAlpha: true, antialias: false,
                                       powerPreference: "high-performance" });
  } catch (e) { gl = null; }
  if (!gl) return;

  var VS =
    "#version 300 es\nin vec2 a;uniform vec4 u_rect;uniform vec2 u_res;out vec2 v;\n" +
    "void main(){vec2 p=u_rect.xy+a*u_rect.zw;vec2 c=(p/u_res)*2.0-1.0;gl_Position=vec4(c.x,-c.y,0.0,1.0);v=a;}";
  var FS =
    "#version 300 es\nprecision highp float;in vec2 v;out vec4 o;uniform sampler2D u_tex;\n" +
    "uniform float u_lod,u_alpha,u_feather,u_radial,u_dpr;uniform vec4 u_clip;uniform vec2 u_res;\n" +
    "void main(){vec4 c=texture(u_tex,v,u_lod);\n" +
    " if(u_lod>0.5){float t=exp2(u_lod)/900.0;\n" +
    "  c=0.25*(texture(u_tex,v+vec2(t,0.0),u_lod)+texture(u_tex,v-vec2(t,0.0),u_lod)\n" +
    "        +texture(u_tex,v+vec2(0.0,t),u_lod)+texture(u_tex,v-vec2(0.0,t),u_lod));}\n" +
    " vec2 p=vec2(gl_FragCoord.x/u_dpr,u_res.y-gl_FragCoord.y/u_dpr);float m;\n" +
    " if(u_radial>0.5){vec2 h=u_clip.zw*0.5;vec2 q=(p-(u_clip.xy+h))/max(h,vec2(1.0));m=1.0-smoothstep(0.18,1.0,length(q));}\n" +
    " else{vec2 d=min(p-u_clip.xy,u_clip.xy+u_clip.zw-p);m=smoothstep(0.0,1.0,clamp(min(d.x,d.y)/max(u_feather,0.5),0.0,1.0));}\n" +
    " o=c*(u_alpha*m);}";
  function sh(t, s) { var x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); return x; }
  var prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
  gl.bindAttribLocation(prog, 0, "a");
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  var U = {};
  ["u_rect", "u_res", "u_tex", "u_lod", "u_alpha", "u_feather", "u_radial", "u_dpr", "u_clip"]
    .forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, 0, 1, 0, 0, 1, 1, 1]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
  gl.clearColor(0, 0, 0, 0);

  root.classList.add("fx");
  canvas.addEventListener("webglcontextlost", function () {  // renderer failure: back to the static page
    root.classList.remove("fx", "lit");
  });

  /* ------------------------------------------------------------ plates */
  var SCENE = JSON.parse(data.textContent), PL = {};
  SCENE.plates.forEach(function (p) { PL[p.id] = p; });
  // The camera draws the page's own photographs — one download each, at the
  // size the browser already chose for this screen. (It used to fetch its own
  // copies, and a size-picking bug made those the largest files.)
  var SRC = {
    crew: D.querySelector(".stop--home .stop__img"),
    event: D.querySelector(".stop--services .stop__img"),
    door: D.querySelector(".split__half:first-child .split__img"),
    detail: D.querySelector(".split__half:last-child .split__img"),
  };
  var tex = {};
  function upload(id) {
    var img = SRC[id];
    if (!img || !img.complete || !img.naturalWidth) return;
    var t = tex[id] || gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    tex[id] = t;
    if (id === "crew") root.classList.add("lit");
    kick();
  }
  Object.keys(SRC).forEach(function (id) {
    var img = SRC[id];
    if (!img) return;
    img.loading = "eager";                           // every one of them is a scroll away
    img.addEventListener("load", function () { upload(id); });   // also a new srcset pick after a resize
    upload(id);
  });

  /* ------------------------------------------------------------ camera */
  var VW = 1, VH = 1, DPR = 1, mob = false, tall = false, stepH = 1;   // tall: portrait screens stack the split
  function smooth(a, b, x) { var t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); }
  function ease(f) { return 0.25 * f + 0.75 * f * f * (3 - 2 * f); }
  function cover(pl) {
    var fc = mob ? pl.focalM : pl.focal;
    var s = Math.max(VW / pl.w, VH / pl.h);
    var x = VW / 2 - fc[0] * pl.w * s, y = VH / 2 - fc[1] * pl.h * s;
    return { s: s, x: Math.min(0, Math.max(VW - pl.w * s, x)), y: Math.min(0, Math.max(VH - pl.h * s, y)) };
  }
  // zoom from A to B in log scale around the one screen point both agree on
  function between(A, B, f) {
    var s = A.s * Math.pow(B.s / A.s, f);
    var px = (B.x - A.x) / (A.s - B.s), py = (B.y - A.y) / (A.s - B.s);
    var Fx = A.s * px + A.x, Fy = A.s * py + A.y;
    return { s: s, x: Fx - s * px, y: Fy - s * py, F: { x: Fx, y: Fy } };
  }
  function draw(id, T, o, aDoor, aSide) {
    var pl = PL[id];
    if (pl.halves) {
      // The split is the screen itself, halved — side by side or stacked — and
      // each 4:5 photo is cover-fitted into its own half, like the page's CSS.
      var row = pl.halves === "row", hw = row ? pl.w / 2 : pl.w, hh = row ? pl.h : pl.h / 2;
      half("door", 0, 0, aDoor == null ? 1 : aDoor, 0.22);
      half("detail", row ? hw : 0, row ? 0 : hh, aSide == null ? 1 : aSide, 0.3);
      return;
    }
    drawTex(id, [T.x, T.y, pl.w * T.s, pl.h * T.s], o, 1);

    function half(tid, ox, oy, a, fy) {
      var ar = 0.8, pw, ph, px = 0, py = 0;
      if (hw / hh > ar) { pw = hw; ph = hw / ar; py = (hh - ph) * fy; }    // crop from below: keep heads
      else { ph = hh; pw = hh * ar; px = (hw - pw) / 2; }
      var clip = [T.x + T.s * ox, T.y + T.s * oy, T.s * hw, T.s * hh];
      if (o.clip) clip = cut(clip, o.clip);
      drawTex(tid, [T.x + T.s * (ox + px), T.y + T.s * (oy + py), T.s * pw, T.s * ph],
              { lod: o.lod, alpha: o.alpha, clip: clip, feather: o.clip ? o.feather : 0.5 }, a);
    }
  }
  function drawTex(id, r, o, a) {
    if (!tex[id] || a <= 0.001) return;
    gl.uniform4f(U.u_rect, r[0], r[1], r[2], r[3]);
    gl.uniform1f(U.u_lod, o.lod || 0);
    gl.uniform1f(U.u_alpha, (o.alpha == null ? 1 : o.alpha) * a);
    var c = o.clip || [-9e4, -9e4, 1.8e5, 1.8e5];
    gl.uniform4f(U.u_clip, c[0], c[1], c[2], c[3]);
    gl.uniform1f(U.u_feather, o.feather || 0.5);
    gl.uniform1f(U.u_radial, o.radial ? 1 : 0);
    gl.bindTexture(gl.TEXTURE_2D, tex[id]);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  function box(pl, T, r) { return [T.x + T.s * r[0] * pl.w, T.y + T.s * r[1] * pl.h, T.s * r[2] * pl.w, T.s * r[3] * pl.h]; }
  function cut(a, b) {
    var x = Math.max(a[0], b[0]), y = Math.max(a[1], b[1]);
    return [x, y, Math.max(0, Math.min(a[0] + a[2], b[0] + b[2]) - x), Math.max(0, Math.min(a[1] + a[3], b[1] + b[3]) - y)];
  }

  // push through the opening in one plate into the next
  function push(pid, cid, portal, f) {
    var pl = PL[pid], ch = PL[cid], A = cover(pl), C = cover(ch), R = portal.rect;
    var m = R[2] * pl.w / ch.w;
    var B = { s: C.s / m, x: 0, y: 0 };
    B.x = C.x - B.s * R[0] * pl.w; B.y = C.y - B.s * R[1] * pl.h;
    var T = f > 0 ? between(A, B, f) : A;
    draw(pid, T, { lod: 1.4 * smooth(0.55, 1, f), alpha: 1 - smooth(0.86, 1, f) });
    if (f <= 0) return;
    var CT = { s: T.s * m, x: T.x + T.s * R[0] * pl.w, y: T.y + T.s * R[1] * pl.h };
    // the opening is nearer than the room behind it, so it opens faster and
    // clears the frame before the next scene fills it (solved, not tuned)
    var z = B.s / A.s, a0 = box(pl, A, portal.aper);
    var e = Math.max(1.05, Math.min(6, Math.log(Math.hypot(VW, VH) / Math.max(20, Math.min(a0[2], a0[3]))) / (0.76 * Math.log(z))));
    var ga = Math.pow(T.s / A.s, e - 1), op = box(pl, T, portal.aper);
    var cx = op[0] + op[2] / 2, cy = op[1] + op[3] / 2;
    op = [cx - op[2] * ga / 2, cy - op[3] * ga / 2, op[2] * ga, op[3] * ga];
    var clip = cut(op, [CT.x, CT.y, ch.w * CT.s, ch.h * CT.s]);
    var fe = smooth(0, 0.5, f);
    if (!mob && !ch.halves && f < 0.6) {            // the opening glows a moment before it opens
      var k = 3.2, hw = clip[2] * k, hh = clip[3] * k;
      gl.blendFunc(gl.ONE, gl.ONE);
      draw(cid, { s: CT.s * k, x: cx + (CT.x - cx) * k, y: cy + (CT.y - cy) * k },
           { lod: 7.5, alpha: 0.22 * smooth(0.02, 0.2, f) * (1 - smooth(0.2, 0.6, f)),
             clip: [cx - hw / 2, cy - hh / 2, hw, hh], radial: true });
      gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    }
    draw(cid, CT, { lod: 5 * (1 - fe), alpha: smooth(0.03, 0.24, f),
                    clip: clip, feather: 0.9 * Math.min(clip[2], clip[3]) * 0.5 * (1 - smooth(0.6, 0.98, f)) });
  }

  // pull back out of the door until it is a pin on the map
  var pin = { x: 0, y: 0 }, splitPortal = null;
  function pullOut(f) {
    var id = "split", pl = PL[id];
    var A = cover(pl), tw = VW * (mob ? 0.22 : 0.1);
    var B = { s: tw / pl.w, x: 0, y: 0 };
    B.x = pin.x - B.s * pl.anchor[0] * pl.w; B.y = pin.y - B.s * pl.anchor[1] * pl.h;
    var T = f > 0 ? between(A, B, f) : A;
    // the side photo goes first; the doorman is the last thing you see, landing on Toronto
    draw(id, T, { lod: 1.2 * smooth(0.5, 1, f) }, 1 - smooth(0.62, 0.97, f), 1 - smooth(0.2, 0.58, f));
  }

  /* -------------------------------------------------------------- DOM */
  var stops = [].slice.call(D.querySelectorAll(".track .stop"));
  var copies = stops.map(function (s) { return s.querySelector(".stop__copy"); });
  var split = D.querySelector(".split"), map = D.querySelector(".map"), gm = D.querySelector(".gm");
  var hq = D.getElementById("gm-hq"), shade = D.querySelector(".shade");
  var heroCta = D.getElementById("hero-cta"), mastCta = D.getElementById("mast-cta");
  var formCta = D.getElementById("form-cta"), contact = D.getElementById("contact");
  var home0 = { x: 0, y: 0, w: 1 }, mast0 = { x: 0, y: 0, w: 1 };

  function centre(el) { var r = el.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width }; }

  function measure() {
    VW = W.innerWidth; VH = W.innerHeight; mob = VW < 760; tall = VH > VW;
    DPR = Math.min(W.devicePixelRatio || 1, VW * VH > 1600000 ? 1.5 : 2);
    canvas.width = Math.round(VW * DPR); canvas.height = Math.round(VH * DPR);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(U.u_res, VW, VH);                   // every rect here is in CSS pixels
    gl.uniform1f(U.u_dpr, canvas.width / VW);
    stepH = stops[0].getBoundingClientRect().height || VH;
    // the split plate is this screen: halves side by side, or stacked when upright
    var sp = PL.split;
    sp.w = VW; sp.h = VH; sp.halves = tall ? "column" : "row"; sp.anchor = tall ? [0.5, 0.25] : [0.25, 0.5];
    var ev = PL.event, ap = (tall ? ev.portalM : ev.portal).aper;
    var pw = Math.max(ap[2], ap[3] * ev.h / ev.w * sp.w / sp.h) * 1.6, ph = pw * ev.w / ev.h * sp.h / sp.w;
    splitPortal = { aper: ap, rect: [ap[0] + ap[2] / 2 - pw / 2, ap[1] + ap[3] / 2 - ph / 2, pw, ph] };
    if (gm) {
      gm.setAttribute("viewBox", gm.getAttribute(tall ? "data-narrow" : "data-full"));
      gm.style.transform = "none";
    }
    [heroCta, mastCta].forEach(function (el) { if (el) el.style.transform = "none"; });
    if (hq) pin = centre(hq);
    if (gm && hq) {                                  // the map scales about Toronto, so the pin never moves
      var g = gm.getBoundingClientRect();
      gm.style.transformOrigin = (pin.x - g.left) + "px " + (pin.y - g.top) + "px";
    }
    if (heroCta) home0 = centre(heroCta);
    if (mastCta) mast0 = centre(mastCta);
    cur = target = progress(); vel = 0;
  }

  function progress() { return Math.max(0, Math.min(stops.length - 1, W.scrollY / stepH)); }
  function arrival() { return Math.max(0, Math.min(1, (W.scrollY - (stops.length - 1) * stepH) / stepH)); }

  function paint(p, q) {
    gl.clear(gl.COLOR_BUFFER_BIT);
    if (p < 1) push("crew", "event", PL.crew.portal, ease(p));
    else if (p < 2) push("event", "split", splitPortal, ease(p - 1));
    else if (p < 3) pullOut(ease(p - 2));
    canvas.dataset.frame = p.toFixed(3);

    // copy: fades by distance, holds still while it can be read
    for (var i = 0; i < copies.length; i++) {
      var el = copies[i]; if (!el) continue;
      var d = p - i, ad = Math.abs(d), td = d > 0 ? Math.max(0, d - 0.08) : Math.min(0, d + 0.08);
      var o = 1 - (i === stops.length - 1 && d < 0 ? smooth(0.18, 0.62, ad) : smooth(0.12, 0.45, ad));
      if (i === stops.length - 1) o *= 1 - smooth(0.2, 0.8, q);
      el.style.opacity = o.toFixed(3);
      el.style.transform = i === 0 ? "none" :
        "translate3d(0," + (-td * 5).toFixed(2) + "vh,0) scale(" + (1 + Math.max(-0.05, Math.min(0.08, td * 0.08))).toFixed(4) + ")";
      el.classList.toggle("is-on", ad < 0.3 && o > 0.5);
    }
    if (split) split.style.opacity = (1 - smooth(0.12, 0.42, Math.abs(p - 2))).toFixed(3);

    // the map: arrives behind the shrinking door, holds, then recedes for the crew
    if (map) {
      var mo = 0, ms = 1;
      if (p >= 2 && p < 3) { var f = ease(p - 2); mo = smooth(0.12, 0.55, f); ms = 1 + 1.1 * (1 - smooth(0, 1, f)); }
      // the map never leaves: it settles back to a faint base under the crew,
      // so no scroll depth between the two screens is ever an empty frame
      else if (p >= 3) { var g = p - 3; mo = 1 - 0.86 * smooth(0.1, 0.75, g); ms = 1 - 0.1 * smooth(0, 1, g); }
      map.style.opacity = mo.toFixed(3);
      if (gm) gm.style.transform = "scale(" + ms.toFixed(4) + ")";
      map.style.setProperty("--route", (1 - smooth(0.55, 1, p >= 3 ? 1 : Math.max(0, p - 2))).toFixed(3));
    }
    if (shade) {
      shade.style.opacity = (1 - smooth(2.25, 2.7, p)).toFixed(3);
      shade.style.setProperty("--side", (1 - smooth(0.2, 0.6, Math.abs(p - 1))).toFixed(3));
    }

    // the ask travels: first screen -> header -> form
    if (heroCta && mastCta) {
      var e1 = smooth(0, 0.45, p);
      heroCta.style.transform = "translate3d(" + ((mast0.x - home0.x) * e1).toFixed(1) + "px," +
        ((mast0.y - home0.y) * e1).toFixed(1) + "px,0) scale(" + (1 - (1 - mast0.w / home0.w) * e1).toFixed(3) + ")";
      heroCta.style.opacity = (1 - smooth(0.25, 0.45, p)).toFixed(3);
      // down into the form — but only when the form's own buttons will be on
      // screen to receive them; on a phone they are below the fold, so the
      // header buttons simply hand over and fade instead of crossing the heading
      var mo2 = smooth(0.3, 0.55, p), dx = 0, dy = 0;
      if (q > 0 && formCta) {
        var fr = formCta.getBoundingClientRect(), landY = fr.top + fr.height / 2 - (1 - q) * VH;
        if (landY < VH - 20) {
          var fc = centre(formCta), e2 = smooth(0.1, 0.75, q);
          dx = (fc.x - mast0.x) * e2; dy = (fc.y - mast0.y) * e2;
          mo2 *= 1 - smooth(0.4, 0.7, q);
        } else {
          mo2 *= 1 - smooth(0.15, 0.45, q);
        }
      }
      mastCta.style.opacity = mo2.toFixed(3);
      mastCta.style.transform = "translate3d(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px,0)";
      mastCta.style.pointerEvents = mo2 > 0.5 ? "auto" : "none";
      if (formCta) {
        var fo = smooth(0.45, 0.85, q);
        formCta.style.opacity = fo.toFixed(3);
        formCta.style.transform = "translate3d(0," + (-(1 - fo) * 28).toFixed(1) + "px,0)";
      }
    }
  }

  /* ------------------------------------------------------------- clock */
  var cur = 0, vel = 0, target = 0, last = 0, raf = 0, qPrev = -1, fps = 0;
  function frame(t) {
    var dt = Math.min(0.033, (t - last) / 1000 || 0.016); last = t;
    target = progress();
    var k = 42, c = 2 * Math.sqrt(k);
    vel += (k * (target - cur) - c * vel) * dt; cur += vel * dt;
    var settled = Math.abs(target - cur) < 0.0005 && Math.abs(vel) < 0.002;
    if (settled) { cur = target; vel = 0; }
    var q = arrival();
    paint(cur, q);
    fps = fps ? fps * 0.9 + 0.1 / dt : 1 / dt;
    W.__swarm = { p: cur, target: target, q: q, stepH: stepH, fps: Math.round(fps), loaded: Object.keys(tex).length };
    if (settled && q === qPrev) { raf = 0; return; }
    qPrev = q;
    raf = W.requestAnimationFrame(frame);
  }
  function kick() { if (!raf) { last = 0; raf = W.requestAnimationFrame(frame); } }

  W.addEventListener("scroll", kick, { passive: true });
  W.addEventListener("resize", function () { measure(); kick(); }, { passive: true });
  W.addEventListener("orientationchange", function () { measure(); kick(); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(function () { measure(); kick(); });

  // keyboard: focusing something on another screen brings the camera to it
  D.addEventListener("focusin", function (e) {
    var s = e.target.closest && e.target.closest(".track .stop");
    if (!s) return;
    var i = stops.indexOf(s);
    if (i >= 0 && Math.round(progress()) !== i) W.scrollTo({ top: i * stepH, behavior: "smooth" });
  });

  measure();
  kick();
})();
