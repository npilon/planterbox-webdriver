Feature: I test screenshot ability
    Scenario: Take a screenshot
        When I go to "basic_page"
        Then I capture a screenshot
        Then I capture a screenshot after 1 second
