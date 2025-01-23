"""A library facilitating work with asynchronous APIs"""

import logging
from logging import NullHandler

from .api import (
    RequestsWaiter,
    delete_none_values_from_dict,
    dict_differences,
    extract_url_params,
    find_uuid_in_text,
    str_to_bool,
    to_curl,
    wait_for_value_in_request,
    wait_for_values_in_request,
)
from .retry import retry
from .waiter_src.checkers import CHECKERS
from .waiter_src.checkers.checker import Checker
from .waiter_src.comparators import COMPARATORS

__version__ = "0.17.0"
__all__ = [
    "Checker",
    "CHECKERS",
    "COMPARATORS",
    "delete_none_values_from_dict",
    "dict_differences",
    "extract_url_params",
    "find_uuid_in_text",
    "retry",
    "RequestsWaiter",
    "str_to_bool",
    "to_curl",
    "wait_for_values_in_request",
    "wait_for_value_in_request",
]

logging.getLogger(__name__).addHandler(NullHandler())
