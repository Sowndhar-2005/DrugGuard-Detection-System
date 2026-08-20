"""
verify_extension.py
DrugGuard — Automated Chrome Extension E2E Test

This script uses Playwright to launch Chromium with your unpacked extension loaded,
navigates to test_page.html, waits for the extension to scan the DOM & apply visual overlays,
and captures a screenshot to verify that the drug-related items are successfully blurred.

Run:
    pip install playwright
    playwright install chromium
    py -3 verify_extension.py
"""

import asyncio
import os
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSION_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "extension"))
TEST_PAGE_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "test_page.html"))
SCREENSHOT_PATH = os.path.join(BASE_DIR, "extension_test_screenshot.png")

async def main():
    print("="*60)
    print("🤖 Launching Chrome with DrugGuard Extension...")
    print("="*60)
    
    async with async_playwright() as p:
        # Launch Chromium with extension loaded
        # Note: Extensions only load in headful mode (headless=False)
        context = await p.chromium.launch_persistent_context(
            user_data_dir=os.path.join(BASE_DIR, "playwright_profile"),
            headless=False,
            args=[
                f"--disable-extensions-except={EXTENSION_PATH}",
                f"--load-extension={EXTENSION_PATH}",
            ]
        )
        
        page = await context.new_page()
        
        # Listen for console messages
        page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[Browser Error] {err}"))
        
        # Navigate to the local test page
        file_url = f"file:///{TEST_PAGE_PATH.replace(os.sep, '/')}"
        print(f"🔗 Navigating to: {file_url}")
        await page.goto(file_url)
        
        # Wait 4 seconds for DOM parsing, API calls, and blur overlay rendering
        print("⏳ Waiting for API responses and visual overlays to render...")
        await page.wait_for_timeout(4000)
        
        # Save verification screenshot
        print("📸 Capturing screenshot...")
        await page.screenshot(path=SCREENSHOT_PATH, full_page=True)
        print(f"✅ Screenshot saved to: {SCREENSHOT_PATH}")
        
        await context.close()
        
    print("="*60)
    print("🎉 Verification complete. Open extension_test_screenshot.png to review!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
