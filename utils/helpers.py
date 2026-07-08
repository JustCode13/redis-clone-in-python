import json
import pickle
import logging
from pathlib import Path
from typing import Any


logger = logging.getLogger(__name__)


class SerializationHelper:
    """Utility helpers for persistence serialization."""

    def dump_json(self, data: Any, path: str) -> None:
        """
        Serialize a Python object to a JSON file.

        Args:
            data: The Python object to serialize.
            path: Destination path of the JSON file.

        Raises:
            TypeError:
                If `path` is not a string, is empty, or if `data`
                contains objects that are not JSON serializable.
            OSError:
                If the file cannot be written.
        """
        # -------------------------
        # Validate path
        # -------------------------
        if not isinstance(path, str):
            raise TypeError("path must be a string")

        path = path.strip()
        if not path:
            raise TypeError("path cannot be empty")

        file_path = Path(path)

        if not file_path.name:
            raise TypeError("path must contain a valid filename")

        # -------------------------
        # Write JSON
        # -------------------------
        try:
            with file_path.open(
                mode="w",
                encoding="utf-8",
                newline="\n",
            ) as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=False,
                )
                file.flush()

        except TypeError:
            logger.exception(
                "Failed to serialize object to JSON: %s",
                file_path,
            )
            raise

        except OSError:
            logger.exception(
                "Failed to write JSON file: %s",
                file_path,
            )
            raise


    def dump_pickle(self, data: Any, path: str) -> None:
        """
        Serialize a Python object to a PICKLE file.

        Args:
            data: The Python object to serialize.
            path: Destination path of the PICKLE file.

        Raises:
            TypeError:
                If `path` is not a string, is empty, or if `data`
                contains objects that are not PICKLE serializable.
            OSError:
                If the file cannot be written.
        """
        # -------------------------
        # Validate path
        # -------------------------
        if not isinstance(path, str):
            raise TypeError("path must be a string")

        path = path.strip()
        if not path:
            raise TypeError("path cannot be empty")

        file_path = Path(path)

        if not file_path.name:
            raise TypeError("path must contain a valid filename")

        # -------------------------
        # Write PICKLE
        # -------------------------
        try:
            with file_path.open(
                mode="w",
                encoding="utf-8",
                newline="\n",
            ) as file:
                pickle.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=False,
                )
                file.flush()

        except TypeError:
            logger.exception(
                "Failed to serialize object to PICKLE: %s",
                file_path,
            )
            raise

        except OSError:
            logger.exception(
                "Failed to write JSON file: %s",
                file_path,
            )
            raise




    def compare_json_pickle(self, sample: Any) -> dict[str, str]:
        """
        Compare JSON and pickle for the given sample object.

        Args:
            sample: Any Python object that may be serialized.

        Returns:
            A dictionary describing the tradeoffs between JSON and pickle.
        """

        json_supported = True

        try:
            json.dumps(sample)
        except (TypeError, OverflowError):
            json_supported = False

        return {
            "json_supported": (
                "Yes"
                if json_supported
                else "No (object is not directly JSON serializable)"
            ),
            "pickle_supported": (
                "Yes (most Python objects can be pickled)"
            ),
            "speed": (
                "Pickle is generally faster for Python objects."
            ),
            "file_size": (
                "JSON is often larger due to its text format."
            ),
            "readability": (
                "JSON is human-readable; pickle is binary."
            ),
            "portability": (
                "JSON is language-independent; pickle is Python-specific."
            ),
            "security": (
                "JSON is safer for untrusted data. Never unpickle data from untrusted sources."
            ),
            "supported_types": (
                "Pickle supports almost every Python object. "
                "JSON supports only basic data types such as dict, list, str, int, float, bool, and None."
            ),
            "recommended_use": (
                "Use JSON for APIs, configuration files, and data exchange. "
                "Use pickle for fast persistence of Python objects."
            ),
        }
    



