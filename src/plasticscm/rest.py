# Copyright (c) 2019 Adam Karpierz
# SPDX-License-Identifier: Zlib

from __future__ import annotations

from typing import ParamSpec, TypeVar, TypeAlias, Protocol, Literal, Any
from collections.abc import Callable
import requests

__all__ = ('REST',)


HttpMethod: TypeAlias = Literal[
    "GET", "OPTIONS", "HEAD", "PUT",
    "POST", "PATCH", "DELETE",
]

class HttpRequestFunc(Protocol):
    def __call__(self, method: HttpMethod, url: str,  # noqa: E704
                 **kwargs: Any) -> requests.Response: ...

class HttpMethodFunc(Protocol):
    def __call__(self, url: str,  # noqa: E704
                 *args: Any,
                 **kwargs: Any) -> requests.Response: ...


_P = ParamSpec("_P")
_R = TypeVar("_R")


class REST:

    @staticmethod
    def __request(method: HttpMethod, url: str, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __get(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.get(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __options(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.options(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __head(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.head(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __put(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.put(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __post(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.post(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __patch(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 200
        response = requests.patch(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def __delete(url: str, *args: Any, **kwargs: Any) -> requests.Response:
        # response.status_code == 204
        response = requests.delete(url, *args, **kwargs)
        response.raise_for_status()
        return response

    @staticmethod
    def REQUEST(method: HttpMethod, url: str,
            rest: HttpRequestFunc = __request) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (method, url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def GET(url: str,
            rest: HttpMethodFunc = __get) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def OPTIONS(url: str,
            rest: HttpMethodFunc = __options) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def HEAD(url: str,
             rest: HttpMethodFunc = __head) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def PUT(url: str,
            rest: HttpMethodFunc = __put) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def POST(url: str,
             rest: HttpMethodFunc = __post) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def PATCH(url: str,
              rest: HttpMethodFunc = __patch) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate

    @staticmethod
    def DELETE(url: str,
               rest: HttpMethodFunc = __delete) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
        def decorate(func: Callable[_P, _R]) -> Callable[_P, _R]:
            func.REST = (url, rest)  # type: ignore[attr-defined]
            return func
        return decorate
