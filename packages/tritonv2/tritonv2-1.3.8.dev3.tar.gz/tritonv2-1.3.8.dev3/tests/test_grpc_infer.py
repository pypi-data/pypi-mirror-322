# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton grpc client test
"""
import unittest
from unittest.mock import patch, MagicMock, Mock
from time import sleep
from time import time
from tritonv2.client_factory import TritonClientFactory
from tritonv2.constants import LimiterConfig, RequestRateDuration
from tritonv2.exceptions import TritonClientException


class TestTritonGRPCClient(unittest.TestCase):

    @patch(
        "tritonclient.grpc.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    def test_server_live_without_limiter(self):
        """
        Verify that client without limiter config works
        """

        url = "dummy_url"
        self.client = TritonClientFactory.create_grpc_client(
            server_url=url,
        )
        self.assertEqual(self.client.server_live(), True)

    @patch(
        "tritonclient.grpc.InferenceServerClient.is_server_live",
        MagicMock(return_value=True),
    )
    def test_server_live_with_limiter(self):
        """
        Verify that client with limiter config works
        """

        url = "dummy_url"
        self.client = TritonClientFactory.create_grpc_client(
            server_url=url,
            limiter_config=LimiterConfig(
                limit=1, interval=RequestRateDuration.SECOND, delay=True
            ),
        )
        self.assertEqual(self.client.server_live(), True)

    def test_server_live_with_0_limiter(self):
        """
        Verify that client with limiter config works
        """

        url = "dummy_url"
        limiter_config = LimiterConfig(
            limit=0, interval=RequestRateDuration.SECOND, delay=False
        )
        self.client = TritonClientFactory.create_grpc_client(
            server_url=url,
            limiter_config=limiter_config,
        )
        # Bucket for 85290822e1d84d369ddd391da12c37c9 with Rate 0/1 is already full
        with self.assertRaises(TritonClientException):
            self.client.server_live()

    def test_server_live_with_limiter_perf(self):
        """
        Verify that client with limiter config works with perf
        """

        url = "dummy_url"
        self.client = TritonClientFactory.create_grpc_client(
            server_url=url,
            limiter_config=LimiterConfig(
                limit=6, interval=5 * RequestRateDuration.SECOND, delay=False
            ),
        )
        track_sleep = Mock(
            side_effect=sleep
        )  # run time.sleep() and track the number of calls
        start = time()
        for i in range(10):
            try:
                self.client.server_live()
                print(f"[{time() - start:07.4f}] Pushed: {i + 1} items")
            except Exception as err:
                print(f"[{time() - start:07.4f}] Error: {err}")
                if "Bucket for" in str(err):
                    track_sleep(0.1)

        print(f"Elapsed: {time() - start:07.4f} seconds")
        assert track_sleep.call_count == 4

    def test_server_live_without_limiter_perf(self):
        """
        Verify that client with limiter config works with perf
        """

        url = "dummy_url"
        self.client = TritonClientFactory.create_grpc_client(
            server_url=url,
        )
        track_sleep = Mock(
            side_effect=sleep
        )  # run time.sleep() and track the number of calls
        start = time()
        for i in range(10):
            try:
                self.client.server_live()
                print(f"[{time() - start:07.4f}] Pushed: {i + 1} items")
            except Exception as err:
                print(f"[{time() - start:07.4f}] Error: {err}")
                if "Bucket for" in str(err):
                    track_sleep(0.1)

        print(f"Elapsed: {time() - start:07.4f} seconds")
        assert track_sleep.call_count == 0
