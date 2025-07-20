"""
created by nikos at 4/26/21
"""
from ..base import EndpointModel
from pymlb_statsapi.utils.stats_api_object import configure_api


class SeasonModel(EndpointModel):

    @configure_api
    def allSeasons(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def season(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def seasons(self, **kwargs):
        return self.get_api_file_object(**kwargs)
