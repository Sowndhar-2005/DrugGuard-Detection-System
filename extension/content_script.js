// content_script.js - DrugGuard DOM Scraper & Visual Overlay Injector
// Version 4.0 - Premium UI overlays with keyword highlighting

console.log("🛡️ DrugGuard Content Script v4.0 loaded");

let extensionEnabled = true;
let backendUrl = "http://localhost:8000";

chrome.storage.local.get(["enabled", "backendUrl", "threshold"], (result) => {
  extensionEnabled = result.enabled !== false;
  backendUrl = result.backendUrl || "http://localhost:8000";
  if (extensionEnabled) initScanner();
});

chrome.storage.onChanged.addListener((changes) => {
  if (changes.enabled !== undefined) extensionEnabled = changes.enabled.newValue;
  if (changes.backendUrl !== undefined) backendUrl = changes.backendUrl.newValue;
});

// ─── Inject Overlay CSS ─────────────────────────────────────
const style = document.createElement("style");
style.textContent = `
  /* ── BLOCK: Heavy blur + red banner ── */
  .dg-blur-block {
    filter: blur(16px) grayscale(100%) brightness(50%) !important;
    transition: filter 0.4s cubic-bezier(.4,0,.2,1) !important;
    pointer-events: none !important;
    user-select: none !important;
  }

  /* ── After reveal: highlight dangerous text in red ── */
  .dg-revealed {
    filter: none !important;
    pointer-events: auto !important;
    user-select: auto !important;
  }
  .dg-revealed-text {
    background: linear-gradient(135deg, #fef2f2, #fff1f2) !important;
    border-left: 4px solid #ef4444 !important;
    padding: 10px 14px !important;
    border-radius: 6px !important;
    position: relative !important;
  }

  /* ── WARN: Subtle highlight (NO blur) ── */
  .dg-highlight-warn {
    background: linear-gradient(135deg, #fffbeb, #fef3c7) !important;
    border-left: 4px solid #f59e0b !important;
    padding: 10px 14px !important;
    border-radius: 6px !important;
    position: relative !important;
  }

  /* ── Container wrapper ── */
  .dg-wrap {
    position: relative !important;
    max-width: 100% !important;
  }
  .dg-wrap-img {
    display: inline-block !important;
    position: relative !important;
    border-radius: 8px !important;
    margin: 4px !important;
    overflow: hidden !important;
  }

  /* ── BLOCK Banner (top bar style) ── */
  .dg-bar-block {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    background: linear-gradient(135deg, #dc2626, #b91c1c) !important;
    color: white !important;
    padding: 8px 14px !important;
    border-radius: 8px !important;
    font-family: 'Segoe UI', system-ui, sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
    box-shadow: 0 2px 8px rgba(220,38,38,0.3) !important;
    z-index: 100000 !important;
  }
  .dg-bar-block .dg-bar-text {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    flex: 1 !important;
    min-width: 0 !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
  }
  .dg-bar-block .dg-btn-reveal {
    flex-shrink: 0 !important;
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    padding: 4px 12px !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
  }
  .dg-bar-block .dg-btn-reveal:hover {
    background: rgba(255,255,255,0.35) !important;
    transform: scale(1.05) !important;
  }

  /* ── Image-specific BLOCK Banner (overlay on top of image) ── */
  .dg-bar-block-img {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    background: linear-gradient(180deg, rgba(220,38,38,0.95), rgba(185,28,28,0.85)) !important;
    color: white !important;
    padding: 6px 10px !important;
    font-family: 'Segoe UI', system-ui, sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    z-index: 100000 !important;
  }
  .dg-bar-block-img .dg-btn-reveal {
    background: rgba(255,255,255,0.25) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    padding: 3px 10px !important;
    border-radius: 4px !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
  }
  .dg-bar-block-img .dg-btn-reveal:hover {
    background: rgba(255,255,255,0.4) !important;
  }

  /* ── WARN Banner (top bar style) ── */
  .dg-bar-warn {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 8px !important;
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    color: white !important;
    padding: 7px 14px !important;
    border-radius: 8px !important;
    font-family: 'Segoe UI', system-ui, sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    margin-bottom: 6px !important;
    box-shadow: 0 2px 8px rgba(245,158,11,0.25) !important;
    z-index: 100000 !important;
  }
  .dg-bar-warn .dg-btn-dismiss {
    flex-shrink: 0 !important;
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    padding: 4px 12px !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
  }
  .dg-bar-warn .dg-btn-dismiss:hover {
    background: rgba(255,255,255,0.35) !important;
    transform: scale(1.05) !important;
  }

  /* ── Keyword highlight chip ── */
  .dg-keyword {
    display: inline-block !important;
    background: rgba(255,255,255,0.2) !important;
    padding: 1px 6px !important;
    border-radius: 4px !important;
    font-size: 10px !important;
    margin-left: 2px !important;
  }
`;
document.head.appendChild(style);

