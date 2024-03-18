from typing import Optional
from playwright.async_api import async_playwright
from fastapi import FastAPI

app = FastAPI()

app.playwright = async_playwright()
app.is_started = False
app.browser = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def read_root():
    return "OK"


@app.get("/api/assess")
async def assess(propery_id: str):
    if not app.is_started:
        app.is_started = True
        app.playwright = await app.playwright.start()

    if not app.browser or not app.browser.is_connected:
        app.browser = await app.playwright.chromium.launch()

    assessment_url = f"https://www.bcassessment.ca//Property/Info/${propery_id}"
    page = await app.browser.new_page()
    await page.goto(assessment_url)

    try:
        cost = await page.locator("#lblTotalAssessedValue").inner_text()
    except Exception as e:
        await page.get_by_role("checkbox").check()
        await page.get_by_role("button").click()
        cost = await page.locator("#lblTotalAssessedValue").inner_text()

    await page.close()
    return {"cost": cost}
