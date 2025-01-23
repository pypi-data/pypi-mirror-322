import os
import pytest

from . import connect
from .exceptions import ErrorMessageException
from .model import InformationResponse, FetchResponse


def get_connection_string():
    return os.environ.get("CONNECTION_STRING")


def no_connection_string():
    return get_connection_string() is None


@pytest.fixture
async def connection():
    async with connect(get_connection_string()) as c:
        yield c


@pytest.mark.skipif(no_connection_string(), reason="No connection string")
async def test_info(connection):
    info = await connection.info()
    assert isinstance(info, InformationResponse)


actor_id = None


@pytest.mark.skipif(no_connection_string(), reason="No connection string")
@pytest.mark.dependency()
async def test_create_actor(connection):
    info = await connection.info()
    base_url = info.base_urls[0]
    actor_count = len(info.actors)

    assert base_url.startswith("http://") or base_url.startswith("https://")

    actor = await connection.create_actor(base_url)

    assert actor["id"].startswith(base_url)

    global actor_id
    actor_id = actor["id"]

    new_info = await connection.info()
    assert len(new_info.actors) == actor_count + 1
    assert actor_id in new_info.actors


@pytest.mark.skipif(no_connection_string(), reason="No connection string")
@pytest.mark.dependency(depends=["test_create_actor"])
async def test_fetch(connection):
    fetch = await connection.fetch(actor_id, actor_id)
    assert isinstance(fetch, FetchResponse)

    assert fetch.uri == actor_id
    assert fetch.data["id"] == actor_id


@pytest.mark.skipif(no_connection_string(), reason="No connection string")
@pytest.mark.dependency(depends=["test_create_actor"])
async def test_trigger_send_message(connection):
    data = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": actor_id + "#12343",
        "type": "AnimalSound",
        "to": "https://www.w3.org/ns/activitystreams#Public",
        "actor": actor_id,
        "content": "moo",
    }

    await connection.trigger("send_message", {"actor": actor_id, "data": data})

    outgoing = await connection.next_outgoing()

    assert outgoing["actor"] == actor_id
    raw_data = outgoing["data"]["raw"]
    assert raw_data["type"] == "AnimalSound"


@pytest.mark.skipif(no_connection_string(), reason="No connection string")
async def test_error_queue(connection):
    with pytest.raises(ErrorMessageException):
        await connection.create_actor("http://unknown.example")
    await connection.next_error()


@pytest.mark.skipif(no_connection_string(), reason="No connection string")
@pytest.mark.dependency(depends=["test_fetch", "test_trigger_send_message"])
async def test_delete_actor(connection):

    await connection.trigger("delete_actor", {"actor": actor_id})

    outgoing = await connection.next_outgoing()

    raw_data = outgoing["data"]["raw"]
    assert raw_data["type"] == "Delete"

    # FIXME
    #
    # info = await connection.info()
    # assert actor_id not in info.actors
