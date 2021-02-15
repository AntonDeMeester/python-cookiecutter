from abc import ABCMeta
from os import environ
from typing import List


class EnvironmentMeta(ABCMeta):
    def __new__(cls, name: str, bases: List[str], namespace: dict):
        for key, value in namespace["__annotations__"].items():
            setattr(cls, key, environ.get(key, None))
        return cls


class Environment(metaclass=EnvironmentMeta):
    ENVIRONMENT: str
    APP_SECRET: str
