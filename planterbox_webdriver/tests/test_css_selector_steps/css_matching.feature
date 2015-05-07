Feature: Wait and match CSS
    Scenario: Everything fires up
        When I go to test page "basic_page"
        Then There should be an element matching $("textarea[name='bio']") within 1 second
