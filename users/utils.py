# from playwright.sync_api import sync_playwright
# from cloudinary.uploader import upload
# import tempfile

# def capture_screenshot_and_upload(url: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)  # Launch browser in headless mode
#         page = browser.new_page()  # Create a new page

#         # Navigate to the URL and wait until the network is idle
#         page.goto(url, timeout=90000, wait_until="domcontentloaded")  

#         screenshot = page.screenshot()  # Take a screenshot of the page
#         browser.close()  # Close the browser

#     # Save the screenshot to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
#         tmpfile.write(screenshot)  # Write the screenshot to the temporary file
#         tmpfile.close()

#         # Upload the screenshot to Cloudinary and return the URL
#         response = upload(tmpfile.name, folder="houses/screenshot")
#         return response['secure_url']


# utils.py
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import cloudinary.uploader
import os

def capture_property_screenshot(property_obj):
    """
    Uses Selenium to capture a screenshot of the property page
    and uploads it to Cloudinary. Returns Cloudinary URL.
    """
    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1200,800")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Build absolute URL for the property detail page
        url = f"{settings.SITE_URL}/property_detail/{property_obj.id}/"
        driver.get(url)

        # Take screenshot into a temporary file
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        driver.save_screenshot(tmp_file.name)

        # Upload screenshot to Cloudinary
        upload_result = cloudinary.uploader.upload(
            tmp_file.name,
            folder="property_screenshots",
            use_filename=True,
            unique_filename=False
        )

        # Return Cloudinary URL
        return upload_result.get("secure_url")

    finally:
        driver.quit()






