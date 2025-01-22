import asyncio
import atexit
import json
import os
import threading

import aiohttp
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from maitai_common.version import version


def _get_aws_instance_metadata(url, timeout=2):
    try:
        token_url = "http://169.254.169.254/latest/api/token"
        token_headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        token_response = requests.put(token_url, headers=token_headers, timeout=timeout)

        if token_response.status_code == 200:
            token = token_response.text
            headers = {"X-aws-ec2-metadata-token": token}
        else:
            headers = None

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def _get_gcp_instance_metadata(url, timeout=2):
    try:
        headers = {"Metadata-Flavor": "Google"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def _get_azure_instance_metadata(timeout=2):
    try:
        headers = {"Metadata": "true"}
        url = "http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01"
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data.get("location")
    except requests.RequestException:
        return None


def _determine_maitai_host():
    if maitai_host := os.environ.get("MAITAI_HOST"):
        return maitai_host.rstrip("/")

    if (
        _get_aws_instance_metadata(
            "http://169.254.169.254/latest/meta-data/placement/region"
        )
        == "us-west-2"
    ):
        return "https://api.aws.us-west-2.trymaitai.ai"

    gcp_zone = _get_gcp_instance_metadata(
        "http://metadata.google.internal/computeMetadata/v1/instance/zone"
    )
    if gcp_zone:
        if "us-west1" in gcp_zone:
            return "https://api.gcp.us-west1.trymaitai.ai"
        elif "us-central1" in gcp_zone:
            return "https://api.gcp.us-central1.trymaitai.ai"

    azure_region = _get_azure_instance_metadata()
    if azure_region == "westus2":
        return "https://api.azure.westus2.trymaitai.ai"

    return "https://api.trymaitai.ai"


class MaitaiClient:
    _session = None
    _async_session = None
    maitai_host = _determine_maitai_host()
    _loop = asyncio.new_event_loop()
    _thr = threading.Thread(
        target=_loop.run_forever, name="Maitai Async Runner", daemon=True
    )

    def __init__(self):
        super().__init__()
        atexit.register(self.cleanup)

    def cleanup(self):
        try:
            if self._loop.is_running():
                self._loop.run_until_complete(self.close_async_session())
        except Exception as e:
            pass
        try:
            self.close_session()
        except Exception as e:
            pass
        if self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thr.is_alive():
            self._thr.join()

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls._session = requests.Session()
            retries = Retry(
                total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504]
            )
            cls._session.mount(
                "http://",
                HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=100),
            )
            cls._session.mount(
                "https://",
                HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=100),
            )
        return cls._session

    @classmethod
    def close_session(cls):
        if cls._session:
            cls._session.close()
            cls._session = None

    @classmethod
    async def close_async_session(cls):
        if cls._async_session:
            await cls._async_session.close()
            cls._async_session = None

    def __del__(self):
        self.cleanup()

    @classmethod
    def run_async(cls, coro):
        """
        Modified helper method to run coroutine in a background thread if not already in an asyncio loop,
        otherwise just run it. This allows for both asyncio and non-asyncio applications to use this method.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # No running event loop
            loop = None

        if loop and loop.is_running():
            # We are in an asyncio loop, schedule coroutine execution
            asyncio.create_task(coro, name="maitai")
        else:
            # Not in an asyncio loop, run in a new event loop in a background thread
            def run():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                new_loop.run_until_complete(coro)
                new_loop.close()

            threading.Thread(target=run).start()

    @classmethod
    def run_async_with_result(cls, coro):
        if not cls._thr.is_alive():
            cls._thr.start()
        future = asyncio.run_coroutine_threadsafe(coro, cls._loop)
        return future.result()

    @classmethod
    def log_error(cls, api_key: str, error: str, path: str):
        cls.run_async_with_result(cls.increment_error(api_key, error, path))

    @classmethod
    async def increment_error(cls, api_key: str, error: str, path: str):
        host = cls.maitai_host
        url = f"{host}/metrics/increment/python_sdk_error"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "x-client-version": version,
        }
        labels = {
            "cause": error,
            "type": "ERROR",
            "path": path,
        }
        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)
            ) as session:
                return await session.put(url, headers=headers, data=json.dumps(labels))
        except:
            pass

    @classmethod
    def init_sdk(cls, api_key: str, host: str, use_async: bool = False):
        """Initialize the SDK by making a request to /config/init_sdk"""
        url = f"{host}/config/init_sdk"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "x-client-version": version,
        }

        if use_async:
            if cls._async_session is None:

                async def init_async():
                    cls._async_session = aiohttp.ClientSession(
                        connector=aiohttp.TCPConnector(
                            ssl=False,
                            limit=100,
                            keepalive_timeout=300,  # 5 minutes keepalive
                            force_close=False,
                        )
                    )
                    async with cls._async_session.get(
                        url, headers=headers, timeout=15
                    ) as response:
                        if response.status != 200:
                            raise Exception(
                                f"Failed to initialize Maitai client: {await response.text()}"
                            )
                        return await response.json()

                return cls.run_async_with_result(init_async())
        else:
            session = cls.get_session()
            response = session.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                raise Exception(f"Failed to initialize Maitai client: {response.text}")
            return response.json()
