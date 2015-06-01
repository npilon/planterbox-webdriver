from ..html_pages import PAGES
from planterbox import (
    hook,
)
from planterbox_webdriver.webdriver import *


@hook('before', 'feature')
def create_webdriver(test):
    from planterbox_webdriver.monkeypatch import fix_inequality
    fix_inequality()
    from selenium import webdriver
    test.world.browser = webdriver.Firefox()


@hook('after', 'feature')
def quit_webdriver(test):
    global browser
    test.world.browser.quit()
    test.world.browser = None


@hook('before', 'scenario')
def reset_browser(test):
    test.world.browser.get('')
