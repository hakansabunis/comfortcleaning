document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      header.classList.toggle("open");
    });
  }

  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  var revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
      revealEls.forEach(function (el) { io.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add("in-view"); });
    }
  }

  var tabBtns = document.querySelectorAll(".tab-btn");
  var tabPanels = document.querySelectorAll(".tab-panel");
  if (tabBtns.length && tabPanels.length) {
    tabBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var target = btn.getAttribute("data-tab");
        tabBtns.forEach(function (b) { b.classList.toggle("active", b === btn); });
        tabPanels.forEach(function (p) {
          p.classList.toggle("active", p.getAttribute("data-panel") === target);
        });
      });
    });
  }

  var qoButtons = document.querySelectorAll(".qo-btn");
  var qoLink = document.getElementById("quickOrderBtn");
  if (qoButtons.length && qoLink) {
    var waBase = qoLink.getAttribute("data-wa-base");
    var waTemplate = qoLink.getAttribute("data-wa-template");
    var updateQoLink = function (service) {
      var text = waTemplate.replace("{service}", service);
      qoLink.href = waBase + "?text=" + encodeURIComponent(text);
    };
    qoButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        qoButtons.forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        updateQoLink(btn.getAttribute("data-service"));
      });
    });
    var activeBtn = document.querySelector(".qo-btn.active");
    if (activeBtn) updateQoLink(activeBtn.getAttribute("data-service"));
  }

  var faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(function (item) {
    var q = item.querySelector(".faq-q");
    var a = item.querySelector(".faq-a");
    if (!q || !a) return;
    q.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      faqItems.forEach(function (other) {
        other.classList.remove("open");
        var otherA = other.querySelector(".faq-a");
        if (otherA) otherA.style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add("open");
        a.style.maxHeight = a.scrollHeight + "px";
      }
    });
  });
});
