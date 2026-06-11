/**
 * background.js
 * DrugGuard — Service Worker (Manifest V3)
 *
 * Manages extension state, handles messages from content script and popup.
 */

// ─── Extension Installation ──────────────────
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === "install") {
    // Set default state
    chrome.storage.local.set({
      drugguard_enabled: true,
      drugguard_stats: {
        scanned: 0,
        warned: 0,
        blocked: 0,
        flaggedItems: [],
      },
    });
    console.log("DrugGuard installed — extension enabled by default.");
  }
});

// ─── Message Handling ────────────────────────
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.type) {
    case "GET_STATE":
      chrome.storage.local.get(["drugguard_enabled"], (result) => {
        sendResponse({ enabled: result.drugguard_enabled !== false });
      });
      return true; // async response

    case "SET_STATE":
      chrome.storage.local.set({ drugguard_enabled: message.enabled }, () => {
        // Notify all content scripts
        chrome.tabs.query({}, (tabs) => {
          tabs.forEach((tab) => {
            chrome.tabs.sendMessage(tab.id, {
              type: "TOGGLE_EXTENSION",
              enabled: message.enabled,
            }).catch(() => {
              // Tab might not have content script loaded
            });
          });
        });
        sendResponse({ ok: true });
      });
      return true;

    case "STATS_UPDATE":
      // Content script is updating stats — forward to popup if open
      // Stats are already stored in chrome.storage.local by content script
      break;

    case "RESET_STATS":
      chrome.storage.local.set({
        drugguard_stats: {
          scanned: 0,
          warned: 0,
          blocked: 0,
          flaggedItems: [],
        },
      });
      sendResponse({ ok: true });
      return true;

    case "FETCH_IMAGE":
      fetchImageAsBase64(message.url)
        .then((base64Data) => sendResponse({ ok: true, data: base64Data }))
        .catch((err) => sendResponse({ ok: false, error: err.message }));
      return true; // async response

    default:
      break;
  }
});

// Helper to fetch remote image and convert it to Base64 in Service Worker
async function fetchImageAsBase64(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch image: ${response.status} ${response.statusText}`);
  }
  const blob = await response.blob();
  const buffer = await blob.arrayBuffer();
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  const base64 = btoa(binary);
  return `data:${blob.type || "image/jpeg"};base64,${base64}`;
}

