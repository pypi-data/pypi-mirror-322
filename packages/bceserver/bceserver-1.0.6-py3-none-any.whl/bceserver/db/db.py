#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : db.py
# Author  : chujianfei
# Description :
"""

from db.config import DBConfig
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def new_db(config: DBConfig) -> Engine:
    """
    new_db_engine
    Args:
        config:

    Returns:

    """
    config.check()
    if config.driver == "sqlite":
        # SQLite 使用文件路径作为数据库
        db_url = f"sqlite:///{config.db or ':memory:'}"
    else:
        # 其他数据库格式：dialect+driver://username:password@host:port/dbname
        db_url = f"{config.driver}://{config.user}:{config.password}@{config.host}:{config.port}/{config.db}"

        # 创建 SQLAlchemy Engine
    engine = create_engine(db_url)
    return engine
