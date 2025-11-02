@schema:Schedule
Feature: Schedule Endpoint
  Test the Schedule endpoint with various query parameters
  Using dates from October 2024 (season is over, data won't change)

  Background:
    Given I use the schedule endpoint

  @method:schedule
  Scenario Outline: Get schedule for specific dates
    Given I call the schedule method
    And I use no path parameters
    And I use query parameters: <query_params>
    When I make the API call
    Then the response should be successful
    And the response should contain the field dates
    And the resource path should match the pattern schedule/schedule

    Examples:
      | query_params                                    |
      | {"sportId": "1", "date": "2024-10-27"}          |
      | {"sportId": "1", "date": "2024-10-26"}          |
      | {"sportId": "1", "date": "2024-10-25"}          |
      | {"sportId": "1", "startDate": "2024-10-20", "endDate": "2024-10-22"} |

  @method:schedule
  Scenario: Get schedule for specific team
    Given I call the schedule method
    And I use no path parameters
    And I use query parameters: {"sportId": "1", "teamId": "147", "date": "2024-10-27"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field dates

  @method:schedule
  Scenario: Get postseason schedule
    Given I call the schedule method
    And I use no path parameters
    And I use query parameters: {"sportId": "1", "date": "2024-10-27", "gameType": "P"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field dates

  @method:tieGames
  Scenario: Get tied games
    Given I call the tieGames method
    And I use no path parameters
    And I use query parameters: {"sportId": "1", "season": "2024"}
    When I make the API call
    Then the response should be successful

  @method:postseasonScheduleSeries
  Scenario: Get postseason series schedule
    Given I call the postseasonScheduleSeries method
    And I use no path parameters
    And I use query parameters: {"sportId": "1", "season": "2024"}
    When I make the API call
    Then the response should be successful
