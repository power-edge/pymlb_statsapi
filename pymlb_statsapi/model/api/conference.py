"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel


class ConferenceModel(EndpointModel):
    @configure_api
    def conferences(self, **kwargs):
        return self.get_api_file_object(**kwargs)
