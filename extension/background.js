// background.js - DrugGuard Coordination Worker

// Keep tracker statistics in sync with local storage
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    enabled: true,
    scannedText: 0,
    scannedImages: 0,
    blockedCount: 0,
    warnedCount: 0,
    threshold: 0.7,
    backendUrl: "http://localhost:8000"
  });
  console.log("DrugGuard Background Worker initialized.");
});

// Listener to handle messaging between Popup and Content Script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getStats") {
    chrome.storage.local.get(["scannedText", "scannedImages", "blockedCount", "warnedCount"], (result) => {
      sendResponse(result);
    });
    return true;
  }
  
  if (request.action === "updateStats") {
    chrome.storage.local.get(["scannedText", "scannedImages", "blockedCount", "warnedCount"], (result) => {
      const updated = {
        scannedText: (result.scannedText || 0) + (request.scannedText || 0),
        scannedImages: (result.scannedImages || 0) + (request.scannedImages || 0),
        blockedCount: (result.blockedCount || 0) + (request.blockedCount || 0),
        warnedCount: (result.warnedCount || 0) + (request.warnedCount || 0)
      };
      chrome.storage.local.set(updated);
      sendResponse({ status: "success", stats: updated });
    });
    return true;
  }
});