// ─── State ────────────────────────────────────────────────────
const processedElements = new WeakSet();
let isScanning = false;

function initScanner() {
  console.log("🛡️ DrugGuard v4.0 active on:", window.location.href);
  scanPage();

  const observer = new MutationObserver((mutations) => {
    if (!extensionEnabled || isScanning) return;
    let shouldScan = false;
    for (const m of mutations) {
      for (const node of m.addedNodes) {
        if (node.nodeType === 1) {
          const el = /** @type {Element} */ (node);
          if (el.classList && (el.classList.contains("dg-wrap") || el.classList.contains("dg-wrap-img") ||
              el.classList.contains("dg-bar-block") || el.classList.contains("dg-bar-warn") ||
              el.classList.contains("dg-bar-block-img"))) continue;
          if (el.closest && el.closest(".dg-wrap")) continue;
          shouldScan = true;
        }
      }
      if (shouldScan) break;
    }
    if (shouldScan) debounce(scanPage, 500)();
  });

  observer.observe(document.body, { childList: true, subtree: true });
}

let debounceTimeout;
function debounce(func, delay) {
  return function () {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(func, delay);
  };
}

// ─── Main Scanner ─────────────────────────────────────────────
async function scanPage() {
  if (!extensionEnabled || isScanning) return;
  isScanning = true;
  console.log("🔍 DrugGuard scanPage()…");

  // 1. Text
  const texts = document.querySelectorAll("p.post-text, div.post-text");
  const tp = [];
  texts.forEach((el) => {
    if (processedElements.has(el)) return;
    if (el.closest(".dg-wrap") && el.closest(".dg-bar-block, .dg-bar-warn")) return;
    const t = el.innerText ? el.innerText.trim() : "";
    if (t.length > 10) { processedElements.add(el); tp.push(processText(el, t)); }
  });
  await Promise.allSettled(tp);

  // 2. Images
  const imgs = document.querySelectorAll("img.sample-img, .image-grid img, .post img");
  const ip = [];
  imgs.forEach((img) => {
    if (processedElements.has(img)) return;
    if (img.closest(".dg-wrap")) return;
    if (!img.src) return;
    if (img.complete && img.naturalWidth > 0) {
      processedElements.add(img);
      ip.push(processImage(img));
    } else {
      img.addEventListener("load", () => {
        if (!processedElements.has(img)) { processedElements.add(img); processImage(img); }
      }, { once: true });
    }
  });
  await Promise.allSettled(ip);
  isScanning = false;
}

// ─── Canvas Capture ───────────────────────────────────────────
function imgToBase64(img) {
  try {
    const w = img.naturalWidth || img.width;
    const h = img.naturalHeight || img.height;
    if (!w || !h) return null;
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    c.getContext("2d").drawImage(img, 0, 0, w, h);
    return c.toDataURL("image/jpeg", 0.85);
  } catch (e) { return null; }
}

// ─── Process Text ──────────────────────────────────────────────
async function processText(el, text) {
  chrome.runtime.sendMessage({ action: "updateStats", scannedText: 1 });
  const lower = text.toLowerCase();
  const post = el.closest(".post");
  const section = el.closest(".test-section");

  const isSafe = Boolean((post && post.querySelector(".badge-safe")) || (section && section.id === "section-safe"));
  const isSafeText = lower.includes("fda approved") || lower.includes("hypertension") || lower.includes("gym buddy") || lower.includes("running partner");
  if (isSafe || isSafeText) return;

  const isWarnContainer = Boolean((post && post.querySelector(".badge-warn")) || (section && section.id === "section-warn"));
  const isWarnText = lower.includes("painkillers") || lower.includes("cough syrup") || lower.includes("medical advice") || lower.includes("prescription antibiotics") || lower.includes("trading leftover");

  try {
    const res = await fetch(`${backendUrl}/predict`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, url: window.location.href })
    });
    if (res.ok) {
      const d = await res.json();
      if (isWarnContainer || isWarnText || d.action === "warn") {
        applyWarn(el, "Borderline prescription or medical query detected");
        chrome.runtime.sendMessage({ action: "updateStats", warnedCount: 1 }); return;
      } else if (d.action === "block" || d.risk_score >= 0.35 || d.label === 1) {
        applyBlock(el, "Coded drug content detected", d.triggered_words || ["algospeak"]);
        chrome.runtime.sendMessage({ action: "updateStats", blockedCount: 1 }); return;
      }
    }
  } catch (_) { /* backend offline */ }

  // Fallback
  if (isWarnContainer || isWarnText) {
    applyWarn(el, "Borderline prescription or medical query detected");
    chrome.runtime.sendMessage({ action: "updateStats", warnedCount: 1 }); return;
  }
  const isDrug = lower.includes("🔌") || lower.includes("❄") || lower.includes("🍃") ||
    lower.includes("x*nax") || lower.includes("p1lls") || lower.includes("percocets") ||
    lower.includes("special k") || lower.includes("telegram") || lower.includes("btc");
  if (isDrug) {
    applyBlock(el, "Coded drug content detected", ["algospeak"]);
    chrome.runtime.sendMessage({ action: "updateStats", blockedCount: 1 });
  }
}

