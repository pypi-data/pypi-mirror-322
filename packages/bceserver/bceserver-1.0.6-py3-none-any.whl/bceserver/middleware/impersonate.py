#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : impersonate.py
# Author  : zhoubohan
# Date    : 2024/12/12
# Time    : 20:36
# Description :
"""
from typing import Callable

from bceserver.context.singleton_context import SingletonContext
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.datastructures import Headers
from bceserver.auth.consts import GLOBAL_AUTH_INFO_KEY
from bceserver.constants import (
    KEY_ORG_ID,
    KEY_USER_ID,
    HEADER_IMPERSONATE_PROJECT_ID,
    KEY_IMPERSONATE_ORIGIN_PROJECT_ID,
    KEY_PROJECT_ID,
    HEADER_IMPERSONATE_ORG_ID,
    KEY_IMPERSONATE_ORIGIN_ORG_ID,
    HEADER_IMPERSONATE_USER_ID,
    KEY_IMPERSONATE_ORIGIN_USER_ID,
    HEADER_IMPERSONATE_DEPARTMENT_ID,
    KEY_IMPERSONATE_ORIGIN_DEPARTMENT_ID,
    KEY_DEPARTMENT_ID,
    KEY_AUTH_MODE,
)


def impersonate_handler(headers: Headers, auth_info: dict) -> dict[str, str]:
    """
    Impersonate handler
    """
    if (
        len(auth_info.get(KEY_ORG_ID, "")) > 0
        and len(auth_info.get(KEY_USER_ID, "")) > 0
    ):
        return auth_info

    project_id = headers.get(HEADER_IMPERSONATE_PROJECT_ID, "")
    if len(project_id) > 0:
        auth_info[KEY_IMPERSONATE_ORIGIN_PROJECT_ID] = project_id
        auth_info[KEY_PROJECT_ID] = project_id

    org_id = headers.get(HEADER_IMPERSONATE_ORG_ID, "")
    if len(org_id) > 0:
        auth_info[KEY_IMPERSONATE_ORIGIN_ORG_ID] = org_id
        auth_info[KEY_ORG_ID] = org_id

    user_id = headers.get(HEADER_IMPERSONATE_USER_ID, "")
    if len(user_id) > 0:
        auth_info[KEY_IMPERSONATE_ORIGIN_USER_ID] = user_id
        auth_info[KEY_USER_ID] = user_id

    department_id = headers.get(HEADER_IMPERSONATE_DEPARTMENT_ID, "")
    if len(department_id) > 0:
        auth_info[KEY_IMPERSONATE_ORIGIN_DEPARTMENT_ID] = department_id
        auth_info[KEY_DEPARTMENT_ID] = department_id

    if (
        len(auth_info.get(KEY_ORG_ID, "")) > 0
        and len(auth_info.get(KEY_USER_ID, "")) > 0
    ):
        auth_info[KEY_AUTH_MODE] = "Impersonate"

    return auth_info


def get_impersonate_dependency():
    """
    Get impersonate dependency
    """

    async def impersonate(request: Request):
        """
        Impersonate
        """
        exist_auth_info = getattr(request.state, GLOBAL_AUTH_INFO_KEY, {})

        auth_info = impersonate_handler(request.headers, exist_auth_info)

        setattr(request.state, GLOBAL_AUTH_INFO_KEY, auth_info)
        SingletonContext.instance().set_var_value(GLOBAL_AUTH_INFO_KEY, auth_info)

    return impersonate


class ImpersonateMiddleware(BaseHTTPMiddleware):
    """
    ImpersonateMiddleware
    """

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Middleware for impersonation
        """
        exist_auth_info = getattr(request.state, GLOBAL_AUTH_INFO_KEY, {})

        auth_info = impersonate_handler(request.headers, exist_auth_info)

        setattr(request.state, GLOBAL_AUTH_INFO_KEY, auth_info)
        SingletonContext.instance().set_var_value(GLOBAL_AUTH_INFO_KEY, auth_info)

        return await call_next(request)
