Feature: I should see, I should not see
    Scenario: Everything fires up
        When I visit "basic_page"
        Then I should see "Hello there!"
        And I should see a link to "Google" with the url "http://google.com/"
        And I should see a link with the url "http://google.com/"
        And I should not see "Bogeyman"

