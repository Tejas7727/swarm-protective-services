/* Swarm — the push.
 *
 * One camera, one night. Every scene is a plate; inside each plate is a
 * doorway (the "portal") holding the next plate. Scroll pushes the camera
 * through the doorway, so the background of one stop becomes the foreground
 * of the next. Nothing is ever replaced — the camera just keeps moving.
 *
 * Scroll snapping is the browser's (CSS scroll-snap), so a flick always lands
 * on a composed frame; a critically damped spring drives the render, so the
 * camera arrives a beat after the scroll and never jumps.
 */
(function () {
  "use strict";

  var D = document, W = window, root = D.documentElement;
  var data = D.getElementById("scene-data");
  if (!data) return;
  var SCENE = JSON.parse(data.textContent);
  var P = SCENE.plates, N = P.length + 1;          // + the booking stop

  var reduced = W.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canvas = D.getElementById("stage");
  var gl = null;
  if (!reduced && canvas) {
    try {
      gl = canvas.getContext("webgl2", { antialias: false, alpha: false, powerPreference: "high-performance" });
    } catch (e) { gl = null; }
  }
  if (!gl) { root.classList.add("plain"); return; }
  root.classList.add("fx");

  /* ---------------------------------------------------------------- gl */
  var VS =
    "#version 300 es\n" +
    "in vec2 a;uniform vec4 u_rect;uniform vec2 u_res;out vec2 v;\n" +
    "void main(){vec2 p=u_rect.xy+a*u_rect.zw;vec2 c=(p/u_res)*2.0-1.0;\n" +
    "gl_Position=vec4(c.x,-c.y,0.0,1.0);v=a;}";
  var FS =
    "#version 300 es\nprecision highp float;\n" +
    "in vec2 v;out vec4 o;uniform sampler2D u_tex;uniform float u_lod,u_alpha,u_exp,u_feather;\n" +
    "uniform vec3 u_tint;uniform vec4 u_clip;uniform vec2 u_res;\n" +
    "void main(){vec4 c=texture(u_tex,v,u_lod);\n" +
    " if(u_lod>0.5){float t=exp2(u_lod)/900.0;\n" +
    "  c=0.25*(texture(u_tex,v+vec2(t,0.0),u_lod)+texture(u_tex,v-vec2(t,0.0),u_lod)\n" +
    "        +texture(u_tex,v+vec2(0.0,t),u_lod)+texture(u_tex,v-vec2(0.0,t),u_lod));}\n" +
    " vec2 p=vec2(gl_FragCoord.x,u_res.y-gl_FragCoord.y);\n" +
    " vec2 d=min(p-u_clip.xy,u_clip.xy+u_clip.zw-p);\n" +
    " float m=smoothstep(0.0,1.0,clamp(min(d.x,d.y)/max(u_feather,0.5),0.0,1.0));\n" +
    " o=vec4(c.rgb*u_tint*u_exp,c.a)*(u_alpha*m);}";

  function shader(type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src); gl.compileShader(s);
    return s;
  }
  var prog = gl.createProgram();
  gl.attachShader(prog, shader(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, FS));
  gl.bindAttribLocation(prog, 0, "a");
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { root.classList.add("plain"); root.classList.remove("fx"); return; }
  gl.useProgram(prog);

  var U = {};
  ["u_rect", "u_res", "u_tex", "u_lod", "u_alpha", "u_exp", "u_tint", "u_clip", "u_feather"]
    .forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });

  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, 0, 1, 0, 0, 1, 1, 1]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
  gl.clearColor(0.031, 0.035, 0.039, 1);

  // one white pixel, for light: the night ends in a bloom, not a dissolve
  var WHITE = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, WHITE);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
                new Uint8Array([255, 255, 255, 255]));
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);

  function pick(sizes, target) {                   // smallest size that still covers
    var best = sizes[0];
    for (var i = sizes.length - 1; i >= 0; i--) if (sizes[i].w >= target) best = sizes[i];
    return best;
  }

  var textures = {}, pending = {};
  function load(key, sizes, target) {
    if (textures[key] || pending[key]) return;
    pending[key] = 1;
    var entry = pick(sizes, target);
    var img = new Image();
    img.decoding = "async";
    img.src = entry.src;
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
      if (key === "p0") root.classList.add("lit");
      need = 2;
    };
    img.onerror = function () { pending[key] = 0; };
  }

  /* ------------------------------------------------------------- camera */
  var VW = 0, VH = 0, DPR = 1, mob = false, stopH = 1;

  function cover(pl, focal) {
    var s = Math.max(VW / pl.w, VH / pl.h);
    var x = VW / 2 - focal[0] * pl.w * s, y = VH / 2 - focal[1] * pl.h * s;
    return { s: s, x: Math.min(0, Math.max(VW - pl.w * s, x)), y: Math.min(0, Math.max(VH - pl.h * s, y)) };
  }
  function focalOf(pl) { return mob && pl.focalM ? pl.focalM : pl.focal; }

  function segment(k, f) {
    var pl = P[k], A = cover(pl, focalOf(pl));
    if (!pl.portal) return { T: A, A: A, F: { x: VW / 2, y: VH / 2 }, m: 0 };
    var ch = P[pl.portal.child], C = cover(ch, focalOf(ch));
    var R = pl.portal.rect;
    var rx = R[0] * pl.w, ry = R[1] * pl.h, rw = R[2] * pl.w;
    var m = rw / ch.w;
    var Bs = C.s / m, Bx = C.x - Bs * rx, By = C.y - Bs * ry;
    var s = A.s * Math.pow(Bs / A.s, f);
    var px = (Bx - A.x) / (A.s - Bs), py = (By - A.y) / (A.s - Bs);
    var Fx = A.s * px + A.x, Fy = A.s * py + A.y;
    return { T: { s: s, x: Fx - s * px, y: Fy - s * py }, A: A, F: { x: Fx, y: Fy },
             m: m, A0: Bs / A.s };
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

  var pointer = { x: 0, y: 0, tx: 0, ty: 0 };

  function render(p, t) {
    var k = Math.min(P.length - 1, Math.floor(p)), f = ease(Math.min(1, Math.max(0, p - k)));
    var seg = segment(k, f), T = { s: seg.T.s, x: seg.T.x, y: seg.T.y };
    var rest = 1 - smooth(0, 0.3, Math.abs(p - Math.round(p)) * 2);

    // past the last plate the camera keeps drifting into the sunrise
    var over = Math.max(0, p - (P.length - 1));
    if (over > 0) {
      var z = 1 + over * 0.16;
      T.s *= z; T.x = VW / 2 + (T.x - VW / 2) * z; T.y = VH * 0.42 + (T.y - VH * 0.42) * z;
    }

    var breathe = 1 + Math.sin(t * 0.00031) * 0.0045;
    T.s *= breathe;
    T.x = VW / 2 + (T.x - VW / 2) * breathe;
    T.y = VH / 2 + (T.y - VH / 2) * breathe;
    T.x += pointer.x * 13 * rest;
    T.y += pointer.y * 8 * rest;

    gl.clear(gl.COLOR_BUFFER_BIT);
    var pl = P[k], g = pl.grade, leaving = pl.portal ? f : 0;
    if (textures["p" + k]) {
      drawPlate(textures["p" + k], pl, T, {
        tint: g.tint, exp: g.exp * (1 - 0.12 * smooth(0.55, 1, leaving)),
        lod: 1.3 * smooth(0.55, 1, leaving), alpha: 1 - smooth(0.86, 1, leaving),
      });
    }

    // the scene inside this one, seen through the doorway
    var clip = null, childT = null;
    if (pl.portal && textures["p" + pl.portal.child]) {
      var ch = P[pl.portal.child], R = pl.portal.rect;
      childT = { s: T.s * seg.m || T.s * (R[2] * pl.w / ch.w),
                 x: T.x + T.s * R[0] * pl.w, y: T.y + T.s * R[1] * pl.h };
      // The doorway is nearer than the room beyond it, so it opens faster than
      // the room grows, and passes the camera before the room fills the frame.
      // How much faster is solved, not guessed: it must clear the viewport by
      // `cross` of the way through the push, whatever the screen shape is.
      var op = clipRect(pl, T, pl.portal.aper);
      var e = 1;
      if (seg.A0 > 1.0001) {
        var rest0 = clipRect(pl, seg.A, pl.portal.aper);
        var G = Math.hypot(VW, VH) / Math.max(20, Math.min(rest0[2], rest0[3]));
        e = Math.log(G) / ((pl.portal.cross || 0.76) * Math.log(seg.A0));
        e = Math.max(1.05, Math.min(6, e));
      }
      var ga = Math.pow(T.s / seg.A.s, e - 1);          // extra opening, about itself
      var ocx = op[0] + op[2] / 2, ocy = op[1] + op[3] / 2;
      op = [ocx - op[2] * ga / 2, ocy - op[3] * ga / 2, op[2] * ga, op[3] * ga];
      // never wider than the scene behind it, or its own edge would show
      clip = intersect(op, [childT.x, childT.y, ch.w * childT.s, ch.h * childT.s]);
      var fe = smooth(0, 0.5, f);
      var soft = 1 - smooth(0.6, 0.98, f);              // the opening hardens as we arrive
      // a soft halo of the next scene's own light, so the eye knows where the
      // camera is about to go before it moves
      if (f < 0.62) {
        var hw = clip[2] * 3.1, hh = clip[3] * 3.1;
        gl.blendFunc(gl.ONE, gl.ONE);
        drawPlate(textures["p" + pl.portal.child], ch, childT, {
          tint: ch.grade.tint, exp: ch.grade.exp * 0.95, lod: 7.5, alpha: 0.2 * (1 - smooth(0.1, 0.5, f)),
          clip: [clip[0] + clip[2] / 2 - hw / 2, clip[1] + clip[3] / 2 - hh / 2, hw, hh],
          feather: Math.min(hw, hh) * 0.5,
        });
        gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      }
      // at rest the next scene is only a glow in the doorway (the halo above);
      // it resolves into a place as the camera starts to move
      drawPlate(textures["p" + pl.portal.child], ch, childT, {
        tint: ch.grade.tint, exp: ch.grade.exp * (0.6 + 0.4 * fe),
        lod: 5.0 * (1 - fe), alpha: smooth(0.04, 0.26, f) * (0.86 + 0.14 * fe),
        clip: clip,
        feather: pl.portal.feather * Math.min(clip[2], clip[3]) * 0.5 * soft,
      });
      // night into morning is a bloom of light, not a window in a wall
      if (pl.portal.flood) {
        var fl = Math.sin(Math.PI * smooth(0.18, 0.95, f)) * 0.92;
        if (fl > 0.002) {
          gl.uniform4f(U.u_rect, 0, 0, VW, VH);
          gl.uniform1f(U.u_lod, 0);
          gl.uniform1f(U.u_alpha, fl);
          gl.uniform1f(U.u_exp, 1);
          gl.uniform3f(U.u_tint, pl.portal.flood[0], pl.portal.flood[1], pl.portal.flood[2]);
          gl.uniform4f(U.u_clip, -9e4, -9e4, 1.8e5, 1.8e5);
          gl.uniform1f(U.u_feather, 0.5);
          gl.bindTexture(gl.TEXTURE_2D, WHITE);
          gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        }
      }
      // and the one inside that, so depth never bottoms out
      if (ch.portal && textures["p" + ch.portal.child] && clip[2] > 40) {
        var gc = P[ch.portal.child], R2 = ch.portal.rect;
        var gT = { s: childT.s * (R2[2] * ch.w / gc.w),
                   x: childT.x + childT.s * R2[0] * ch.w, y: childT.y + childT.s * R2[1] * ch.h };
        var c2 = intersect(clip, clipRect(ch, childT, ch.portal.aper));
        if (c2[2] > 2 && c2[3] > 2) {
          drawPlate(textures["p" + ch.portal.child], gc, gT, {
            tint: gc.grade.tint, exp: gc.grade.exp * 0.7, lod: 5.6, alpha: 0.9,
            clip: c2, feather: Math.min(c2[2], c2[3]) * 0.4,
          });
        }
      }
    }

    // people in front of the camera pass it faster than the street behind them
    if (pl.layers && pl.layers.length && seg.F) {
      for (var i = 0; i < pl.layers.length; i++) {
        var L = pl.layers[i], key = "l" + k + "_" + i;
        if (!textures[key]) continue;
        var lx = T.x + T.s * L.rect[0] * pl.w, ly = T.y + T.s * L.rect[1] * pl.h;
        var lw = T.s * L.rect[2] * pl.w, lh = T.s * L.rect[3] * pl.h;
        var gz = Math.pow(T.s / seg.A.s, L.depth - 1);
        var ox = pointer.x * 30 * rest, oy = pointer.y * 16 * rest;
        var rx2 = seg.F.x + (lx - seg.F.x) * gz + ox, ry2 = seg.F.y + (ly - seg.F.y) * gz + oy;
        var a = 1 - smooth(L.fade[0], L.fade[1], f);
        if (a <= 0.002) continue;
        gl.uniform4f(U.u_rect, rx2, ry2, lw * gz, lh * gz);
        gl.uniform1f(U.u_lod, 3.4 * smooth(L.fade[0], L.fade[1] + 0.06, f));
        gl.uniform1f(U.u_alpha, a);
        gl.uniform1f(U.u_exp, g.exp);
        gl.uniform3f(U.u_tint, g.tint[0], g.tint[1], g.tint[2]);
        gl.uniform4f(U.u_clip, -9e4, -9e4, 1.8e5, 1.8e5);
        gl.uniform1f(U.u_feather, 0.5);
        gl.bindTexture(gl.TEXTURE_2D, textures[key]);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      }
    }
  }

  /* -------------------------------------------------------------- copy */
  var stops = [].slice.call(D.querySelectorAll(".stop"));
  var hud = D.getElementById("hud");
  var hudTime = hud && hud.querySelector("[data-time]");
  var hudLabel = hud && hud.querySelector("[data-label]");
  var ticks = [].slice.call(D.querySelectorAll(".tick"));
  var active = -1;

  function paintCopy(p) {
    for (var i = 0; i < stops.length; i++) {
      var d = p - i, ad = Math.abs(d);
      var el = stops[i], boxes = el.children;
      var hide = ad > 0.62;
      if (hide) el.setAttribute("inert", ""); else el.removeAttribute("inert");
      var o = 1 - smooth(0.08, 0.42, ad);
      var tf = "translate3d(0," + (-d * 1.6).toFixed(2) + "vh,0) scale(" +
        (1 + Math.max(-0.06, Math.min(0.18, d * 0.17))).toFixed(4) + ")";
      for (var b = 0; b < boxes.length; b++) {
        var box = boxes[b];
        if (hide) {
          if (box.style.visibility !== "hidden") {
            box.style.visibility = "hidden"; box.style.opacity = "0";
            box.classList.remove("in");
          }
          continue;
        }
        box.style.visibility = "visible";
        box.style.opacity = o.toFixed(3);
        box.style.transform = tf;
        box.classList.toggle("in", ad < 0.34);
      }
    }
    var a = Math.max(0, Math.min(stops.length - 1, Math.round(p)));
    if (a !== active) {
      active = a;
      var el2 = stops[a];
      if (hudTime) hudTime.textContent = el2.getAttribute("data-time") || "";
      if (hudLabel) hudLabel.textContent = el2.getAttribute("data-label") || "";
      if (hud) hud.classList.toggle("hud--live", a === 0);
      for (var j = 0; j < ticks.length; j++) ticks[j].setAttribute("aria-current", j === a ? "true" : "false");
      root.setAttribute("data-stop", el2.id || String(a));
    }
  }

  /* ------------------------------------------------------------- drive */
  var target = 0, cur = 0, vel = 0, last = 0, need = 2, fps = 0;

  function measure() {
    VW = W.innerWidth; VH = W.innerHeight;
    DPR = Math.min(W.devicePixelRatio || 1, VW * VH > 1600000 ? 1.5 : 2);
    mob = VW < 760;
    canvas.width = Math.round(VW * DPR); canvas.height = Math.round(VH * DPR);
    canvas.style.width = VW + "px"; canvas.style.height = VH + "px";
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(U.u_res, canvas.width, canvas.height);
    stopH = stops[0] ? stops[0].getBoundingClientRect().height : VH;
    var wide = Math.round(VW * DPR);
    load("p0", P[0].sizes, wide);
    if (P[0].layers[0]) load("l0_0", P[0].layers[0].sizes, Math.round(wide * 0.6));
    need = 2;
  }

  function progress() {
    var y = W.scrollY || W.pageYOffset || 0;
    return Math.max(0, Math.min(N - 1, y / Math.max(1, stopH)));
  }

  function frame(t) {
    var dt = Math.min(0.033, (t - last) / 1000 || 0.016); last = t;
    target = progress();
    var k = 40, c = 2 * Math.sqrt(k);
    vel += (k * (target - cur) - c * vel) * dt;
    cur += vel * dt;
    if (Math.abs(target - cur) < 0.0004 && Math.abs(vel) < 0.0015) { cur = target; vel = 0; }
    // the camera always renders (pointer parallax and the breath keep moving)
    pointer.x += (pointer.tx - pointer.x) * Math.min(1, dt * 6);
    pointer.y += (pointer.ty - pointer.y) * Math.min(1, dt * 6);
    render(cur, t);
    paintCopy(cur);
    // the camera's playhead, published for the book detector and for tests:
    // nothing else about a canvas changes when the picture inside it does
    canvas.dataset.frame = cur.toFixed(3);
    fps = fps ? fps * 0.9 + (1 / dt) * 0.1 : 1 / dt;
    W.__push = { p: cur, target: target, stopH: stopH, fps: Math.round(fps),
                 loaded: Object.keys(textures).length };
    // pull the rest of the night in once the first frame is up
    if (t > 600) {
      for (var i = 1; i < P.length; i++) load("p" + i, P[i].sizes, Math.round(VW * DPR * 0.8));
    }
    W.requestAnimationFrame(frame);
  }

  W.addEventListener("resize", measure, { passive: true });
  W.addEventListener("orientationchange", measure, { passive: true });
  W.addEventListener("pointermove", function (e) {
    if (mob) return;
    pointer.tx = (e.clientX / VW - 0.5) * 2;
    pointer.ty = (e.clientY / VH - 0.5) * 2;
  }, { passive: true });
  W.addEventListener("blur", function () { pointer.tx = pointer.ty = 0; });

  measure();
  cur = target = progress();
  paintCopy(cur);
  W.requestAnimationFrame(frame);

  /* -------------------------------------------------------- interaction */
  ticks.forEach(function (b, i) {
    b.addEventListener("click", function () {
      W.scrollTo({ top: i * stopH, behavior: "smooth" });
    });
  });

  var modes = { venue: "A venue", event: "An event", person: "A person" };
  var reply = D.getElementById("reply");
  [].slice.call(D.querySelectorAll(".chip")).forEach(function (chip) {
    chip.addEventListener("click", function () {
      var m = chip.getAttribute("data-mode");
      root.setAttribute("data-mode", m);
      [].slice.call(D.querySelectorAll(".chip")).forEach(function (c) {
        c.setAttribute("aria-pressed", c === chip ? "true" : "false");
      });
      [].slice.call(D.querySelectorAll("[data-" + m + "]")).forEach(function (el) {
        var next = el.getAttribute("data-" + m);
        if (!next || el.textContent === next) return;
        el.style.opacity = "0";
        setTimeout(function () { el.textContent = next; el.style.opacity = ""; }, 190);
      });
      var sel = D.getElementById("q-service");
      if (sel) { sel.value = modes[m] === "A person" ? "Close protection" : (m === "venue" ? "Venue / bar" : "Event"); }
      if (reply) {
        reply.textContent = "Copy — " + modes[m].toLowerCase().replace(/^an? /, "") + ". Here is the night.";
        reply.classList.add("on");
      }
      setTimeout(function () { W.scrollTo({ top: stopH, behavior: "smooth" }); }, 520);
    });
  });

})();

