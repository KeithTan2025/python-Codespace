"""
TOTO Results OCR Scraper (Playwright + Tesseract)
- Fetches https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx
- Takes a full-page screenshot
- Extracts visible text using Tesseract OCR
- Saves image and text locally

Dependencies:
  pip install playwright pillow pytesseract
  playwright install chromium

Note: Tesseract OCR must be installed separately on your system.
"""
import sys
import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import pytesseract
import os

OUTPUT_IMAGE = "toto_results.png"
OUTPUT_TEXT = "toto_results.txt"
AMOUNT_TEXT = "toto_amount.txt"

URL = "https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx"


async def main():
    async with async_playwright() as p:
        print("🌐 Launching browser in headless mode...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            print(f"📥 Navigating to {URL}...")
            await page.goto(URL, wait_until="networkidle")

            # Emulate a wide viewport for full content capture
            await page.set_viewport_size({"width": 1920, "height": 1080})

            # Wait extra moment for any JS-rendered content
            await page.wait_for_timeout(2000)

            # Capture full page
            await page.screenshot(path=OUTPUT_IMAGE, full_page=True)
            print(f"📸 Screenshot saved as '{OUTPUT_IMAGE}'")

            # Run OCR
            print("🔍 Running OCR on screenshot...")
            image = Image.open(OUTPUT_IMAGE)
            extracted_text = pytesseract.image_to_string(image, lang='eng').strip()

            # Save text
            with open(OUTPUT_TEXT, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"📄 Extracted text saved as '{OUTPUT_TEXT}'")

            with open(OUTPUT_TEXT) as f:
                amount_text = f.readlines()[25]
                print(amount_text)

            try:
                with open(OUTPUT_TEXT, 'r') as f:
                    for line in f:
                        start = 0
                        while True:
                            pos = line.find("Next Jackpot", start)
                            if pos == -1:
                                break
                            # Extract up to 10 characters after the match
                            after = line[pos + len("Next Jackpot") : pos + len("Next Jackpot") + 10]
                            after_no_spaces = after.replace(' ', '')
                            print(repr(after_no_spaces))  # Use repr to show spaces, newlines, etc.
                            start = pos + 1  # Allow overlapping matches (optional)
            except FileNotFoundError:
                print(f"Error: File '{OUTPUT_TEXT}' not found.", file=sys.stderr)
                sys.exit(1)


            # Save amount
            with open(AMOUNT_TEXT, "w", encoding="utf-8") as f:
                f.write(after_no_spaces)
            print(f"📄 Amount text saved as '{AMOUNT_TEXT}'")


        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())