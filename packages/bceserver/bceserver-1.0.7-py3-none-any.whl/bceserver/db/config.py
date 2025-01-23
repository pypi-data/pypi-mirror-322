#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : config.py
# Author  : chujianfei
# Description :
"""

from typing import Optional

from pydantic import BaseModel

from conf import DEFAULT_CONFIG_FILE_PATH, ENV_SERVER_CONFIG_PATH
import os

from context import SingletonContext

DRIVER_MYSQL = "MySQL"
DRIVER_SQLITE = "SQLite"
DRIVER_POSTGRESQL = "PostgreSQL"
DRIVER_CLICKHOUSE = "ClickHouse"

GLOBAL_DB_CONFIG_KEY = "db_config"


class DBConfig(BaseModel):
    """
    DBConfig
    """

    driver: str
    host: str
    port: int
    user: str
    password: str
    db: str
    dsn_params: Optional[str] = None
    conn_max_idle_time: int = None
    conn_max_life_time: int = None
    max_idle_conns: int = None
    max_open_conns: int = None

    def check(self):
        """
        check
        Returns:

        """
        if self.driver == DRIVER_MYSQL:
            self._check_mysql()
        elif self.driver == DRIVER_SQLITE:
            self._check_sqlite()
        elif self.driver == DRIVER_POSTGRESQL:
            self._check_postgresql()
        elif self.driver == DRIVER_CLICKHOUSE:
            self._check_clickhouse()

    def _check_mysql(self):
        """
        _check_mysql
        Returns:

        """
        assert self.host is not None and self.host.strip() != "", "DBConfig.Host is empty"
        assert isinstance(self.port, int) and self.port > 0, "DBConfig.Port is empty"
        assert self.user is not None and self.user.strip() != "", "DBConfig.User is empty"
        assert self.password is not None and self.password.strip() != "", "DBConfig.Password is empty"
        assert self.db is not None and self.db.strip() != "", "DBConfig.DB is empty"

    def _check_sqlite(self):
        """
        _check_sqlite
        Returns:

        """
        assert self.db is not None and self.db.strip() != "", "DBConfig.DB is empty"

    def _check_postgresql(self):
        """
        _check_postgresql
        Returns:

        """
        assert self.host is not None and self.host.strip() != "", "DBConfig.Host is empty"
        assert isinstance(self.port, int) and self.port > 0, "DBConfig.Port is empty"
        assert self.user is not None and self.user.strip() != "", "DBConfig.User is empty"
        assert self.password is not None and self.password.strip() != "", "DBConfig.Password is empty"
        assert self.db is not None and self.db.strip() != "", "DBConfig.DB is empty"

    def _check_clickhouse(self):
        """
        _check_clickhouse
        Returns:

        """
        assert self.host is not None and self.host.strip() != "", "DBConfig.Host is empty"
        assert isinstance(self.port, int) and self.port > 0, "DBConfig.Port is empty"
        assert self.user is not None and self.user.strip() != "", "DBConfig.User is empty"
        assert self.password is not None and self.password.strip() != "", "DBConfig.Password is empty"
        assert self.db is not None and self.db.strip() != "", "DBConfig.DB is empty"


def new_db_config():
    """
    new_db_config
    Returns:

    """
    from toml import load

    config_file_path = DEFAULT_CONFIG_FILE_PATH
    if (
            os.environ.get(ENV_SERVER_CONFIG_PATH) is not None
            and os.environ.get(ENV_SERVER_CONFIG_PATH) != ""
    ):
        config_file_path = os.environ.get(ENV_SERVER_CONFIG_PATH)

    db_config_data = load(config_file_path).get("db", {})
    filtered_config = {k: v for k, v in db_config_data.items()}

    config = DBConfig(**filtered_config)
    SingletonContext.instance().set_var_value(GLOBAL_DB_CONFIG_KEY, config)
    return config
