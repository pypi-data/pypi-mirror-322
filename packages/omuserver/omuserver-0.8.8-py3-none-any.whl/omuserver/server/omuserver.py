import asyncio
import json
import os
import subprocess
import sys

import aiohttp
from aiohttp import web
from loguru import logger
from omu import Identifier
from omu.address import Address
from omu.helper import asyncio_error_logger

from omuserver import __version__
from omuserver.config import Config
from omuserver.directories import Directories
from omuserver.extension.asset import AssetExtension
from omuserver.extension.dashboard import DashboardExtension
from omuserver.extension.endpoint import EndpointExtension
from omuserver.extension.i18n import I18nExtension
from omuserver.extension.logger import LoggerExtension
from omuserver.extension.permission import PermissionExtension
from omuserver.extension.plugin import PluginExtension
from omuserver.extension.registry import RegistryExtension
from omuserver.extension.server import ServerExtension
from omuserver.extension.signal import SignalExtension
from omuserver.extension.table import TableExtension
from omuserver.helper import safe_path_join
from omuserver.network import Network
from omuserver.network.packet_dispatcher import ServerPacketDispatcher
from omuserver.security.security import PermissionManager

from .server import Server, ServerEvents

USER_AGENT_HEADERS = {
    "User-Agent": json.dumps(
        [
            "omu",
            {
                "name": "omuserver",
                "version": __version__,
            },
        ]
    )
}


class OmuServer(Server):
    def __init__(
        self,
        config: Config,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self._config = config
        self._loop = self._set_loop(loop or asyncio.new_event_loop())
        self._address = config.address
        self._event = ServerEvents()
        self._directories = config.directories
        self._directories.mkdir()
        self._packet_dispatcher = ServerPacketDispatcher()
        self._network = Network(self, self._packet_dispatcher)
        self._network.event.start += self._handle_network_start
        self._network.add_http_route("/", self._handle_index)
        self._network.add_http_route("/version", self._handle_version)
        self._network.add_http_route("/proxy", self._handle_proxy)
        self._network.add_http_route("/asset", self._handle_assets)
        self._security = PermissionManager(self)
        self._running = False
        self._endpoints = EndpointExtension(self)
        self._permissions = PermissionExtension(self)
        self._tables = TableExtension(self)
        self._dashboard = DashboardExtension(self)
        self._registries = RegistryExtension(self)
        self._server = ServerExtension(self)
        self._signals = SignalExtension(self)
        self._plugins = PluginExtension(self)
        self._assets = AssetExtension(self)
        self._i18n = I18nExtension(self)
        self._logger = LoggerExtension(self)
        self.client = aiohttp.ClientSession(
            loop=self.loop,
            headers=USER_AGENT_HEADERS,
            timeout=aiohttp.ClientTimeout(total=10),
        )

    def _set_loop(self, loop: asyncio.AbstractEventLoop) -> asyncio.AbstractEventLoop:
        loop = asyncio.new_event_loop()
        loop.set_exception_handler(asyncio_error_logger)
        return loop

    async def _handle_index(self, request: web.Request) -> web.StreamResponse:
        return web.FileResponse(self._directories.index)

    async def _handle_version(self, request: web.Request) -> web.Response:
        return web.json_response(
            {
                "version": __version__,
            }
        )

    async def _handle_proxy(self, request: web.Request) -> web.StreamResponse:
        url = request.query.get("url")
        no_cache = bool(request.query.get("no_cache"))
        if not url:
            return web.Response(status=400)
        try:
            async with self.client.get(
                url,
            ) as resp:
                headers = {
                    "Cache-Control": "no-cache" if no_cache else "max-age=3600",
                    "Content-Type": resp.content_type,
                    "Access-Control-Allow-Origin": "*",
                }
                response = web.StreamResponse(
                    status=resp.status,
                    headers=headers,
                )
                await response.prepare(request)
                try:
                    async for chunk in resp.content.iter_any():
                        await response.write(chunk)
                except ConnectionResetError:
                    pass
                return response
        except TimeoutError:
            return web.Response(status=504)
        except aiohttp.ClientResponseError as e:
            return web.Response(status=e.status, text=e.message)
        except Exception as e:
            logger.opt(exception=e).error("Failed to proxy request")
            return web.Response(status=500)

    async def _handle_assets(self, request: web.Request) -> web.StreamResponse:
        id = request.query.get("id")
        if not id:
            return web.Response(status=400)
        identifier = Identifier.from_key(id)
        path = identifier.get_sanitized_path()
        try:
            path = safe_path_join(self._directories.assets, path)

            if not path.exists():
                return web.Response(status=404)
            return web.FileResponse(path)
        except Exception as e:
            logger.error(e)
            return web.Response(status=500)

    def run(self) -> None:
        async def _run():
            await self.start()

        if self._loop is None:
            asyncio.run(_run())
        else:
            self._loop.create_task(_run())
            self._loop.run_forever()

    async def _handle_network_start(self) -> None:
        logger.info(f"Listening on {self.address.host}:{self.address.port}")
        try:
            await self._event.start()
        except Exception as e:
            await self.stop()
            self.loop.stop()
            raise e

    async def start(self) -> None:
        self._running = True
        try:
            await self._network.start()
        except Exception as e:
            logger.opt(exception=e).error("Failed to start server")
            await self.stop()
            self.loop.stop()
            raise e

    async def stop(self) -> None:
        logger.info("Stopping server")
        self._running = False
        await self._event.stop()
        await self.network.stop()

    async def restart(self) -> None:
        await self.stop()
        child = subprocess.Popen(
            args=[sys.executable, "-m", "omuserver", *sys.argv[1:]],
            cwd=os.getcwd(),
        )
        logger.info(f"Restarting server with PID {child.pid}")
        os._exit(0)

    @property
    def config(self) -> Config:
        return self._config

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def address(self) -> Address:
        return self._address

    @property
    def permission_manager(self) -> PermissionManager:
        return self._security

    @property
    def directories(self) -> Directories:
        return self._directories

    @property
    def network(self) -> Network:
        return self._network

    @property
    def packet_dispatcher(self) -> ServerPacketDispatcher:
        return self._packet_dispatcher

    @property
    def endpoints(self):
        return self._endpoints

    @property
    def permissions(self):
        return self._permissions

    @property
    def tables(self):
        return self._tables

    @property
    def dashboard(self):
        return self._dashboard

    @property
    def registries(self):
        return self._registries

    @property
    def server(self):
        return self._server

    @property
    def signals(self):
        return self._signals

    @property
    def plugins(self):
        return self._plugins

    @property
    def assets(self):
        return self._assets

    @property
    def i18n(self):
        return self._i18n

    @property
    def logger(self):
        return self._logger

    @property
    def running(self) -> bool:
        return self._running

    @property
    def event(self) -> ServerEvents:
        return self._event
