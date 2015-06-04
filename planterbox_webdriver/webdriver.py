"""Webdriver support for lettuce"""

from importlib import import_module

from planterbox import step

from planterbox_webdriver.util import (
    find_any_field,
    find_button,
    find_field,
    find_option,
    option_in_select,
    wait_for,
)

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    NoAlertPresentException,
    WebDriverException)

# pylint:disable=missing-docstring,redefined-outer-name


def contains_content(browser, content):
    # Search for an element that contains the whole of the text we're looking
    #  for in it or its subelements, but whose children do NOT contain that
    #  text - otherwise matches <body> or <html> or other similarly useless
    #  things.
    for elem in browser.find_elements_by_xpath(unicode(
        u'//*[contains(normalize-space(.),"{content}") '
        u'and not(./*[contains(normalize-space(.),"{content}")])]'.format(
            content=content))):

        try:
            if elem.is_displayed():
                return True
        except StaleElementReferenceException:
            pass

    return False


@wait_for
def wait_for_elem(browser, xpath):
    return browser.find_elements_by_xpath(str(xpath))


@wait_for
def wait_for_content(browser, content):
    return contains_content(browser, content)


def lookup_url(test, url):
    if hasattr(test, 'PAGES'):
        return getattr(test, 'PAGES', {}).get(url, url)
    else:
        module = import_module(test.__module__)
        return getattr(module, 'PAGES', {}).get(url, url)


# URLS
@step('I visit "(.*?)"$')
@step('I go to "(.*?)"$')
def visit(test, url):
    url = lookup_url(test, url)
    test.browser.get(url)


# Links
@step('I click "(.*?)"$')
def click(test, name):
    elem = test.browser.find_element_by_link_text(name)
    elem.click()


@step('I should see a link with the url "(.*?)"$')
def should_see_link(test, link_url):
    test.assertTrue(test.browser.find_element_by_xpath(
        u'//a[@href="%s"]' % link_url
    ))


@step('I should see a link to "(.*?)" with the url "(.*?)"$')
def should_see_link_text(test, link_text, link_url):
    test.assertTrue(test.browser.find_element_by_xpath(
        u'//a[@href="%s"][./text()="%s"]' % (link_url, link_text)
    ))


@step('I should see a link that contains the text "(.*?)" '
      'and the url "(.*?)"$')
def should_include_link_text(test, link_text, link_url):
    test.assertTrue(test.browser.find_element_by_xpath(
        u'//a[@href="%s"][contains(., "%s")]' % (link_url, link_text)
    ))


# General
@step('The element with id of "(.*?)" contains "(.*?)"$')
def element_contains(test, element_id, value):
    test.assertTrue(test.browser.find_element_by_xpath(
        u'id("{id}")[contains(., "{value}")]'.format(
            id=element_id, value=value,
        )
    ))


@step('The element with id of "(.*?)" does not contain "(.*?)"$')
def element_not_contains(test, element_id, value):
    elem = test.browser.find_elements_by_xpath(
        u'id("{id}")[contains(., "{value}")]'.format(
            id=element_id, value=value,
        )
    )
    test.assertFalse(elem)


@wait_for
def wait_for_visible_elem(browser, xpath):
    elem = browser.find_elements_by_xpath(str(xpath))
    if not elem:
        return False
    return elem[0].is_displayed()


@step(r'I should see an element with id of "(.*?)" within (\d+) seconds?$')
def should_see_id_in_seconds(test, element_id, timeout):
    elem = wait_for_visible_elem(test.browser,
                                 u'id("%s")' % element_id,
                                 timeout=int(timeout),
                                 )
    test.assertTrue(elem)


@step('I should see an element with id of "(.*?)"$')
def should_see_id(test, element_id):
    elem = test.browser.find_element_by_xpath(
        u'id("%s")' % element_id
    )
    test.assertTrue(elem.is_displayed())


@step('I should not see an element with id of "(.*?)"$')
def should_not_see_id(test, element_id):
    try:
        elem = test.browser.find_element_by_xpath(
            u'id("%s")' % element_id
        )
        test.assertFalse(elem.is_displayed())
    except NoSuchElementException:
        pass


@step(r'I should see "([^"]+)" within (\d+) seconds?$')
def should_see_in_seconds(test, text, timeout):
    test.assertTrue(wait_for_content(
        test.browser, text, timeout=int(timeout)
    ))


@step('I should see "([^"]+)"$')
def should_see(test, text):
    test.assertTrue(contains_content(test.browser, text))


@step('I see "([^"]+)"$')
def see(test, text):
    test.assertTrue(contains_content(test.browser, text))


@step('I should not see "([^"]+)"$')
def should_not_see(test, text):
    test.assertFalse(contains_content(test.browser, text))


