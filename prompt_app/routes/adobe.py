from flask import Blueprint, current_app, render_template, request
from selenium.common.exceptions import WebDriverException

from ..services.adobe_stock import AdobeScrapingError, scrape_image_descriptions

adobe_bp = Blueprint("adobe", __name__)


@adobe_bp.route("/scrape", methods=["GET", "POST"])
def search():
    search_term = ""
    descriptions = None
    error = None
    if request.method == "POST":
        search_term = request.form.get("topic", "").strip()
        try:
            descriptions = scrape_image_descriptions(
                search_term,
                current_app.config["ADOBE_STOCK_SEARCH_URL"],
                current_app.config["ADOBE_SCRAPER_TIMEOUT"],
            )
        except (AdobeScrapingError, WebDriverException) as exc:
            descriptions = []
            error = str(exc)
    return render_template("adobe.html", images=descriptions, error=error, topic=search_term)
