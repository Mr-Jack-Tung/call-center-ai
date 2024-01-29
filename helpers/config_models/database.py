from enum import Enum
from pydantic import validator, SecretStr, Field
from pydantic_settings import BaseSettings
from typing import Optional


class Mode(str, Enum):
    COSMOS_DB = "cosmos_db"
    SQLITE = "sqlite"


class CosmosDbModel(BaseSettings, env_prefix="database_cosmos_db_"):
    access_key: SecretStr
    container: str
    database: str
    endpoint: str


class SqliteModel(BaseSettings, env_prefix="database_sqlite_"):
    path: str = ".local"
    schema_version: int = Field(default=3, frozen=True)
    table: str = "calls"

    def full_path(self) -> str:
        """
        Returns the full path to the sqlite database file.

        Formatted as: `{path}-v{schema_version}.sqlite`.
        """
        return f"{self.path}-v{self.schema_version}.sqlite"


class DatabaseModel(BaseSettings, env_prefix="database_"):
    cosmos_db: Optional[CosmosDbModel] = None
    mode: Mode = Mode.SQLITE
    sqlite: Optional[SqliteModel] = None

    @validator("cosmos_db", always=True)
    def check_cosmos_db(cls, v, values, **kwargs):
        if not v and values.get("mode", None) == Mode.COSMOS_DB:
            raise ValueError("Cosmos DB config required")
        return v

    @validator("sqlite", always=True)
    def check_sqlite(cls, v, values, **kwargs):
        if not v and values.get("mode", None) == Mode.SQLITE:
            raise ValueError("Sqlite config required")
        return v
