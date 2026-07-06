(function () {
  "use strict";

  // Render KaTeX math (system-model equations in §2.1, formal metrics in §5).
  // Delimiters: \( \) for inline, \[ \] for display blocks -- matches what's
  // written in docs/index.html. Guarded in case the CDN script fails to load
  // (e.g. offline preview) so the rest of the page still works.
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false }
      ],
      throwOnError: false
    });
  }

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
    var revealTargets = document.querySelectorAll(".section .panel, .intuition__step, .principle-list li, .limits-list li, .gap-item, .deep-dive");
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

  // Scrollspy: highlight the nav link matching the section currently in view
  if ("IntersectionObserver" in window) {
    var navLinks = Array.prototype.slice.call(navList ? navList.querySelectorAll('a[href^="#"]') : []);
    var linkById = {};
    navLinks.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      linkById[id] = link;
    });
    var spySections = Object.keys(linkById)
      .map(function (id) { return document.getElementById(id); })
      .filter(Boolean);

    var spyObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var id = entry.target.id;
          var link = linkById[id];
          if (!link) return;
          if (entry.isIntersecting) {
            navLinks.forEach(function (l) { l.classList.remove("is-active"); });
            link.classList.add("is-active");
          }
        });
      },
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    spySections.forEach(function (section) { spyObserver.observe(section); });
  }

  // Back-to-top button: appears after scrolling past the hero, scrolls smoothly to #top
  var backToTop = document.getElementById("backToTop");
  if (backToTop) {
    var toggleBackToTop = function () {
      if (window.scrollY > 480) {
        backToTop.classList.add("is-visible");
      } else {
        backToTop.classList.remove("is-visible");
      }
    };
    window.addEventListener("scroll", toggleBackToTop, { passive: true });
    toggleBackToTop();
  }
})();
