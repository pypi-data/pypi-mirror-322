from __future__ import annotations

import enum


class ServerHealth(enum.StrEnum):
    READY = "ready"
    ERROR = "error"
    STARTING = "starting"
