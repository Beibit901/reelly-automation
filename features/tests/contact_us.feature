Feature: Reelly Contact us page

  Scenario: User can open the Contact us page
    Given Open Reelly main page
    And Log in to Reelly
    When Click on settings option
    And Click on Contact us option
    Then Verify Contact us page opens
    And Verify at least 4 social media icons are shown
    And Verify Connect the company button is available and clickable
