import asyncio
import datetime as dt
import importlib.util
import io
from typing import Any, Literal

import pandas as pd
from bayesline.api import (AsyncDataFrameAccessor, AsyncSettingsRegistry,
                           DataFrameAccessor, SettingsRegistry)
from bayesline.api.equity import (AssetExposureApi, AssetUniverseApi,
                                  AsyncAssetExposureApi, AsyncAssetUniverseApi,
                                  AsyncBayeslineEquityApi,
                                  AsyncBayeslineEquityByodApi,
                                  AsyncBayeslineEquityExposureApi,
                                  AsyncBayeslineEquityPortfolioApi,
                                  AsyncBayeslineEquityUniverseApi,
                                  AsyncBayeslineFactorRiskModelsApi,
                                  AsyncBayeslineModelConstructionApi,
                                  AsyncBayeslinePortfolioHierarchyApi,
                                  AsyncBayeslinePortfolioReportApi,
                                  AsyncByodApi, AsyncFactorRiskEngineApi,
                                  AsyncFactorRiskModelApi,
                                  AsyncModelConstructionEngineApi,
                                  AsyncPortfolioHierarchyApi,
                                  AsyncPortfolioReportApi, BayeslineEquityApi,
                                  BayeslineEquityByodApi,
                                  BayeslineEquityExposureApi,
                                  BayeslineEquityPortfolioApi,
                                  BayeslineEquityUniverseApi,
                                  BayeslineFactorRiskModelsApi,
                                  BayeslineModelConstructionApi,
                                  BayeslinePortfolioHierarchyApi,
                                  BayeslinePortfolioReportApi, ByodApi,
                                  ByodSettings, ByodSettingsMenu,
                                  ExposureSettings, ExposureSettingsMenu,
                                  FactorRiskEngineApi, FactorRiskModelApi,
                                  FactorRiskModelSettings,
                                  FactorRiskModelSettingsMenu, FactorType,
                                  InferAssetIdException,
                                  ModelConstructionEngineApi,
                                  ModelConstructionSettings,
                                  ModelConstructionSettingsMenu,
                                  PortfolioHierarchyApi,
                                  PortfolioHierarchySettings,
                                  PortfolioHierarchySettingsMenu,
                                  PortfolioReportApi, ReportSettings,
                                  ReportSettingsMenu, UniverseSettings,
                                  UniverseSettingsMenu)
from bayesline.api.types import DataFrameFormat, DateLike, IdType

from bayesline.apiclient._src.client import ApiClient, AsyncApiClient
from bayesline.apiclient._src.dataframe import (AsyncDataFrameAccessorClient,
                                                DataFrameAccessorClient)
from bayesline.apiclient._src.settings import (AsyncHttpSettingsRegistryClient,
                                               HttpSettingsRegistryClient)

tqdm = lambda x: x  # noqa: E731
if importlib.util.find_spec("tqdm"):
    from tqdm import tqdm  # type: ignore


def _make_params_dict(**kwargs: Any) -> dict[str, Any]:
    """Remove None values from kwargs and return as dict."""
    return {k: v for k, v in kwargs.items() if v is not None}


