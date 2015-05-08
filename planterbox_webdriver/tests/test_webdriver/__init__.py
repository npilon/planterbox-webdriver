from ..html_pages import PAGES

browser = None

from planterbox import (
    hook,
)
from planterbox_webdriver.webdriver import *


def setUpModule(feat):
    from selenium import webdriver
    global browser
    browser = webdriver.Firefox()


def tearDownModule(feat):
    global browser
    browser.quit()
    browser = None


@hook('before', 'scenario')
def reset_browser(scenario):
    browser.get('')
