# -*- coding: utf-8 -*-
"""
@File        : orm.py
@Author      : Aug
@Time        : 2023/2/13 15:38
@Description :
"""
import os
from pathlib import Path
from pydantic.networks import PostgresDsn

from conf import config


def get_orm_models():
    """获取models"""
    models = []
    db_path = Path(__file__).parent / 'models'

    for child in db_path.iterdir():
        if child.is_file() and not child.name.startswith('__') and not child.name.startswith('.'):
            models.append(f'db.models.{child.stem}')
    return models


TORTOISE_ORM = {
    'connections': {
        'default': PostgresDsn.build(
            scheme="postgres",
            user=config.get("db_user"),
            password=config.get("db_password"),
            host=config.get("db_host"),
            port=config.get("db_port"),
            path=f'/{config.get("db_name")}',
        ),
    },
    'apps': {
        'models': {'models': get_orm_models(), 'default_connection': 'default'},
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai',
}
