Feature: CSS-based formstuff
    Scenario: Everything fires up
        When I go to test page "basic_page"
        Then I fill in $("input[name='user']") with "A test string"
        And I check $("input[value='Bike']")
