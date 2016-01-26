from ..html_pages import PAGES
from planterbox import (
    hook,
)
from planterbox_webdriver.css_selector_steps import *
from planterbox_webdriver.webdriver import visit

@hook('before', 'feature')
def create_webdriver(test):
    from planterbox_webdriver.monkeypatch import fix_inequality
    fix_inequality()
    from selenium import webdriver
    test.browser = webdriver.Firefox()


@hook('after', 'feature')
def quit_webdriver(test):
    test.browser.quit()
    test.browser = None


@hook('before', 'scenario')
def reset_browser(test):
    test.browser.get('')