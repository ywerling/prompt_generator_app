import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-change-me")
    ADOBE_STOCK_SEARCH_URL = "https://stock.adobe.com/search"
    ADOBE_SCRAPER_TIMEOUT = 20
