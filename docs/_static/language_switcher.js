// aiorubi docs — language switcher (EN / FA)
// Shows a clearly visible pill-style toggle in the header; if the header mount
// point is missing or hidden (unusual themes/layouts), falls back to a fixed
// floating pill at the bottom-right corner.
(function () {
  "use strict";

  var LANGS = ["en", "fa"];
  var LANG_SEGMENT = /(^|\/)(en|fa)(?=\/|$)/g;
  var STORE_KEY = "aiorubi-docs-lang";

  // Position + value of the LAST bare "en"/"fa" path segment. Matching the last
  // (not the first) makes the switcher correct for both hosting layouts:
  //   /fa/latest/page.html          (one RTD project per language)
  //   /en/latest/fa/page.html       (both languages nested under one project)
  function langSegment(path) {
    var last = null, m;
    LANG_SEGMENT.lastIndex = 0;
    while ((m = LANG_SEGMENT.exec(path)) !== null) {
      last = { index: m.index + m[1].length, lang: m[2] };
    }
    return last;
  }

  function currentLang() {
    var seg = langSegment(location.pathname);
    if (seg) return seg.lang;
    return document.documentElement.lang === "fa" ? "fa" : "en";
  }

  function siblingUrl(target) {
    var path = location.pathname;
    var seg = langSegment(path);
    if (seg) {
      return path.slice(0, seg.index) + target + path.slice(seg.index + seg.lang.length);
    }
    // served without a lang segment: assume <target>/<file> beside the current page
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
