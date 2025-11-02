@schema:Person
Feature: Person (Player) Endpoint
  Test the Person endpoint for retrieving player information

  Background:
    Given I use the person endpoint

  @method:person
  Scenario Outline: Get player information
    Given I call the person method
    And I use no path parameters
    And I use query parameters: {"personIds": "<person_id>"}
    When I make the API call
    Then the response should be successful
    And the response should contain the field people
    And each item in people should have fullName

    Examples: Star Players
      | person_id |
      | 660271    |
      | 592450    |
      | 545361    |
      | 608070    |
      | 665487    |

  # NOTE: This test is commented out because the MLB API returns 500 Internal Server Error
  # for this endpoint. This appears to be a server-side issue with the MLB API.
  # @method:award
  # Scenario: Get player awards
  #   Given I call the award method
  #   And I use path parameters: {"personId": "660271"}
  #   And I use no query parameters
  #   When I make the API call
  #   Then the response should be successful
  #   And the response should contain the field people

  @method:freeAgents
  Scenario: Get free agents
    Given I call the freeAgents method
    And I use no path parameters
    And I use query parameters: {"season": "2024"}
    When I make the API call
    Then the response should be successful
