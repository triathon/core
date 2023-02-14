# -*- coding: utf-8 -*-
"""
@File        : route.py
@Author      : Aug
@Time        : 2023/2/13 15:48
@Description : 路由
"""
from fastapi.routing import APIRouter

from api.v1.detection import detection_router


v1_route = APIRouter(prefix="/api/v1")

v1_route.include_router(detection_router)
