"""Asynchronous Python client for Peblar EV chargers."""

from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

import backoff
import orjson
from aiohttp import ClientResponseError, CookieJar, hdrs
from aiohttp.client import ClientError, ClientSession
from yarl import URL

from .exceptions import (
    PeblarAuthenticationError,
    PeblarConnectionError,
    PeblarConnectionTimeoutError,
    PeblarError,
)
from .models import (
    BaseModel,
    PeblarApiToken,
    PeblarEVInterface,
    PeblarEVInterfaceChange,
    PeblarHealth,
    PeblarLocalRestApiAccess,
    PeblarLogin,
    PeblarMeter,
    PeblarModbusApiAccess,
    PeblarReboot,
    PeblarSmartCharging,
    PeblarSystem,
    PeblarSystemInformation,
    PeblarUpdate,
    PeblarUserConfiguration,
    PeblarVersions,
)

if TYPE_CHECKING:
    from peblar.const import AccessMode, PackageType, SmartChargingMode


@dataclass(kw_only=True)
class Peblar:
    """Main class for handling connections with a Peblar EV chargers."""

    host: str
    request_timeout: float = 8
    session: ClientSession | None = None

    _close_session: bool = False

    def __post_init__(self) -> None:
        """Initialize the Peblar object."""
        self.url = URL.build(scheme="http", host=self.host, path="/api/v1/")

    @backoff.on_exception(
        backoff.expo,
        PeblarConnectionError,
        max_tries=3,
        logger=None,
    )
    async def request(
        self,
        uri: URL,
        *,
        method: str = hdrs.METH_GET,
        data: BaseModel | None = None,
    ) -> str:
        """Handle a request to a Peblar charger."""
        if self.session is None:
            self.session = ClientSession(
                cookie_jar=CookieJar(unsafe=True),
                json_serialize=orjson.dumps,  # type: ignore[arg-type]
            )
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method=method,
                    url=self.url.join(uri),
                    headers={"Content-Type": "application/json"},
                    data=data.to_json() if data else None,
                )
                response.raise_for_status()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Peblar charger"
            raise PeblarConnectionTimeoutError(msg) from exception
        except ClientResponseError as exception:
            if exception.status == 401:
                msg = "Authentication error. Provided password is invalid."
                raise PeblarAuthenticationError(msg) from exception
            msg = "Error occurred while communicating to the Peblar charger"
            raise PeblarError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating to the Peblar charger"
            raise PeblarConnectionError(msg) from exception

        return await response.text()

    async def login(self, *, password: str) -> None:
        """Login into the Peblar charger."""
        await self.request(
            URL("auth/login"),
            method=hdrs.METH_POST,
            data=PeblarLogin(
                password=password,
            ),
        )

    async def rest_api(
        self,
        *,
        enable: bool | None = None,
        access_mode: AccessMode | None = None,
    ) -> PeblarApi:
        """Get and control access to the REST API."""
        user = await self.user_configuration()
        if not user.local_rest_api_allowed:
            msg = "The use of the local REST API is not allowed for this device."
            raise PeblarError(msg)

        if enable is not None and user.local_rest_api_enabled == enable:
            enable = None

        if access_mode is not None and user.local_rest_api_access_mode == access_mode:
            access_mode = None

        if enable is not None or access_mode:
            await self.request(
                URL("config/user"),
                method=hdrs.METH_PATCH,
                data=PeblarLocalRestApiAccess(enabled=enable, access_mode=access_mode),
            )
            if enable is not None:
                user.local_rest_api_enabled = enable

        if not user.local_rest_api_enabled:
            msg = "The local REST API is not enabled for this device."
            raise PeblarError(msg)

        return PeblarApi(host=self.host, token=await self.api_token())

    async def modbus_api(
        self,
        *,
        enable: bool | None = None,
        access_mode: AccessMode | None = None,
    ) -> None:
        """Control access to the Modbus API."""
        user = await self.user_configuration()
        if not user.modbus_server_allowed:
            msg = "The use of the Modbus API is not allowed for this device."
            raise PeblarError(msg)

        if user.modbus_server_enabled == enable:
            enable = None

        if user.modbus_server_access_mode == access_mode:
            access_mode = None

        if enable is not None or access_mode:
            await self.request(
                URL("config/user"),
                method=hdrs.METH_PATCH,
                data=PeblarModbusApiAccess(enabled=enable, access_mode=access_mode),
            )

    async def api_token(self, *, generate_new_api_token: bool = False) -> str:
        """Get the API token."""
        url = URL("config/api-token")

        if generate_new_api_token:
            await self.request(url, method=hdrs.METH_POST)

        result = await self.request(url)
        return PeblarApiToken.from_json(result).api_token

    async def available_versions(self) -> PeblarVersions:
        """Get available versions."""
        result = await self.request(
            URL("system/software/automatic-update/available-versions")
        )
        return PeblarVersions.from_json(result)

    async def current_versions(self) -> PeblarVersions:
        """Get current versions."""
        result = await self.request(
            URL("system/software/automatic-update/current-versions")
        )
        return PeblarVersions.from_json(result)

    async def smart_charging(self, smart_charging_mode: SmartChargingMode) -> None:
        """Enable or disable smart charging."""
        await self.request(
            URL("config/user"),
            method=hdrs.METH_PATCH,
            data=PeblarSmartCharging(smart_charging=smart_charging_mode),
        )

    async def identify(self) -> None:
        """Identify the Peblar charger."""
        await self.request(URL("system/identify"), method=hdrs.METH_PUT)

    async def reboot(self) -> None:
        """Reboot the Peblar charger."""
        await self.request(
            URL("system/reboot"),
            method=hdrs.METH_POST,
            data=PeblarReboot(),
        )

    async def update(self, *, package_type: PackageType) -> None:
        """Update the Peblar charger to the latest version."""
        await self.request(
            URL("system/software/automatic-update/update"),
            method=hdrs.METH_POST,
            data=PeblarUpdate(package_type=package_type),
        )

    async def system_information(self) -> PeblarSystemInformation:
        """Get information about the Peblar charger."""
        result = await self.request(URL("system/info"))
        return PeblarSystemInformation.from_json(result)

    async def user_configuration(self) -> PeblarUserConfiguration:
        """Get information about the user configuration."""
        result = await self.request(URL("config/user"))
        return PeblarUserConfiguration.from_json(result)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The Peblar object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()


