#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : context
# Author  : zhoubohan
# Date    : 2024/12/15
# Time    : 14:50
# Description :
"""
from contextvars import ContextVar
from typing import Dict, Any

_context_var = ContextVar[Dict[str, Any]]("context")


def get_context() -> Dict[str, Any]:
    """
    Get context.
    """
    try:
        return _context_var.get()
    except LookupError:
        ctx = {}
        _context_var.set(ctx)
        return ctx


def reset_context() -> Dict[str, Any]:
    """
    Reset context.
    """
    ctx = {}
    _context_var.set(ctx)
    return ctx


def get_value(key: str, default: Any = None) -> Any:
    """
    Get value from context.
    """
    return get_context().get(key, default)


def set_value(key: str, value: Any) -> None:
    """
    Set value to context.
    """
    get_context()[key] = value
