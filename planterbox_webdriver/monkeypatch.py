def fixed__ne__(self, other):
    return not self.__eq__(other)

def fix_inequality():
    from selenium.webdriver.remote.webelement import WebElement

    if '__ne__' not in dir(WebElement):
        WebElement.__ne__ = fixed__ne__
