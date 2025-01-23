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


from conf import Config
from db.mongodb.config import MongoDBConfig, check
from pymongo import MongoClient


def new_mongodb(config: MongoDBConfig):
    """
    new_mongodb_client
    Args:
        config:

    Returns:

    """
    config.check()
    mongo_uri = "mongodb://{}:{}@{}:{}".format(config.user,
                                               config.password,
                                               config.host,
                                               config.port)
    return MongoClient(mongo_uri)
