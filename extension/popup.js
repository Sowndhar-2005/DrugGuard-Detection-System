// popup.js - Controls, toggles, configuration, and statistics update

document.addEventListener("DOMContentLoaded", () => {
  const extensionToggle = document.getElementById("extension-toggle");
  const statusBadge = document.getElementById("status-badge");
  const activeUrlDisplay = document.getElementById("active-url-display");
  const backendUrlInput = document.getElementById("backend-url");
  const thresholdRange = document.getElementById("threshold-range");
  const thresholdVal = document.getElementById("threshold-val");
  
  const statScannedText = document.getElementById("stat-scanned-text");
  const statScannedImg = document.getElementById("stat-scanned-img");
  const statBlocked = document.getElementById("stat-blocked");
  const statWarned = document.getElementById("stat-warned");

  const saveSettingsBtn = document.getElementById("save-settings-btn");
  const refreshPageBtn = document.getElementById("refresh-page-btn");
  const resetStatsBtn = document.getElementById("reset-stats-btn");

  // ── Get Active Tab URL ──
  if (chrome.tabs && chrome.tabs.query) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0] && tabs[0].url) {
        const tabUrl = tabs[0].url;
        activeUrlDisplay.textContent = `🌐 Site: ${tabUrl.length > 35 ? tabUrl.substring(0, 35) + "..." : tabUrl}`;
        activeUrlDisplay.title = tabUrl;
      } else {
        activeUrlDisplay.textContent = "🌐 Site: Current Webpage";
      }
    });
  }

  // ── Load Settings and Stats ──
  function loadSettings() {
    chrome.storage.local.get(
      ["enabled", "backendUrl", "threshold", "scannedText", "scannedImages", "blockedCount", "warnedCount"],
      (res) => {
        // Load toggle
        const isEnabled = res.enabled !== false;
        extensionToggle.checked = isEnabled;
        updateBadge(isEnabled);

        // Load config inputs
        if (backendUrlInput) {
          backendUrlInput.value = res.backendUrl || "http://localhost:8000";
        }
        const thresh = res.threshold !== undefined ? res.threshold : 0.7;
        thresholdRange.value = thresh;
        thresholdVal.textContent = parseFloat(thresh).toFixed(2);

        // Load stats
        statScannedText.textContent = res.scannedText || 0;
        statScannedImg.textContent = res.scannedImages || 0;
        statBlocked.textContent = res.blockedCount || 0;
        statWarned.textContent = res.warnedCount || 0;
      }
    );
  }

  function updateBadge(enabled) {
    if (enabled) {
      statusBadge.textContent = "Active protection";
      statusBadge.className = "status-badge status-active";
    } else {
      statusBadge.textContent = "Protection disabled";
      statusBadge.className = "status-badge status-inactive";
    }
  }

  // ── Event Handlers ──

  // Slider change
  thresholdRange.addEventListener("input", (e) => {
    thresholdVal.textContent = parseFloat(e.target.value).toFixed(2);
  });

  // Enable/Disable switch
  extensionToggle.addEventListener("change", (e) => {
    const isChecked = e.target.checked;
    chrome.storage.local.set({ enabled: isChecked });
    updateBadge(isChecked);
  });

  // Save Config
  saveSettingsBtn.addEventListener("click", () => {
    const url = backendUrlInput ? backendUrlInput.value.trim() : "http://localhost:8000";
    const threshold = parseFloat(thresholdRange.value);

    chrome.storage.local.set({
      backendUrl: url,
      threshold: threshold
    }, () => {
      alert("Settings saved successfully!");
    });
  });

  // Refresh Webpage Button
  if (refreshPageBtn) {
    refreshPageBtn.addEventListener("click", () => {
      if (chrome.tabs && chrome.tabs.query) {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs && tabs[0] && tabs[0].id) {
            chrome.tabs.reload(tabs[0].id, () => {
              window.close(); // Close popup after triggering reload
            });
          }
        });
      }
    });
  }

  // Reset Stats
  resetStatsBtn.addEventListener("click", () => {
    if (confirm("Are you sure you want to reset scanned stats?")) {
      chrome.storage.local.set({
        scannedText: 0,
        scannedImages: 0,
        blockedCount: 0,
        warnedCount: 0
      }, () => {
        statScannedText.textContent = 0;
        statScannedImg.textContent = 0;
        statBlocked.textContent = 0;
        statWarned.textContent = 0;
      });
    }
  });

  // Initial call
  loadSettings();
  
  // Periodically refresh stats
  setInterval(() => {
    chrome.storage.local.get(["scannedText", "scannedImages", "blockedCount", "warnedCount"], (res) => {
      statScannedText.textContent = res.scannedText || 0;
      statScannedImg.textContent = res.scannedImages || 0;
      statBlocked.textContent = res.blockedCount || 0;
      statWarned.textContent = res.warnedCount || 0;
    });
  }, 1000);
});
