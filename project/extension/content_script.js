/**
 * content_script.js
 * DrugGuard — Content Script
 *
 * Scans visible text on web pages, sends to the FastAPI backend,
 * and applies visual overlays (warn/block) based on risk scores.
 */

(() => {
  "use strict";

  const API_URL = "http://localhost:8000/predict";
  const IMAGE_API_URL = "http://localhost:8000/predict_image";
  const BATCH_INTERVAL = 500; // ms debounce
  const MIN_TEXT_LENGTH = 20;

  // Track what we've already processed
  let processedElements = new WeakSet();
  let pendingBatch = [];
  let batchTimer = null;
  let extensionEnabled = true;
  let stats = { scanned: 0, warned: 0, blocked: 0, flaggedItems: [] };

  // ─── Styles ──────────────────────────────────
  const STYLES = {
    warn: `
      outline: 3px solid #f59e0b !important;
      outline-offset: 2px;
      position: relative;
    `,
    block: `
      filter: blur(8px) !important;
      user-select: none !important;
      position: relative;
      cursor: pointer;
    `,
  };

  function injectStyles() {
    if (document.getElementById("drugguard-styles")) return;
    const style = document.createElement("style");
    style.id = "drugguard-styles";
    style.textContent = `
      .drugguard-warn {
        outline: 3px solid #f59e0b !important;
        outline-offset: 2px;
        position: relative;
      }
      .drugguard-warn::before {
        content: "⚠️";
        position: absolute;
        top: -10px;
        right: -10px;
        font-size: 16px;
        z-index: 10000;
        background: #fef3c7;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
      }
      .drugguard-block {
        filter: blur(8px) !important;
        user-select: none !important;
        position: relative;
        cursor: pointer;
        transition: filter 0.3s ease;
      }
      .drugguard-block-banner {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(220, 38, 38, 0.95);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        z-index: 10001;
        pointer-events: auto;
        cursor: pointer;
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
        letter-spacing: 0.3px;
      }
      .drugguard-block-banner:hover {
        background: rgba(185, 28, 28, 0.95);
      }
      .drugguard-revealed {
        filter: none !important;
        user-select: auto !important;
        outline: 3px solid #dc2626 !important;
        outline-offset: 2px;
      }
    `;
    document.head.appendChild(style);
  }

  // ─── DOM Scanning ─────────────────────────────
  // Target only leaf-level or near-leaf content elements to avoid
  // scanning the same text multiple times through parent containers.
  function isLeafContent(el) {
    // A "leaf" for our purposes: element has no block-level children
    const blockTags = new Set(["P", "DIV", "ARTICLE", "SECTION", "BLOCKQUOTE", "LI", "TD", "TH", "H1", "H2", "H3", "H4", "H5", "H6", "PRE"]);
    for (const child of el.children) {
      if (blockTags.has(child.tagName)) return false;
    }
    return true;
  }

  function getTextElements() {
    const selectors = "p, article, h1, h2, h3, h4, h5, h6, li, td, th, blockquote, pre, [data-testid], [role='article'], [role='main']";
    const elements = document.querySelectorAll(selectors);
    const results = [];

    elements.forEach((el) => {
      if (processedElements.has(el)) return;
      if (!isLeafContent(el)) return;
      // Use innerText so we get what the user actually sees (respects CSS visibility)
      const text = (el.innerText || el.textContent || "").trim();
      
      // Skip scanning elements containing extension/system texts to avoid false positive blocks
      if (text.includes("DrugGuard") || text.includes("Extension Test Page") || text.includes("Monitoring active") || text.includes("Recent Flags")) {
        return;
      }
      
      if (text.length >= MIN_TEXT_LENGTH) {
        results.push({ element: el, text: text });
      }
    });

    // Also grab standalone divs/spans with substantial text but no block children
    document.querySelectorAll("div, span").forEach((el) => {
      if (processedElements.has(el)) return;
      if (!isLeafContent(el)) return;
      const text = (el.innerText || el.textContent || "").trim();
      if (text.length >= MIN_TEXT_LENGTH && text.length <= 2000) {
        results.push({ element: el, text: text });
      }
    });

    return results;
  }

  // ─── API Communication ─────────────────────────
  let backendReachable = true;

  async function sendToPredictAPI(text) {
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) return null;
      backendReachable = true;
      return await response.json();
    } catch (err) {
      if (backendReachable) {
        console.warn("[DrugGuard] Cannot reach backend at", API_URL, "— start the FastAPI server.");
        backendReachable = false;
      }
      return null;
    }
  }

  // ─── Batch Processing ─────────────────────────
  function queueForAnalysis(element, text) {
    pendingBatch.push({ element, text });

    if (batchTimer) clearTimeout(batchTimer);
    batchTimer = setTimeout(processBatch, BATCH_INTERVAL);
  }

  async function processBatch() {
    if (!extensionEnabled || pendingBatch.length === 0) return;

    const batch = [...pendingBatch];
    pendingBatch = [];

    // Mark all as processed immediately to prevent re-queuing while waiting
    batch.forEach(({ element }) => processedElements.add(element));

    // Parallel fetch — faster than sequential
    const promises = batch.map(({ element, text }) =>
      sendToPredictAPI(text).then((result) => ({ element, text, result }))
    );

    const results = await Promise.all(promises);

    for (const { element, text, result } of results) {
      if (result) {
        stats.scanned++;
        applyAction(element, text, result);
      }
    }

    // Update stats in storage
    updateStats();
  }

  // ─── Visual Overlays ──────────────────────────
  function applyAction(element, text, result) {
    const { action, risk_score, triggered_words } = result;

    if (action === "safe") return;

    if (action === "warn") {
      stats.warned++;
      element.classList.add("drugguard-warn");
      addFlaggedItem(text, risk_score, "warn", triggered_words);
    }

    if (action === "block") {
      stats.blocked++;

      // Make parent relative for banner positioning
      const parent = element.parentElement;
      if (parent && getComputedStyle(parent).position === "static") {
        parent.style.position = "relative";
      }

      element.classList.add("drugguard-block");

      // Create banner
      const banner = document.createElement("div");
      banner.className = "drugguard-block-banner";
      banner.textContent = "⚠️ Drug-related content detected — Click to reveal";
      element.parentElement.appendChild(banner);

      addFlaggedItem(text, risk_score, "block", triggered_words);
    }
  }

  function addFlaggedItem(text, riskScore, action, triggeredWords) {
    const snippet = text.length > 80 ? text.substring(0, 80) + "…" : text;
    stats.flaggedItems.unshift({
      text: snippet,
      riskScore: Math.round(riskScore * 100),
      action,
      triggeredWords: triggeredWords || [],
      timestamp: Date.now(),
    });

    // Keep only last 20 items
    if (stats.flaggedItems.length > 20) {
      stats.flaggedItems = stats.flaggedItems.slice(0, 20);
    }
  }

  // ─── Stats ────────────────────────────────────
  function updateStats() {
    chrome.storage.local.set({
      drugguard_stats: {
        scanned: stats.scanned,
        warned: stats.warned,
        blocked: stats.blocked,
        flaggedItems: stats.flaggedItems,
      },
    });

    // Notify background
    chrome.runtime.sendMessage({
      type: "STATS_UPDATE",
      stats: {
        scanned: stats.scanned,
        warned: stats.warned,
        blocked: stats.blocked,
      },
    });
  }

  // ─── Initial Scan ─────────────────────────────
  function scanPage() {
    if (!extensionEnabled) return;
    const elements = getTextElements();
    elements.forEach(({ element, text }) => {
      queueForAnalysis(element, text);
    });
    scanImages();
  }

  // ─── Image Scanning ───────────────────────────
  async function imageToBase64Direct(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) return null;
      const blob = await response.blob();
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = () => resolve(null);
        reader.readAsDataURL(blob);
      });
    } catch (e) {
      return null;
    }
  }

  function imageToBase64Canvas(img) {
    try {
      const canvas = document.createElement("canvas");
      canvas.width = img.naturalWidth || img.width;
      canvas.height = img.naturalHeight || img.height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(img, 0, 0);
      return canvas.toDataURL("image/jpeg");
    } catch (e) {
      // CORS tainted canvas or other error
      return null;
    }
  }

  async function scanImage(img) {
    console.log("[DrugGuard debug] scanImage called for:", img.src);
    if (processedElements.has(img)) {
      console.log("[DrugGuard debug] Already processed:", img.src);
      return;
    }

    // Check dimensions
    const width = img.naturalWidth || img.width;
    const height = img.naturalHeight || img.height;
    console.log("[DrugGuard debug] Dimensions:", width, "x", height);
    if (width < 50 || height < 50) return;

    // Skip scanning images containing extension/system texts in alt tags
    const altText = img.alt || "";
    if (altText.includes("DrugGuard") || altText.includes("Extension Test Page")) {
      console.log("[DrugGuard debug] Safelisted alt:", img.src);
      return;
    }

    processedElements.add(img);
    const url = img.src;
    if (!url || url.startsWith("chrome-extension:") || url.startsWith("devtools:") || url.startsWith("about:")) {
      console.log("[DrugGuard debug] Ignored scheme:", url);
      return;
    }

    console.log("[DrugGuard debug] Converting to base64...");
    // 1. Try direct fetch in content script first (works for file:// and same-origin)
    let base64 = await imageToBase64Direct(url);
    console.log("[DrugGuard debug] Direct fetch base64 loaded:", !!base64);

    // 2. Try canvas conversion if direct fetch failed
    if (!base64) {
      base64 = imageToBase64Canvas(img);
      console.log("[DrugGuard debug] Canvas base64 loaded:", !!base64);
    }

    if (base64) {
      console.log("[DrugGuard debug] Sending to predict_image...");
      predictImage(img, base64);
    } else {
      console.log("[DrugGuard debug] Falling back to background proxy...");
      // 3. Fallback: request background service worker to fetch it (bypasses CORS on remote sites)
      chrome.runtime.sendMessage({ type: "FETCH_IMAGE", url: url }, (response) => {
        if (chrome.runtime.lastError) {
          console.log("[DrugGuard debug] Background error:", chrome.runtime.lastError.message);
          return;
        }
        console.log("[DrugGuard debug] Background response:", response);
        if (response && response.ok && response.data) {
          predictImage(img, response.data);
        }
      });
    }
  }

  function scanImages() {
    if (!extensionEnabled) return;
    const images = document.querySelectorAll("img");
    images.forEach((img) => {
      if (processedElements.has(img)) return;
      if (!img.complete) {
        img.addEventListener("load", () => scanImage(img), { once: true });
      } else {
        scanImage(img);
      }
    });
  }

  async function predictImage(img, base64Data) {
    if (!extensionEnabled) return;
    try {
      const response = await fetch(IMAGE_API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Data }),
      });
      if (!response.ok) return;
      const result = await response.json();
      stats.scanned++;
      applyImageAction(img, result);
      updateStats();
    } catch (err) {
      console.warn("[DrugGuard] Error analyzing image:", err);
    }
  }

  function applyImageAction(img, result) {
    const { action, risk_score, triggered_words } = result;
    if (action === "safe") return;

    if (action === "warn") {
      stats.warned++;
      img.classList.add("drugguard-warn");
      addFlaggedItem("[IMAGE] Containing words: " + (triggered_words.join(", ") || "suspicious text"), risk_score, "warn", triggered_words);
    }

    if (action === "block") {
      stats.blocked++;

      const parent = img.parentElement;
      if (parent && getComputedStyle(parent).position === "static") {
        parent.style.position = "relative";
      }

      img.classList.add("drugguard-block");

      const banner = document.createElement("div");
      banner.className = "drugguard-block-banner";
      banner.textContent = "⚠️ Drug-related image detected — Click to reveal";
      img.parentElement.appendChild(banner);

      addFlaggedItem("[IMAGE] Flagged words: " + (triggered_words.join(", ") || "illicit text"), risk_score, "block", triggered_words);
    }
  }

  // ─── MutationObserver ─────────────────────────
  function observeDOM() {
    const observer = new MutationObserver((mutations) => {
      if (!extensionEnabled) return;

      let hasNewContent = false;
      for (const mutation of mutations) {
        if (mutation.addedNodes.length > 0) {
          hasNewContent = true;
          break;
        }
      }

      if (hasNewContent) {
        // Debounce re-scan
        setTimeout(scanPage, 300);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  // ─── Init ─────────────────────────────────────
  function init() {
    // Check if extension is enabled
    chrome.storage.local.get(["drugguard_enabled"], (result) => {
      extensionEnabled = result.drugguard_enabled !== false; // default: enabled

      if (extensionEnabled) {
        injectStyles();
        scanPage();
        observeDOM();
      }
    });

    // Listen for enable/disable messages
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.type === "TOGGLE_EXTENSION") {
        extensionEnabled = message.enabled;
        if (extensionEnabled) {
          injectStyles();
          scanPage();
          observeDOM();
        }
        sendResponse({ ok: true });
      }

      if (message.type === "GET_STATS") {
        sendResponse({
          scanned: stats.scanned,
          warned: stats.warned,
          blocked: stats.blocked,
        });
      }

      if (message.type === "FORCE_RESCAN") {
        // Clear processed elements by re-initializing the WeakSet
        processedElements = new WeakSet();

        // Remove warning and block overlays from the page
        document.querySelectorAll(".drugguard-warn").forEach((el) => {
          el.classList.remove("drugguard-warn");
        });
        document.querySelectorAll(".drugguard-block").forEach((el) => {
          el.classList.remove("drugguard-block");
        });
        document.querySelectorAll(".drugguard-revealed").forEach((el) => {
          el.classList.remove("drugguard-revealed");
        });
        document.querySelectorAll(".drugguard-block-banner").forEach((el) => {
          el.remove();
        });

        // Reset page stats
        stats = { scanned: 0, warned: 0, blocked: 0, flaggedItems: [] };
        updateStats();

        // Start scanning again
        scanPage();
        sendResponse({ ok: true });
      }
    });

    // Global delegated click listener to ensure click-to-reveal always works
    // Uses capture phase (true) to intercept clicks before other event handlers block them
    document.addEventListener("click", (e) => {
      if (!extensionEnabled) return;

      const banner = e.target.closest(".drugguard-block-banner");
      const blockEl = e.target.closest(".drugguard-block");

      if (banner) {
        e.stopPropagation();
        e.preventDefault();
        const parent = banner.parentElement;
        if (parent) {
          const blurred = parent.querySelector(".drugguard-block");
          if (blurred) {
            blurred.classList.remove("drugguard-block");
            blurred.classList.add("drugguard-revealed");
          }
        }
        banner.remove();
      } else if (blockEl) {
        e.stopPropagation();
        e.preventDefault();
        blockEl.classList.remove("drugguard-block");
        blockEl.classList.add("drugguard-revealed");
        const parent = blockEl.parentElement;
        if (parent) {
          const bannerEl = parent.querySelector(".drugguard-block-banner");
          if (bannerEl) bannerEl.remove();
        }
      }
    }, true);
  }

  init();
})();
