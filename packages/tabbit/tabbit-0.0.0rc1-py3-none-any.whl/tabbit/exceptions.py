from __future__ import annotations


class TabbitError(Exception):
    pass


class TabbitDatabaseError(TabbitError):
    pass


class TabbitLoggerError(TabbitError):
    pass
