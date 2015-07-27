"""Steps and utility functions for taking screenshots."""

from collections import defaultdict
import time
import uuid

from planterbox import (
    hook,
    step,
)
import os.path
import json


def resolution_path(test):
    window_size = test.browser.get_window_size()
    return os.path.join(
        test.screenshot_root,
        '{}x{}'.format(window_size['width'], window_size['height']),
    )


@step(r'I capture a screenshot$')
def capture_screenshot(test):
    shot_name = '{}.png'.format(uuid.uuid4())

    if getattr(test, 'screenshot_path', None) is None:
        test.screenshot_path = resolution_path(test)

    if not os.path.isdir(test.screenshot_path):
        os.makedirs(test.screenshot_path)
    filename = os.path.join(
        test.screenshot_path,
        shot_name,
    )
    test.browser.get_screenshot_as_file(filename)
    test.screenshot_report[test.scenario_name].append(shot_name)


@step(r'I capture a screenshot after (\d+) seconds?$')
def capture_screenshot_delay(test, delay):
    time.sleep(int(delay))
    capture_screenshot(test)


@hook('before', 'feature')
def set_save_directory(test):
    """
        Sets the root save directory for saving screenshots.
    """

    root = os.path.join(
        test.config['screenshot.dir'][0],
        test.config['start_date'][0],
        test.config['screenshot.source'][0],
    )

    if not os.path.isdir(root):
        os.makedirs(root)

    test.screenshot_root = root
    test.screenshot_report = defaultdict(list)


@hook('after', 'feature')
def record_run_feature_report(test):
    if getattr(test, 'screenshot_report', None):
        feature_name_json = '{}.json'.format(
            os.path.splitext(os.path.basename(test.feature_path))[0]
        )
        feature_json_path = os.path.join(test.screenshot_path,
                                         feature_name_json,
                                         )
        with open(feature_json_path, 'w') as f:
            json.dump(test.screenshot_report, f)

        del test.screenshot_report
        del test.screenshot_path
        del test.screenshot_root