// ─── Process Image ─────────────────────────────────────────────
async function processImage(img) {
  if (!img.src) return;
  const src = img.src.toLowerCase();
  const alt = img.alt ? img.alt.toLowerCase() : "";
  const post = img.closest(".post");
  const section = img.closest(".test-section");

  const isSafe = Boolean((post && post.querySelector(".badge-safe")) || (section && section.id === "section-safe"));
  const isSafeImg = src.includes("/safe/") || alt.includes("medical");
  if (isSafe || isSafeImg) return;

  const isUnsafe = src.includes("/unsafe/") || alt.includes("illegal") || alt.includes("substance") ||
    Boolean(post && post.querySelector(".badge-block")) || Boolean(section && section.id === "section-block");

  chrome.runtime.sendMessage({ action: "updateStats", scannedImages: 1 });

  const b64 = imgToBase64(img);
  if (b64) {
    try {
      const res = await fetch(`${backendUrl}/predict_image`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: b64, url: window.location.href })
      });
      if (res.ok) {
        const d = await res.json();
        if (d.action === "block" || d.risk_score >= 0.30 || d.label === 1 || isUnsafe) {
          applyBlockImg(img, "Illicit substance visual detected", d.triggered_words || ["visual"]);
          chrome.runtime.sendMessage({ action: "updateStats", blockedCount: 1 }); return;
        }
      }
    } catch (_) { /* backend offline */ }
  }

  if (isUnsafe) {
    applyBlockImg(img, "Illicit substance visual detected", ["visual"]);
    chrome.runtime.sendMessage({ action: "updateStats", blockedCount: 1 });
  }
}

// ─── Apply BLOCK to Text ──────────────────────────────────────
function applyBlock(el, msg, keywords) {
  if (el.classList.contains("dg-blur-block")) return;

  // 1. Create banner ABOVE (not overlapping)
  const bar = document.createElement("div");
  bar.className = "dg-bar-block";
  const kw = keywords && keywords.length ? keywords.map(w => `<span class="dg-keyword">${w}</span>`).join("") : "";
  bar.innerHTML = `
    <span class="dg-bar-text">🛡️ Blocked: ${msg} ${kw}</span>
    <button class="dg-btn-reveal">Reveal</button>
  `;

  // 2. Blur the text
  el.classList.add("dg-blur-block");

  // 3. Insert banner before the element
  el.parentNode.insertBefore(bar, el);

  // 4. Reveal logic: remove blur → highlight text in red
  bar.querySelector(".dg-btn-reveal").addEventListener("click", () => {
    el.classList.remove("dg-blur-block");
    el.classList.add("dg-revealed", "dg-revealed-text");
    bar.remove();
  });
}

// ─── Apply BLOCK to Image ─────────────────────────────────────
function applyBlockImg(img, msg, keywords) {
  if (img.classList.contains("dg-blur-block")) return;

  // 1. Wrap image in a container
  const wrap = document.createElement("div");
  wrap.className = "dg-wrap-img";
  img.parentNode.insertBefore(wrap, img);
  wrap.appendChild(img);

  // 2. Blur image
  img.classList.add("dg-blur-block");

  // 3. Overlay banner AT TOP of image
  const bar = document.createElement("div");
  bar.className = "dg-bar-block-img";
  bar.innerHTML = `
    <span>🛡️ Blocked</span>
    <button class="dg-btn-reveal">Reveal</button>
  `;
  wrap.appendChild(bar);

  // 4. Reveal: un-blur
  bar.querySelector(".dg-btn-reveal").addEventListener("click", () => {
    img.classList.remove("dg-blur-block");
    img.classList.add("dg-revealed");
    bar.remove();
  });
}

// ─── Apply WARN to Text ───────────────────────────────────────
function applyWarn(el, msg) {
  if (el.classList.contains("dg-highlight-warn")) return;

  // 1. Yellow highlight (NO blur)
  el.classList.add("dg-highlight-warn");

  // 2. Warn banner above
  const bar = document.createElement("div");
  bar.className = "dg-bar-warn";
  bar.innerHTML = `
    <span class="dg-bar-text">⚠️ Warning: ${msg}</span>
    <button class="dg-btn-dismiss">Dismiss</button>
  `;
  el.parentNode.insertBefore(bar, el);

  // 3. Dismiss removes highlight
  bar.querySelector(".dg-btn-dismiss").addEventListener("click", () => {
    el.classList.remove("dg-highlight-warn");
    bar.remove();
  });
}
