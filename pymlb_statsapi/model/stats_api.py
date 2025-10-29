# from .api_docs import ApiDocsModel
from .api import (
    AwardsModel,
    BroadcastModel,
    ConferenceModel,
    ConfigModel,
    DivisionModel,
    DraftModel,
    GameModel,
    GamepaceModel,
    HighLowModel,
    HomeRunDerbyModel,
    JobModel,
    LeagueModel,
    MilestonesModel,
    PersonModel,
    ScheduleModel,
    SeasonModel,
    SportsModel,
    StandingsModel,
    StatsModel,
    StreaksModel,
    TeamModel,
)


class StatsAPIModelRegistry:
    # ApiDocs = ApiDocsModel.from_doc()  # from_doc not working for api_docs json
    # ApiDocs = ApiDocsModel.from_json(json.dumps(sl.load_api_docs()))

    # rest are under the stats-api directory
    Awards = AwardsModel.from_doc("awards")
    Broadcast = BroadcastModel.from_doc("broadcast")
    Conference = ConferenceModel.from_doc("conference")
    Config = ConfigModel.from_doc("config")
    Division = DivisionModel.from_doc("division")
    Draft = DraftModel.from_doc("draft")
    Game = GameModel.from_doc("game")
    Gamepace = GamepaceModel.from_doc("gamepace")
    HighLow = HighLowModel.from_doc("highlow")
    HomeRunDerby = HomeRunDerbyModel.from_doc("homerunderby")
    Job = JobModel.from_doc("job")
    League = LeagueModel.from_doc("league")
    Milestones = MilestonesModel.from_doc("milestones")
    Person = PersonModel.from_doc("person")
    Schedule = ScheduleModel.from_doc("schedule")
    Season = SeasonModel.from_doc("season")
    Sports = SportsModel.from_doc("sports")
    Standings = StandingsModel.from_doc("standings")
    Stats = StatsModel.from_doc("stats")
    Streaks = StreaksModel.from_doc("streaks")
    Team = TeamModel.from_doc("team")


StatsAPI = StatsAPIModelRegistry()
