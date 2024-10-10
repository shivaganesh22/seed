from django.test import TestCase

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)
try:
    browser.get("https://www.google.com")
    print("Page title was '{}'".format(browser.title))
finally:
    browser.quit()