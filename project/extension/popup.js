/**
 * popup.js
 * DrugGuard — Popup Dashboard Logic
 *
 * Reads stats from chrome.storage.local, manages toggle state,
 * and renders the flagged items list.
 */

document.addEventListener("DOMContentLoaded", () => {
  const toggleSwitch = document.getElementById("toggleSwitch");
  const statusDot = document.getElementById("statusDot");
  const statusText = document.getElementById("statusText");
  const scannedCount = document.getElementById("scannedCount");
  const warnedCount = document.getElementById("warnedCount");
  const blockedCount = document.getElementById("blockedCount");
  const flaggedList = document.getElementById("flaggedList");
  const flagCount = document.getElementById("flagCount");
  const emptyState = document.getElementById("emptyState");

  // ─── Load Initial State ─────────────────
  function loadState() {
    // Get enabled state
    chrome.storage.local.get(["drugguard_enabled", "drugguard_stats"], (result) => {
      const enabled = result.drugguard_enabled !== false;
      toggleSwitch.checked = enabled;
      updateStatusUI(enabled);

      // Load stats
      const stats = result.drugguard_stats || {
        scanned: 0,
        warned: 0,
        blocked: 0,
        flaggedItems: [],
      };

      updateStatsUI(stats);
      renderFlaggedItems(stats.flaggedItems || []);
    });
  }

  // ─── Update Status Indicator ───────────
  function updateStatusUI(enabled) {
    if (enabled) {
      statusDot.className = "status-dot active";
      statusText.className = "status-text active";
      statusText.textContent = "Monitoring active";
    } else {
      statusDot.className = "status-dot inactive";
      statusText.className = "status-text";
      statusText.textContent = "Protection paused";
    }
  }

  // ─── Update Stats Numbers ──────────────
  function updateStatsUI(stats) {
    animateCounter(scannedCount, parseInt(scannedCount.textContent) || 0, stats.scanned);
    animateCounter(warnedCount, parseInt(warnedCount.textContent) || 0, stats.warned);
    animateCounter(blockedCount, parseInt(blockedCount.textContent) || 0, stats.blocked);
  }

  function animateCounter(element, from, to) {
    if (from === to) {
      element.textContent = to;
      return;
    }
    const duration = 400;
    const startTime = Date.now();

    function tick() {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      const current = Math.round(from + (to - from) * eased);
      element.textContent = current;
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  // ─── Render Flagged Items ──────────────
  function renderFlaggedItems(items) {
    const displayItems = items.slice(0, 5);
    flagCount.textContent = items.length;

    if (displayItems.length === 0) {
      emptyState.style.display = "block";
      // Remove any existing items
      const existingItems = flaggedList.querySelectorAll(".flagged-item");
      existingItems.forEach((item) => item.remove());
      return;
    }

    emptyState.style.display = "none";

    // Clear existing items (except empty state)
    const existingItems = flaggedList.querySelectorAll(".flagged-item");
    existingItems.forEach((item) => item.remove());

    displayItems.forEach((item) => {
      const div = document.createElement("div");
      div.className = "flagged-item";

      const badgeClass = item.action === "block" ? "block" : "warn";
      const badgeEmoji = item.action === "block" ? "🔴" : "🟡";
      const badgeLabel = item.action === "block" ? "Blocked" : "Suspicious";

      div.innerHTML = `
        <div class="flagged-item-top">
          <span class="badge ${badgeClass}">${badgeEmoji} ${badgeLabel}</span>
          <span class="risk-score">${item.riskScore}%</span>
        </div>
        <div class="flagged-text">${escapeHtml(item.text)}</div>
      `;

      flaggedList.appendChild(div);
    });
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // ─── Toggle Handler ────────────────────
  toggleSwitch.addEventListener("change", () => {
    const enabled = toggleSwitch.checked;

    chrome.runtime.sendMessage({ type: "SET_STATE", enabled }, () => {
      updateStatusUI(enabled);
    });
  });

  // ─── Rescan Handler ────────────────────
  const refreshBtn = document.getElementById("refreshBtn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
          chrome.tabs.sendMessage(tabs[0].id, { type: "FORCE_RESCAN" }, (response) => {
            // Visual feedback
            const originalText = refreshBtn.innerHTML;
            refreshBtn.innerHTML = "⏳ Scanning...";
            refreshBtn.style.pointerEvents = "none";
            setTimeout(() => {
              refreshBtn.innerHTML = "✅ Done";
              setTimeout(() => {
                refreshBtn.innerHTML = originalText;
                refreshBtn.style.pointerEvents = "auto";
                loadState(); // reload stats
              }, 800);
            }, 800);
          });
        }
      });
    });
  }

  // ─── Listen for Storage Changes ────────
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== "local") return;

    if (changes.drugguard_stats) {
      const stats = changes.drugguard_stats.newValue;
      updateStatsUI(stats);
      renderFlaggedItems(stats.flaggedItems || []);
    }

    if (changes.drugguard_enabled) {
      const enabled = changes.drugguard_enabled.newValue;
      toggleSwitch.checked = enabled;
      updateStatusUI(enabled);
    }
  });

  // ─── Init ──────────────────────────────
  loadState();
});
