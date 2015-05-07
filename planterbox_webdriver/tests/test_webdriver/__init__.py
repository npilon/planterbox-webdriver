from ..html_pages import PAGES

browser = None


from planterbox import (
    hook,
)
from planterbox_webdriver.webdriver import *


@hook('before', 'feature')
def instantiate_browser(feature_suite):
    from selenium import webdriver
    global browser
    browser = webdriver.Firefox()


@hook('after', 'feature')
def quit_browser(feature_suite):
    global browser
    browser.quit()
    browser = None


@hook('before', 'scenario')
def reset_browser(scenario):
    browser.get('')
