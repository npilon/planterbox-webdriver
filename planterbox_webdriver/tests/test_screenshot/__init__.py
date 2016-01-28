from glob import glob
from json import load
import os.path
from shutil import rmtree
from tempfile import mkdtemp

from ..html_pages import PAGES
from planterbox import (
    hook,
)
from planterbox_webdriver.webdriver import (
    visit,
)
from planterbox_webdriver.screenshot import (
    capture_screenshot,
    capture_screenshot_delay,
)
from ..test_webdriver import (
    create_webdriver,
    quit_webdriver,
    reset_browser,
)


@hook('before', 'feature')
def test_set_save_directory(test):
    from planterbox_webdriver.screenshot import set_save_directory
    test_temp = mkdtemp()
    test.config._mvd['screenshot.source'] = 'tests'
    test.config._mvd['screenshot.dir'] = [test_temp]
    set_save_directory(test)


@hook('after', 'feature')
def test_record_run_feature_report(test):
    from planterbox_webdriver.screenshot import record_run_feature_report
    screenshot_path = test.screenshot_path
    screenshot_report = test.screenshot_report
    record_run_feature_report(test)
    test.assertTrue(os.path.isdir(screenshot_path))
    feature_name_json = '{}.json'.format(
        os.path.splitext(os.path.basename(test.feature_path))[0]
    )
    feature_json_path = os.path.join(screenshot_path,
                                     feature_name_json,
                                     )
    pngs = glob(os.path.join(screenshot_path,
                             '*.png',
                             ))
    test.assertGreater(len(pngs), 0)
    with open(feature_json_path, 'r') as f:
        test.assertEqual(load(f), screenshot_report)
    rmtree(test.config['screenshot.dir'][0])
