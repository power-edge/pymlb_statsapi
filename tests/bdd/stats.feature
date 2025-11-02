@schema:Stats
Feature: Stats Endpoint
  Test the Stats endpoint for retrieving statistical data

  Background:
    Given I use the stats endpoint

  # NOTE: The following player stats scenarios are commented out because the
  # person.json schema is missing the /v1/people/{personId}/stats endpoint.
  # The schema only includes game-specific stats endpoints, not season/career stats.
  # These tests should be re-enabled once the schema is updated to include:
  # - /v1/people/{personId}/stats endpoint with season/career stats support

  # Scenario: Get player season stats
  #   Given I call the playerStats method
  #   And I use path parameters: {"personId": "660271"}
  #   And I use query parameters: {"stats": "season", "season": "2024", "group": "hitting"}
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field stats

  # Scenario: Get player career stats
  #   Given I call the playerStats method
  #   And I use path parameters: {"personId": "660271"}
  #   And I use query parameters: {"stats": "career", "group": "hitting"}
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field stats

  # Scenario Outline: Get stats for different groups
  #   Given I call the playerStats method
  #   And I use path parameters: {"personId": "<person_id>"}
  #   And I use query parameters: {"stats": "season", "season": "2024", "group": "<group>"}
  #   When I make the API call
  #   Then the response should be successful

  #   Examples:
  #     | person_id | group    |
  #     | 660271    | hitting  |
  #     | 665487    | pitching |
  #     | 592450    | fielding |
