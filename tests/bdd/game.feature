@schema:Game
Feature: Game Endpoint
  Test the Game endpoint with completed games from October 2024
  Using World Series games for consistent, complete data

  Background:
    Given I use the game endpoint

  Scenario Outline: Get game data for completed World Series games
    Given I call the <method> method
    And I use path parameters: {"game_pk": "<game_pk>"}
    And I use no query parameters
    When I make the API call
    Then the response should be successful
    And the response should not be empty

    @method:boxscore
    Examples: World Series 2024 Games
      | method      | game_pk |
      | boxscore    | 747175  |

    @method:liveGameV1
    Examples: World Series 2024 Games
      | method      | game_pk |
      | liveGameV1  | 747175  |

    @method:playByPlay
    Examples: World Series 2024 Games
      | method      | game_pk |
      | playByPlay  | 747175  |

    @method:linescore
    Examples: World Series 2024 Games
      | method      | game_pk |
      | linescore   | 747175  |

    @method:content
    Examples: World Series 2024 Games
      | method      | game_pk |
      | content     | 747175  |

  @method:liveGameV1
  Scenario: Get game with timecode
    Given I call the liveGameV1 method
    And I use path parameters: {"game_pk": "747175"}
    And I use query parameters: {"timecode": "20241027_000000"}
    When I make the API call
    Then the response should be successful

  @method:getGameContextMetrics
  Scenario: Get game contextMetrics
    Given I call the getGameContextMetrics method
    And I use path parameters: {"gamePk": "747175"}
    And I use query parameters: {"timecode": "20241027_120000"}
    When I make the API call
    Then the response should be successful

  @method:getWinProbability
  Scenario: Get game winProbability
    Given I call the getWinProbability method
    And I use path parameters: {"gamePk": "747175"}
    And I use query parameters: {"timecode": "20241027_120000"}
    When I make the API call
    Then the response should be successful
