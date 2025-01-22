from __future__ import annotations

__all__ = ["FastAPI"]

import inspect
from typing import Any

import uvicorn
from fastapi import APIRouter, Depends
from fastapi import FastAPI as BaseFastAPI
from fastapi import HTTPException, Security, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    SecurityScopes,
)

from verse.core import (
    Component,
    Context,
    DataModel,
    Operation,
    Provider,
    Response,
)
from verse.core.exceptions import BaseError

app = None


class FastAPI(Provider):
    component: Component
    api_keys: list[str] | None
    host: str
    port: int
    reload: bool
    workers: int
    nparams: dict[str, Any]

    _app: BaseFastAPI

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        reload: bool = False,
        workers: int = 1,
        nparams: dict[str, Any] = dict(),
        **kwargs,
    ):
        """Initialize.

        Args:
            host:
                Host IP address.
            port:
                HTTP port.
            reload:
                A value indicating whether the app should be reloaded
                when any files are modified.
            workers:
                Number of uvicorn worker processes.
            nparams:
                Native parameters to FastAPI and uvicorn client.
        """
        self.host = host
        self.port = port
        self.reload = reload
        self.workers = workers
        self.nparams = nparams
        self._app = BaseFastAPI(**self.nparams)

    def __run__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        api = GenericAPI(self.get_component().component)
        return self._start(api)

    async def __arun__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        api = GenericAsyncAPI(self.get_component().component)
        return self._start(api)

    def _start(self, api: BaseAPI) -> Response[Any]:
        dependencies = []
        if self.get_component().api_keys is not None:
            auth = Auth(self.get_component().api_keys)
            dependencies.append(Security(auth.authenticate))
        self._app.include_router(api.router, dependencies=dependencies)
        if self.reload is False and self.workers == 1:
            uvicorn.run(
                self._app,
                host=self.host or self.get_component().host,
                port=self.port or self.get_component().port,
                reload=self.reload,
                workers=self.workers,
            )
        else:
            global app
            app = self._app
            uvicorn.run(
                self._get_app_string(),
                host=self.host or self.get_component().host,
                port=self.port or self.get_component().port,
                reload=self.reload,
                workers=self.workers,
            )
        return Response(result=None)

    def _get_app_string(self) -> str:
        module = inspect.getmodule(self)
        if module is not None:
            return f"{module.__name__}:app"
        raise ModuleNotFoundError("Module not found")


class BaseAPI:
    component: Component
    router: APIRouter


class Request(DataModel):
    operation: Operation | None = None
    context: Context | None = None


class GenericAPI(BaseAPI):
    def __init__(self, component: Component):
        self.component = component
        self.router = APIRouter()
        self.router.add_api_route("/", self.run, methods=["POST"])

    def run(self, request: Request) -> Any:
        try:
            return self.component.__run__(
                operation=request.operation, context=request.context
            )
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))


class GenericAsyncAPI(BaseAPI):
    def __init__(self, component: Component):
        self.component = component
        self.router = APIRouter()
        self.router.add_api_route("/", self.run, methods=["POST"])

    async def run(self, request: Request) -> Any:
        try:
            return await self.component.__arun__(
                operation=request.operation,
                context=request.context,
            )
        except BaseError as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))


class Auth:
    api_keys: list[str]

    def __init__(self, api_keys: list[str]):
        self.api_keys = api_keys

    async def authenticate(
        self,
        security_scopes: SecurityScopes,
        token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer()),
    ) -> None:
        if token is not None and token.credentials in self.api_keys:
            return
        raise UnauthenticatedException()


class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str = "Requires authentication"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )
