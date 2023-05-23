import pytest

from aiokeepin import KeepinClient
from aiokeepin.exceptions import (
    InvalidAPIKeyError,
    KeepinStatusError,
    NotFoundError,
)


@pytest.mark.asyncio
async def test_invalid_api_key_error():
    client = KeepinClient("invalid-api-key")

    with pytest.raises(InvalidAPIKeyError):
        await client.get("/clients")

    try:
        await client.get("/clients")
    except InvalidAPIKeyError as e:
        assert e.status_code == 401

    try:
        await client.get("/clients")
    except KeepinStatusError as e:
        assert e.status_code == 401


@pytest.mark.asyncio
async def test_not_found():
    client = KeepinClient("api_key")

    with pytest.raises(NotFoundError):
        await client.get("/clientssdf")

    try:
        await client.get("/clientssdf")
    except NotFoundError as e:
        assert e.status_code == 404

    try:
        await client.get("/clientssdf")
    except KeepinStatusError as e:
        assert e.status_code == 404
