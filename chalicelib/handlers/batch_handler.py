import inject
from typing import Any, Dict
from aws_lambda_powertools import Logger
from chalice import Blueprint
from chalice import Rate
from chalicelib.utilities.inject import initializer


batch = Blueprint(__name__)


@batch.schedule(Rate(4, unit=Rate.HOURS))
def batch_handler(event: Dict[str, Any]) -> None:

    inject.configure(initializer)
    logger = inject.instance(Logger)

    try:
        logger.info("batch_handler start")

    except Exception as e:
        logger.exception(e)
    finally:
        inject.clear()
