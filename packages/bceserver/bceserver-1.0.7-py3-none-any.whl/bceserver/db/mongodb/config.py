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
from pydantic import BaseModel

from conf import DEFAULT_CONFIG_FILE_PATH, ENV_SERVER_CONFIG_PATH
import os

from context import SingletonContext

GLOBAL_MONGO_DB_CONFIG_KEY = "mongodb_config"


class MongoDBConfig(BaseModel):
    """
    MongoDBConfig
    """

    host: str
    port: int
    user: str
    password: str
    db: str
    collection: str
    shard_user: str = None
    shard_password: str = None

    def check(self):
        """
        check
        Args:
            config:

        Returns:

        """
        assert self.host is not None and self.host.strip() != "", "MongoDB Config.Host is empty"
        assert isinstance(self.port, int) and self.port > 0, "MongoDB Config.Port is empty"
        assert self.user is not None and self.user.strip() != "", "MongoDB Config.User is empty"
        assert self.password is not None and self.password.strip() != "", "MongoDB Config.Password is empty"
        assert self.db is not None and self.db.strip() != "", "MongoDB Config.DB is empty"
        assert self.collection is not None and self.collection.strip() != "", "MongoDB Config.Collection is empty"


def new_mongodb_config() -> MongoDBConfig:
    """
    new_mongodb_config
    Returns:

    """
    from toml import load

    config_file_path = DEFAULT_CONFIG_FILE_PATH
    if (
            os.environ.get(ENV_SERVER_CONFIG_PATH) is not None
            and os.environ.get(ENV_SERVER_CONFIG_PATH) != ""
    ):
        config_file_path = os.environ.get(ENV_SERVER_CONFIG_PATH)

    db_config_data = load(config_file_path).get("mongodb", {})
    filtered_config = {k: v for k, v in db_config_data.items()}

    config = MongoDBConfig(**filtered_config)
    SingletonContext.instance().set_var_value(GLOBAL_MONGO_DB_CONFIG_KEY, config)
    return config
