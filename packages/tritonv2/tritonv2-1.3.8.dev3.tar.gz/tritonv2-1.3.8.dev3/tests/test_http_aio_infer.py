# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton http client test
"""
import unittest
from unittest.mock import patch, MagicMock, Mock
from time import sleep
from time import time
from geventhttpclient.response import HTTPSocketResponse

from tritonv2.client_factory import TritonClientFactory
from tritonv2.constants import LimiterConfig, RequestRateDuration
from tritonv2.exceptions import TritonClientException


class TestTritonAioHTTPClient(unittest.TestCase):
    @patch(
        "geventhttpclient.response.HTTPSocketResponse._read_headers",
        MagicMock(return_value=None),
    )
    def setUp(self) -> None:
        self.response = HTTPSocketResponse("dummy_sock")

    @patch(
        "tritonclient.http.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    async def test_server_live_without_limiter(self):
        """
        Verify that client without limiter config works
        """

        url = "dummy_url"
        async with TritonClientFactory.create_http_aio_client(
            server_url=url,
        ) as client:
            self.assertEqual(client.server_live(), True)

    @patch(
        "tritonclient.http.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    async def test_server_live_with_limiter(self):
        """
        Verify that client with limiter config works
        """

        url = "dummy_url"
        async with TritonClientFactory.create_http_aio_client(
            server_url=url,
            limiter_config=LimiterConfig(
                limit=1, interval=RequestRateDuration.SECOND, delay=True
            ),
        ) as client:
            self.assertEqual(client.server_live(), True)

    @patch(
        "tritonclient.http.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    async def test_server_live_with_0_limiter(self):
        """
        Verify that client with limiter config works
        """

        url = "dummy_url"
        async with TritonClientFactory.create_http_aio_client(
            server_url=url,
            limiter_config=LimiterConfig(
                limit=0, interval=RequestRateDuration.SECOND, delay=False
            ),
        ) as client:
            # Bucket for 85290822e1d84d369ddd391da12c37c9 with Rate 0/1 is already full
            with self.assertRaises(TritonClientException):
                client.server_live()

    @patch(
        "tritonclient.http.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    async def test_server_live_with_limiter_perf(self):
        """
        Verify that client with limiter config works with perf
        """

        url = "dummy_url"
        async with TritonClientFactory.create_http_aio_client(
            server_url=url,
            limiter_config=LimiterConfig(
                limit=6, interval=5 * RequestRateDuration.SECOND, delay=False
            ),
        ) as client:
            track_sleep = Mock(
                side_effect=sleep
            )  # run time.sleep() and track the number of calls
            start = time()
            for i in range(10):
                try:
                    client.server_live()
                    print(f"[{time() - start:07.4f}] Pushed: {i + 1} items")
                except Exception as err:
                    print(f"[{time() - start:07.4f}] Error: {err}")
                    track_sleep(0.1)

            print(f"Elapsed: {time() - start:07.4f} seconds")
            assert track_sleep.call_count == 4

    @patch(
        "tritonclient.http.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    async def test_server_live_without_limiter_perf(self):
        """
        Verify that client with limiter config works with perf
        """

        url = "dummy_url"
        async with TritonClientFactory.create_http_aio_client(
            server_url=url,
        ) as client:
            track_sleep = Mock(
                side_effect=sleep
            )  # run time.sleep() and track the number of calls
            start = time()
            for i in range(10):
                try:
                    client.server_live()
                    print(f"[{time() - start:07.4f}] Pushed: {i + 1} items")
                except Exception as err:
                    print(f"[{time() - start:07.4f}] Error: {err}")
                    track_sleep(0.1)

            print(f"Elapsed: {time() - start:07.4f} seconds")
            assert track_sleep.call_count == 0
