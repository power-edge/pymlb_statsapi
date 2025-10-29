"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel


class AwardsModel(EndpointModel):
    @configure_api
    def awards(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def awardRecipients(self, **kwargs):
        return self.get_api_file_object(**kwargs)
