"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel


class HomeRunDerbyModel(EndpointModel):
    @configure_api
    def homeRunDerby(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def homeRunDerbyBracket(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def homeRunDerbyPool(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def homeRunDerbyGameBracket(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def homeRunDerbyGamePool(self, **kwargs):
        return self.get_api_file_object(**kwargs)
