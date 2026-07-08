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

  // 3D cursor-tilt: subtle perspective tilt on panels/pipeline stages/status pill,
  // following the pointer. Skipped on touch devices (no meaningful hover) and
  // when reduced motion is preferred.
  var supportsHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (!prefersReducedMotion && supportsHover) {
    var tiltTargets = document.querySelectorAll(".panel, .dsp-stage, .hero__status-pill");
    var maxTilt = 6; // degrees

    tiltTargets.forEach(function (el) {
      el.addEventListener("mouseenter", function () {
        el.classList.add("tilt-active");
      });
      el.addEventListener("mousemove", function (e) {
        var rect = el.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width;
        var py = (e.clientY - rect.top) / rect.height;
        var rotateY = (px - 0.5) * (maxTilt * 2);
        var rotateX = (0.5 - py) * (maxTilt * 2);
        el.style.transform =
          "perspective(700px) rotateX(" + rotateX.toFixed(2) + "deg) rotateY(" + rotateY.toFixed(2) + "deg) translateZ(2px)";
      });
      el.addEventListener("mouseleave", function () {
        el.classList.remove("tilt-active");
        el.style.transform = "perspective(700px) rotateX(0deg) rotateY(0deg) translateZ(0)";
      });
    });
  }
})();
