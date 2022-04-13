import argparse
import os
import sys
from chalice import Chalice
from chalice.test import Client
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from chalicelib.handlers.batch_handler import batch


STAGE = "local"

BATCH_DEFINITIONS = {
    "batch": {
        "batch": batch
    }
}


def batch_execute(batch_type):
    app = Chalice(app_name="unit_test")
    app.register_blueprint(batch_type)
    with Client(app, stage_name=STAGE) as client:

        dummy_event = client.events.generate_cw_event(
            "aws: events",
            "Scheduled Event",
            {},
            ["dummy:arn"]
        )

        client.lambda_.invoke("batch_handler", dummy_event)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="batchをローカル実行します")
    parser.add_argument("type", choices=["batch"])
    args = parser.parse_args()

    if args.type in BATCH_DEFINITIONS:
        definition = BATCH_DEFINITIONS[args.type]
        batch_execute(definition["batch"])
