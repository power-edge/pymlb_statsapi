Feature: StatsAPI
  As a user of the StatsAPI
  I want to retrieve StatsAPI Objects for various endpoints
  So that I can ingest the mlb stats api data

  Scenario Outline: Retrieve endpoint objects
    Given the StatsAPI endpoint <endpoint_name>
    And the api <api_name>
    And the query parameters <query_params>
    Then I can create an endpoint object
    And I can get the endpoint object data

    Examples:
      | endpoint_name | api_name   | query_params |
      | Schedule      | schedule | {"sportId": 1} |

#  Scenario: Retrieve endpoint objects with invalid endpoint
