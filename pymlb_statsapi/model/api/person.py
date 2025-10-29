"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel


class PersonModel(EndpointModel):
    date_formats = {"updatedSince": "%Y-%m-%dT%H:%M:%SZ"}

    @configure_api
    def award(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def changes(self, **kwargs):
        """badly misnamed in the api_docs^ +this duplicates the api.description or api.operations[].nickname space"""
        return self.get_api_file_object(**kwargs)

    @configure_api
    def currentGameStats(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def freeAgents(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def gameStats(self, **kwargs):
        """also duplicates the api.description or api.operations[].nickname space"""
        return self.get_api_file_object(**kwargs)

    @configure_api
    def person(self, **kwargs):
        return self.get_api_file_object(**kwargs)
