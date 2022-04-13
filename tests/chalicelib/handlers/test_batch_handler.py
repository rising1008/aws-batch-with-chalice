import ast
import pytest
from chalice import Chalice
from chalice.test import Client
from chalicelib.handlers.batch_handler import batch


@pytest.fixture
def create_mocked_batch_handler() -> Chalice:
    app = Chalice(app_name="unit_test")
    app.register_blueprint(batch)
    yield app


def test_should_call_handler (create_mocked_batch_handler, capsys):

    with Client(create_mocked_batch_handler) as client:

        dummy_event = client.events.generate_cw_event(
            "aws: events",
            "Scheduled Event",
            {},
            ["dummy:arn"]
        )

        client.lambda_.invoke("batch_handler", dummy_event)

        log = ast.literal_eval(capsys.readouterr()[1])

        assert log['level'] == 'INFO'
