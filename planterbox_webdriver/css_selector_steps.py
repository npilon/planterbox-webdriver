import os.path
import time

from planterbox import step

from selenium.common.exceptions import WebDriverException

import logging
log = logging.getLogger(__name__)


def wait_for_elem(browser, sel, timeout=15):
    start = time.time()
    elems = []
    while time.time() - start < timeout:
        elems = find_elements_by_jquery(browser, sel)
        if elems:
            return elems
        time.sleep(0.2)
    return elems


def load_jquery(browser):
    """Ensure that JQuery is available to the browser."""
    jquery = open(os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'jquery-2.2.0.min.js')
    ))
    browser.execute_script(jquery.read())


def find_elements_by_jquery(browser, selector):
    """Find HTML elements using jQuery-style selectors.

    Ensures that jQuery is available to the browser; if it gets a
    WebDriverException that looks like jQuery is not available, it attempts to
    include it and reexecute the script."""
    try:
        return browser.execute_script(
            """return ($ || jQuery)(arguments[0]).get();""", selector
        )
    except WebDriverException as e:
        if e.msg.startswith(u'$ is not defined'):
            load_jquery(browser)
            return browser.execute_script(
                """return ($ || jQuery)(arguments[0]).get();""", selector,
            )
        else:
            raise


def find_element_by_jquery(test, browser, selector):
    """Find a single HTML element using jQuery-style selectors."""
    elements = find_elements_by_jquery(browser, selector)
    test.assertGreater(len(elements), 0,
                       u'No elements matched: {}'.format(selector))
    return elements[0]


def find_parents_by_jquery(browser, selector):
    """Find HTML elements' parents using jQuery-style selectors.

    In addition to reliably including jQuery, this also finds the pa"""
    try:
        return browser.execute_script(
            """return ($ || jQuery)(arguments[0]).parent().get();""", selector
        )
    except WebDriverException as e:
        if e.msg.startswith(u'$ is not defined'):
            load_jquery(browser)
            return browser.execute_script(
                """return ($ || jQuery)(arguments[0]).parent().get();""",
                selector,
            )
        else:
            raise


@step(r'There should be an element matching \$\("(.*?)"\)$')
def check_element_by_selector(test, selector):
    elems = find_elements_by_jquery(test.browser, selector)
    test.assertTrue(elems)


@step(
    r'There should be an element matching \$\("(.*?)"\) within (\d+) seconds?$'
)
def wait_for_element_by_selector(test, selector, seconds):
    elems = wait_for_elem(test.browser, selector, int(seconds))
    test.assertTrue(elems)


@step(r'There should be exactly (\d+) elements matching \$\("(.*?)"\)$')
def count_elements_exactly_by_selector(test, number, selector):
    elems = find_elements_by_jquery(test.browser, selector)
    test.assertEqual(len(elems), int(number))


@step(r'I fill in \$\("(.*?)"\) with "(.*?)"$')
def fill_in_by_selector(test, selector, value):
    elem = find_element_by_jquery(test, test.browser, selector)
    elem.clear()
    elem.send_keys(value)


@step(r'I submit \$\("(.*?)"\)')
def submit_by_selector(test, selector):
    elem = find_element_by_jquery(test, test.browser, selector)
    elem.submit()


@step(r'I check \$\("(.*?)"\)$')
def check_by_selector(test, selector):
    elem = find_element_by_jquery(test, test.browser, selector)
    if not elem.is_selected():
        elem.click()


@step(r'I click \$\("(.*?)"\)$')
def click_by_selector(test, selector):
    # No need for separate button press step with selector style.
    elem = find_element_by_jquery(test, test.browser, selector)
    elem.click()


@step(r'I follow the link \$\("(.*?)"\)$')
def click_link_by_selector(test, selector):
    elem = find_element_by_jquery(test, test.browser, selector)
    href = elem.get_attribute('href')
    test.browser.get(href)


@step(r'\$\("(.*?)"\) should be selected$')
def selected_by_selector(test, selector):
    elem = find_element_by_jquery(test, test.browser, selector)
    test.assertTrue(elem.is_selected())


@step(r'I select \$\("(.*?)"\)$')
def select_by_selector(test, selector):
    option = find_element_by_jquery(test, test.browser, selector)
    selectors = find_parents_by_jquery(test.browser, selector)
    test.assertGreater(len(selectors), 0)
    selector = selectors[0]
    selector.click()
    time.sleep(0.3)
    option.click()
    test.assertTrue(option.is_selected())


@step(r'There should not be an element matching \$\("(.*?)"\)$')
def check_no_element_by_selector(test, selector):
    elems = find_elements_by_jquery(test.browser, selector)
    test.assertFalse(elems)


__all__ = [
    maybe_step_name for maybe_step_name, maybe_step in globals().items()
    if hasattr(maybe_step, 'planterbox_patterns')
]
