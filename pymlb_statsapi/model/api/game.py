"""
created by nikos at 4/26/21
"""

from pymlb_statsapi.utils.stats_api_object import configure_api

from ..base import EndpointModel

YMDTHMS = "%Y-%m-%dT%H:%M:%SZ"
YYYYMMDD_HHMMSS = "%Y%m%d_%H%M%S"
MMDDYYYY_HHMMSS = "%m%d%Y_%H%M%S"


class GameModel(EndpointModel):
    date_formats = {
        "updatedSince": YMDTHMS,
        "timecode": YYYYMMDD_HHMMSS,
        "startTimecode": MMDDYYYY_HHMMSS,
        "endTimecode": MMDDYYYY_HHMMSS,
    }

    @configure_api
    def liveGameV1(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def liveGameDiffPatchV1(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def liveTimestampv11(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def currentGameStats(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def getGameContextMetrics(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def getWinProbability(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def boxscore(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def content(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def colorFeed(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def colorTimestamps(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def linescore(self, **kwargs):
        return self.get_api_file_object(**kwargs)

    @configure_api
    def playByPlay(self, **kwargs):
        return self.get_api_file_object(**kwargs)
