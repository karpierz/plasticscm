# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

from public import public
import requests


@public
class REST:

    def __request(method: str, url: str, **kwargs):
        # response.status_code == 200
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def __get(url: str, *args, **kwargs):
        # response.status_code == 200
        response = requests.get(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __options(url: str, *args, **kwargs):
        # response.status_code == 200
        response = requests.options(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __head(url: str, *args, **kwargs):
        # response.status_code == 200
        response = requests.head(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __put(url: str, *args, **kwargs):
        # response.status_code == 200
        response = requests.put(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __post(url: str, *args, **kwargs):
        # response.status_code == 200
        response = requests.post(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __patch(url: str, *args, **kwargs):
        # response.status_code == 200
        response = requests.patch(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def __delete(url: str, *args, **kwargs):
        # response.status_code == 204
        response = requests.delete(url, *args, **kwargs)
        response.raise_for_status()
        return response

    def REQUEST(method: str, url: str, rest=__request):
        def decorate(func):
            func.REST = (method, url, rest)
            return func
        return decorate

    def GET(url: str, rest=__get):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def OPTIONS(url: str, rest=__options):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def HEAD(url: str, rest=__head):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def PUT(url: str, rest=__put):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def POST(url: str, rest=__post):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def PATCH(url: str, rest=__patch):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate

    def DELETE(url: str, rest=__delete):
        def decorate(func):
            func.REST = (url, rest)
            return func
        return decorate
