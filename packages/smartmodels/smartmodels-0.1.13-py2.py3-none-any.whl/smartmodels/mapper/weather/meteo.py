from agptools.helpers import (
    I,
    DATE,
    FLOAT,
    SAFE_STR,
)

from syncmodels.mapper import Mapper

from ...model.weather.meteo import MeteorologicalStation, MeteorologicalStationStats, MeteorologicalWarning, MeteorologicalWarning

class MeteorologicalStationStatsMapper(Mapper):
    """Identyty, no mapping needed"""
    PYDANTIC = MeteorologicalStationStats





