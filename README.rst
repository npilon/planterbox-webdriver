planterbox-webdriver
====================

.. image:: https://api.travis-ci.org/npilon/planterbox-webdriver.png?branch=master
        :target: https://travis-ci.org/npilon/planterbox-webdriver

A suite of steps for
`planterbox <https://github.com/npilon/planterbox>`__ for web testing
with Selenium

Usage
-----

1. Install ``planterbox`` and ``planterbox-webdriver``: ``pip install planterbox planterbox-webdriver``
2. Add a ``unittest.cfg`` to your project that enables ``planterbox``:

::

    [unittest]
    plugins = planterbox

    [planterbox]
    always-on = True

3. Create a package containing your tests; its ``__init__.py`` defines the steps you will have available in your ``.feature`` files.
This package must be detected by ``nose2`` as containing tests; see `nose2's docs for details <http://nose2.readthedocs.io/en/latest/usage.html>`_.

4. Add a "before" hook that sets up a webdriver for your tests:
   
::
 
    @hook('before', 'feature')
    def create_webdriver(test):
        from selenium import webdriver
        test.browser = webdriver.Firefox()
        
5. ``from planterbox_webdriver.webdriver import *`` if you want steps that let you find elements in your tests with XPath
6. ``from planterbox_webdriver.css_selector_steps import *`` for steps that let you find elements in your tests with jQuery-style CSS selectors
7. Add a ``.feature`` file in this package containing tests specified using `Gherkin <https://github.com/cucumber/cucumber/wiki/Gherkin>`_. ``planterbox`` will turn these into appropriate test case objects and give them to nose to run.
8. Run your tests: ``nose2``
