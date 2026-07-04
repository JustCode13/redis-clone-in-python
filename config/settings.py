from pathlib import Path
import typing
class Settings:
    def __init__(self):
        self.host: str = "127.0.0.1"
        self.port: int = 6379
        self.data_directory: Path = Path("data")
        self.aof_enabled: bool = True
        self.rdb_enabled: bool = True
        self.max_keys: int = 10000
        self.snapshot_interval: int = 300
        self.log_level: str = "INFO"