class BayeslineAssetUniverseApiClient(AssetUniverseApi):

    def __init__(
        self,
        client: ApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
    ):
        self._client = client
        self._universe_settings = universe_settings
        self._id_types = id_types

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    def coverage(self, id_type: IdType | None = None) -> list[str]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = self._client.post(
            "coverage",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        return response.json()

    def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        response = self._client.post(
            "dates",
            params={"range_only": range_only, "trade_only": trade_only},
            json=self._universe_settings.model_dump(),
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {
            "mode": mode,
            "filter_mode": filter_mode,
        }
        _check_and_add_id_type(self._id_types, id_type, params)
        response = self._client.post(
            "input-id-mapping",
            params=params,
            json=self._universe_settings.model_dump(),
        )
        return pd.read_parquet(
            io.BytesIO(response.content),
            engine="pyarrow",
        )

    def counts(
        self,
        dates: bool = True,
        industry_level: int = 0,
        region_level: int = 0,
        universe_type: Literal["estimation", "coverage", "both"] = "both",
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["dates"] = dates
        params["industry_level"] = industry_level
        params["region_level"] = region_level
        params["universe_type"] = universe_type

        response = self._client.post(
            "counts",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        return pd.read_parquet(
            io.BytesIO(response.content),
            engine="pyarrow",
        )

    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        df_format: DataFrameFormat = "unstacked",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        response = self._client.post(
            "",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        df.set_index(list(df.columns[:2]), inplace=True)
        df = df.assign(value=1.0)

        if df_format == "stacked":
            return df
        else:
            return df["value"].unstack()


class AsyncBayeslineAssetUniverseApiClient(AsyncAssetUniverseApi):

    def __init__(
        self,
        client: AsyncApiClient,
        universe_settings: UniverseSettings,
        id_types: list[IdType],
    ):
        self._client = client
        self._universe_settings = universe_settings
        self._id_types = id_types

    @property
    def settings(self) -> UniverseSettings:
        return self._universe_settings

    @property
    def id_types(self) -> list[IdType]:
        return list(self._id_types)

    async def coverage(self, id_type: IdType | None = None) -> list[str]:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        response = await self._client.post(
            "coverage",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        return response.json()

    async def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        response = await self._client.post(
            "dates",
            params={"range_only": range_only, "trade_only": trade_only},
            json=self._universe_settings.model_dump(),
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    async def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {
            "mode": mode,
            "filter_mode": filter_mode,
        }
        _check_and_add_id_type(self._id_types, id_type, params)
        response = await self._client.post(
            "input-id-mapping",
            params=params,
            json=self._universe_settings.model_dump(),
        )
        return pd.read_parquet(
            io.BytesIO(response.content),
            engine="pyarrow",
        )

    async def counts(
        self,
        dates: bool = True,
        industry_level: int = 0,
        region_level: int = 0,
        universe_type: Literal["estimation", "coverage", "both"] = "both",
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["dates"] = dates
        params["industry_level"] = industry_level
        params["region_level"] = region_level
        params["universe_type"] = universe_type

        response = await self._client.post(
            "counts",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        df_format: DataFrameFormat = "unstacked",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        response = await self._client.post(
            "",
            params=params,
            json=self._universe_settings.model_dump(),
        )

        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        df.set_index(list(df.columns[:2]), inplace=True)
        df = df.assign(value=1.0)

        if df_format == "stacked":
            return df
        else:
            return df["value"].unstack()


class BayeslineEquityUniverseApiClient(BayeslineEquityUniverseApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("universe")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            UniverseSettings,
            UniverseSettingsMenu,
        )

    @property
    def settings(self) -> SettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | UniverseSettings) -> AssetUniverseApi:
        id_types = self._settings.available_settings().id_types

        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return BayeslineAssetUniverseApiClient(
                self._client, ref_or_settings, id_types
            )
        else:
            universe_settings = self.settings.get(ref_or_settings)
            return BayeslineAssetUniverseApiClient(
                self._client,
                universe_settings,
                id_types,
            )


class AsyncBayeslineEquityUniverseApiClient(AsyncBayeslineEquityUniverseApi):
    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("universe")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            UniverseSettings,
            UniverseSettingsMenu,
        )

    @property
    def settings(self) -> AsyncSettingsRegistry[UniverseSettings, UniverseSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | UniverseSettings
    ) -> AsyncAssetUniverseApi:
        settings_menu = await self._settings.available_settings()
        id_types = settings_menu.id_types

        if isinstance(ref_or_settings, UniverseSettings):
            settings_menu.validate_settings(ref_or_settings)
            return AsyncBayeslineAssetUniverseApiClient(
                self._client, ref_or_settings, id_types
            )
        else:
            universe_settings = await self.settings.get(ref_or_settings)
            return AsyncBayeslineAssetUniverseApiClient(
                self._client,
                universe_settings,
                id_types,
            )


class BayeslineAssetExposureApiClient(AssetExposureApi):

    def __init__(
        self,
        client: ApiClient,
        exposure_settings: ExposureSettings,
        id_types: list[IdType],
        universe_api: BayeslineEquityUniverseApi,
    ):
        self._client = client
        self._exposure_settings = exposure_settings
        self._id_types = id_types
        self._universe_api = universe_api

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    def dates(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = self._client.post(
            "dates",
            params={"range_only": range_only},
            json={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["by"] = by
        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = self._client.post(
            "/coverage-stats",
            params=params,
            json={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        response.raise_for_status()

        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        df.set_index(list(df.columns[:1]), inplace=True)
        df.sort_index(inplace=True)
        df.columns = pd.MultiIndex.from_tuples(
            df.columns.str.split(".").to_list(), names=["style", "substyle"]  # type: ignore
        )

        return df

    def get(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        if isinstance(universe, str | int):
            universe_settings = self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
        }

        response = self._client.post(
            "",
            params=params,
            json=body,
        )

        def _read_df(r: Any) -> pd.DataFrame:
            return pd.read_parquet(io.BytesIO(r.content), engine="pyarrow")

        if response.headers["content-type"] == "application/json":
            df = pd.concat(
                _read_df(self._client.post(page, json=body, absolute_url=True))
                for page in tqdm(response.json()["urls"])
            )
        else:
            df = _read_df(response)

        df.set_index(list(df.columns[:2]), inplace=True)
        df.sort_index(inplace=True)
        df.columns = pd.MultiIndex.from_tuples(
            df.columns.str.split(".").to_list(), names=["factor_group", "factor"]  # type: ignore
        )

        return df


class AsyncBayeslineAssetExposureApiClient(AsyncAssetExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        exposure_settings: ExposureSettings,
        id_types: list[IdType],
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client
        self._exposure_settings = exposure_settings
        self._id_types = id_types
        self._universe_api = universe_api

    @property
    def settings(self) -> ExposureSettings:
        return self._exposure_settings

    async def dates(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = await self._client.post(
            "dates",
            params={"range_only": range_only},
            json={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    async def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)
        params["by"] = by

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AsyncAssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        response = await self._client.post(
            "/coverage-stats",
            params=params,
            json={
                "universe_settings": universe_settings.model_dump(),
                "exposure_settings": self._exposure_settings.model_dump(),
            },
        )
        response.raise_for_status()
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        df.sort_index(inplace=True)
        return df

    async def get(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        _check_and_add_id_type(self._id_types, id_type, params)

        if start is not None:
            start = pd.to_datetime(start).to_pydatetime()
            params["start"] = start.strftime("%Y-%m-%d")
        if end is not None:
            end = pd.to_datetime(end).to_pydatetime()
            params["end"] = end.strftime("%Y-%m-%d")

        if isinstance(universe, str | int):
            universe_settings = await self._universe_api.settings.get(universe)
        elif isinstance(universe, UniverseSettings):
            universe_settings = universe
        elif isinstance(universe, AssetUniverseApi):
            universe_settings = universe.settings
        else:
            raise ValueError(f"illegal universe input {universe}")

        body = {
            "universe_settings": universe_settings.model_dump(),
            "exposure_settings": self._exposure_settings.model_dump(),
        }

        response = await self._client.post(
            "",
            params=params,
            json=body,
        )

        def _read_df(r: Any) -> pd.DataFrame:
            return pd.read_parquet(io.BytesIO(r.content), engine="pyarrow")

        if response.headers["content-type"] == "application/json":
            tasks = []
            pages = response.json()["urls"]
            results = []
            tasks = [
                self._client.post(page, json=body, absolute_url=True) for page in pages
            ]
            results.extend(await asyncio.gather(*tasks))

            df = pd.concat(_read_df(r) for r in results)
        else:
            df = _read_df(response)

        df.set_index(list(df.columns[:2]), inplace=True)
        df.sort_index(inplace=True)
        df.columns = pd.MultiIndex.from_tuples(
            df.columns.str.split(".").to_list(), names=["factor_group", "factor"]  # type: ignore
        )

        return df


class BayeslineEquityExposureApiClient(BayeslineEquityExposureApi):

    def __init__(self, client: ApiClient, universe_api: BayeslineEquityUniverseApi):
        self._client = client.append_base_path("exposures")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api

    @property
    def settings(self) -> SettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    def load(self, ref_or_settings: str | int | ExposureSettings) -> AssetExposureApi:
        id_types = self._universe_api.settings.available_settings().id_types

        if isinstance(ref_or_settings, ExposureSettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return BayeslineAssetExposureApiClient(
                self._client,
                ref_or_settings,
                id_types,
                self._universe_api,
            )
        else:
            exposure_settings = self.settings.get(ref_or_settings)
            return BayeslineAssetExposureApiClient(
                self._client,
                exposure_settings,
                id_types,
                self._universe_api,
            )


class AsyncBayeslineEquityExposureApiClient(AsyncBayeslineEquityExposureApi):

    def __init__(
        self,
        client: AsyncApiClient,
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("exposures")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            ExposureSettings,
            ExposureSettingsMenu,
        )
        self._universe_api = universe_api

    @property
    def settings(self) -> AsyncSettingsRegistry[ExposureSettings, ExposureSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ExposureSettings
    ) -> AsyncAssetExposureApi:
        id_types = (await self._universe_api.settings.available_settings()).id_types

        if isinstance(ref_or_settings, ExposureSettings):
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return AsyncBayeslineAssetExposureApiClient(
                self._client, ref_or_settings, id_types, self._universe_api
            )
        else:
            exposure_settings = await self.settings.get(ref_or_settings)
            return AsyncBayeslineAssetExposureApiClient(
                self._client,
                exposure_settings,
                id_types,
                self._universe_api,
            )


class FactorRiskModelApiClient(FactorRiskModelApi):

    def __init__(
        self,
        client: ApiClient,
        model_id: int,
        settings: FactorRiskModelSettings,
        asset_exposures: AssetExposureApi,
        asset_universe: AssetUniverseApi,
    ):
        self._client = client
        self._model_id = model_id
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe

    def _resolve_id_type(self, id_type: IdType | None) -> IdType:
        if id_type is None:
            universe_settings = self._settings.universe
            if isinstance(universe_settings, (str, int)):
                universe_settings = self._asset_universe.settings
            return universe_settings.id_type
        else:
            return id_type

    def dates(self) -> list[dt.date]:
        response = self._client.get(f"model/{self._model_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    def factors(self, *which: FactorType) -> list[str]:
        response = self._client.get(
            f"model/{self._model_id}/factors",
            params={"which": list(which)},
        )
        return response.json()

    def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return self._asset_exposures.get(
            self._settings.universe, start=start, end=end, id_type=id_type
        )

    def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return self._asset_universe.get(start=start, end=end, id_type=id_type)

    def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = self._client.get(
            f"model/{self._model_id}/estimation-universe",
            params={"start": start, "end": end, "id_type": id_type},
        )
        out = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        out.set_index("date", inplace=True)
        out.columns.name = id_type
        return out

    def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = self._client.get(
            f"model/{self._model_id}/market-caps",
            params={"start": start, "end": end, "id_type": id_type},
        )
        out = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        out.set_index("date", inplace=True)
        out.columns.name = id_type
        return out

    def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = self._client.get(
            f"model/{self._model_id}/future-asset-returns",
            params={"start": start, "end": end, "id_type": id_type},
        )
        out = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        out.set_index("date", inplace=True)
        out.columns.name = id_type
        return out

    def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pd.DataFrame:
        response = self._client.get(
            f"model/{self._model_id}/market-stats",
            params={
                "estimation_universe": estimation_universe,
                "industries": industries,
                "regions": regions,
            },
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def t_stats(self) -> pd.DataFrame:
        response = self._client.get(f"model/{self._model_id}/t-stats")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def p_values(self) -> pd.DataFrame:
        response = self._client.get(f"model/{self._model_id}/p-values")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def r2(self) -> pd.Series:
        response = self._client.get(f"model/{self._model_id}/r2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    def sigma2(self) -> pd.Series:
        response = self._client.get(f"model/{self._model_id}/sigma2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = self._client.get(
            f"model/{self._model_id}/style-correlation",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = self._client.get(
            f"model/{self._model_id}/industry-exposures",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def fcov(
        self,
        start: DateLike | int | None = -1,
        end: DateLike | int | None = None,
        dates: list[DateLike] | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            if not isinstance(start, int):
                params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
            else:
                params["start"] = start  # type: ignore

        if end is not None:
            if not isinstance(end, int):
                params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
            else:
                params["end"] = end  # type: ignore

        body = {"dates": None}
        if dates is not None:
            body["dates"] = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in dates]  # type: ignore

        response = self._client.post(
            f"model/{self._model_id}/fcov", params=params, json=body
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if freq is not None:
            params["freq"] = freq
        if cumulative:
            params["cumulative"] = cumulative
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = self._client.get(
            f"model/{self._model_id}/fret",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class AsyncFactorRiskModelApiClient(AsyncFactorRiskModelApi):

    def __init__(
        self,
        client: AsyncApiClient,
        model_id: int,
        settings: FactorRiskModelSettings,
        asset_exposures: AsyncAssetExposureApi,
        asset_universe: AsyncAssetUniverseApi,
    ):
        self._client = client
        self._model_id = model_id
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe

    def _resolve_id_type(self, id_type: IdType | None) -> IdType:
        if id_type is None:
            universe_settings = self._settings.universe
            if isinstance(universe_settings, (str, int)):
                universe_settings = self._asset_universe.settings
            return universe_settings.id_type
        else:
            return id_type

    async def dates(self) -> list[dt.date]:
        response = await self._client.get(f"model/{self._model_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]

    async def factors(self, *which: FactorType) -> list[str]:
        response = await self._client.get(
            f"model/{self._model_id}/factors",
            params={"which": list(which)},
        )
        return response.json()

    async def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return await self._asset_exposures.get(
            self._settings.universe, start=start, end=end, id_type=id_type
        )

    async def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        return await self._asset_universe.get(start=start, end=end, id_type=id_type)

    async def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = await self._client.get(
            f"model/{self._model_id}/estimation-universe",
            params={"start": start, "end": end, "id_type": id_type},
        )
        out = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        out.set_index("date", inplace=True)
        out.columns.name = id_type
        return out

    async def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = await self._client.get(
            f"model/{self._model_id}/market-caps",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        id_type = self._resolve_id_type(id_type)
        response = await self._client.get(
            f"model/{self._model_id}/future-asset-returns",
            params={"start": start, "end": end, "id_type": id_type},
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pd.DataFrame:
        response = await self._client.get(
            f"model/{self._model_id}/market-stats",
            params={
                "estimation_universe": estimation_universe,
                "industries": industries,
                "regions": regions,
            },
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def t_stats(self) -> pd.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/t-stats")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def p_values(self) -> pd.DataFrame:
        response = await self._client.get(f"model/{self._model_id}/p-values")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def r2(self) -> pd.Series:
        response = await self._client.get(f"model/{self._model_id}/r2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    async def sigma2(self) -> pd.Series:
        response = await self._client.get(f"model/{self._model_id}/sigma2")
        df = pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")
        return df[df.columns[0]]

    async def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = await self._client.get(
            f"model/{self._model_id}/style-correlation",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = await self._client.get(
            f"model/{self._model_id}/industry-exposures",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def fcov(
        self,
        start: DateLike | int | None = -1,
        end: DateLike | int | None = None,
        dates: list[DateLike] | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            if not isinstance(start, int):
                params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
            else:
                params["start"] = start  # type: ignore

        if end is not None:
            if not isinstance(end, int):
                params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
            else:
                params["end"] = end  # type: ignore

        body = {"dates": None}
        if dates is not None:
            body["dates"] = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in dates]  # type: ignore

        response = await self._client.post(
            f"model/{self._model_id}/fcov", params=params, json=body
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if freq is not None:
            params["freq"] = freq
        if cumulative:
            params["cumulative"] = cumulative
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        response = await self._client.get(
            f"model/{self._model_id}/fret",
            params=params,
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class ModelConstructionEngineApiClient(ModelConstructionEngineApi):

    def __init__(
        self,
        client: ApiClient,
        settings: ModelConstructionSettings,
    ):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> ModelConstructionSettings:
        return self._settings


class AsyncModelConstructionEngineApiClient(AsyncModelConstructionEngineApi):

    def __init__(
        self,
        client: AsyncApiClient,
        settings: ModelConstructionSettings,
    ):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> ModelConstructionSettings:
        return self._settings


class FactorRiskEngineApiClient(FactorRiskEngineApi):

    def __init__(
        self,
        client: ApiClient,
        settings: FactorRiskModelSettings,
        asset_exposures: AssetExposureApi,
        asset_universe: AssetUniverseApi,
        model_id: int | None = None,
    ):
        self._client = client
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe
        self._model_id = model_id

    @property
    def settings(self) -> FactorRiskModelSettings:
        return self._settings

    def get(self) -> FactorRiskModelApi:
        if self._model_id is None:
            self._model_id = self._client.post(
                "model", json=self._settings.model_dump()
            ).json()

        return FactorRiskModelApiClient(
            self._client, self._model_id, self._settings, self._asset_exposures, self._asset_universe  # type: ignore
        )


class AsyncFactorRiskEngineApiClient(AsyncFactorRiskEngineApi):

    def __init__(
        self,
        client: AsyncApiClient,
        settings: FactorRiskModelSettings,
        asset_exposures: AsyncAssetExposureApi,
        asset_universe: AsyncAssetUniverseApi,
        model_id: int | None = None,
    ):
        self._client = client
        self._settings = settings
        self._asset_exposures = asset_exposures
        self._asset_universe = asset_universe
        self._model_id = model_id

    @property
    def settings(self) -> FactorRiskModelSettings:
        return self._settings

    async def get(self) -> AsyncFactorRiskModelApi:
        if self._model_id is None:
            self._model_id = (
                await self._client.post("model", json=self._settings.model_dump())
            ).json()

        return AsyncFactorRiskModelApiClient(
            self._client,
            self._model_id,
            self._settings,
            self._asset_exposures,
            self._asset_universe,
        )


class PortfolioReportApiClient(PortfolioReportApi):

    def __init__(self, client: ApiClient, report_id: str, settings: ReportSettings):
        self._client = client
        self._report_id = report_id
        self._settings = settings

    @property
    def settings(self) -> ReportSettings:
        return self._settings

    def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
        add_totals_columns: bool = False,
        serverside: bool = False,
    ) -> pd.DataFrame | DataFrameAccessor:
        url = self._report_id if not serverside else f"{self._report_id}/serverside"
        response = self._client.post(
            url,
            json={"order": order},
            params=_make_params_dict(
                date=pd.to_datetime(date).strftime("%Y-%m-%d") if date else None,
                date_start=(
                    pd.to_datetime(date_start).strftime("%Y-%m-%d")
                    if date_start
                    else None
                ),
                date_end=(
                    pd.to_datetime(date_end).strftime("%Y-%m-%d") if date_end else None
                ),
                subtotals=subtotals,
                add_totals_columns=add_totals_columns,
            ),
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"could not get report {(response.json())}") from e

        if serverside:
            content_json = response.json()

            # Convert to appropriate dtypes
            schema_dtypes = {
                col: dtype for col, dtype in content_json["col_schema"].items()
            }

            # Create an empty DataFrame with the deserialized schema
            empty_df = pd.DataFrame(
                {col: pd.Series(dtype=dtype) for col, dtype in schema_dtypes.items()}
            )
            content_json["col_schema"] = {
                col: dtype for col, dtype in empty_df.dtypes.items()
            }
            return DataFrameAccessorClient(self._client, **content_json)
        else:
            return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def dates(self) -> list[dt.date]:
        response = self._client.get(f"{self._report_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]


class AsyncPortfolioReportApiClient(AsyncPortfolioReportApi):

    def __init__(
        self, client: AsyncApiClient, report_id: str, settings: ReportSettings
    ):
        self._client = client
        self._report_id = report_id
        self._settings = settings

    @property
    def settings(self) -> ReportSettings:
        return self._settings

    async def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
        serverside: bool = False,
        add_totals_columns: bool = False,
    ) -> pd.DataFrame | AsyncDataFrameAccessor:
        url = self._report_id if not serverside else f"{self._report_id}/serverside"
        response = await self._client.post(
            url,
            json={"order": order},
            params=_make_params_dict(
                date=pd.to_datetime(date).strftime("%Y-%m-%d") if date else None,
                date_start=(
                    pd.to_datetime(date_start).strftime("%Y-%m-%d")
                    if date_start
                    else None
                ),
                date_end=(
                    pd.to_datetime(date_end).strftime("%Y-%m-%d") if date_end else None
                ),
                subtotals=subtotals,
                add_totals_columns=add_totals_columns,
            ),
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"could not get report {(response.json())}") from e

        if serverside:
            content_json = response.json()

            # Convert to appropriate dtypes
            schema_dtypes = {
                col: dtype for col, dtype in content_json["col_schema"].items()
            }

            # Create an empty DataFrame with the deserialized schema
            empty_df = pd.DataFrame(
                {col: pd.Series(dtype=dtype) for col, dtype in schema_dtypes.items()}
            )
            content_json["col_schema"] = {
                col: dtype for col, dtype in empty_df.dtypes.items()
            }
            return AsyncDataFrameAccessorClient(self._client, **content_json)
        else:
            return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def dates(self) -> list[dt.date]:
        response = await self._client.get(f"{self._report_id}/dates")
        return [pd.to_datetime(d).to_pydatetime().date() for d in response.json()]


class BayeslineModelConstructionApiClient(BayeslineModelConstructionApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("modelconstruction")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            ModelConstructionSettings,
            ModelConstructionSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[ModelConstructionSettings, ModelConstructionSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | ModelConstructionSettings
    ) -> ModelConstructionEngineApi:
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
            return ModelConstructionEngineApiClient(self._client, settings)
        else:
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            return ModelConstructionEngineApiClient(self._client, settings_obj)


class AsyncBayeslineModelConstructionApiClient(AsyncBayeslineModelConstructionApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("modelconstruction")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            ModelConstructionSettings,
            ModelConstructionSettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[
        ModelConstructionSettings, ModelConstructionSettingsMenu
    ]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ModelConstructionSettings
    ) -> AsyncModelConstructionEngineApi:
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
        if isinstance(ref_or_settings, ModelConstructionSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
            return AsyncModelConstructionEngineApiClient(self._client, settings)
        else:
            ref = ref_or_settings
            settings_obj = await self.settings.get(ref)
            return AsyncModelConstructionEngineApiClient(self._client, settings_obj)


class BayeslineFactorRiskModelsApiClient(BayeslineFactorRiskModelsApi):

    def __init__(
        self,
        client: ApiClient,
        exposure_api: BayeslineEquityExposureApi,
        universe_api: BayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("riskmodels")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            FactorRiskModelSettings,
            FactorRiskModelSettingsMenu,
        )
        self._exposure_api = exposure_api
        self._universe_api = universe_api

    @property
    def settings(
        self,
    ) -> SettingsRegistry[FactorRiskModelSettings, FactorRiskModelSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | FactorRiskModelSettings
    ) -> FactorRiskEngineApi:
        if isinstance(ref_or_settings, FactorRiskModelSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
            asset_exposures = self._exposure_api.load(settings.exposures)
            asset_universe = self._universe_api.load(settings.universe)
            return FactorRiskEngineApiClient(
                self._client, settings, asset_exposures, asset_universe
            )
        else:
            ref = ref_or_settings
            settings_obj = self.settings.get(ref)
            if isinstance(ref, str):
                model_id = self.settings.names()[ref]
            else:
                model_id = ref
            asset_exposures = self._exposure_api.load(settings_obj.exposures)
            asset_universe = self._universe_api.load(settings_obj.universe)
            return FactorRiskEngineApiClient(
                self._client, settings_obj, asset_exposures, asset_universe, model_id
            )


class AsyncBayeslineFactorRiskModelsApiClient(AsyncBayeslineFactorRiskModelsApi):

    def __init__(
        self,
        client: AsyncApiClient,
        exposure_api: AsyncBayeslineEquityExposureApi,
        universe_api: AsyncBayeslineEquityUniverseApi,
    ):
        self._client = client.append_base_path("riskmodels")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            FactorRiskModelSettings,
            FactorRiskModelSettingsMenu,
        )
        self._exposure_api = exposure_api
        self._universe_api = universe_api

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[FactorRiskModelSettings, FactorRiskModelSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | FactorRiskModelSettings
    ) -> AsyncFactorRiskEngineApi:
        if isinstance(ref_or_settings, FactorRiskModelSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
            asset_exposures = await self._exposure_api.load(settings.exposures)
            asset_universe = await self._universe_api.load(settings.universe)
            return AsyncFactorRiskEngineApiClient(
                self._client, settings, asset_exposures, asset_universe
            )
        else:
            ref = ref_or_settings
            settings_obj = await self.settings.get(ref)
            if isinstance(ref, str):
                names = await self.settings.names()
                model_id = names[ref]
            else:
                model_id = ref
            asset_exposures = await self._exposure_api.load(settings_obj.exposures)
            asset_universe = await self._universe_api.load(settings_obj.universe)
            return AsyncFactorRiskEngineApiClient(
                self._client, settings_obj, asset_exposures, asset_universe, model_id
            )


class BayeslinePortfolioReportApiClient(BayeslinePortfolioReportApi):
    def __init__(
        self,
        client: ApiClient,
        portfoliohierarchy_api: BayeslinePortfolioHierarchyApi,
    ):
        self._client = client.append_base_path("portfolioreport")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            ReportSettings,
            ReportSettingsMenu,
        )
        self._portfoliohierarchy_api = portfoliohierarchy_api

    @property
    def settings(
        self,
    ) -> SettingsRegistry[ReportSettings, ReportSettingsMenu]:
        return self._settings

    def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
        dates: list[DateLike] | tuple[DateLike, DateLike] | None = None,
    ) -> PortfolioReportApi:
        if isinstance(ref_or_settings, ReportSettings):
            settings = ref_or_settings
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(settings)
        else:
            ref = ref_or_settings
            settings = self.settings.get(ref)

        hierarchy: PortfolioHierarchySettings | None = None
        if hierarchy_ref_or_settings is not None:
            if isinstance(hierarchy_ref_or_settings, PortfolioHierarchySettings):
                hierarchy = hierarchy_ref_or_settings
            else:
                hierarchy = (
                    self._portfoliohierarchy_api.load(hierarchy_ref_or_settings)
                ).settings

        dates_params = {"start_date": None, "end_date": None, "dates": None}
        if dates is not None:
            if isinstance(dates, tuple):
                dates_params["start_date"] = pd.to_datetime(dates[0]).strftime("%Y-%m-%d")  # type: ignore
                dates_params["end_date"] = pd.to_datetime(dates[1]).strftime("%Y-%m-%d")  # type: ignore
            else:
                dates_params["dates"] = [  # type: ignore
                    pd.to_datetime(d).strftime("%Y-%m-%d") for d in dates
                ]

        params = {
            "settings": settings.model_dump(),
            **dates_params,
        }

        if hierarchy is not None:
            params["hierarchy"] = hierarchy.model_dump()

        response = self._client.post(
            "/report",
            json=params,
        )
        report_id = response.json()["report_id"]
        return PortfolioReportApiClient(self._client, report_id, settings)


class AsyncBayeslinePortfolioReportApiClient(AsyncBayeslinePortfolioReportApi):
    def __init__(
        self,
        client: AsyncApiClient,
        portfoliohierarchy_api: AsyncBayeslinePortfolioHierarchyApi,
    ):
        self._client = client.append_base_path("portfolioreport")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            ReportSettings,
            ReportSettingsMenu,
        )
        self._portfoliohierarchy_api = portfoliohierarchy_api

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[ReportSettings, ReportSettingsMenu]:
        return self._settings

    async def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
        dates: list[DateLike] | tuple[DateLike, DateLike] | None = None,
    ) -> AsyncPortfolioReportApi:
        if isinstance(ref_or_settings, ReportSettings):
            settings = ref_or_settings
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(settings)
        else:
            ref = ref_or_settings
            settings = await self.settings.get(ref)

        hierarchy: PortfolioHierarchySettings | None = None
        if hierarchy_ref_or_settings is not None:
            if isinstance(hierarchy_ref_or_settings, PortfolioHierarchySettings):
                hierarchy = hierarchy_ref_or_settings
            else:
                hierarchy = (
                    await self._portfoliohierarchy_api.load(hierarchy_ref_or_settings)
                ).settings

        dates_params = {"start_date": None, "end_date": None, "dates": None}
        if dates is not None:
            if isinstance(dates, tuple):
                dates_params["start_date"] = pd.to_datetime(dates[0]).strftime("%Y-%m-%d")  # type: ignore
                dates_params["end_date"] = pd.to_datetime(dates[1]).strftime("%Y-%m-%d")  # type: ignore
            else:
                dates_params["dates"] = [  # type: ignore
                    pd.to_datetime(d).strftime("%Y-%m-%d") for d in dates
                ]

        params = {
            "settings": settings.model_dump(),
            **dates_params,
        }

        if hierarchy is not None:
            params["hierarchy"] = hierarchy.model_dump()

        response = await self._client.post(
            "/report",
            json=params,
        )
        report_id = response.json()["report_id"]
        return AsyncPortfolioReportApiClient(self._client, report_id, settings)


class ByodApiClient(ByodApi):

    def __init__(self, client: ApiClient, identifier: int, settings: ByodSettings):
        self._client = client
        self._identifier = identifier
        self._settings = settings

    @property
    def settings(self) -> ByodSettings:
        return self._settings

    def is_uploaded(self) -> bool:
        response = self._client.get(f"{self._identifier}")
        return response.json()["is_uploaded"]

    def get_raw(self) -> pd.DataFrame:
        response = self._client.get(f"{self._identifier}/raw")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        if id_type is not None:
            params["id_type"] = id_type

        response = self._client.get(f"{self._identifier}/processed", params=params)
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def upload(self, df: pd.DataFrame, overwrite: bool = False) -> None:
        if self.is_uploaded() and not overwrite:
            raise ValueError(
                "Data has already been uploaded. Set overwrite=True to re-upload."
            )
        out = io.BytesIO()
        df.to_parquet(out, engine="pyarrow")
        self._client.post(f"{self._identifier}/upload", data=out.getvalue(), json=None)


class AsyncByodApiClient(AsyncByodApi):

    def __init__(self, client: AsyncApiClient, identifier: int, settings: ByodSettings):
        self._client = client
        self._identifier = identifier
        self._settings = settings

    @property
    def settings(self) -> ByodSettings:
        return self._settings

    async def is_uploaded(self) -> bool:
        response = await self._client.get(f"{self._identifier}")
        return response.json()["is_uploaded"]

    async def get_raw(self) -> pd.DataFrame:
        response = await self._client.get(f"{self._identifier}/raw")
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {}
        if start is not None:
            params["start"] = pd.to_datetime(start).strftime("%Y-%m-%d")
        if end is not None:
            params["end"] = pd.to_datetime(end).strftime("%Y-%m-%d")
        if id_type is not None:
            params["id_type"] = id_type

        response = await self._client.get(
            f"{self._identifier}/processed", params=params
        )
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def upload(self, df: pd.DataFrame, overwrite: bool = False) -> None:
        if await self.is_uploaded() and not overwrite:
            raise ValueError(
                "Data has already been uploaded. Set overwrite=True to re-upload."
            )
        out = io.BytesIO()
        df.to_parquet(out, engine="pyarrow")
        await self._client.post(
            f"{self._identifier}/upload", data=out.getvalue(), json=None
        )


class BayeslineEquityByodApiClient(BayeslineEquityByodApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("byod")
        self._settings = HttpSettingsRegistryClient(
            self._client, ByodSettings, ByodSettingsMenu
        )

    @property
    def settings(self) -> SettingsRegistry[ByodSettings, ByodSettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | ByodSettings, *, name: str | None = None
    ) -> ByodApi:
        if isinstance(ref_or_settings, ByodSettings):
            settings = ref_or_settings

            if name is None:
                raise ValueError("Must provide a name when using inline byod settings.")
            identifier = self.settings.save(name, settings)
        else:
            settings = self.settings.get(ref_or_settings)

            if isinstance(ref_or_settings, str):
                name = ref_or_settings
                identifier = self.settings.names()[ref_or_settings]
            else:
                name = self.settings.ids()[ref_or_settings]
                identifier = ref_or_settings

        settings_menu = self.settings.available_settings()
        settings_menu.validate_settings(settings)

        return ByodApiClient(self._client, identifier, settings)

    def generate_settings(
        self,
        df: pd.DataFrame,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        try:
            return super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=asset_id_col,
                asset_id_type=asset_id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
        except InferAssetIdException as e:
            id_cols = {col: list(df[col].drop_duplicates()) for col in e.id_cols}
            id_types = e.id_types
            inferred_ids = self._client.post(
                "infer-id-type", json=id_cols, params={"id_types": id_types}
            ).json()
            id_col, id_type = inferred_ids["id_col"], inferred_ids["id_type"]
            if id_type is None or id_col is None:
                raise ValueError("No matching id type/column found")
            return super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=id_col,
                asset_id_type=id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )


class AsyncBayeslineEquityByodApiClient(AsyncBayeslineEquityByodApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("byod")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client, ByodSettings, ByodSettingsMenu
        )

    @property
    def settings(self) -> AsyncSettingsRegistry[ByodSettings, ByodSettingsMenu]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | ByodSettings, *, name: str | None = None
    ) -> AsyncByodApi:
        if isinstance(ref_or_settings, ByodSettings):
            settings = ref_or_settings

            if name is None:
                raise ValueError("Must provide a name when using inline byod settings.")
            identifier = await self.settings.save(name, settings)
        else:
            settings = await self.settings.get(ref_or_settings)

            if isinstance(ref_or_settings, str):
                name = ref_or_settings
                identifier = (await self.settings.names())[ref_or_settings]
            else:
                name = (await self.settings.ids())[ref_or_settings]
                identifier = ref_or_settings

        settings_menu = await self.settings.available_settings()
        settings_menu.validate_settings(settings)

        return AsyncByodApiClient(self._client, identifier, settings)

    async def generate_settings(
        self,
        df: pd.DataFrame,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        try:
            return await super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=asset_id_col,
                asset_id_type=asset_id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
        except InferAssetIdException as e:
            id_cols = {col: list(df[col].drop_duplicates()) for col in e.id_cols}
            id_types = e.id_types
            inferred_ids = (
                await self._client.post(
                    "infer-id-type", json=id_cols, params={"id_types": id_types}
                )
            ).json()
            id_col, id_type = inferred_ids["id_col"], inferred_ids["id_type"]
            if id_type is None or id_col is None:
                raise ValueError("No matching id type/column found")
            return await super().generate_settings(
                df,
                styles=styles,
                portfolios=portfolios,
                date_col=date_col,
                asset_id_col=id_col,
                asset_id_type=id_type,
                extra_cols=extra_cols,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )


class PortfolioHierarchyApiClient(PortfolioHierarchyApi):

    def __init__(self, client: ApiClient, settings: PortfolioHierarchySettings):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> PortfolioHierarchySettings:
        return self._settings

    def get_id_types(self) -> dict[str, list[IdType]]:
        return self._client.post("id-types", json=self._settings.model_dump()).json()

    def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        response = self._client.post(
            "dates", json=self._settings.model_dump(), params={"collapse": collapse}
        )
        response_data = response.json()
        return {
            p: [pd.to_datetime(d).date() for d in response_data[p]]
            for p in response_data.keys()
        }

    def get(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params = {}
        if start_date is not None:
            params["start_date"] = pd.to_datetime(start_date).strftime("%Y-%m-%d")
        if end_date is not None:
            params["end_date"] = pd.to_datetime(end_date).strftime("%Y-%m-%d")
        if id_type is not None:
            params["id_type"] = id_type
        response = self._client.post(
            "/",
            params=params,
            json=self._settings.model_dump(),
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class AsyncPortfolioHierarchyApiClient(AsyncPortfolioHierarchyApi):

    def __init__(self, client: AsyncApiClient, settings: PortfolioHierarchySettings):
        self._client = client
        self._settings = settings

    @property
    def settings(self) -> PortfolioHierarchySettings:
        return self._settings

    async def get_id_types(self) -> dict[str, list[IdType]]:
        return (
            await self._client.post("id-types", json=self._settings.model_dump())
        ).json()

    async def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        response = await self._client.post(
            "dates", json=self._settings.model_dump(), params={"collapse": collapse}
        )
        response_data = response.json()
        return {
            p: [pd.to_datetime(d).date() for d in response_data[p]]
            for p in response_data.keys()
        }

    async def get(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        params = {}
        if start_date is not None:
            params["start_date"] = pd.to_datetime(start_date).strftime("%Y-%m-%d")
        if end_date is not None:
            params["end_date"] = pd.to_datetime(end_date).strftime("%Y-%m-%d")
        if id_type is not None:
            params["id_type"] = id_type
        response = await self._client.post(
            "/",
            params=params,
            json=self._settings.model_dump(),
        )

        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class BayeslinePortfolioHierarchyApiClient(BayeslinePortfolioHierarchyApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("portfoliohierarchy")
        self._settings = HttpSettingsRegistryClient(
            self._client,
            PortfolioHierarchySettings,
            PortfolioHierarchySettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> SettingsRegistry[PortfolioHierarchySettings, PortfolioHierarchySettingsMenu]:
        return self._settings

    def load(
        self, ref_or_settings: str | int | PortfolioHierarchySettings
    ) -> PortfolioHierarchyApi:
        if isinstance(ref_or_settings, PortfolioHierarchySettings):
            settings_menu = self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return PortfolioHierarchyApiClient(self._client, ref_or_settings)
        else:
            portfoliohierarchy_settings = self.settings.get(ref_or_settings)
            return PortfolioHierarchyApiClient(
                self._client,
                portfoliohierarchy_settings,
            )


class AsyncBayeslinePortfolioHierarchyApiClient(AsyncBayeslinePortfolioHierarchyApi):
    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("portfoliohierarchy")
        self._settings = AsyncHttpSettingsRegistryClient(
            self._client,
            PortfolioHierarchySettings,
            PortfolioHierarchySettingsMenu,
        )

    @property
    def settings(
        self,
    ) -> AsyncSettingsRegistry[
        PortfolioHierarchySettings, PortfolioHierarchySettingsMenu
    ]:
        return self._settings

    async def load(
        self, ref_or_settings: str | int | PortfolioHierarchySettings
    ) -> AsyncPortfolioHierarchyApi:
        if isinstance(ref_or_settings, PortfolioHierarchySettings):
            settings_menu = await self._settings.available_settings()
            settings_menu.validate_settings(ref_or_settings)
            return AsyncPortfolioHierarchyApiClient(self._client, ref_or_settings)
        else:
            portfoliohierarchy_settings = await self.settings.get(ref_or_settings)
            return AsyncPortfolioHierarchyApiClient(
                self._client,
                portfoliohierarchy_settings,
            )


class AsyncBayeslineEquityPortfolioApiClient(AsyncBayeslineEquityPortfolioApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("portfolio")

    @property
    def name(self) -> str:
        return self._client.sync().get("name").json()

    async def get_id_types(self) -> dict[str, list[IdType]]:
        return (await self._client.get("id-types")).json()

    async def get_coverage(
        self,
        names: str | list[str] | None = None,
        by: Literal["date", "asset"] = "date",
        stats: list[str] | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {"by": str(by)}
        if stats is not None:
            params["stats"] = stats
        response = await self._client.post(
            "coverage",
            params=params,
            json={"names": names},
        )
        if response.status_code == 404:
            raise KeyError(response.json()["detail"])
        elif response.status_code == 400:
            raise ValueError(response.json()["detail"])
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    async def get_portfolio_names(self) -> list[str]:
        response = await self._client.get("names")
        return response.json()

    async def get_portfolio_groups(self) -> dict[str, list[str]]:
        response = await self._client.get("groups")
        return response.json()

    async def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]:
        response = await self._client.post(
            "dates",
            params={"collapse": collapse},
            json={"names": names},
        )
        response_data = response.json()
        if response.status_code == 404:
            raise KeyError(response_data["detail"])
        elif response.status_code == 400:
            raise ValueError(response_data["detail"])
        return {
            p: [pd.to_datetime(d).date() for d in response_data[p]]
            for p in response_data.keys()
        }

    async def get_portfolio(
        self,
        names: str | list[str],
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: str | None = None,
    ) -> pd.DataFrame:
        response = await self._client.post(
            "data",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "id_type": id_type,
            },
            json={"names": names},
        )
        if response.status_code == 404:
            raise KeyError(response.json()["detail"])
        elif response.status_code == 400:
            raise ValueError(response.json()["detail"])
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class BayeslineEquityPortfolioApiClient(BayeslineEquityPortfolioApi):

    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("portfolio")

    @property
    def name(self) -> str:
        return self._client.get("name").json()

    def get_id_types(self) -> dict[str, list[IdType]]:
        return self._client.get("id-types").json()

    def get_coverage(
        self,
        names: str | list[str] | None = None,
        by: Literal["date", "asset"] = "date",
        stats: list[str] | None = None,
    ) -> pd.DataFrame:
        params: dict[str, Any] = {"by": str(by)}
        if stats is not None:
            params["stats"] = stats
        response = self._client.post("coverage", params=params, json={"names": names})
        if response.status_code == 404:
            raise KeyError(response.json()["detail"])
        elif response.status_code == 400:
            raise ValueError(response.json()["detail"])
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")

    def get_portfolio_names(self) -> list[str]:
        response = self._client.get("names")
        return response.json()

    def get_portfolio_groups(self) -> dict[str, list[str]]:
        response = self._client.get("groups")
        return response.json()

    def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]:
        response = self._client.post(
            "dates",
            params={"collapse": collapse},
            json={"names": names},
        )
        response_data = response.json()
        if response.status_code == 404:
            raise KeyError(response_data["detail"])
        elif response.status_code == 400:
            raise ValueError(response_data["detail"])
        return {
            p: [pd.to_datetime(d).date() for d in response_data[p]]
            for p in response_data.keys()
        }

    def get_portfolio(
        self,
        names: str | list[str],
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: str | None = None,
    ) -> pd.DataFrame:
        response = self._client.post(
            "data",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "id_type": id_type,
            },
            json={"names": names},
        )
        if response.status_code == 404:
            raise KeyError(response.json()["detail"])
        elif response.status_code == 400:
            raise ValueError(response.json()["detail"])
        return pd.read_parquet(io.BytesIO(response.content), engine="pyarrow")


class BayeslineEquityApiClient(BayeslineEquityApi):
    def __init__(self, client: ApiClient):
        self._client = client.append_base_path("equity")
        self._universe_client = BayeslineEquityUniverseApiClient(self._client)
        self._exposure_client = BayeslineEquityExposureApiClient(
            self._client,
            self._universe_client,
        )
        self._modelconstruction_client = BayeslineModelConstructionApiClient(
            self._client
        )
        self._factorrisk_client = BayeslineFactorRiskModelsApiClient(
            self._client, self._exposure_client, self._universe_client
        )
        self._portfoliohierarchy_client = BayeslinePortfolioHierarchyApiClient(
            self._client
        )
        self._portfolioreport_client = BayeslinePortfolioReportApiClient(
            self._client,
            self._portfoliohierarchy_client,
        )
        self._byod_client = BayeslineEquityByodApiClient(self._client)
        self._portfolio_client = BayeslineEquityPortfolioApiClient(self._client)

    @property
    def universes(self) -> BayeslineEquityUniverseApi:
        return self._universe_client

    @property
    def exposures(self) -> BayeslineEquityExposureApi:
        return self._exposure_client

    @property
    def modelconstruction(self) -> BayeslineModelConstructionApi:
        return self._modelconstruction_client

    @property
    def riskmodels(self) -> BayeslineFactorRiskModelsApi:
        return self._factorrisk_client

    @property
    def portfolioreport(self) -> BayeslinePortfolioReportApi:
        return self._portfolioreport_client

    @property
    def byod(self) -> BayeslineEquityByodApi:
        return self._byod_client

    @property
    def portfolios(self) -> BayeslineEquityPortfolioApi:
        return self._portfolio_client

    @property
    def portfoliohierarchy(self) -> BayeslinePortfolioHierarchyApi:
        return self._portfoliohierarchy_client


class AsyncBayeslineEquityApiClient(AsyncBayeslineEquityApi):

    def __init__(self, client: AsyncApiClient):
        self._client = client.append_base_path("equity")
        self._universe_client = AsyncBayeslineEquityUniverseApiClient(self._client)

        self._exposure_client = AsyncBayeslineEquityExposureApiClient(
            self._client, self._universe_client
        )
        self._modelconstruction_client = AsyncBayeslineModelConstructionApiClient(
            self._client
        )
        self._factorrisk_client = AsyncBayeslineFactorRiskModelsApiClient(
            self._client, self._exposure_client, self._universe_client
        )
        self._portfoliohierarchy_client = AsyncBayeslinePortfolioHierarchyApiClient(
            self._client
        )
        self._portfolioreport_client = AsyncBayeslinePortfolioReportApiClient(
            self._client,
            self._portfoliohierarchy_client,
        )
        self._byod_client = AsyncBayeslineEquityByodApiClient(self._client)
        self._portfolio_client = AsyncBayeslineEquityPortfolioApiClient(self._client)

    @property
    def universes(self) -> AsyncBayeslineEquityUniverseApi:
        return self._universe_client

    @property
    def exposures(self) -> AsyncBayeslineEquityExposureApi:
        return self._exposure_client

    @property
    def modelconstruction(self) -> AsyncBayeslineModelConstructionApi:
        return self._modelconstruction_client

    @property
    def riskmodels(self) -> AsyncBayeslineFactorRiskModelsApi:
        return self._factorrisk_client

    @property
    def portfolioreport(self) -> AsyncBayeslinePortfolioReportApi:
        return self._portfolioreport_client

    @property
    def byod(self) -> AsyncBayeslineEquityByodApi:
        return self._byod_client

    @property
    def portfolios(self) -> AsyncBayeslineEquityPortfolioApi:
        return self._portfolio_client

    @property
    def portfoliohierarchy(self) -> AsyncBayeslinePortfolioHierarchyApi:
        return self._portfoliohierarchy_client


def _check_and_add_id_type(
    id_types: list[IdType],
    id_type: IdType | None,
    params: dict[str, Any],
) -> None:
    if id_type is not None:
        if id_type not in id_types:
            raise ValueError(f"given id type {id_type} is not supported")
        params["id_type"] = id_type
