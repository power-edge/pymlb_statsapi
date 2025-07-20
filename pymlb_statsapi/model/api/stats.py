"""
created by nikos at 4/26/21
"""
from ..base import EndpointModel
from pymlb_statsapi.utils.stats_api_object import configure_api


class StatsModel(EndpointModel):

    @configure_api
    def groupedStats(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def leaders(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def stats(self, **kwargs):
        return self.get_api_file_object(**kwargs)
