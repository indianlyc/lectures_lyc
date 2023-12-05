from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # for browser_type in [p.chromium]: # , p.firefox, p.webkit]:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://www.tinkercad.com')
    page.screenshot(path=f'example-{p.chromium.name}.png')
    browser.close()