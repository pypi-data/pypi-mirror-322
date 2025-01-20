# coding: utf-8

"""
    Satstream API

    Satstream API  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: team@satstream.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import satstream_python_sdk
from satstream_python_sdk.api.mempool_api import MempoolApi  # noqa: E501
from satstream_python_sdk.rest import ApiException


class TestMempoolApi(unittest.TestCase):
    """MempoolApi unit test stubs"""

    def setUp(self):
        self.api = MempoolApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_mempool_ancestors(self):
        """Test case for get_mempool_ancestors

        Get mempool ancestors  # noqa: E501
        """
        pass

    def test_get_mempool_descendants(self):
        """Test case for get_mempool_descendants

        Get mempool descendants  # noqa: E501
        """
        pass

    def test_get_mempool_info(self):
        """Test case for get_mempool_info

        Get mempool information  # noqa: E501
        """
        pass

    def test_get_raw_mempool(self):
        """Test case for get_raw_mempool

        Get raw mempool  # noqa: E501
        """
        pass

    def test_test_mempool_accept(self):
        """Test case for test_mempool_accept

        Test mempool accept  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
