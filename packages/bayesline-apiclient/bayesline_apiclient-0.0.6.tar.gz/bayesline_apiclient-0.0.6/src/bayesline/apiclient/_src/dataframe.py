import io
from copy import deepcopy
from typing import Any

import numpy as np
import pandas as pd
from bayesline.api import AsyncDataFrameAccessor, DataFrameAccessor
from bayesline.api.types import DNFFilterExpressions

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient


class DataFrameAccessorClient(DataFrameAccessor):

    def __init__(
        self,
        client: ApiClient,
        identifier: str,
        col_schema: dict[str, np.dtype],
        filters: dict[str, Any],
    ):
        self._client = client
        self._base_path = client.base_path
        self._identifier = identifier
        self._schema = col_schema
        self._filters = filters

    @property
    def columns(self) -> list[str]:
        return list(self._schema.keys())

    @property
    def filters(self) -> dict[str, list[Any] | dict[str, Any]]:
        return deepcopy(self._filters)

    @property
    def schema(self) -> dict[str, np.dtype]:
        return deepcopy(self._schema)

    def get_data(
        self,
        columns: list[str] | None = None,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
    ) -> pd.DataFrame:
        if columns is not None and len(columns) == 0:
            return pd.DataFrame()

        url = f"/serverside/{self._identifier}"

        response = self._client.post(
            url,
            json={"filters": filters or [], "columns": columns},
            params={"unique": unique},
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def set_client(self, client: ApiClient):
        self._client = client.with_base_path(self._base_path)


class AsyncDataFrameAccessorClient(AsyncDataFrameAccessor):

    def __init__(
        self,
        client: AsyncApiClient,
        identifier: str,
        col_schema: dict[str, np.dtype],
        filters: dict[str, Any],
    ):
        self._client = client
        self._base_path = client.base_path
        self._identifier = identifier
        self._schema = col_schema
        self._filters = filters

    @property
    def columns(self) -> list[str]:
        return list(self._schema.keys())

    @property
    def filters(self) -> dict[str, list[Any] | dict[str, Any]]:
        return deepcopy(self._filters)

    @property
    def schema(self) -> dict[str, np.dtype]:
        return deepcopy(self._schema)

    async def get_data(
        self,
        columns: list[str] | None = None,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
    ) -> pd.DataFrame:
        if columns is not None and len(columns) == 0:
            return pd.DataFrame()

        url = f"/serverside/{self._identifier}"

        response = await self._client.post(
            url,
            json={"filters": filters or [], "columns": columns},
            params={"unique": unique},
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def set_client(self, client: AsyncApiClient):
        self._client = client.with_base_path(self._base_path)
