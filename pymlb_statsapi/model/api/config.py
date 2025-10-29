"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel


class ConfigModel(EndpointModel):
    @configure_api
    def awards(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def baseballStats(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def eventTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def fielderDetailTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def gameStatus(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def gameTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def gamedayTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def groupByTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def hitTrajectories(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def jobTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def languages(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def leagueLeaderTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def logicalEvents(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def metrics(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def pitchCodes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def pitchTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def platforms(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def playerStatusCodes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def positions(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def reviewReasons(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def rosterTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def runnerDetailTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def scheduleEventTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def sitCodes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def sky(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def aggregateSortEnum(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def standingsTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statFields(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statGroups(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statSearchConfig(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statSearchGroupByTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statSearchParams(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def statSearchStats(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def transactionTypes(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def windDirection(self, **kwargs):
        return self.get_api_file_object(**kwargs)
