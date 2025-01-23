"""Metadata for CLI tool."""

__app_name__ = "mgr"


from leaguemanager.__metadata__ import __version__
from leaguemanager.domain import Scheduler, StandingsTable, TabulateFixture

# from .domain.scheduling import _generator

__all__ = ["__app_name__", "__version__", "Scheduler", "StandingsTable", "TabulateFixture"]
