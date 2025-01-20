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


class AlluxioRuntimeSpec(object):
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
        'alluxio_version': 'VersionSpec',
        'api_gateway': 'AlluxioCompTemplateSpec',
        'data': 'Data',
        'disable_prometheus': 'bool',
        'fuse': 'AlluxioFuseSpec',
        'hadoop_config': 'str',
        'image_pull_secrets': 'list[V1LocalObjectReference]',
        'init_users': 'InitUsersSpec',
        'job_master': 'AlluxioCompTemplateSpec',
        'job_worker': 'AlluxioCompTemplateSpec',
        'jvm_options': 'list[str]',
        'management': 'RuntimeManagement',
        'master': 'AlluxioCompTemplateSpec',
        'pod_metadata': 'PodMetadata',
        'properties': 'dict(str, str)',
        'replicas': 'int',
        'run_as': 'User',
        'tieredstore': 'TieredStore',
        'volumes': 'list[V1Volume]',
        'worker': 'AlluxioCompTemplateSpec'
    }

    attribute_map = {
        'alluxio_version': 'alluxioVersion',
        'api_gateway': 'apiGateway',
        'data': 'data',
        'disable_prometheus': 'disablePrometheus',
        'fuse': 'fuse',
        'hadoop_config': 'hadoopConfig',
        'image_pull_secrets': 'imagePullSecrets',
        'init_users': 'initUsers',
        'job_master': 'jobMaster',
        'job_worker': 'jobWorker',
        'jvm_options': 'jvmOptions',
        'management': 'management',
        'master': 'master',
        'pod_metadata': 'podMetadata',
        'properties': 'properties',
        'replicas': 'replicas',
        'run_as': 'runAs',
        'tieredstore': 'tieredstore',
        'volumes': 'volumes',
        'worker': 'worker'
    }

    def __init__(self, alluxio_version=None, api_gateway=None, data=None, disable_prometheus=None, fuse=None, hadoop_config=None, image_pull_secrets=None, init_users=None, job_master=None, job_worker=None, jvm_options=None, management=None, master=None, pod_metadata=None, properties=None, replicas=None, run_as=None, tieredstore=None, volumes=None, worker=None, local_vars_configuration=None):  # noqa: E501
        """AlluxioRuntimeSpec - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._alluxio_version = None
        self._api_gateway = None
        self._data = None
        self._disable_prometheus = None
        self._fuse = None
        self._hadoop_config = None
        self._image_pull_secrets = None
        self._init_users = None
        self._job_master = None
        self._job_worker = None
        self._jvm_options = None
        self._management = None
        self._master = None
        self._pod_metadata = None
        self._properties = None
        self._replicas = None
        self._run_as = None
        self._tieredstore = None
        self._volumes = None
        self._worker = None
        self.discriminator = None

        if alluxio_version is not None:
            self.alluxio_version = alluxio_version
        if api_gateway is not None:
            self.api_gateway = api_gateway
        if data is not None:
            self.data = data
        if disable_prometheus is not None:
            self.disable_prometheus = disable_prometheus
        if fuse is not None:
            self.fuse = fuse
        if hadoop_config is not None:
            self.hadoop_config = hadoop_config
        if image_pull_secrets is not None:
            self.image_pull_secrets = image_pull_secrets
        if init_users is not None:
            self.init_users = init_users
        if job_master is not None:
            self.job_master = job_master
        if job_worker is not None:
            self.job_worker = job_worker
        if jvm_options is not None:
            self.jvm_options = jvm_options
        if management is not None:
            self.management = management
        if master is not None:
            self.master = master
        if pod_metadata is not None:
            self.pod_metadata = pod_metadata
        if properties is not None:
            self.properties = properties
        if replicas is not None:
            self.replicas = replicas
        if run_as is not None:
            self.run_as = run_as
        if tieredstore is not None:
            self.tieredstore = tieredstore
        if volumes is not None:
            self.volumes = volumes
        if worker is not None:
            self.worker = worker

    @property
    def alluxio_version(self):
        """Gets the alluxio_version of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The alluxio_version of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: VersionSpec
        """
        return self._alluxio_version

    @alluxio_version.setter
    def alluxio_version(self, alluxio_version):
        """Sets the alluxio_version of this AlluxioRuntimeSpec.


        :param alluxio_version: The alluxio_version of this AlluxioRuntimeSpec.  # noqa: E501
        :type: VersionSpec
        """

        self._alluxio_version = alluxio_version

    @property
    def api_gateway(self):
        """Gets the api_gateway of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The api_gateway of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: AlluxioCompTemplateSpec
        """
        return self._api_gateway

    @api_gateway.setter
    def api_gateway(self, api_gateway):
        """Sets the api_gateway of this AlluxioRuntimeSpec.


        :param api_gateway: The api_gateway of this AlluxioRuntimeSpec.  # noqa: E501
        :type: AlluxioCompTemplateSpec
        """

        self._api_gateway = api_gateway

    @property
    def data(self):
        """Gets the data of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The data of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: Data
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this AlluxioRuntimeSpec.


        :param data: The data of this AlluxioRuntimeSpec.  # noqa: E501
        :type: Data
        """

        self._data = data

    @property
    def disable_prometheus(self):
        """Gets the disable_prometheus of this AlluxioRuntimeSpec.  # noqa: E501

        Disable monitoring for Alluxio Runtime Prometheus is enabled by default  # noqa: E501

        :return: The disable_prometheus of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: bool
        """
        return self._disable_prometheus

    @disable_prometheus.setter
    def disable_prometheus(self, disable_prometheus):
        """Sets the disable_prometheus of this AlluxioRuntimeSpec.

        Disable monitoring for Alluxio Runtime Prometheus is enabled by default  # noqa: E501

        :param disable_prometheus: The disable_prometheus of this AlluxioRuntimeSpec.  # noqa: E501
        :type: bool
        """

        self._disable_prometheus = disable_prometheus

    @property
    def fuse(self):
        """Gets the fuse of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The fuse of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: AlluxioFuseSpec
        """
        return self._fuse

    @fuse.setter
    def fuse(self, fuse):
        """Sets the fuse of this AlluxioRuntimeSpec.


        :param fuse: The fuse of this AlluxioRuntimeSpec.  # noqa: E501
        :type: AlluxioFuseSpec
        """

        self._fuse = fuse

    @property
    def hadoop_config(self):
        """Gets the hadoop_config of this AlluxioRuntimeSpec.  # noqa: E501

        Name of the configMap used to support HDFS configurations when using HDFS as Alluxio's UFS. The configMap must be in the same namespace with the AlluxioRuntime. The configMap should contain user-specific HDFS conf files in it. For now, only \"hdfs-site.xml\" and \"core-site.xml\" are supported. It must take the filename of the conf file as the key and content of the file as the value.  # noqa: E501

        :return: The hadoop_config of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: str
        """
        return self._hadoop_config

    @hadoop_config.setter
    def hadoop_config(self, hadoop_config):
        """Sets the hadoop_config of this AlluxioRuntimeSpec.

        Name of the configMap used to support HDFS configurations when using HDFS as Alluxio's UFS. The configMap must be in the same namespace with the AlluxioRuntime. The configMap should contain user-specific HDFS conf files in it. For now, only \"hdfs-site.xml\" and \"core-site.xml\" are supported. It must take the filename of the conf file as the key and content of the file as the value.  # noqa: E501

        :param hadoop_config: The hadoop_config of this AlluxioRuntimeSpec.  # noqa: E501
        :type: str
        """

        self._hadoop_config = hadoop_config

    @property
    def image_pull_secrets(self):
        """Gets the image_pull_secrets of this AlluxioRuntimeSpec.  # noqa: E501

        ImagePullSecrets that will be used to pull images  # noqa: E501

        :return: The image_pull_secrets of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: list[V1LocalObjectReference]
        """
        return self._image_pull_secrets

    @image_pull_secrets.setter
    def image_pull_secrets(self, image_pull_secrets):
        """Sets the image_pull_secrets of this AlluxioRuntimeSpec.

        ImagePullSecrets that will be used to pull images  # noqa: E501

        :param image_pull_secrets: The image_pull_secrets of this AlluxioRuntimeSpec.  # noqa: E501
        :type: list[V1LocalObjectReference]
        """

        self._image_pull_secrets = image_pull_secrets

    @property
    def init_users(self):
        """Gets the init_users of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The init_users of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: InitUsersSpec
        """
        return self._init_users

    @init_users.setter
    def init_users(self, init_users):
        """Sets the init_users of this AlluxioRuntimeSpec.


        :param init_users: The init_users of this AlluxioRuntimeSpec.  # noqa: E501
        :type: InitUsersSpec
        """

        self._init_users = init_users

    @property
    def job_master(self):
        """Gets the job_master of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The job_master of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: AlluxioCompTemplateSpec
        """
        return self._job_master

    @job_master.setter
    def job_master(self, job_master):
        """Sets the job_master of this AlluxioRuntimeSpec.


        :param job_master: The job_master of this AlluxioRuntimeSpec.  # noqa: E501
        :type: AlluxioCompTemplateSpec
        """

        self._job_master = job_master

    @property
    def job_worker(self):
        """Gets the job_worker of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The job_worker of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: AlluxioCompTemplateSpec
        """
        return self._job_worker

    @job_worker.setter
    def job_worker(self, job_worker):
        """Sets the job_worker of this AlluxioRuntimeSpec.


        :param job_worker: The job_worker of this AlluxioRuntimeSpec.  # noqa: E501
        :type: AlluxioCompTemplateSpec
        """

        self._job_worker = job_worker

    @property
    def jvm_options(self):
        """Gets the jvm_options of this AlluxioRuntimeSpec.  # noqa: E501

        Options for JVM  # noqa: E501

        :return: The jvm_options of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: list[str]
        """
        return self._jvm_options

    @jvm_options.setter
    def jvm_options(self, jvm_options):
        """Sets the jvm_options of this AlluxioRuntimeSpec.

        Options for JVM  # noqa: E501

        :param jvm_options: The jvm_options of this AlluxioRuntimeSpec.  # noqa: E501
        :type: list[str]
        """

        self._jvm_options = jvm_options

    @property
    def management(self):
        """Gets the management of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The management of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: RuntimeManagement
        """
        return self._management

    @management.setter
    def management(self, management):
        """Sets the management of this AlluxioRuntimeSpec.


        :param management: The management of this AlluxioRuntimeSpec.  # noqa: E501
        :type: RuntimeManagement
        """

        self._management = management

    @property
    def master(self):
        """Gets the master of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The master of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: AlluxioCompTemplateSpec
        """
        return self._master

    @master.setter
    def master(self, master):
        """Sets the master of this AlluxioRuntimeSpec.


        :param master: The master of this AlluxioRuntimeSpec.  # noqa: E501
        :type: AlluxioCompTemplateSpec
        """

        self._master = master

    @property
    def pod_metadata(self):
        """Gets the pod_metadata of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The pod_metadata of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: PodMetadata
        """
        return self._pod_metadata

    @pod_metadata.setter
    def pod_metadata(self, pod_metadata):
        """Sets the pod_metadata of this AlluxioRuntimeSpec.


        :param pod_metadata: The pod_metadata of this AlluxioRuntimeSpec.  # noqa: E501
        :type: PodMetadata
        """

        self._pod_metadata = pod_metadata

    @property
    def properties(self):
        """Gets the properties of this AlluxioRuntimeSpec.  # noqa: E501

        Configurable properties for Alluxio system. <br> Refer to <a href=\"https://docs.alluxio.io/os/user/stable/en/reference/Properties-List.html\">Alluxio Configuration Properties</a> for more info  # noqa: E501

        :return: The properties of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this AlluxioRuntimeSpec.

        Configurable properties for Alluxio system. <br> Refer to <a href=\"https://docs.alluxio.io/os/user/stable/en/reference/Properties-List.html\">Alluxio Configuration Properties</a> for more info  # noqa: E501

        :param properties: The properties of this AlluxioRuntimeSpec.  # noqa: E501
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def replicas(self):
        """Gets the replicas of this AlluxioRuntimeSpec.  # noqa: E501

        The replicas of the worker, need to be specified  # noqa: E501

        :return: The replicas of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this AlluxioRuntimeSpec.

        The replicas of the worker, need to be specified  # noqa: E501

        :param replicas: The replicas of this AlluxioRuntimeSpec.  # noqa: E501
        :type: int
        """

        self._replicas = replicas

    @property
    def run_as(self):
        """Gets the run_as of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The run_as of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: User
        """
        return self._run_as

    @run_as.setter
    def run_as(self, run_as):
        """Sets the run_as of this AlluxioRuntimeSpec.


        :param run_as: The run_as of this AlluxioRuntimeSpec.  # noqa: E501
        :type: User
        """

        self._run_as = run_as

    @property
    def tieredstore(self):
        """Gets the tieredstore of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The tieredstore of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: TieredStore
        """
        return self._tieredstore

    @tieredstore.setter
    def tieredstore(self, tieredstore):
        """Sets the tieredstore of this AlluxioRuntimeSpec.


        :param tieredstore: The tieredstore of this AlluxioRuntimeSpec.  # noqa: E501
        :type: TieredStore
        """

        self._tieredstore = tieredstore

    @property
    def volumes(self):
        """Gets the volumes of this AlluxioRuntimeSpec.  # noqa: E501

        Volumes is the list of Kubernetes volumes that can be mounted by the alluxio runtime components and/or fuses.  # noqa: E501

        :return: The volumes of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: list[V1Volume]
        """
        return self._volumes

    @volumes.setter
    def volumes(self, volumes):
        """Sets the volumes of this AlluxioRuntimeSpec.

        Volumes is the list of Kubernetes volumes that can be mounted by the alluxio runtime components and/or fuses.  # noqa: E501

        :param volumes: The volumes of this AlluxioRuntimeSpec.  # noqa: E501
        :type: list[V1Volume]
        """

        self._volumes = volumes

    @property
    def worker(self):
        """Gets the worker of this AlluxioRuntimeSpec.  # noqa: E501


        :return: The worker of this AlluxioRuntimeSpec.  # noqa: E501
        :rtype: AlluxioCompTemplateSpec
        """
        return self._worker

    @worker.setter
    def worker(self, worker):
        """Sets the worker of this AlluxioRuntimeSpec.


        :param worker: The worker of this AlluxioRuntimeSpec.  # noqa: E501
        :type: AlluxioCompTemplateSpec
        """

        self._worker = worker

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
        if not isinstance(other, AlluxioRuntimeSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AlluxioRuntimeSpec):
            return True

        return self.to_dict() != other.to_dict()