# Browser
@step('I should be at "(.*?)"$')
@step('The browser\'s URL should be "(.*?)"$')
def browser_url_should_be(test, url):
    test.assertEqual(lookup_url(test, url),
                     test.browser.current_url)


@step('The browser\'s URL should contain "(.*?)"$')
def url_should_contain(test, url):
    test.assertIn(url, test.browser.current_url)


@step('The browser\'s URL should not contain "(.*?)"$')
def url_should_not_contain(test, url):
    test.assertNotIn(url, test.browser.current_url)


# Forms
@step('I should see a form that goes to "(.*?)"$')
def see_form(test, url):
    test.assertTrue(test.browser.find_element_by_xpath(
        u'//form[@action="%s"]' % url
    ))


DATE_FIELDS = (
    'datetime',
    'datetime-local',
    'date',
)


TEXT_FIELDS = (
    'text',
    'textarea',
    'password',
    'month',
    'time',
    'week',
    'number',
    'range',
    'email',
    'url',
    'tel',
    'color',
)


@step('I fill in "(.*?)" with "(.*?)"$')
def fill_in_textfield(test, field_name, value):
    date_field = find_any_field(test.browser,
                                DATE_FIELDS,
                                field_name)
    if date_field:
        field = date_field
    else:
        field = find_any_field(test.browser,
                               TEXT_FIELDS,
                               field_name)

    test.assertTrue(field, 'Can not find a field named "%s"' % field_name)
    if date_field:
        field.send_keys(Keys.DELETE)
    else:
        field.clear()
    field.send_keys(value)


@step('I press "(.*?)"$')
def press_button(test, value):
    button = find_button(test.browser, value)
    button.click()


@step('I click on label "([^"]*)"')
def click_on_label(test, label):
    """
    Click on a label
    """

    elem = test.browser.find_element_by_xpath(
        u'//label[normalize-space(text()) = "%s"]' % label
    )
    elem.click()


@step(r'Element with id "([^"]*)" should be focused')
def element_focused(test, id):
    """
    Check if the element is focused
    """

    elem = test.browser.find_element_by_xpath(
        u'id("{id}")'.format(id=id)
    )
    focused = test.browser.switch_to_active_element()

    test.assertEqual(elem, focused)


@step(r'Element with id "([^"]*)" should not be focused')
def element_not_focused(test, id):
    """
    Check if the element is not focused
    """

    elem = test.browser.find_element_by_xpath(
        u'id("{id}")'.format(id=id)
    )
    focused = test.browser.switch_to_active_element()

    test.assertNotEqual(elem, focused)


@step(r'Input "([^"]*)" (?:has|should have) value "([^"]*)"')
def input_has_value(test, field_name, value):
    """
    Check that the form input element has given value.
    """
    text_field = find_any_field(test.browser,
                                DATE_FIELDS + TEXT_FIELDS,
                                field_name)
    test.assertTrue(text_field,
                    u'Can not find a field named "%s"' % field_name)
    test.assertEqual(text_field.get_attribute('value'), value)


@step(r'I submit the only form')
def submit_the_only_form(test):
    """
    Look for a form on the page and submit it.
    """
    form = test.browser.find_element_by_xpath(str('//form'))
    form.submit()


@step(r'I submit the form with id "([^"]*)"')
def submit_form_id(test, id):
    """
    Submit the form having given id.
    """
    form = test.browser.find_element_by_xpath(
        u'id("{id}")'.format(id=id)
    )
    form.submit()


@step(r'I submit the form with action "([^"]*)"')
def submit_form_action(test, url):
    """
    Submit the form having given action URL.
    """
    form = test.browser.find_element_by_xpath(
        u'//form[@action="%s"]' % url
    )
    form.submit()


# Checkboxes
@step('I check "(.*?)"$')
def check_checkbox(test, value):
    check_box = find_field(test.browser, 'checkbox', value)
    if not check_box.is_selected():
        check_box.click()


@step('I uncheck "(.*?)"$')
def uncheck_checkbox(test, value):
    check_box = find_field(test.browser, 'checkbox', value)
    if check_box.is_selected():
        check_box.click()


@step('The "(.*?)" checkbox should be checked$')
def assert_checked_checkbox(test, value):
    check_box = find_field(test.browser, 'checkbox', value)
    test.assertTrue(check_box.is_selected())


@step('The "(.*?)" checkbox should not be checked$')
def assert_not_checked_checkbox(test, value):
    check_box = find_field(test.browser, 'checkbox', value)
    test.assertFalse(check_box.is_selected())


# Selectors
@step('I select "(.*?)" from "(.*?)"$')
def select_single_item(test, option_name, select_name):
    option_box = find_option(test.browser, select_name, option_name)
    option_box.click()


