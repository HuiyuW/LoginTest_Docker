Feature: Login to the TaaS Serviceportal

  Scenario: Successful login to the TaaS Serviceportal
    Given I open the login page
    When I enter username "vw2xn87" and password "xOqMiHJegL3JvnOCK9rb0vOG1pZ7Oc1C7fAfRR0WEuk4keuwEc0yAUF3QSahP8G3IBKw2FO2zvcr7njD"
    And I click the login button
    Then I should see the terms and conditions popup
    When I accept the terms and conditions
    Then I should be logged in and see my profile avatar and ID

  Scenario: Login with incorrect password
    Given I open the login page
    When I enter username "vw2xn87" and password "1234"
    And I click the login button
    When I accept the terms and conditions
    Then I should be on the login page

  Scenario: Logout after successful login
    Given I open the login page
    When I enter username "vw2xn87" and password "xOqMiHJegL3JvnOCK9rb0vOG1pZ7Oc1C7fAfRR0WEuk4keuwEc0yAUF3QSahP8G3IBKw2FO2zvcr7njD"
    And I click the login button
    Then I should see the terms and conditions popup
    When I accept the terms and conditions
    Then I should be logged in and see my profile avatar and ID
    When I click the profile avatar
    And I click the logout button
    Then I should be on the login page