from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer


def initializer(binder):
    binder.bind(Logger, Logger())
    binder.bind(Tracer, Tracer())
