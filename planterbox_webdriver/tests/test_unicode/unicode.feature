Feature: Unicode Planterbox Webdriver tests
    send_keys with unicode works as expected
    find_element_by_jquery with unicode in it works as expected
    wait_for_elem with unicode in it works as expected
    
   
    Scenario: send_keys with unicode works as expected
        When I visit "unicode_page"
        Then I fill in $("input[name='unicode_input']") with "Iñtërnâtiônàlizætiøn"


    Scenario: find_element_by_jquery with unicode in it works as expected
        When I visit "unicode_page"
        Then There should be an element matching $("span.test_string:contains('Iñtërnâtiônàlizæ')")
        
        
    Scenario: wait_for_elem with unicode in it works as expected
        When I visit "unicode_page"
        Then There should be an element matching $("span.test_string:contains('Iñtërnâtiônàlizæ')") within 2 seconds

