# almabtrieb

An implementation of the Cattle Drive protocol. It is able to connect to a message broker both through AMQP and MQTT.

## Installation

For amqp, e.g. RabbitMQ

```bash
pip install almabtrieb[amqp]
```

For mqtt and mqtt over websockets

```bash
pip install almabtrieb[mqtt]   
```

## Usage

The following code example illustrates the usage of almabtrieb.

```python
from almabtrieb import connect

async with connect("amqp://user:password@localhost:5672/") as connection:
    info = await connection.info()

    print("Your actors: ", ", ".join(info.actors))
    actor_id = info.actors[0]

    # Retrieving a remote object
    result = await connection.fetch(actor_id, "http://remote.example/object/id")
    print(json.dumps(result["raw"], indent=2))

    # Sending an activity
    data = {
        "actor": actor_id,
        "message": {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Follow",
            "actor": actor_id,
            "object": "https://remote.actor/actor/id"
        }
    }
    await connection.trigger("send_message", data)
```

## Running tests

Tests can be run with

```bash
uv run pytest
```

We note that some tests require installing the mqtt and amqp libraries via

```bash
uv sync --all-extras
```

### Running tests against cattle_grid

Create an account on cattle_grid with

```bash
python -mcattle_grid account new almabtrieb password
```

Then with cattle grid running one can run

```bash
CONNECTION_STRING=mqtt://almabtrieb:password@localhost:11883 \
    uv run pytest almabtrieb/test_real.py
CONNECTION_STRING=ws://almabtrieb:password@localhost:15675/ws \
    uv run pytest almabtrieb/test_real.py
CONNECTION_STRING="amqp://almabtrieb:password@localhost:5672/" \
    uv run pytest almabtrieb/test_real.py
```

FIXME: check mqtts and amqps.
