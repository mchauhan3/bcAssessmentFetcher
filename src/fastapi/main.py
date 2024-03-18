from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
from fastapi import FastAPI, HTTPException

app = FastAPI()

app.is_started = False
app.browser = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return "OK"


@app.get("/api/assess", status_code=200)
async def assess(property_id: str):
    if not app.is_started:
        app.is_started = True
        app.playwright = await async_playwright().start()

    if not app.browser or not app.browser.is_connected:
        app.browser = await app.playwright.chromium.launch(headless=False)

    assessment_url = f"https://www.bcassessment.ca//Property/Info/${property_id}"
    captcha_url = "https://www.bcassessment.ca/Property/UsageValidation"

    page = await app.browser.new_page()
    await stealth_async(page)
    await page.goto(assessment_url)

    def handle_captcha(frame):
        if frame.url == captcha_url:
            raise HTTPException(status_code=451, detail="Cannot proceed with captcha")

    page.on("framenavigated", handle_captcha)
    cost = await page.locator("#lblTotalAssessedValue").inner_text()

    await page.close()
    return {"cost": cost}
