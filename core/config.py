from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class ServerConfig:
    """
    Central runtime configuration for the Redis clone.
    """

    DEFAULT_OPTIONS: dict[str, str] = {
        "maxclients": "1000",
        "timeout": "0",
        "tcp-keepalive": "300",
        "appendfsync": "everysec",
        "save": "60 1000",
    }

    def __init__(
        self,
        host: str,
        port: int,
        max_memory: int,
        snapshot_interval: int,
        aof_enabled: bool,
        db_path: str,
    ) -> None:
        self.host = host
        self.port = port
        self.max_memory = max_memory
        self.snapshot_interval = snapshot_interval
        self.aof_enabled = aof_enabled
        self.db_path = db_path

        self.extra_options: dict[str, str] = (
            self.DEFAULT_OPTIONS.copy()
        )

        self.validate()

    def validate(self) -> None:
        """
        Validate every configuration value.
        """

        if not isinstance(self.host, str):
            raise ValueError("host must be a string")

        if not self.host.strip():
            raise ValueError("host cannot be empty")

        if not isinstance(self.port, int):
            raise ValueError("port must be an integer")

        if self.port < 1 or self.port > 65535:
            raise ValueError(
                "port must be between 1 and 65535"
            )

        if not isinstance(self.max_memory, int):
            raise ValueError(
                "max_memory must be an integer"
            )

        if self.max_memory <= 0:
            raise ValueError(
                "max_memory must be greater than zero"
            )

        if not isinstance(
            self.snapshot_interval,
            int,
        ):
            raise ValueError(
                "snapshot_interval must be an integer"
            )

        if self.snapshot_interval < 0:
            raise ValueError(
                "snapshot_interval cannot be negative"
            )

        if not isinstance(
            self.aof_enabled,
            bool,
        ):
            raise ValueError(
                "aof_enabled must be a bool"
            )

        if not isinstance(self.db_path, str):
            raise ValueError(
                "db_path must be a string"
            )

        if not self.db_path.strip():
            raise ValueError(
                "db_path cannot be empty"
            )

        db_directory = Path(self.db_path)

        if not db_directory.exists():
            raise FileNotFoundError(
                f"Database directory does not exist: "
                f"{db_directory}"
            )

        if not db_directory.is_dir():
            raise ValueError(
                f"Path is not a directory: "
                f"{db_directory}"
            )

        if not os.access(
            db_directory,
            os.R_OK | os.W_OK,
        ):
            raise ValueError(
                "Database directory must be "
                "readable and writable"
            )

        if not isinstance(
            self.extra_options,
            dict,
        ):
            raise ValueError(
                "extra_options must be a dictionary"
            )

        for key, value in (
            self.extra_options.items()
        ):
            if not isinstance(key, str):
                raise ValueError(
                    "option keys must be strings"
                )

            if not isinstance(value, str):
                raise ValueError(
                    "option values must be strings"
                )

    def load_json(self, path: str) -> None:
        """
        Load configuration from JSON.
        """

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: "
                f"{file_path}"
            )

        with file_path.open(
            mode="r",
            encoding="utf-8",
        ) as handle:
            data = json.load(handle)

        if not isinstance(data, dict):
            raise ValueError(
                "Configuration root must be an object"
            )

        self.host = data.get(
            "host",
            self.host,
        )

        self.port = data.get(
            "port",
            self.port,
        )

        self.max_memory = data.get(
            "max_memory",
            self.max_memory,
        )

        self.snapshot_interval = data.get(
            "snapshot_interval",
            self.snapshot_interval,
        )

        self.aof_enabled = data.get(
            "aof_enabled",
            self.aof_enabled,
        )

        self.db_path = data.get(
            "db_path",
            self.db_path,
        )

        options = data.get(
            "extra_options",
            {},
        )

        if options:
            if not isinstance(options, dict):
                raise ValueError(
                    "extra_options must be a dictionary"
                )

            self.extra_options = {
                str(k): str(v)
                for k, v in options.items()
            }

        self.validate()

    def save_json(self, path: str) -> None:
        """
        Write configuration safely.
        """

        self.validate()

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        temporary_path = file_path.with_suffix(file_path.suffix + ".tmp")

        with temporary_path.open(
            mode="w",
            encoding="utf-8",
        ) as handle:
            json.dump(
                self.export(),
                handle,
                indent=4,
                sort_keys=True,
            )
            handle.flush()
            os.fsync(handle.fileno())

        temporary_path.replace(file_path)

    def get_option(self, key: str) -> str:
        """
        Return CONFIG value.
        """

        if not isinstance(key, str):
            raise TypeError(
                "key must be a string"
            )

        try:
            return self.extra_options[key]
        except KeyError:
            raise KeyError(
                f"Unknown configuration option: {key}"
            ) from None

    def set_option(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Update CONFIG SET value.
        """

        if not isinstance(key, str):
            raise ValueError(
                "key must be a string"
            )

        if not key.strip():
            raise ValueError(
                "key cannot be empty"
            )

        if not isinstance(value, str):
            raise ValueError(
                "value must be a string"
            )

        self.extra_options[key] = value

    def export(self) -> dict[str, object]:
        """
        Return serializable configuration.
        """

        return {
            "host": self.host,
            "port": self.port,
            "max_memory": self.max_memory,
            "snapshot_interval": self.snapshot_interval,
            "aof_enabled": self.aof_enabled,
            "db_path": self.db_path,
            "extra_options": dict(
                self.extra_options
            ),
        }


def create_default_config() -> ServerConfig:
    """
    Create default runtime configuration.
    """

    default_db_path = Path.cwd() / "data"

    default_db_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return ServerConfig(
        host="127.0.0.1",
        port=6379,
        max_memory=256 * 1024 * 1024,
        snapshot_interval=300,
        aof_enabled=True,
        db_path=str(default_db_path),
    )


def load_configuration(
    path: str,
) -> ServerConfig:
    """
    Load validated configuration file.
    """

    config = create_default_config()
    config.load_json(path)
    return config


def save_configuration(
    config: ServerConfig,
    path: str,
) -> None:
    """
    Persist configuration.
    """

    if not isinstance(
        config,
        ServerConfig,
    ):
        raise TypeError(
            "config must be a ServerConfig instance"
        )

    config.save_json(path)