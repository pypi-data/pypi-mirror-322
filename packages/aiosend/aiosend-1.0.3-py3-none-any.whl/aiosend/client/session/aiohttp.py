import ssl
from typing import TYPE_CHECKING, cast

import certifi
from aiohttp import ClientSession, TCPConnector
from aiohttp.http import SERVER_SOFTWARE

from aiosend.__meta__ import __version__

from .base import BaseSession

if TYPE_CHECKING:
    import aiosend
    from aiosend.client import APIServer
    from aiosend.methods import CryptoPayMethod
    from aiosend.types import _CryptoPayType


class AiohttpSession(BaseSession):
    """
    Http session based on aiohttp.

    This class is a wrapper of `aiohttp.ClientSession`.
    """

    def __init__(self, api_server: "APIServer") -> None:
        super().__init__(api_server)
        self._session: ClientSession | None = None

    async def request(
        self,
        token: str,
        client: "aiosend.CryptoPay",
        method: "CryptoPayMethod[_CryptoPayType]",
    ) -> "_CryptoPayType":
        """Make http request."""
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._session = ClientSession(
            connector=TCPConnector(
                ssl_context=ssl_context,
            ),
        )
        async with self._session as session:
            resp = await session.post(
                url=self.api_server.url(method),
                data=method.model_dump_json(exclude_none=True),
                headers={
                    "Crypto-Pay-API-Token": token,
                    "Content-Type": "application/json",
                    "User-Agent": f"{SERVER_SOFTWARE} aiosend/{__version__}",
                },
            )
            response = self._check_response(client, method, await resp.text())
        return cast("_CryptoPayType", response.result)
