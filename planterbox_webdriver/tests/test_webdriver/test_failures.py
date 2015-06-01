from importlib import import_module
from unittest import TestCase

from mock import Mock

from ..html_pages import PAGES
from planterbox import (
    FeatureTestCase,
    hook,
)
from planterbox_webdriver.webdriver import *


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


class TestFailures(TestCase):
    def tearDown(self):
        if hasattr(self, 'failure'):
            del self.failure

    def test_labels_fail(self):
        feature_text = """Feature: I expect a step to fail.
            Scenario: Test labels fail
                When I go to "basic_page"
                And I click on label "Favorite Colors:"
                Then element with id "fav_colors" should not be focused"""

        def captureFailure(*args):
            self.failure = args

        feature_test = FeatureTestCase(
            world=import_module(self.__module__),
            feature_path=__file__,
            feature_text=feature_text,
        )
        feature_test.run(result=Mock(
            addFailure=Mock(side_effect=captureFailure),
            addError=Mock(side_effect=Exception),
            addSuccess=Mock(side_effect=Exception),
        ))
        feature_exc_info = self.failure[1]
        failstep = 'Then element with id "fav_colors" should not be focused'
        self.assertEqual(feature_exc_info.failed_step.strip(), failstep)
        failname = 'Scenario: Test labels fail'
        self.assertEqual(feature_exc_info.scenario_name.strip(), failname)
        expected_completed = [
            'When I go to "basic_page"',
            'And I click on label "Favorite Colors:"'
        ]
        completed_steps = [s.strip() for s in feature_exc_info.completed_steps]
        self.assertEqual(completed_steps, expected_completed)

    def test_combos_fail(self):
        feature_text = """Feature: I expect a step to fail.
           Scenario: Combo boxes fail
              Given I go to "basic_page"
              Then I should not see option "Mercedes" in selector "car_choice"
        """

        def captureFailure(*args):
            self.failure = args

        feature_test = FeatureTestCase(
            world=import_module(self.__module__),
            feature_path=__file__,
            feature_text=feature_text,
        )
        feature_test.run(result=Mock(
            addFailure=Mock(side_effect=captureFailure),
            addError=Mock(side_effect=Exception),
            addSuccess=Mock(side_effect=Exception),
        ))
        feature_exc_info = self.failure[1]
        failstep = ('Then I should not see option "Mercedes" '
                    'in selector "car_choice"')
        self.assertEqual(feature_exc_info.failed_step.strip(), failstep)
        failname = 'Scenario: Combo boxes fail'
        self.assertEqual(feature_exc_info.scenario_name.strip(), failname)
        expected_completed = [
            'Given I go to "basic_page"',
        ]
        completed_steps = [s.strip() for s in feature_exc_info.completed_steps]
        self.assertEqual(completed_steps, expected_completed)