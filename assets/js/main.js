(function () {
  var header = document.querySelector(".site-header");
  var menuBtn = document.querySelector(".menu-btn");
  var menu = document.getElementById("mobile-menu");

  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  function setMenu(open) {
    menu.hidden = !open;
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("menu-open", open);
    if (header && open) header.classList.remove("is-hidden");
    if (window.__lenis) {
      if (open) window.__lenis.stop();
      else window.__lenis.start();
    }
  }

  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () {
      setMenu(menu.hidden);
    });
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !menu.hidden) {
        setMenu(false);
        menuBtn.focus();
      }
    });
    var desktop = window.matchMedia("(min-width: 900px)");
    var onChange = function (mq) {
      if (mq.matches && !menu.hidden) setMenu(false);
    };
    if (desktop.addEventListener) desktop.addEventListener("change", onChange);
    else if (desktop.addListener) desktop.addListener(onChange);
  }

  /* Wipe card: a dusty layer the visitor clears with the pointer or a finger */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  Array.prototype.forEach.call(document.querySelectorAll("[data-wipe]"), function (card) {
    var canvas = card.querySelector(".wipe-canvas");
    var reset = card.querySelector(".wipe-reset");
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext("2d");
    var probe = document.createElement("canvas");
    probe.width = 48;
    probe.height = 42;
    var pctx = probe.getContext("2d", { willReadFrequently: true });
    var w = 0, h = 0, dpr = 1, last = null, done = false, touched = false, checkTimer = 0, hinted = false;

    function paint() {
      var r = canvas.getBoundingClientRect();
      if (!r.width) return;
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.width = Math.round(r.width * dpr);
      h = canvas.height = Math.round(r.height * dpr);
      ctx.globalCompositeOperation = "source-over";
      ctx.shadowBlur = 0;
      var g = ctx.createLinearGradient(0, 0, w, h);
      g.addColorStop(0, "rgba(156, 141, 118, 0.97)");
      g.addColorStop(1, "rgba(112, 99, 82, 0.98)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, w, h);
      var i, x, y, rad, rg;
      for (i = 0; i < 22; i++) {
        x = Math.random() * w;
        y = Math.random() * h;
        rad = (50 + Math.random() * 140) * dpr;
        rg = ctx.createRadialGradient(x, y, 0, x, y, rad);
        rg.addColorStop(0, "rgba(84, 70, 55, 0.32)");
        rg.addColorStop(1, "rgba(84, 70, 55, 0)");
        ctx.fillStyle = rg;
        ctx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
      }
      for (i = 0; i < 2200; i++) {
        var light = Math.random() < 0.5;
        ctx.fillStyle = light ? "rgba(214, 203, 182, " + (Math.random() * 0.35) + ")" : "rgba(60, 50, 38, " + (Math.random() * 0.3) + ")";
        var size = (Math.random() * 2.2 + 0.4) * dpr;
        ctx.fillRect(Math.random() * w, Math.random() * h, size, size);
      }
      done = false;
      canvas.style.transition = "";
      canvas.style.opacity = "1";
      card.classList.add("is-dusty");
      card.classList.remove("is-clean", "is-wiping");
    }

    function stroke(x0, y0, x1, y1) {
      ctx.globalCompositeOperation = "destination-out";
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      ctx.lineWidth = 70 * dpr;
      ctx.shadowColor = "rgba(0, 0, 0, 1)";
      ctx.shadowBlur = 24 * dpr;
      ctx.strokeStyle = "rgba(0, 0, 0, 0.9)";
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
    }

    function check() {
      checkTimer = 0;
      pctx.clearRect(0, 0, probe.width, probe.height);
      pctx.drawImage(canvas, 0, 0, probe.width, probe.height);
      var data = pctx.getImageData(0, 0, probe.width, probe.height).data;
      var clear = 0, total = data.length / 4;
      for (var i = 3; i < data.length; i += 4) if (data[i] < 60) clear++;
      if (clear / total > 0.58) finish();
    }

    function finish() {
      done = true;
      canvas.style.transition = "opacity 0.9s ease";
      canvas.style.opacity = "0";
      card.classList.remove("is-dusty", "is-wiping");
      card.classList.add("is-clean");
    }

    function point(e) {
      var r = canvas.getBoundingClientRect();
      return [(e.clientX - r.left) * dpr, (e.clientY - r.top) * dpr];
    }

    canvas.addEventListener("pointermove", function (e) {
      if (done) return;
      var p = point(e);
      if (last) stroke(last[0], last[1], p[0], p[1]);
      else stroke(p[0], p[1], p[0] + 0.5, p[1]);
      last = p;
      touched = true;
      card.classList.add("is-wiping");
      if (!checkTimer) checkTimer = setTimeout(check, 220);
    });
    ["pointerleave", "pointerup", "pointercancel"].forEach(function (type) {
      canvas.addEventListener(type, function () { last = null; });
    });
    if (reset) reset.addEventListener("click", paint);

    function demo() {
      if (hinted || touched || reduce || done) return;
      hinted = true;
      var t0 = performance.now(), prev = null, dur = 1300;
      (function step(now) {
        if (touched) return;
        var k = Math.min(1, (now - t0) / dur);
        var x = w * (0.1 + 0.8 * k);
        var y = h * (0.5 + Math.sin(k * Math.PI * 2.2) * 0.2 - k * 0.1);
        if (prev) stroke(prev[0], prev[1], x, y);
        prev = [x, y];
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    }

    paint();
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries, obs) {
        if (entries[0].isIntersecting) {
          setTimeout(demo, 700);
          obs.disconnect();
        }
      }, { threshold: 0.6 }).observe(card);
    }
    var lastWidth = canvas.getBoundingClientRect().width;
    window.addEventListener("resize", function () {
      var nowWidth = canvas.getBoundingClientRect().width;
      if (Math.abs(nowWidth - lastWidth) > 40 && !done) { lastWidth = nowWidth; paint(); }
    });
  });
})();
