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
from fluid.models.juice_fs_comp_template_spec import JuiceFSCompTemplateSpec  # noqa: E501
from fluid.rest import ApiException

class TestJuiceFSCompTemplateSpec(unittest.TestCase):
    """JuiceFSCompTemplateSpec unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test JuiceFSCompTemplateSpec
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = fluid.models.juice_fs_comp_template_spec.JuiceFSCompTemplateSpec()  # noqa: E501
        if include_optional :
            return JuiceFSCompTemplateSpec(
                enabled = True, 
                env = [
                    None
                    ], 
                network_mode = '0', 
                node_selector = {
                    'key' : '0'
                    }, 
                options = {
                    'key' : '0'
                    }, 
                pod_metadata = fluid.models./pod_metadata..PodMetadata(
                    annotations = {
                        'key' : '0'
                        }, 
                    labels = {
                        'key' : '0'
                        }, ), 
                ports = [
                    None
                    ], 
                replicas = 56, 
                resources = None, 
                volume_mounts = [
                    None
                    ]
            )
        else :
            return JuiceFSCompTemplateSpec(
        )

    def testJuiceFSCompTemplateSpec(self):
        """Test JuiceFSCompTemplateSpec"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
