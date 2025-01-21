# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton model config
"""
import unittest


class TestModelConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.config_file_path = "./data/config.pbtxt"

    def test_create_from_text(self):
        """
        test create from text
        """
        from tritonv2.model_config import ModelConfig

        with open(self.config_file_path, "r") as f:
            config_text = f.read()
        config = ModelConfig.create_from_text(config_text)
        self.assertEqual(config.as_dict()["name"], "avi_ocrnet")

    def test_create_from_file(self):
        """
        test create from file
        """
        from tritonv2.model_config import ModelConfig
        from tritonv2.utils import BlobStoreFactory

        bs = BlobStoreFactory.create(kind="local", bucket="data", endpoint_url="./")
        config = ModelConfig.create_from_file(self.config_file_path, bs)
        self.assertEqual(config.as_dict()["name"], "avi_ocrnet")

    def test_set_model_input_field(self):
        """
        test set model input field
        """
        from tritonv2.model_config import ModelConfig
        from tritonv2.utils import BlobStoreFactory

        bs = BlobStoreFactory.create(kind="local", bucket="data", endpoint_url="./")
        config = ModelConfig.create_from_file(self.config_file_path, bs)
        config.set_model_input_field("x", "dims", [1, 3, 512, 512])
        config.write_to_file("./data/config_modify_input.pbtxt", bs)

    def test_set_model_output_field(self):
        """
        test set model output field
        """
        from tritonv2.model_config import ModelConfig
        from tritonv2.utils import BlobStoreFactory

        bs = BlobStoreFactory.create(kind="local", bucket="data", endpoint_url="./")
        config = ModelConfig.create_from_file(self.config_file_path, bs)
        config.set_model_output_field("argmax_0.tmp_0", "dims", [1, 3, 512, 512])
        config.write_to_file("./data/config_modify_output.pbtxt", bs)

    def test_set_model_field(self):
        """
        test set model field
        """
        from tritonv2.model_config import ModelConfig
        from tritonv2.utils import BlobStoreFactory

        bs = BlobStoreFactory.create(kind="local", bucket="data", endpoint_url="./")
        config = ModelConfig.create_from_file(self.config_file_path, bs)
        config.set_model_input_field("x", "dims", [1, 3, 512, 512])
        config.set_model_output_field("argmax_0.tmp_0", "dims", [1, 900, 900])
        config.write_to_file("./data/config_modify_field.pbtxt", bs)
