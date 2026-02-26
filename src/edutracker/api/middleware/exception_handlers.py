from fastapi import Request
from fastapi.responses import JSONResponse
import logging

from edutracker.application.common.exceptions import (
    InvalidGoogleTokenError,
    InvalidRefreshTokenError,
    InactiveUserError,
    CorporateEmailRequiredError,
    InvalidAccessTokenError,
    AccessTokenExpiredError,
    InvalidTokenPayloadError,
    UserNotFoundError,
    ForbiddenError,
)

logger = logging.getLogger("http")


def register_exception_handlers(app):

    @app.exception_handler(InvalidGoogleTokenError)
    async def invalid_google_handler(request: Request, exc: InvalidGoogleTokenError):
        return JSONResponse(
            status_code=401,
            content={"error": "invalid_google_token"}
        )
    
    @app.exception_handler(InvalidRefreshTokenError)
    async def invalid_google_handler(request: Request, exc: InvalidRefreshTokenError):
        return JSONResponse(
            status_code=401,
            content={"error": "invalid_refresh_token"}
        )
    
    @app.exception_handler(CorporateEmailRequiredError)
    async def invalid_google_handler(request: Request, exc: CorporateEmailRequiredError):
        return JSONResponse(
            status_code=403,
            content={"error": "corporate_email_required"}
        )
    
    @app.exception_handler(InactiveUserError)
    async def invalid_google_handler(request: Request, exc: InactiveUserError):
        return JSONResponse(
            status_code=403,
            content={"error": "user_inactive"}
        )
    
    @app.exception_handler(AccessTokenExpiredError)
    async def _(request: Request, exc: AccessTokenExpiredError):
        return JSONResponse(
            status_code=401, 
            content={"error": "token_expired"}
        )


    @app.exception_handler(InvalidAccessTokenError)
    async def _(request: Request, exc: InvalidAccessTokenError):
        return JSONResponse(
            status_code=401, 
            content={"error": "invalid_token"}
        )


    @app.exception_handler(InvalidTokenPayloadError)
    async def _(request: Request, exc: InvalidTokenPayloadError):
        return JSONResponse(
            status_code=401, 
            content={"error": "invalid_token_payload"}
        )


    @app.exception_handler(UserNotFoundError)
    async def _(request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=401, 
            content={"error": "user_not_found"}
            )
    
    @app.exception_handler(Exception)
    async def invalid_google_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception", exc_info=exc)

        return JSONResponse(
            status_code=500,
            content={"error": "internal_server_error"}
        )
    
    @app.exception_handler(ForbiddenError)
    async def forbidden_handler(request, exc):
        return JSONResponse(
            status_code=403,
            content={"error": "forbidden"}
        )
