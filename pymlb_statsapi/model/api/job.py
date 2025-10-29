"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel


class JobModel(EndpointModel):
    @configure_api
    def getJobsByType(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def datacasters(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def officialScorers(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def umpires(self, **kwargs):
        return self.get_api_file_object(**kwargs)
