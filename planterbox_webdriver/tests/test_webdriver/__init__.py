from ..html_pages import PAGES

browser = None


def setUpModule():
    from selenium import webdriver
    global browser
    browser = webdriver.Firefox()


def tearDownModule():
    global browser
    browser.quit()


from planterbox import (
    hook,
)
from planterbox_webdriver.webdriver import *


@hook('before', 'scenario')
def reset_browser(scenario):
    browser.get('')
