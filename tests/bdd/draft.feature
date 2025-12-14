@schema:Draft
Feature: Draft Endpoint
  Test the Draft endpoint with historical draft data
  Using completed drafts for consistent, stable data

  Background:
    Given I use the draft endpoint

  @method:draftPicks
  Scenario Outline: Get draft picks for a specific year
    Given I call the draftPicks method
    And I use path parameters: {"year": "<year>"}
    And I use query parameters: {"limit": "5"}
    When I make the API call
    Then the response should be successful
    And the response should not be empty
    And the response should contain the field drafts

    Examples: Historical Draft Years
      | year |
      | 2020 |
      | 2024 |

  @method:draftProspects
  Scenario Outline: Get draft prospects for a specific year
    Given I call the draftProspects method
    And I use path parameters: {"year": "<year>"}
    And I use query parameters: {"limit": "5"}
    When I make the API call
    Then the response should be successful
    And the response should not be empty
    And the response should contain the field prospects

    Examples: Historical Draft Years
      | year |
      | 2020 |
      | 2024 |

  @method:latestDraftPicks
  Scenario: Get latest draft picks for a specific year
    Given I call the latestDraftPicks method
    And I use path parameters: {"year": "2024"}
    And I use no query parameters
    When I make the API call
    Then the response should be successful
