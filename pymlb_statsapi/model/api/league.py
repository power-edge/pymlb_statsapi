"""
created by nikos at 4/26/21
"""
from ..base import EndpointModel
from pymlb_statsapi.utils.stats_api_object import configure_api


class LeagueModel(EndpointModel):

    @configure_api
    def allStarFinalVote(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def allStarWriteIns(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def allStarsFinalVote(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def allStarsWriteIns(self, **kwargs):
        return self.get_api_file_object(**kwargs)
