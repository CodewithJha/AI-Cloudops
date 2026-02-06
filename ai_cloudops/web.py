import webbrowser
from .config import app_config


def open_default_webpage():
    webbrowser.open_new(app_config.default_web_url)

