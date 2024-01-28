# -*- coding: utf-8 -*-
"""
@File        : web.py
@Author      : Aug
@Time        : 2023/2/13 14:35
@Description :
"""
import http
import traceback
import sys
import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise

root_path = os.path.abspath(__file__)
rootPath = '/'.join(root_path.split('/')[:-2])
sys.path.append(rootPath)

from db.orm import TORTOISE_ORM
from api.v1 import v1_route
from conf import logger


class WebAPP(object):

    _app = FastAPI()

    @staticmethod
    def create_start_app_handler():
        """start"""
        async def start_app():
            pass
        return start_app

    @staticmethod
    def create_stop_app_handler():
        """stop"""
        async def stop_app():
            pass
        return stop_app

    def mount_middlewares(self):
        """middlewares"""
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    def create_app(self) -> FastAPI:
        """create APP"""
        register_tortoise(app=self._app, config=TORTOISE_ORM)
        self._app.add_event_handler('startup', self.create_start_app_handler())
        self._app.add_event_handler('shutdown', self.create_stop_app_handler())
        self.mount_middlewares()
        return self._app

    @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        """request validation error return value overwrite"""
        return JSONResponse({"code": http.HTTPStatus.BAD_REQUEST, "msg": str(exc)},
                            status_code=http.HTTPStatus.BAD_REQUEST)

    @_app.exception_handler(Exception)
    async def all_exception_handler(request, exc: Exception):
        """CatchAllExceptions"""
        logger.error(f"GLOBAL-EXCEPTION\n"
                     f"URL:{request.url}\n"
                     f"Headers:{request.headers}\n"
                     f"Body:{request.body}\n"
                     f"{traceback.format_exc()}")
        return JSONResponse({"code": 500, "msg": "SERVER-ERROR"},
                            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)


web_app = WebAPP()
app = web_app.create_app()
app.include_router(v1_route)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("web:app", host="0.0.0.0", workers=5, reload=False)