@step('I select the following from "([^"]*?)":?', multiline=True)
def select_multi_items(test, select_name, option_names):
    # Ensure only the options selected are actually selected
    option_names = [on.strip() for on
                    in option_names.split('\n') if on.strip()]
    select_box = find_field(test.browser, 'select', select_name)

    select = Select(select_box)
    select.deselect_all()

    for option in option_names:
        try:
            select.select_by_value(option)
        except NoSuchElementException:
            select.select_by_visible_text(option)


@step('The "(.*?)" option from "(.*?)" should be selected$')
def assert_single_selected(test, option_name, select_name):
    option_box = find_option(test.browser, select_name, option_name)
    test.assertTrue(option_box.is_selected())


@step('The following options from "([^"]*?)" should be selected:?',
      multiline=True)
def assert_multi_selected(test, select_name, option_names):
    # Ensure its not selected unless its one of our options
    option_names = [on.strip() for on
                    in option_names.split('\n') if on.strip()]
    select_box = find_field(test.browser, 'select', select_name)
    option_elems = select_box.find_elements_by_xpath(str('./option'))
    for option in option_elems:
        if option.get_attribute('id') in option_names or \
           option.get_attribute('name') in option_names or \
           option.get_attribute('value') in option_names or \
           option.text in option_names:
            test.assertTrue(option.is_selected())
        else:
            test.assertFalse(option.is_selected())


@step(r'I should see option "([^"]*)" in selector "([^"]*)"')
def select_contains(test, option, id_):
    test.assertIsNotNone(option_in_select(test.browser, id_, option))


@step(r'I should not see option "([^"]*)" in selector "([^"]*)"')
def select_does_not_contain(test, option, id_):
    test.assertIsNone(option_in_select(test.browser, id_, option))


# Radios
@step('I choose "(.*?)"$')
def choose_radio(test, value):
    box = find_field(test.browser, 'radio', value)
    box.click()


@step('The "(.*?)" option should be chosen$')
def assert_radio_selected(test, value):
    box = find_field(test.browser, 'radio', value)
    test.assertTrue(box.is_selected())


@step('The "(.*?)" option should not be chosen$')
def assert_radio_not_selected(test, value):
    box = find_field(test.browser, 'radio', value)
    test.assertFalse(box.is_selected())


# Alerts
@step('I accept the alert')
def accept_alert(test):
    """
    Accept the alert
    """

    try:
        alert = Alert(test.browser)
        alert.accept()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I dismiss the alert')
def dismiss_alert(test):
    """
    Dismiss the alert
    """

    try:
        alert = Alert(test.browser)
        alert.dismiss()
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step(r'I should see an alert with text "([^"]*)"')
def check_alert(test, text):
    """
    Check the alert text
    """

    try:
        alert = Alert(test.browser)
        test.assertEqual(alert.text, text)
    except WebDriverException:
        # PhantomJS is kinda poor
        pass


@step('I should not see an alert')
def check_no_alert(test):
    """
    Check there is no alert
    """

    try:
        alert = Alert(test.browser)
        raise AssertionError("Should not see an alert. Alert '%s' shown." %
                             alert.text)
    except NoAlertPresentException:
        pass


# Tooltips
@step(r'I should see an element with tooltip "([^"]*)"')
def see_tooltip(test, tooltip):
    """
    Press a button having a given tooltip.
    """
    elem = test.browser.find_elements_by_xpath(
        u'//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)
    )
    elem = [e for e in elem if e.is_displayed()]
    test.assertTrue(elem)


@step(r'I should not see an element with tooltip "([^"]*)"')
def no_see_tooltip(test, tooltip):
    """
    Press a button having a given tooltip.
    """
    elem = test.browser.find_elements_by_xpath(
        u'//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)
    )
    elem = [e for e in elem if e.is_displayed()]
    test.assertFalse(elem)


@step(r'I (?:click|press) the element with tooltip "([^"]*)"')
def press_by_tooltip(test, tooltip):
    """
    Press a button having a given tooltip.
    """
    for button in test.browser.find_elements_by_xpath(
        u'//*[@title="%(tooltip)s" or @data-original-title="%(tooltip)s"]' %
        dict(tooltip=tooltip)
    ):
        try:
            button.click()
            break
        except Exception:
            pass
    else:
        raise AssertionError("No button with tooltip '{0}' found"
                             .format(tooltip))


@step(r'The page title should be "([^"]*)"')
def page_title(test, title):
    """
    Check that the page title matches the given one.
    """

    test.assertEqual(test.browser.title, title)


@step(r'I switch to the frame with id "([^"]*)"')
def switch_to_frame(test, frame):
    elem = test.browser.find_element_by_id(frame)
    test.browser.switch_to_frame(elem)


@step(r'I switch back to the main view')
def switch_to_main(test):
    test.browser.switch_to_default_content()
