import sqlite3
from forms import CharacterForm
from utils import process_character_form_data
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from urllib.parse import urlencode
import time

from flask import Flask, render_template, request


# creates the flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = '52jMEfBA3347dbefePSSiheXox3E7e'

# Define constants for Webscrapping feature
ADOBE_STOCK_SEARCH_URL = "https://stock.adobe.com/search"
WEBSCRAPPER_TIMEOUT = 20


class AdobeScrapingError(RuntimeError):
    """Raised when Adobe does not make search results available to Selenium."""

# Define constants for Landscape generator
LANDSCAPE_DROPDOWNS = [
    {
        "name": "time_of_day",
        "label": "Time of day",
        "options": ["sunrise", "morning", "midday", "afternoon", "evening", "sunset", "night"],
        "default": "sunrise",
    },
    {
        "name": "weather",
        "label": "Weather",
        "options": ["clear", "cloudy", "misty", "rainy", "stormy", "snowy"],
        "default": "clear",
    },
    {
        "name": "season",
        "label": "Season",
        "options": ["spring", "summer", "autumn", "winter"],
        "default": "spring",
    },
]

STYLE_KEYWORDS = {
    "photorealistic": "photorealistic, hyperrealistic, 8k, DSLR, sharp focus",
    "digital_art": "digital art, artstation, trending, vibrant colours",
    "oil_painting": "oil painting, impasto, textured canvas, classical",
    "watercolor": "watercolour, soft edges, wet-on-wet, pastel tones",
    "anime": "anime style, manga, cel shading, clean lines",
    "concept_art": "concept art, cinematic, detailed environment, matte painting",
    "pixel_art": "pixel art, 16-bit, retro game style",
    "3d_render": "3D render, octane render, subsurface scattering, ray tracing",
}

LIGHTING_KEYWORDS = {
    "golden_hour": "golden hour lighting, warm tones, long shadows",
    "neon": "neon glow, cyberpunk lighting, colourful reflections",
    "studio": "studio lighting, softbox, professional photography",
    "dramatic": "dramatic lighting, chiaroscuro, deep shadows, high contrast",
    "soft": "soft diffused lighting, overcast, gentle shadows",
    "volumetric": "volumetric lighting, god rays, atmospheric haze",
}

PLATFORM_SUFFIX = {
    "midjourney": "--ar {ratio} --v 6 --style raw",
    "dalle": "",
    "stable_diffusion": ", masterpiece, best quality",
    "firefly": "",
    "leonardo": ", ultra detailed, high quality",
}


# Function to initialize the Selenium WebDriver
def init_webdriver():
    # Setting up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # Use Chrome's current headless implementation
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    return driver


