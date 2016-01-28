Feature: I exercise basic functionality of webdriver
    Scenario: Assert page title
        When I go to "basic_page"
        Then the page title should be "A Basic Page"

    Scenario: Links and text I don't see
        When I visit "basic_page"
        Then I should see "Hello there!"
        And I should see a link to "Google" with the url "http://google.com/"
        And I should see a link with the url "http://google.com/"
        And I should not see "Bogeyman"

    Scenario: Links containing text
        When I go to "basic_page"
        Then  I should see a link to "Google" with the url "http://google.com/"
        And I see "Hello there!"

    Scenario: Links containing partial text
        When I go to "basic_page"
        Then The browser's URL should contain "file://"
        And I should see a link that contains the text "Goo" and the url "http://google.com/"

    Scenario: Follow links
        Given I go to "link_page"
        And I see "Page o link"
        When I click "Next Page"
        Then I should be at "link_dest"
        And The browser's URL should be "link_dest"
        And The browser's URL should not contain "http://"

    Scenario: Hidden text
        When I go to "basic_page"
        Then I should see an element with id of "bio_field"
        And I should see an element with id of "somediv" within 2 seconds
        And I should not see an element with id of "hidden_text"

    Scenario: Hidden text 2
        When I go to "basic_page"
        Then I should see "Hello there" within 1 second
        And I should not see an element with id of "hidden_text"

    Scenario: tooltips
        When I go to "tooltips"
        Then I should see an element with tooltip "A tooltip"
        And I should not see an element with tooltip "Does not exist"
        And I should not see an element with tooltip "Hidden"
        When I click the element with tooltip "A tooltip"
        Then the browser's URL should contain "#anchor"

    Scenario: Test labels
        When I go to "basic_page"
        And I click on label "Password:"
        Then element with id "pass" should be focused
        And element with id "bio_field" should not be focused


# Forms stuff
    Scenario: Fill in a form
        Given I go to "basic_page"
        And I fill in "bio" with "everything awesome"
        And I fill in "pass" with "neat"
        When I press "Submit!"
        Then The browser's URL should contain "bio=everything"

    Scenario: Submit only form
        When I go to "basic_page"
        And I submit the form with id "the-form"
        Then the browser's URL should contain "bio="
        And the browser's URL should contain "user="

    Scenario: Test input values
        When I go to "basic_page"
        And I fill in "username" with "Danni"
        Then input "username" has value "Danni"

    Scenario: Test date input
        When I go to "basic_page"
        And I fill in "dob" with "1900/01/01"
        Then input "dob" has value "1900/01/01"

    Scenario: Checkboxes checked
        Given I go to "basic_page"
        When I check "I have a bike"
        Then The "I have a bike" checkbox should be checked
        And The "I have a car" checkbox should not be checked

    Scenario: Checkboxes unchecked
        Given I go to "basic_page"
        And I check "I have a bike"
        And The "I have a bike" checkbox should be checked
        When I uncheck "I have a bike"
        Then The "I have a bike" checkbox should not be checked

    Scenario: Combo boxes
        Given I go to "basic_page"
        Then I should see option "Mercedes" in selector "car_choice"
        And I should see option "Volvo" in selector "car_choice"
        And I should not see option "Skoda" in selector "car_choice"
        When I select "Mercedes" from "car_choice"
        Then The "Mercedes" option from "car_choice" should be selected

    Scenario: Multi-combo-boxes
        Given I go to "basic_page"
        When I select the following from "Favorite Colors:":
            """
            Blue
            Green
            """
        Then The following options from "Favorite Colors:" should be selected:
            """
            Blue
            Green
            """

    Scenario: Radio buttons
        When I go to "basic_page"
        And I choose "Male"
        Then The "Male" option should be chosen
        And The "Female" option should not be chosen

    Scenario: Accept alert
        When I go to "alert_page"
        Then I should see an alert with text "This is an alerting alert"
        When I accept the alert
        Then I should not see an alert
        And I should see "true"

    Scenario: Dismiss alert
        When I go to "alert_page"
        Then I should see an alert with text "This is an alerting alert"
        When I dismiss the alert
        Then I should not see an alert
        And I should see "false"
