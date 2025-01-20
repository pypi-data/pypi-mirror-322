# coding: utf-8

"""
    fluid

    client for fluid  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import fluid
from fluid.models.client_metrics import ClientMetrics  # noqa: E501
from fluid.rest import ApiException

class TestClientMetrics(unittest.TestCase):
    """ClientMetrics unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ClientMetrics
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = fluid.models.client_metrics.ClientMetrics()  # noqa: E501
        if include_optional :
            return ClientMetrics(
                enabled = True, 
                scrape_target = '0'
            )
        else :
            return ClientMetrics(
        )

    def testClientMetrics(self):
        """Test ClientMetrics"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
