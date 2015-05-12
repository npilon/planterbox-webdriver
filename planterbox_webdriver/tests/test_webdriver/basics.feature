Feature: I should see, I should not see
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

    Scenario: Page title
        When I go to "basic_page"
        Then the page title should be "A Basic Page"
        
    Scenario: I fill in a form
        Given I go to "basic_page"
        And I fill in "bio" with "everything awesome"
        And I fill in "pass" with "neat"
        When I press "Submit!"
        Then The browser's URL should contain "bio=everything"

