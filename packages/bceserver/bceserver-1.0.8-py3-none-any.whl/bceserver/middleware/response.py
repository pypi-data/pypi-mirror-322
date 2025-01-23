#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : response.py
# Author  : chujianfei
# Date    : 2024/12/12
# Time    : 20:36
# Description :
"""
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import json
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

from bceserver.errors.errors import wrap_error


# 添加封装类
class BaseResponse:
    """
    Base class for response objects.
    """

    def to_dict(self) -> dict:
        """Convert the response object to a dictionary."""
        return self.__dict__


class ResultResponse(BaseResponse):
    """
    Result response class.
    """

    def __init__(self, result: Any):
        self.success = True
        self.result = result


class PageResponse(BaseResponse):
    """
    Page response class.
    """

    def __init__(self, page: Any):
        self.success = True
        self.page = page


class ErrorResponse(BaseResponse):
    """
    Error response class.
    """

    def __init__(self, code: str, message: str, request_id: str):
        self.success = False
        self.message = {
            "code": code,
            "global": message,
            "requestID": request_id,
        }


class ModifyResponseMiddleware(BaseHTTPMiddleware):
    """
    Middleware class for modifying responses.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Dispatch the request and modify the response.
        Args:
            request:
            call_next:

        Returns:

        """
        try:
            response = await call_next(request)
        except Exception as e:
            # 捕获异常并返回自定义错误响应
            error_response = ErrorResponse(
                code=wrap_error(e).code,
                message=str(e),
                request_id=request.headers.get("X-BCE-Request-ID", ""),
            )
            return JSONResponse(content=error_response.to_dict(), status_code=500)

        # 获取响应体
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        # 验证 JSON 格式
        if body and not self.is_valid_json(body):
            error_response = ErrorResponse(
                code="InappropriateJSON",
                message="Invalid JSON format in response",
                request_id=response.headers.get("X-BCE-Request-ID", ""),
            )
            return JSONResponse(content=error_response.to_dict(), status_code=400)

        # 处理错误响应
        if response.status_code // 100 != 2:
            try:
                error_details = json.loads(body)
                error_response = ErrorResponse(
                    code=error_details.get("code", "UnknownError"),
                    message=error_details.get("message", "An error occurred"),
                    request_id=error_details.get("request_id", ""),
                )
            except Exception:
                error_response = ErrorResponse(
                    code="ParseError",
                    message="Failed to parse error response",
                    request_id="",
                )
            return JSONResponse(content=error_response.to_dict(), status_code=response.status_code)

        # 处理分页响应
        try:
            page_data = json.loads(body)
            if "totalCount" in page_data and "result" in page_data:
                page_response = PageResponse(page_data)
                return JSONResponse(content=page_response.to_dict())
        except Exception:
            error_response = ErrorResponse(
                code="ParseError",
                message="Failed to parse error response",
                request_id="",
            )
            return JSONResponse(content=error_response.to_dict(), status_code=response.status_code)

        # 处理通用响应
        try:
            content = json.loads(body)
            result_response = ResultResponse(content)
            return JSONResponse(content=result_response.to_dict())
        except Exception:
            return response

    @staticmethod
    def is_valid_json(data: bytes) -> bool:
        """
        判断是否为有效的 JSON 格式
        Args:
            data:

        Returns:

        """
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False

