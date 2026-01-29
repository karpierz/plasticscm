# Copyright (c) 2019 Adam Karpierz
# SPDX-License-Identifier: Zlib

from __future__ import annotations

from typing import ParamSpec, TypeVar, Type, Any
from collections.abc import Callable
import functools
import locale

__all__ = ('PlasticError', 'PlasticHttpError')


class PlasticError(Exception):
    """Plastic error."""

    def __init__(self, error_message: str | bytes = "",
                 response_code: Any = None, response_body: Any = None) -> None:
        """Initializer"""
        if isinstance(error_message, bytes):
            error_message = self._safe_decode(error_message)
        else:
            try:
                error_message = str(error_message)
            except Exception:
                error_message = "<unprintable error message>"
        assert isinstance(error_message, str)
        super().__init__(error_message)
        self.__error_message = error_message  # Parsed error message from PlasticSCM
        self.__response_code = response_code  # Http status code
        self.__response_body = response_body  # Full http response

    error_message = property(lambda self: self.__error_message)
    response_code = property(lambda self: self.__response_code)
    response_body = property(lambda self: self.__response_body)

    def __str__(self) -> str:
        """Convert to string"""
        if self.__response_code is not None:
            return f"{self.__response_code}: {self.__error_message}"
        else:
            return f"{self.__error_message}"

    @staticmethod
    def _safe_decode(data: bytes) -> str:
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            pass
        try:
            enc = locale.getpreferredencoding(False)
            return data.decode(enc)
        except Exception:
            pass
        return data.decode("utf-8", errors="surrogateescape")


_P = ParamSpec("_P")
_R = TypeVar("_R")

def on_http_error(error: Type[PlasticError]) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """Manage PlasticHttpError exceptions.

    This decorator function can be used to catch PlasticHttpError exceptions
    raise specialized exceptions instead.

    Args:
        error: The exception type to raise -- must inherit from PlasticError
    """

    def wrap(fun: Callable[_P, _R]) -> Callable[_P, _R]:
        @functools.wraps(fun)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            try:
                return fun(*args, **kwargs)
            except PlasticHttpError as exc:
                raise error(exc.error_message, exc.response_code, exc.response_body)
        return wrapper

    return wrap


class PlasticHttpError(PlasticError):
    """Plastic HTTP error."""


class RedirectError(PlasticError):
    """Plastic redirection error."""
