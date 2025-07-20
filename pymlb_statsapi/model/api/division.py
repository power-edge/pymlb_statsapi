"""
created by nikos at 4/26/21
"""
from ..base import EndpointModel
from pymlb_statsapi.utils.stats_api_object import configure_api


class DivisionModel(EndpointModel):

    @configure_api
    def divisions(self, **kwargs):
        return self.get_api_file_object(**kwargs)
