from ..html_pages import PAGES
from planterbox import (
    hook,
)
from planterbox_webdriver.css_selector_steps import *
from planterbox_webdriver.webdriver import visit

browser = None


@hook('before', 'feature')
def create_webdriver(feat):
    from planterbox_webdriver.monkeypatch import fix_inequality
    fix_inequality()
    from selenium import webdriver
    global browser
    browser = webdriver.Firefox()


@hook('after', 'feature')
def quit_webdriver(feat):
    global browser
    browser.quit()
    browser = None


@hook('before', 'scenario')
def reset_browser(scenario):
    browser.get('')
