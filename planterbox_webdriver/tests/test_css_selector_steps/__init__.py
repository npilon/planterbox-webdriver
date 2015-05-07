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
    step,
)
from planterbox_webdriver.css_selector_steps import *


@hook('before', 'scenario')
def reset_browser(scenario):
    browser.get('')


@step(r'I go to test page "(\w+)"')
def go_to_test_page(test, page_name):
    from ..html_pages import PAGES
    url = PAGES[page_name]
    browser.get(url)
