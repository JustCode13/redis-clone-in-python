from __future__ import annotations

from typing import Type


class RedisCloneError(Exception):
    """
    Base exception for the Redis clone project.

    Every custom exception in the project should inherit from this class.
    """

    def __init__(self, message: str) -> None:
        if not isinstance(message, str):
            raise TypeError("message must be a string")

        if not message.strip():
            raise ValueError("message cannot be empty")

        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class InvalidRESPError(RedisCloneError):
    """Malformed RESP protocol received."""


class UnknownCommandError(RedisCloneError):
    """Unsupported Redis command."""


class InvalidTTLError(RedisCloneError):
    """Invalid expiration value."""


class PersistenceError(RedisCloneError):
    """Persistence subsystem failed."""


class ConfigurationError(RedisCloneError):
    """Runtime configuration invalid."""


class DatabaseCorruptionError(RedisCloneError):
    """Loaded persistence is inconsistent."""


class MemoryLimitExceeded(RedisCloneError):
    """LRU eviction unable to free memory."""


class ConnectionClosedError(RedisCloneError):
    """Peer disconnected unexpectedly."""


class SkipListError(RedisCloneError):
    """Sorted-set structure became inconsistent."""


class PubSubError(RedisCloneError):
    """Pub/Sub operation failed."""


class RetryLimitExceeded(RedisCloneError):
    """Retry decorator exhausted attempts."""


def raise_if(
    condition: bool,
    exc: Type[Exception],
    message: str,
) -> None:
    """
    Raise the supplied exception if the condition evaluates to True.

    Args:
        condition:
            Boolean expression to evaluate.

        exc:
            Exception class to instantiate.

        message:
            Error message passed to the exception.

    Raises:
        TypeError:
            If 'condition' is not a bool.

        TypeError:
            If 'exc' is not an Exception subclass.

        TypeError:
            If 'message' is not a string.

        exc:
            If condition is True.
    """

    if not isinstance(condition, bool):
        raise TypeError("condition must be a bool")

    if not isinstance(message, str):
        raise TypeError("message must be a string")

    if not isinstance(exc, type):
        raise TypeError("exc must be an exception class")

    if not issubclass(exc, Exception):
        raise TypeError("exc must inherit from Exception")

    if condition:
        raise exc(message)