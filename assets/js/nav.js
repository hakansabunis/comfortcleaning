document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  if (!header || !toggle) return;
  toggle.addEventListener("click", function () {
    header.classList.toggle("open");
  });
});
