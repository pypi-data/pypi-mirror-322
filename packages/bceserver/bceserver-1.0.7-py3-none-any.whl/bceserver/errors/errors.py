#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 Copyright (c) 2024 Baidu, Inc.
# All rights reserved.
#
# File    : errors.py
# Author  : chujianfei
# Description :
"""
from baidubce.exception import BceError, BceServerError
from pymongo.errors import DuplicateKeyError
from sqlalchemy.exc import IntegrityError, NoResultFound
import re

# Common errors
ERROR_NOT_IMPLEMENTED = BceServerError(
    status_code=500,
    code="NotImplemented",
    message="API ."
)
ERROR_ACCESS_DENIED = BceServerError(
    status_code=403,
    code="AccessDenied",
    message="Access denied."
)
ERROR_INAPPROPRIATE_JSON = BceServerError(
    status_code=400,
    code="InappropriateJSON",
    message="The JSON you provided was well-formed and valid, but not appropriate for this operation."
)
ERROR_INTERNAL_ERROR = BceServerError(
    status_code=500,
    code="InternalError",
    message="We encountered an internal error. Please try again."
)
ERROR_INVALID_HTTP_REQUEST = BceServerError(
    status_code=400,
    code="InvalidHTTPRequest",
    message="There was an error in the body of your HTTP request."
)
ERROR_INVALID_URI = BceServerError(
    status_code=400,
    code="InvalidURI",
    message="Could not parse the specified URI."
)
ERROR_MALFORMED_JSON = BceServerError(
    status_code=400,
    code="MalformedJSON",
    message="The JSON you provided was not well-formed."
)
ERROR_INVALID_VERSION = BceServerError(
    status_code=404,
    code="InvalidVersion",
    message="The API version specified was invalid."
)
ERROR_OPT_IN_REQUIRED = BceServerError(
    status_code=403,
    code="OptInRequired",
    message="A subscription for the service is required."
)
ERROR_REQUEST_EXPIRED = BceServerError(
    status_code=400,
    code="RequestExpired",
    message="Request has expired."
)
ERROR_IDEMPOTENT_PARAMETER_MISMATCH = BceServerError(
    status_code=403,
    code="IdempotentParameterMismatch",
    message="The request uses the same client token as a previous, but non-identical request."
)
ERROR_SIGNATURE_DOES_NOT_MATCH = BceServerError(
    status_code=400,
    code="SignatureDoesNotMatch",
    message="The request signature we calculated does not match the signature you provided. "
            "Check your Secret Access Key and signing method. Consult the service documentation for details."
)
ERROR_RESOURCE_NOT_FOUND = BceServerError(
    status_code=404,
    code="ResourceNotFound",
    message="The resource was not found."
)
ERROR_RESOURCE_IS_EXISTS = BceServerError(
    status_code=409,
    code="ResourceIsExists",
    message="The resource already exists."
)
ERROR_API_NOT_FOUND = BceServerError(
    status_code=404,
    code="APINotFound",
    message="The API was not found."
)

# Regex for specific database errors
db_order_err_msg_regex = re.compile(r"^Unknown column '(?P<column>.+?)' in 'order clause'")


def new_invalid_parameter_error(message):
    """
    new_invalid_parameter_error returns a new invalid parameter error.
    Returns:

    """
    return BceServerError(status_code=400, code="InvalidParameter", message=message)


def new_empty_parameter_error(parameter_name):
    """
    new_empty_parameter_error returns a new empty parameter error.
    Args:
        parameter_name:

    Returns:

    """
    return BceServerError(status_code=400, code="InvalidParameter", message="Parameter " + parameter_name + " is empty")


def new_db_error(err):
    """
    new_db_error returns a new database error.
    Args:
        err:

    Returns:

    """
    if err is None:
        return None

    if isinstance(err, NoResultFound):
        return ERROR_RESOURCE_NOT_FOUND

    if isinstance(err, IntegrityError):
        if "UNIQUE constraint failed" in str(err):
            return ERROR_RESOURCE_IS_EXISTS

    match = db_order_err_msg_regex.search(str(err))
    if match:
        return new_invalid_parameter_error("Unknown field used in orderBy")

    if isinstance(err, DuplicateKeyError):
        return ERROR_RESOURCE_IS_EXISTS

    return BceServerError(status_code=500, code="InternalError", message=str(err))


def wrap_error(err: Exception, message: str = "") -> BceServerError:
    """
    Wrap an existing error with additional context.
    If the error is an instance of Error, augment its message.
    Otherwise, create a new Error instance.

    Args:
        err (Exception): The original error.
        message (str): The additional context to wrap the error with.

    Returns:
        BceServerError: A new or modified Error instance.
    """
    if isinstance(err, BceServerError):
        # 如果是自定义 Error 类型，添加上下文信息到 message
        return BceServerError(
            status_code=err.status_code,
            code=err.code,
            message=f"{message} {str(err)}",
            request_id=err.request_id,
        )
    else:
        # 如果是其他类型的错误，创建一个新的 Error 实例
        return BceServerError(
            status_code=500,
            code="InternalError",
            message=f"{message} {str(err)}"
        )
