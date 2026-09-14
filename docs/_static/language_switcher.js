// aiorubi docs — language switcher (EN / FA)
// Shows a clearly visible pill-style toggle in the header; if the header mount
// point is missing or hidden (unusual themes/layouts), falls back to a fixed
// floating pill at the bottom-right corner.
(function () {
  "use strict";

  var LANGS = ["en", "fa"];
  var STORE_KEY = "aiorubi-docs-lang";

  function currentLang() {
    var m = location.pathname.match(/^\/(en|fa)(\/|$)/);
    if (m) return m[1];
    return document.documentElement.lang === "fa" ? "fa" : "en";
  }

  function siblingUrl(target) {
    var path = location.pathname;
    var m = path.match(/^\/(en|fa)(\/|$)/);
    if (m) return path.replace(/^\/(en|fa)/, "/" + target);
    // served without a lang prefix (e.g. root index.html redirect page)
    var file = path.split("/").pop() || "index.html";
    if (!/\.html$/.test(file)) file = "index.html";
    return target + "/" + file;
  }

  function remember(lang) {
    try { localStorage.setItem(STORE_KEY, lang); } catch (e) {}
  }

  remember(currentLang());

  function buildSwitcher() {
    var cur = currentLang();
    var wrap = document.createElement("div");
    wrap.className = "language-switcher";
    wrap.setAttribute("role", "group");
    wrap.setAttribute("aria-label", "Language / زبان");
    LANGS.forEach(function (lang) {
      var a = document.createElement("a");
      a.href = siblingUrl(lang);
      a.textContent = lang === "fa" ? "فا" : "EN";
      a.title = lang === "fa" ? "نسخهٔ فارسی" : "English version";
      a.setAttribute("hreflang", lang);
      if (lang === cur) {
        a.classList.add("active");
        a.setAttribute("aria-current", "true");
      } else {
        a.addEventListener("click", function () { remember(lang); });
      }
      wrap.appendChild(a);
    });
    return wrap;
  }

  function visible(el) {
    return !!(el && el.offsetParent !== null);
  }

  function mount() {
    var cur = currentLang();
    var sw = buildSwitcher();

    // 1) header mount: right before the TOC icon inside .header-right
    var headerRight = document.querySelector(".mobile-header .header-right");
    if (headerRight) {
      var tocIcon = headerRight.querySelector(".toc-overlay-icon");
      headerRight.insertBefore(sw, tocIcon || null);
    }

    // 2) fallback: if header mount missing or not actually visible, float it
    if (!headerRight || !visible(sw)) {
      var float = document.createElement("div");
      float.className = "language-switcher-float";
      float.appendChild(buildSwitcher());
      document.body.appendChild(float);
    }

    // keep the stored language fresh on navigation
    remember(cur);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
