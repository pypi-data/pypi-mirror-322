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
from satstream_python_sdk.api.psbts_api import PSBTsApi  # noqa: E501
from satstream_python_sdk.rest import ApiException


class TestPSBTsApi(unittest.TestCase):
    """PSBTsApi unit test stubs"""

    def setUp(self):
        self.api = PSBTsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_analyze_psbt(self):
        """Test case for analyze_psbt

        Analyze PSBT  # noqa: E501
        """
        pass

    def test_combine_psbt(self):
        """Test case for combine_psbt

        Combine PSBTs  # noqa: E501
        """
        pass

    def test_create_psbt(self):
        """Test case for create_psbt

        Create PSBT  # noqa: E501
        """
        pass

    def test_decode_psbt(self):
        """Test case for decode_psbt

        Decode PSBT  # noqa: E501
        """
        pass

    def test_join_psbts(self):
        """Test case for join_psbts

        Join PSBTs  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
