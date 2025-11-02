@schema:Season
Feature: Season Endpoint
  Test the Season endpoint for retrieving season information
  Demonstrates method overloading (base vs seasonId variants)

  Background:
    Given I use the season endpoint

  @method:seasons
  Scenario: Get all seasons (overloaded method - base variant)
    Given I call the seasons method
    And I use no path parameters
    And I use query parameters: {"sportId": "1"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field seasons
    And the seasons should have at least 1 items

  @method:seasons
  Scenario: Get specific season (overloaded method - seasonId variant)
    Given I call the seasons method
    And I use path parameters: {"seasonId": "2024"}
    And I use query parameters: {"sportId": "1"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field seasons

  @method:seasons
  Scenario Outline: Get multiple specific seasons
    Given I call the seasons method
    And I use path parameters: {"seasonId": "<season_id>"}
    And I use query parameters: {"sportId": "1"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field seasons

    Examples:
      | season_id |
      | 2024      |
      | 2023      |
      | 2022      |
      | 2021      |

  @method:allSeasons
  Scenario: Get all seasons list
    Given I call the allSeasons method
    And I use no path parameters
    And I use query parameters: {"sportId": "1"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field seasons