/* ---------------------------------------------------------------------- ui
 * Everything below runs whether or not the film does: the quote dialog, the
 * clock, the year. A browser without WebGL still gets a working site.
 */
(function () {
  "use strict";
  var D = document, W = window;

  var clock = D.getElementById("clock");
  if (clock) {
    var tick = function () {
      try {
        clock.textContent = new Intl.DateTimeFormat("en-CA", {
          hour: "2-digit", minute: "2-digit", hour12: false, timeZone: "America/Toronto",
        }).format(new Date());
      } catch (e) { clock.textContent = "24/7"; }
    };
    tick(); setInterval(tick, 20000);
  }
  var yr = D.getElementById("yr");
  if (yr) yr.textContent = String(new Date().getFullYear());

  var dlg = D.getElementById("quote");
  if (!dlg) return;
  function open() {
    if (dlg.open) return;
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    var first = dlg.querySelector("input");
    if (first) setTimeout(function () { first.focus(); }, 40);
  }
  [].slice.call(D.querySelectorAll("[data-quote]")).forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); open(); });
  });
  if (location.hash === "#quote") setTimeout(open, 60);
  var close = dlg.querySelector("[data-close]");
  if (close) close.addEventListener("click", function () { dlg.close(); });
  dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });

  var form = dlg.querySelector("[data-form]");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (form.querySelector('[name="company"]').value) return;   // honeypot
    var data = new FormData(form), endpoint = form.getAttribute("data-endpoint");
    var sent = form.querySelector(".q__sent");
    if (endpoint) {
      fetch(endpoint, { method: "POST", headers: { Accept: "application/json" }, body: data })
        .then(function () { if (sent) sent.hidden = false; })
        .catch(function () { if (sent) sent.hidden = false; });
      return;
    }
    // no form service wired up yet — hand the details to the visitor's mail app
    var body = [];
    data.forEach(function (v, k) { if (k !== "company" && v) body.push(k + ": " + v); });
    var mail = "mailto:" + (form.getAttribute("data-to") || "dispatch@swarmprotective.ca") +
      "?subject=" + encodeURIComponent("Quote request — " + (data.get("service") || "security")) +
      "&body=" + encodeURIComponent(body.join("\n"));
    W.location.href = mail;
    if (sent) sent.hidden = false;
  });
})();