@dataclass(kw_only=True)
class PeblarApi:
    """Main class for handling connections with the Local Peblar REST API."""

    host: str
    token: str
    request_timeout: float = 8
    session: ClientSession | None = None

    _close_session: bool = False

    def __post_init__(self) -> None:
        """Initialize the Peblar object."""
        self.url = URL.build(scheme="http", host=self.host, path="/api/wlac/v1/")

    @backoff.on_exception(
        backoff.expo,
        PeblarConnectionError,
        max_tries=3,
        logger=None,
    )
    async def request(
        self,
        uri: URL,
        *,
        method: str = hdrs.METH_GET,
        data: BaseModel | None = None,
    ) -> str:
        """Handle a request to a Peblar charger Local REST API."""
        if self.session is None:
            self.session = ClientSession(
                json_serialize=orjson.dumps,  # type: ignore[arg-type]
            )
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method=method,
                    url=self.url.join(uri),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": self.token,
                    },
                    data=data.to_json() if data else None,
                )
                response.raise_for_status()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Peblar charger API"
            raise PeblarConnectionTimeoutError(msg) from exception
        except ClientResponseError as exception:
            if exception.status == 401:
                msg = "Authentication error. Provided password is invalid."
                raise PeblarAuthenticationError(msg) from exception
            msg = "Error occurred while communicating to the Peblar charger API"
            raise PeblarError(msg) from exception
        except (
            ClientError,
            socket.gaierror,
        ) as exception:
            msg = "Error occurred while communicating to the Peblar charger API"
            raise PeblarConnectionError(msg) from exception

        return await response.text()

    async def ev_interface(
        self,
        *,
        charge_current_limit: int | None = None,
        force_single_phase: bool | None = None,
    ) -> PeblarEVInterface:
        """Get information about the EV interface."""
        url = URL("evinterface")
        if charge_current_limit is not None or force_single_phase is not None:
            await self.request(
                url,
                method=hdrs.METH_PATCH,
                data=PeblarEVInterfaceChange(
                    charge_current_limit=charge_current_limit,
                    force_single_phase=force_single_phase,
                ),
            )

        result = await self.request(url)
        return PeblarEVInterface.from_json(result)

    async def health(self) -> PeblarHealth:
        """Get health information from the Peblar API."""
        result = await self.request(URL("health"))
        return PeblarHealth.from_json(result)

    async def meter(self) -> PeblarMeter:
        """Get meter information from the Peblar API."""
        result = await self.request(URL("meter"))
        return PeblarMeter.from_json(result)

    async def system(self) -> PeblarSystem:
        """Get system information from the Peblar API."""
        result = await self.request(URL("system"))
        return PeblarSystem.from_json(result)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The PeblarApi object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
