from __future__ import annotations

from fastapi import FastAPI

from tabbit.database.session import SessionManager
from tabbit.database.session import session_manager
from tabbit.routers.root import root_router


def setup_app(session_manager: SessionManager) -> FastAPI:
    """Configure and initialize the ASGI application.

    Args:
        session_manager: Database session manager instance for handling
           database connections throughout the application lifecycle.

    Returns:
        An ASGI application.
    """
    app = FastAPI(title="Tabbit")
    app.include_router(root_router)
    app.state.session_manager = session_manager
    return app


app = setup_app(session_manager=session_manager)