# Function to scrape Adobe Stock Images using Selenium
def scrape_adobe_images(query):
    query = (query or "").strip()
    if not query:
        return []

    driver = init_webdriver()
    try:
        # Going directly to the results page avoids depending on Adobe's changing
        # home-page search input (which no longer reliably has name="keyword").
        search_url = f"{ADOBE_STOCK_SEARCH_URL}?{urlencode({'k': query})}"
        driver.get(search_url)

        WebDriverWait(driver, WEBSCRAPPER_TIMEOUT).until(
            lambda current_driver: current_driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        # Adobe has used both native images and ARIA-labelled image containers.
        # Poll while scrolling because result cards are lazy-loaded.
        result_selector = (
            "img[alt]:not([alt='']), "
            "[role='img'][aria-label]:not([aria-label='']), "
            "a[href*='/images/'][aria-label]:not([aria-label=''])"
        )
        deadline = time.monotonic() + WEBSCRAPPER_TIMEOUT
        images = []
        while time.monotonic() < deadline:
            images = driver.find_elements(By.CSS_SELECTOR, result_selector)
            if images:
                break
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(0.5)

        if not images:
            page_title = driver.title or "untitled page"
            raise AdobeScrapingError(
                "Adobe did not provide image results to the automated browser "
                f"(page: {page_title}). It may be showing a consent, region, "
                "CAPTCHA, or bot-protection page."
            )

        # Return plain strings: WebElement objects become invalid after quit().
        descriptions = []
        seen = set()
        for image in images:
            description = (
                image.get_attribute("alt")
                or image.get_attribute("aria-label")
                or ""
            ).strip()
            if len(description) > 1 and description not in seen:
                descriptions.append(description)
                seen.add(description)
            if len(descriptions) == 100:
                break

        return descriptions

    finally:
        driver.quit()

# Function to establish a connection to the database
def get_db_connection():
    database_path = Path(app.instance_path) / "prompts.db"
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            prompt TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    return connection


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prompt", methods=["GET", "POST"])
def prompt():
    title = ""
    prompt_text = ""
    submitted = False
    saved = False

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        prompt_text = request.form.get("prompt", "").strip()
        submitted = bool(title and prompt_text)

        if submitted and request.form.get("save_prompt") == "yes":
            with get_db_connection() as connection:
                connection.execute(
                    "INSERT INTO prompts (title, prompt) VALUES (?, ?)",
                    (title, prompt_text),
                )
            saved = True

    return render_template(
        "prompt.html",
        title=title,
        prompt_text=prompt_text,
        submitted=submitted,
        saved=saved,
    )


@app.route("/landscape", methods=["GET", "POST"])
def landscape():
    description = ""
    generated_prompt = ""
    selections = {
        dropdown["name"]: dropdown["default"]
        for dropdown in LANDSCAPE_DROPDOWNS
    }

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        for dropdown in LANDSCAPE_DROPDOWNS:
            selected = request.form.get(dropdown["name"], dropdown["default"])
            if selected in dropdown["options"]:
                selections[dropdown["name"]] = selected
        generated_prompt = request.form.get("generated_prompt", "").strip()

        if request.form.get("action") == "generate" and description:
            generated_prompt = (
                f"{description} Set during {selections['time_of_day']}, with "
                f"{selections['weather']} weather in {selections['season']}. "
                "Expansive landscape composition, rich natural detail, "
                "atmospheric depth, and cinematic lighting."
            )

    return render_template(
        "landscape.html",
        description=description,
        dropdowns=LANDSCAPE_DROPDOWNS,
        selections=selections,
        generated_prompt=generated_prompt,
    )

@app.route("/prompt_generator", methods=["GET", "POST"])
def prompt_generator():
    result = None
    idea = platform = style = lighting = ratio = keywords = None
    if request.method == "POST":
        idea      = request.form.get("idea", "").strip()
        platform  = request.form.get("platform", "midjourney")
        style     = request.form.get("style", "")
        lighting  = request.form.get("lighting", "")
        ratio     = request.form.get("ratio", "1:1")
        keywords  = request.form.get("keywords", "").strip()

        parts = [idea]

        if style and style in STYLE_KEYWORDS:
            parts.append(STYLE_KEYWORDS[style])

        if lighting and lighting in LIGHTING_KEYWORDS:
            parts.append(LIGHTING_KEYWORDS[lighting])

        if keywords:
            parts.append(keywords)

        prompt = ", ".join(p for p in parts if p)

        suffix = PLATFORM_SUFFIX.get(platform, "")
        if suffix:
            prompt += " " + suffix.replace("{ratio}", ratio)

        result = prompt

    return render_template("prompt_generator.html",
                           result=result, idea=idea, platform=platform,
                           style=style, lighting=lighting, ratio=ratio,
                           keywords=keywords)


@app.route("/character", methods=["GET", "POST"])
def character():
    form = CharacterForm()

    if request.method == "POST":
        prompt = process_character_form_data(request.form)

        # print(prompt)
        return render_template('character.html', form=form, prompt=prompt)

    # Render the template without a result if the form is not submitted
    return render_template('character.html', form=form)

@app.route("/scrape", methods=["GET", "POST"])
def adobe():
    search_term = ""
    # print("scrape called")
    if request.method == "POST":
        # print("scrape post")
        search_term = request.form.get("topic")
        error = None
        try:
            images = scrape_adobe_images(search_term)
        except (AdobeScrapingError, WebDriverException) as exc:
            images = []
            error = str(exc)
        # for image in images:
        #     print(f'{image.get_attribute("alt")}{image.get_attribute("name")}\n')
        return render_template('adobe.html',
                               images=images,
                               error=error,
                               topic=search_term)

    return render_template('adobe.html',
                           images=None,
                           topic=search_term)



if __name__ == "__main__":
    app.run(debug=True)
