@schema:Team
Feature: Team Endpoint
  Test the Team endpoint for retrieving team information

  Background:
    Given I use the team endpoint

  @method:teams
  Scenario: Get all teams
    Given I call the teams method
    And I use no path parameters
    And I use query parameters: {"sportId": "1", "season": "2024"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field teams
    And the teams should have at least 30 items

  @method:teams
  Scenario Outline: Get specific team information
    Given I call the teams method
    And I use no path parameters
    And I use query parameters: {"teamId": "<team_id>"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field teams

    Examples: MLB Teams
      | team_id |
      | 147     |
      | 121     |
      | 111     |
      | 112     |
      | 117     |

  @method:roster
  Scenario: Get team roster
    Given I call the roster method
    And I use path parameters: {"teamId": "147", "rosterType": "active"}
    And I use query parameters: {"season": "2024"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field roster

  @method:coaches
  Scenario: Get team coaches
    Given I call the coaches method
    And I use path parameters: {"teamId": "147"}
    And I use query parameters: {"season": "2024"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field roster

  @method:stats
  Scenario: Get team stats
    Given I call the stats method
    And I use no path parameters
    And I use query parameters: {"sportId": "1", "season": "2024", "stats": "season", "group": "hitting"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field stats

  @method:alumni
  Scenario: Get team alumni
    Given I call the alumni method
    And I use path parameters: {"teamId": "147"}
    And I use query parameters: {"season": "2024"}
    When I make the API call
    Then the response should be successful
