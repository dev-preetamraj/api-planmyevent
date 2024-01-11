from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from accounts.routers import token_router, register_user_router, profile_router
from planMyTrip.utils.custom_exceptions import InternalServerError
from planMyTrip.utils.custom_response import CustomResponse

app = FastAPI()


@app.exception_handler(InternalServerError)
async def internal_server_exception_handler(request: Request, exc: InternalServerError):
    return CustomResponse(
        success=exc.success,
        status_code=exc.status_code,
        data=exc.data,
        message=exc.message,
    ).json_response()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return CustomResponse(
        success=False, status_code=exc.status_code, data=None, message=exc.detail
    ).json_response()


@app.exception_handler(RequestValidationError)
async def custom_request_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    data = [{"field": err["loc"][-1], "message": err["msg"]} for err in exc.errors()]
    return CustomResponse(
        success=False,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Some validations have failed",
        data=data,
    ).json_response()


origins = ["http://127.0.0.1:3000", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(token_router.router, prefix="/api/v1/auth/token", tags=["Accounts"])
app.include_router(
    register_user_router.router, prefix="/api/v1/auth", tags=["Accounts"]
)
app.include_router(profile_router.router, prefix="/api/v1/auth/me", tags=["Accounts"])
