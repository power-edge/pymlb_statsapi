@schema:Sports @schema:League @schema:Division
Feature: League, Division, and Sport Endpoints
  Test reference data endpoints

  # NOTE: The following tests are commented out because the schemas are incomplete.
  # The sports.json, league.json, and division.json schemas only contain specific
  # methods (sportPlayers, allStarFinalVote, etc.) but not the general list endpoints.
  # These need to be added to the schemas before these tests can work.

  # Scenario: Get all sports
  #   Given I use the sports endpoint
  #   And I call the sports method
  #   And I use no path parameters
  #   And I use no query parameters
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field sports

  # Scenario: Get specific sport
  #   Given I use the sports endpoint
  #   And I call the sports method
  #   And I use path parameters: {"sportId": "1"}
  #   And I use no query parameters
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field sports

  # Scenario: Get all leagues
  #   Given I use the league endpoint
  #   And I call the league method
  #   And I use no path parameters
  #   And I use query parameters: {"sportId": "1"}
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field leagues

  # Scenario: Get specific league
  #   Given I use the league endpoint
  #   And I call the league method
  #   And I use path parameters: {"leagueId": "103"}
  #   And I use no query parameters
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field leagues

  # Scenario: Get all divisions
  #   Given I use the division endpoint
  #   And I call the divisions method
  #   And I use no path parameters
  #   And I use query parameters: {"sportId": "1"}
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field divisions

  # Scenario: Get specific division
  #   Given I use the division endpoint
  #   And I call the divisions method
  #   And I use path parameters: {"divisionId": "200"}
  #   And I use no query parameters
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field divisions
