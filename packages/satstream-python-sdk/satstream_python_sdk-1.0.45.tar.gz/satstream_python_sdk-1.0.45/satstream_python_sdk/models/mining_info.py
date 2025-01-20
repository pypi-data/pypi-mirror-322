# coding: utf-8

"""
    Satstream API

    Satstream API  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: team@satstream.io
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MiningInfo(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'blocks': 'int',
        'chain': 'str',
        'currentblocktx': 'int',
        'currentblockweight': 'int',
        'difficulty': 'float',
        'networkhashps': 'float',
        'pooledtx': 'int',
        'warnings': 'str'
    }

    attribute_map = {
        'blocks': 'blocks',
        'chain': 'chain',
        'currentblocktx': 'currentblocktx',
        'currentblockweight': 'currentblockweight',
        'difficulty': 'difficulty',
        'networkhashps': 'networkhashps',
        'pooledtx': 'pooledtx',
        'warnings': 'warnings'
    }

    def __init__(self, blocks=None, chain=None, currentblocktx=None, currentblockweight=None, difficulty=None, networkhashps=None, pooledtx=None, warnings=None):  # noqa: E501
        """MiningInfo - a model defined in Swagger"""  # noqa: E501
        self._blocks = None
        self._chain = None
        self._currentblocktx = None
        self._currentblockweight = None
        self._difficulty = None
        self._networkhashps = None
        self._pooledtx = None
        self._warnings = None
        self.discriminator = None
        if blocks is not None:
            self.blocks = blocks
        if chain is not None:
            self.chain = chain
        if currentblocktx is not None:
            self.currentblocktx = currentblocktx
        if currentblockweight is not None:
            self.currentblockweight = currentblockweight
        if difficulty is not None:
            self.difficulty = difficulty
        if networkhashps is not None:
            self.networkhashps = networkhashps
        if pooledtx is not None:
            self.pooledtx = pooledtx
        if warnings is not None:
            self.warnings = warnings

    @property
    def blocks(self):
        """Gets the blocks of this MiningInfo.  # noqa: E501

        The current block  # noqa: E501

        :return: The blocks of this MiningInfo.  # noqa: E501
        :rtype: int
        """
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        """Sets the blocks of this MiningInfo.

        The current block  # noqa: E501

        :param blocks: The blocks of this MiningInfo.  # noqa: E501
        :type: int
        """

        self._blocks = blocks

    @property
    def chain(self):
        """Gets the chain of this MiningInfo.  # noqa: E501

        Current network name  # noqa: E501

        :return: The chain of this MiningInfo.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this MiningInfo.

        Current network name  # noqa: E501

        :param chain: The chain of this MiningInfo.  # noqa: E501
        :type: str
        """

        self._chain = chain

    @property
    def currentblocktx(self):
        """Gets the currentblocktx of this MiningInfo.  # noqa: E501

        The number of block transactions of the last assembled block  # noqa: E501

        :return: The currentblocktx of this MiningInfo.  # noqa: E501
        :rtype: int
        """
        return self._currentblocktx

    @currentblocktx.setter
    def currentblocktx(self, currentblocktx):
        """Sets the currentblocktx of this MiningInfo.

        The number of block transactions of the last assembled block  # noqa: E501

        :param currentblocktx: The currentblocktx of this MiningInfo.  # noqa: E501
        :type: int
        """

        self._currentblocktx = currentblocktx

    @property
    def currentblockweight(self):
        """Gets the currentblockweight of this MiningInfo.  # noqa: E501

        The block weight of the last assembled block  # noqa: E501

        :return: The currentblockweight of this MiningInfo.  # noqa: E501
        :rtype: int
        """
        return self._currentblockweight

    @currentblockweight.setter
    def currentblockweight(self, currentblockweight):
        """Sets the currentblockweight of this MiningInfo.

        The block weight of the last assembled block  # noqa: E501

        :param currentblockweight: The currentblockweight of this MiningInfo.  # noqa: E501
        :type: int
        """

        self._currentblockweight = currentblockweight

    @property
    def difficulty(self):
        """Gets the difficulty of this MiningInfo.  # noqa: E501

        The current difficulty  # noqa: E501

        :return: The difficulty of this MiningInfo.  # noqa: E501
        :rtype: float
        """
        return self._difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        """Sets the difficulty of this MiningInfo.

        The current difficulty  # noqa: E501

        :param difficulty: The difficulty of this MiningInfo.  # noqa: E501
        :type: float
        """

        self._difficulty = difficulty

    @property
    def networkhashps(self):
        """Gets the networkhashps of this MiningInfo.  # noqa: E501

        The network hashes per second  # noqa: E501

        :return: The networkhashps of this MiningInfo.  # noqa: E501
        :rtype: float
        """
        return self._networkhashps

    @networkhashps.setter
    def networkhashps(self, networkhashps):
        """Sets the networkhashps of this MiningInfo.

        The network hashes per second  # noqa: E501

        :param networkhashps: The networkhashps of this MiningInfo.  # noqa: E501
        :type: float
        """

        self._networkhashps = networkhashps

    @property
    def pooledtx(self):
        """Gets the pooledtx of this MiningInfo.  # noqa: E501

        The size of the mempool  # noqa: E501

        :return: The pooledtx of this MiningInfo.  # noqa: E501
        :rtype: int
        """
        return self._pooledtx

    @pooledtx.setter
    def pooledtx(self, pooledtx):
        """Sets the pooledtx of this MiningInfo.

        The size of the mempool  # noqa: E501

        :param pooledtx: The pooledtx of this MiningInfo.  # noqa: E501
        :type: int
        """

        self._pooledtx = pooledtx

    @property
    def warnings(self):
        """Gets the warnings of this MiningInfo.  # noqa: E501

        Any network and blockchain warnings  # noqa: E501

        :return: The warnings of this MiningInfo.  # noqa: E501
        :rtype: str
        """
        return self._warnings

    @warnings.setter
    def warnings(self, warnings):
        """Sets the warnings of this MiningInfo.

        Any network and blockchain warnings  # noqa: E501

        :param warnings: The warnings of this MiningInfo.  # noqa: E501
        :type: str
        """

        self._warnings = warnings

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(MiningInfo, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MiningInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
