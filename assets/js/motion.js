/* Scroll and entrance motion. Runs only when motion is allowed and GSAP loaded; otherwise the page stays static. */
(function () {
  var root = document.documentElement;
  if (!root.classList.contains("motion")) return;
  if (!window.gsap || !window.ScrollTrigger) {
    root.classList.remove("motion");
    return;
  }
  var gsap = window.gsap;
  var ScrollTrigger = window.ScrollTrigger;
  gsap.registerPlugin(ScrollTrigger);
  var SplitText = window.SplitText;
  if (SplitText) gsap.registerPlugin(SplitText);
  window.__motionReady = true;

  var q = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var qa = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  /* Smooth scrolling, kept in sync with ScrollTrigger */
  var lenis = null;
  if (window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.1 });
    window.__lenis = lenis;
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  qa('a[href^="#"]:not(.skip-link)').forEach(function (a) {
    var id = a.getAttribute("href");
    if (id.length < 2) return;
    a.addEventListener("click", function (ev) {
      var target = q(id);
      if (!target) return;
      ev.preventDefault();
      if (lenis) lenis.scrollTo(target, { duration: 1.4 });
      else target.scrollIntoView({ behavior: "smooth" });
    });
  });

  /* Header hides while reading down, returns on the way up */
  var header = q(".site-header");
  if (header) {
    ScrollTrigger.create({
      start: 0,
      end: "max",
      onUpdate: function (self) {
        var hide = self.direction === 1 && self.scroll() > 360 && !document.body.classList.contains("menu-open");
        header.classList.toggle("is-hidden", hide);
      }
    });
  }

  /* Hero entrance */
  var heroTitle = q('[data-split="hero"]');
  if (heroTitle) {
    if (SplitText) {
      SplitText.create(heroTitle, {
        type: "lines,words",
        linesClass: "split-line",
        mask: "lines",
        autoSplit: true,
        onSplit: function (self) {
          gsap.set(heroTitle, { autoAlpha: 1 });
          return gsap.from(self.words, { yPercent: 118, duration: 1.35, ease: "expo.out", stagger: 0.06, delay: 0.1 });
        }
      });
    } else {
      gsap.set(heroTitle, { autoAlpha: 1 });
    }
  }
  var heroIn = qa("[data-hero-in]");
  if (heroIn.length) {
    gsap.fromTo(heroIn, { autoAlpha: 0, y: 34 }, { autoAlpha: 1, y: 0, duration: 1.2, ease: "expo.out", stagger: 0.12, delay: 0.45 });
  }

  /* Section headings rise line by line */
  qa("[data-split]").forEach(function (el) {
    if (el === heroTitle || el.getAttribute("data-split") === "hero") return;
    if (!SplitText) { gsap.set(el, { autoAlpha: 1 }); return; }
    SplitText.create(el, {
      type: "lines",
      linesClass: "split-line",
      mask: "lines",
      autoSplit: true,
      onSplit: function (self) {
        gsap.set(el, { autoAlpha: 1 });
        return gsap.from(self.lines, {
          yPercent: 110,
          duration: 1.15,
          ease: "expo.out",
          stagger: 0.1,
          scrollTrigger: { trigger: el, start: "top 88%", once: true }
        });
      }
    });
  });

  /* Story: words fill in while the section is pinned */
  var story = q("[data-story]");
  if (story && SplitText) {
    var storySection = story.closest(".story");
    var words = SplitText.create(story, { type: "words", wordsClass: "story-word" }).words;
    gsap.fromTo(words, { opacity: 0.13 }, {
      opacity: 1,
      ease: "none",
      stagger: 0.1,
      scrollTrigger: { trigger: storySection, start: "top top", end: "+=130%", scrub: 0.4, pin: true }
    });
  }

  var mm = gsap.matchMedia();

  /* Services: horizontal track on large screens */
  mm.add("(min-width: 1024px) and (min-height: 660px)", function () {
    var sec = q(".services");
    if (!sec) return;
    var track = q(".services-track", sec);
    var bar = q(".services-progress i", sec);
    sec.classList.add("is-horizontal");
    var distance = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
    gsap.to(track, {
      x: function () { return -distance(); },
      ease: "none",
      scrollTrigger: {
        trigger: sec,
        start: "top top",
        end: function () { return "+=" + distance(); },
        pin: true,
        scrub: 0.8,
        invalidateOnRefresh: true,
        onUpdate: function (self) { if (bar) bar.style.transform = "scaleX(" + self.progress.toFixed(4) + ")"; }
      }
    });
    return function () { sec.classList.remove("is-horizontal"); };
  });

  /* Hero depth on desktop */
  mm.add("(min-width: 900px)", function () {
    var hero = q(".hero");
    if (!hero) return;
    gsap.to(".hero-copy", { yPercent: -10, opacity: 0.35, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
    gsap.to(".phone", { y: -90, ease: "none", scrollTrigger: { trigger: hero, start: "top top", end: "bottom top", scrub: true } });
  });

  /* Generic reveals */
  var reveals = qa(".reveal");
  gsap.set(reveals, { autoAlpha: 0, y: 44 });
  ScrollTrigger.batch(reveals, {
    start: "top 90%",
    once: true,
    onEnter: function (batch) {
      gsap.to(batch, {
        autoAlpha: 1,
        y: 0,
        duration: 1.1,
        ease: "expo.out",
        stagger: 0.09,
        overwrite: true,
        onComplete: function () { gsap.set(batch, { clearProps: "transform" }); }
      });
    }
  });

  /* Process line draws as you read */
  qa(".process-track").forEach(function (trk) {
    var line = q(".process-line i", trk);
    gsap.to(line, { scaleY: 1, ease: "none", scrollTrigger: { trigger: trk, start: "top 70%", end: "bottom 65%", scrub: 0.5 } });
    qa(".process li", trk).forEach(function (li) {
      ScrollTrigger.create({
        trigger: li,
        start: "top 68%",
        onEnter: function () { li.classList.add("is-active"); },
        onLeaveBack: function () { li.classList.remove("is-active"); }
      });
    });
  });

  /* Hero phone: the photo, price, order conversation plays on a loop */
  var phone = q(".phone-wrap");
  if (phone) {
    var steps = qa(".chat-steps li", phone);
    var msg = function (n) { return q('[data-msg="' + n + '"]', phone); };
    var bubbles = qa(".msg, .chat-done", phone);
    var typing = msg(2);
    var setStep = function (n) { steps.forEach(function (li, i) { li.classList.toggle("is-active", i < n); }); };
    var pop = function (el) {
      return gsap.fromTo(el, { autoAlpha: 0, y: 12, scale: 0.94 }, { autoAlpha: 1, y: 0, scale: 1, duration: 0.55, ease: "back.out(1.7)", transformOrigin: el.classList.contains("msg--out") ? "100% 100%" : "0% 100%" });
    };
    var tl = gsap.timeline({ repeat: -1, repeatDelay: 0.4, paused: true });
    tl.call(function () { setStep(0); })
      .set(bubbles, { autoAlpha: 0 })
      .set(typing, { display: "none", autoAlpha: 0 })
      .add(pop(msg(1)), 0.6).call(function () { setStep(1); }, null, 0.7)
      .set(typing, { display: "flex", autoAlpha: 1 }, 1.7)
      .set(typing, { display: "none" }, 3.1)
      .add(pop(msg(3)), 3.1).call(function () { setStep(2); }, null, 3.2)
      .add(pop(msg(4)), 4.4)
      .add(pop(msg(5)), 5.8)
      .add(pop(msg(6)), 6.8).call(function () { setStep(3); }, null, 6.9)
      .to(bubbles, { autoAlpha: 0, duration: 0.5, ease: "power2.in" }, 10.5);
    var phoneVisible = true;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        phoneVisible = entries[0].isIntersecting;
        if (phoneVisible && tl.time() > 0) tl.play();
        else if (!phoneVisible) tl.pause();
      }).observe(phone);
    }
    gsap.delayedCall(1, function () { if (phoneVisible) tl.play(); });
  }

  /* Marquee speeds up a little with scroll velocity */
  var marquee = q(".marquee-track");
  if (marquee && lenis && marquee.getAnimations) {
    var anim = marquee.getAnimations()[0];
    var rate = 1;
    gsap.ticker.add(function () {
      if (!anim) return;
      var targetRate = 1 + Math.min(5, Math.abs(lenis.velocity) * 0.18);
      rate += (targetRate - rate) * 0.08;
      anim.playbackRate = rate;
    });
  }

  /* Magnetic primary buttons */
  if (finePointer) {
    qa(".magnetic").forEach(function (btn) {
      var xTo = gsap.quickTo(btn, "x", { duration: 0.6, ease: "power3.out" });
      var yTo = gsap.quickTo(btn, "y", { duration: 0.6, ease: "power3.out" });
      btn.addEventListener("pointermove", function (e) {
        var r = btn.getBoundingClientRect();
        xTo((e.clientX - (r.left + r.width / 2)) * 0.22);
        yTo((e.clientY - (r.top + r.height / 2)) * 0.32);
      });
      btn.addEventListener("pointerleave", function () { xTo(0); yTo(0); });
    });
  }

  /* Keep trigger positions right when content height changes */
  var refreshSoon = (function () {
    var t = 0;
    return function () { clearTimeout(t); t = setTimeout(function () { ScrollTrigger.refresh(); }, 350); };
  })();
  document.addEventListener("toggle", refreshSoon, true);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(refreshSoon);
  window.addEventListener("load", refreshSoon);
})();
