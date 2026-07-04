from pathlib import Path
import typing
class Settings:
    def __init__(self):
        # Network Settings
        self.host: str = str
        self.port: int = int
        # Storage Settings
        self.data_directory: Path = Path
        # Persistence Settings
        self.aof_enabled: bool = bool
        self.rdb_enabled: bool = bool
        self.snapshot_interval: int = int
        # Limits 
        self.max_keys: int = int
        # Logging
        self.log_level: str = str

    def load_defaults(self) -> None:
        self.host: str = "127.0.0.1"
        self.port: int = 6379
        self.data_directory: Path = Path("data")
        self.aof_enabled: bool = True
        self.rdb_enabled: bool = True
        self.snapshot_interval: int = 300
        self.max_keys: int = 10000
        self.log_level: str = ""

        return None

    def update(self,key, value) -> None:
        if (key == "host"):
            if not isinstance(value,str):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "port"):
            if not isinstance(value,int):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "data_directory"):
            if not isinstance(value,Path):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "aof_enabled"):
            if not isinstance(value,bool):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "rdb_enabled"):
            if not isinstance(value,bool):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "snapshot_interval"):
            if not isinstance(value,int):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "max_keys"):
            if not isinstance(value,int):
                return KeyError("Wrong Value Type")

            self.host = value
        elif (key == "log_level"):
            if not isinstance(value,str):
                return KeyError("Wrong Value Type")

            self.host = value
        
        else: 
            KeyError("Invalid Key")

        return None
    
