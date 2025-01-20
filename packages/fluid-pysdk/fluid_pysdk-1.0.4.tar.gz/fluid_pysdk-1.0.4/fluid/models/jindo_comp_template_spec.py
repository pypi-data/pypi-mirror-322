# coding: utf-8

"""
    fluid

    client for fluid  # noqa: E501

    The version of the OpenAPI document: v0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from fluid.configuration import Configuration


class JindoCompTemplateSpec(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'disabled': 'bool',
        'env': 'dict(str, str)',
        'image_pull_secrets': 'list[V1LocalObjectReference]',
        'labels': 'dict(str, str)',
        'node_selector': 'dict(str, str)',
        'pod_metadata': 'PodMetadata',
        'ports': 'dict(str, int)',
        'properties': 'dict(str, str)',
        'replicas': 'int',
        'resources': 'V1ResourceRequirements',
        'tolerations': 'list[V1Toleration]',
        'volume_mounts': 'list[V1VolumeMount]'
    }

    attribute_map = {
        'disabled': 'disabled',
        'env': 'env',
        'image_pull_secrets': 'imagePullSecrets',
        'labels': 'labels',
        'node_selector': 'nodeSelector',
        'pod_metadata': 'podMetadata',
        'ports': 'ports',
        'properties': 'properties',
        'replicas': 'replicas',
        'resources': 'resources',
        'tolerations': 'tolerations',
        'volume_mounts': 'volumeMounts'
    }

    def __init__(self, disabled=None, env=None, image_pull_secrets=None, labels=None, node_selector=None, pod_metadata=None, ports=None, properties=None, replicas=None, resources=None, tolerations=None, volume_mounts=None, local_vars_configuration=None):  # noqa: E501
        """JindoCompTemplateSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._disabled = None
        self._env = None
        self._image_pull_secrets = None
        self._labels = None
        self._node_selector = None
        self._pod_metadata = None
        self._ports = None
        self._properties = None
        self._replicas = None
        self._resources = None
        self._tolerations = None
        self._volume_mounts = None
        self.discriminator = None

        if disabled is not None:
            self.disabled = disabled
        if env is not None:
            self.env = env
        if image_pull_secrets is not None:
            self.image_pull_secrets = image_pull_secrets
        if labels is not None:
            self.labels = labels
        if node_selector is not None:
            self.node_selector = node_selector
        if pod_metadata is not None:
            self.pod_metadata = pod_metadata
        if ports is not None:
            self.ports = ports
        if properties is not None:
            self.properties = properties
        if replicas is not None:
            self.replicas = replicas
        if resources is not None:
            self.resources = resources
        if tolerations is not None:
            self.tolerations = tolerations
        if volume_mounts is not None:
            self.volume_mounts = volume_mounts

    @property
    def disabled(self):
        """Gets the disabled of this JindoCompTemplateSpec.  # noqa: E501

        If disable JindoFS master or worker  # noqa: E501

        :return: The disabled of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this JindoCompTemplateSpec.

        If disable JindoFS master or worker  # noqa: E501

        :param disabled: The disabled of this JindoCompTemplateSpec.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled

    @property
    def env(self):
        """Gets the env of this JindoCompTemplateSpec.  # noqa: E501

        Environment variables that will be used by Jindo component. <br>  # noqa: E501

        :return: The env of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._env

    @env.setter
    def env(self, env):
        """Sets the env of this JindoCompTemplateSpec.

        Environment variables that will be used by Jindo component. <br>  # noqa: E501

        :param env: The env of this JindoCompTemplateSpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._env = env

    @property
    def image_pull_secrets(self):
        """Gets the image_pull_secrets of this JindoCompTemplateSpec.  # noqa: E501

        ImagePullSecrets that will be used to pull images  # noqa: E501

        :return: The image_pull_secrets of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: list[V1LocalObjectReference]
        """
        return self._image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, image_pull_secrets):
        """Sets the image_pull_secrets of this JindoCompTemplateSpec.

        ImagePullSecrets that will be used to pull images  # noqa: E501

        :param image_pull_secrets: The image_pull_secrets of this JindoCompTemplateSpec.  # noqa: E501
        :type: list[V1LocalObjectReference]
        """

        self._image_pull_secrets = image_pull_secrets

    @property
    def labels(self):
        """Gets the labels of this JindoCompTemplateSpec.  # noqa: E501

        Labels will be added on JindoFS Master or Worker pods. DEPRECATED: This is a deprecated field. Please use PodMetadata instead. Note: this field is set to be exclusive with PodMetadata.Labels  # noqa: E501

        :return: The labels of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this JindoCompTemplateSpec.

        Labels will be added on JindoFS Master or Worker pods. DEPRECATED: This is a deprecated field. Please use PodMetadata instead. Note: this field is set to be exclusive with PodMetadata.Labels  # noqa: E501

        :param labels: The labels of this JindoCompTemplateSpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._labels = labels

    @property
    def node_selector(self):
        """Gets the node_selector of this JindoCompTemplateSpec.  # noqa: E501

        NodeSelector is a selector which must be true for the master to fit on a node  # noqa: E501

        :return: The node_selector of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._node_selector

    @node_selector.setter
    def node_selector(self, node_selector):
        """Sets the node_selector of this JindoCompTemplateSpec.

        NodeSelector is a selector which must be true for the master to fit on a node  # noqa: E501

        :param node_selector: The node_selector of this JindoCompTemplateSpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._node_selector = node_selector

    @property
    def pod_metadata(self):
        """Gets the pod_metadata of this JindoCompTemplateSpec.  # noqa: E501


        :return: The pod_metadata of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: PodMetadata
        """
        return self._pod_metadata

    @pod_metadata.setter
    def pod_metadata(self, pod_metadata):
        """Sets the pod_metadata of this JindoCompTemplateSpec.


        :param pod_metadata: The pod_metadata of this JindoCompTemplateSpec.  # noqa: E501
        :type: PodMetadata
        """

        self._pod_metadata = pod_metadata

    @property
    def ports(self):
        """Gets the ports of this JindoCompTemplateSpec.  # noqa: E501


        :return: The ports of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: dict(str, int)
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this JindoCompTemplateSpec.


        :param ports: The ports of this JindoCompTemplateSpec.  # noqa: E501
        :type: dict(str, int)
        """

        self._ports = ports

    @property
    def properties(self):
        """Gets the properties of this JindoCompTemplateSpec.  # noqa: E501

        Configurable properties for the Jindo component. <br>  # noqa: E501

        :return: The properties of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this JindoCompTemplateSpec.

        Configurable properties for the Jindo component. <br>  # noqa: E501

        :param properties: The properties of this JindoCompTemplateSpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def replicas(self):
        """Gets the replicas of this JindoCompTemplateSpec.  # noqa: E501

        Replicas is the desired number of replicas of the given template. If unspecified, defaults to 1. replicas is the min replicas of dataset in the cluster  # noqa: E501

        :return: The replicas of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this JindoCompTemplateSpec.

        Replicas is the desired number of replicas of the given template. If unspecified, defaults to 1. replicas is the min replicas of dataset in the cluster  # noqa: E501

        :param replicas: The replicas of this JindoCompTemplateSpec.  # noqa: E501
        :type: int
        """

        self._replicas = replicas

    @property
    def resources(self):
        """Gets the resources of this JindoCompTemplateSpec.  # noqa: E501


        :return: The resources of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: V1ResourceRequirements
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this JindoCompTemplateSpec.


        :param resources: The resources of this JindoCompTemplateSpec.  # noqa: E501
        :type: V1ResourceRequirements
        """

        self._resources = resources

    @property
    def tolerations(self):
        """Gets the tolerations of this JindoCompTemplateSpec.  # noqa: E501

        If specified, the pod's tolerations.  # noqa: E501

        :return: The tolerations of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: list[V1Toleration]
        """
        return self._tolerations

    @tolerations.setter
    def tolerations(self, tolerations):
        """Sets the tolerations of this JindoCompTemplateSpec.

        If specified, the pod's tolerations.  # noqa: E501

        :param tolerations: The tolerations of this JindoCompTemplateSpec.  # noqa: E501
        :type: list[V1Toleration]
        """

        self._tolerations = tolerations

    @property
    def volume_mounts(self):
        """Gets the volume_mounts of this JindoCompTemplateSpec.  # noqa: E501

        VolumeMounts specifies the volumes listed in \".spec.volumes\" to mount into the jindo runtime component's filesystem.  # noqa: E501

        :return: The volume_mounts of this JindoCompTemplateSpec.  # noqa: E501
        :rtype: list[V1VolumeMount]
        """
        return self._volume_mounts

    @volume_mounts.setter
    def volume_mounts(self, volume_mounts):
        """Sets the volume_mounts of this JindoCompTemplateSpec.

        VolumeMounts specifies the volumes listed in \".spec.volumes\" to mount into the jindo runtime component's filesystem.  # noqa: E501

        :param volume_mounts: The volume_mounts of this JindoCompTemplateSpec.  # noqa: E501
        :type: list[V1VolumeMount]
        """

        self._volume_mounts = volume_mounts

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, JindoCompTemplateSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JindoCompTemplateSpec):
            return True

        return self.to_dict() != other.to_dict()
