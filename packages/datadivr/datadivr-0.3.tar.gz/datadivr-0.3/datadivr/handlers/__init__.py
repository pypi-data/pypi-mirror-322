"""Message handlers for DataDivr."""

from datadivr.handlers.builtin.sum_handler import handle_sum_result, msg_handler, sum_handler
from datadivr.handlers.custom_handlers import get_node_info_handler  # Import your custom handler
from datadivr.handlers.registry import HandlerType, get_handlers, websocket_handler

__all__ = [
    "HandlerType",
    "get_handlers",
    "handle_sum_result",
    "msg_handler",
    "sum_handler",
    "websocket_handler",
    "get_node_info_handler",
]
