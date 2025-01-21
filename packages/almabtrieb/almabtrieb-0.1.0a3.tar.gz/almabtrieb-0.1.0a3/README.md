# almabtrieb

## Supported protocols

- [MQTT 5](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html)
- [AMQP](https://www.amqp.org), I think 0.9.1 as supported by RabbitMQ

## Running tests

Create an account on cattle_grid with

```bash
python -mcattle_grid account new almabtrieb password
```

Then with cattle grid running one can run

```bash
CONNECTION_STRING=mqtt://almabtrieb:password@localhost:11883 uv run pytest almabtrieb/test_real.py
CONNECTION_STRING=ws://almabtrieb:password@localhost:15675/ws uv run pytest almabtrieb/test_real.py
CONNECTION_STRING="amqp://almabtrieb:password@localhost:5672/" uv run pytest almabtrieb/test_real.py
```

FIXME: check mqtts and amqps.
