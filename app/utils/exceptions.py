from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def error_response(code: str, message: str, status: int):
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": message}},
    )


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return error_response("validation_error", str(exc), 422)

    @app.exception_handler(KeyError)
    async def key_error_handler(request: Request, exc: KeyError):
        return error_response("not_found", f"Missing key: {exc}", 404)

    @app.exception_handler(Exception)
    async def generic_handler(request: Request, exc: Exception):
        return error_response("server_error", str(exc), 500)
