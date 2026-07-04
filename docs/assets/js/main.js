(function () {
  "use strict";

  // Mobile nav toggle
  var navToggle = document.getElementById("navToggle");
  var navList = document.getElementById("navList");
  if (navToggle && navList) {
    navToggle.addEventListener("click", function () {
      var isOpen = navList.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    navList.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navList.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Mermaid diagram init (dark theme matched to the instrument-panel palette)
  if (window.mermaid) {
    mermaid.initialize({
      startOnLoad: true,
      theme: "base",
      themeVariables: {
        background: "#1B232C",
        primaryColor: "#1B232C",
        primaryTextColor: "#E8E6DE",
        primaryBorderColor: "#4FD1C5",
        lineColor: "#4FD1C5",
        secondaryColor: "#12181F",
        tertiaryColor: "#12181F",
        fontFamily: "IBM Plex Mono, monospace",
        clusterBkg: "#12181F",
        clusterBorder: "#2A3440"
      }
    });
  }

  // Scroll-reveal for section panels (skipped entirely if reduced motion is preferred)
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!prefersReducedMotion && "IntersectionObserver" in window) {
    var revealTargets = document.querySelectorAll(".section .panel, .method-steps li, .media-slot, .limits-list li");
    revealTargets.forEach(function (el) { el.classList.add("reveal"); });

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealTargets.forEach(function (el) { observer.observe(el); });
  }
})();
