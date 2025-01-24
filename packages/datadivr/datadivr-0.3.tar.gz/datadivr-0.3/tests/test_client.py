import json
from unittest.mock import AsyncMock, patch

import pytest
import websockets

from datadivr.exceptions import UnsupportedWebSocketTypeError
from datadivr.transport.client import WebSocketClient
from datadivr.transport.messages import send_message
from datadivr.transport.models import WebSocketMessage


@pytest.fixture
def mock_websocket():
    # Use AsyncMock to avoid issues with unawaited coroutine warnings
    return AsyncMock(spec=websockets.WebSocketClientProtocol)


@pytest.fixture
def client():
    return WebSocketClient("ws://test.com/ws")


@pytest.mark.asyncio
async def test_connect(client, mock_websocket):
    mock_connect = AsyncMock(return_value=mock_websocket)
    mock_websocket.send = AsyncMock()

    with patch("websockets.connect", mock_connect):
        await client.connect()
        assert client.websocket == mock_websocket
        mock_connect.assert_called_once_with(client.uri)


@pytest.mark.asyncio
async def test_send_message(client, mock_websocket):
    client.websocket = mock_websocket
    mock_websocket.send = AsyncMock()

    payload = {"test": "data"}
    await client.send_message(payload=payload, event_name="test_event")

    expected_message = WebSocketMessage(event_name="test_event", payload=payload, to="others")
    mock_websocket.send.assert_called_once_with(json.dumps(expected_message.model_dump()))


@pytest.mark.asyncio
async def test_handle_event(client, mock_websocket):
    mock_handler = AsyncMock()
    client.handlers = {"test_event": mock_handler}

    message = {"event_name": "test_event", "payload": {"data": "test"}}

    await client.handle_event(message, mock_websocket)
    mock_handler.assert_called_once()


@pytest.mark.asyncio
async def test_send_handler_names(client, mock_websocket):
    client.websocket = mock_websocket
    client.handlers = {"test_handler1": AsyncMock(), "test_handler2": AsyncMock()}
    mock_websocket.send = AsyncMock()

    await client.send_handler_names()

    expected_message = WebSocketMessage(
        event_name="CLI_HELLO", payload={"handlers": ["test_handler1", "test_handler2"]}, to="others"
    )
    mock_websocket.send.assert_called_once_with(json.dumps(expected_message.model_dump()))


@pytest.mark.asyncio
async def test_send_message_invalid_socket_type():
    """Test sending a message with an invalid socket type."""
    message = WebSocketMessage(event_name="test")
    invalid_socket = AsyncMock()  # Change to AsyncMock
    # Remove all websocket-related attributes
    del invalid_socket.send
    del invalid_socket.send_json

    with pytest.raises(UnsupportedWebSocketTypeError):
        await send_message(invalid_socket, message)
