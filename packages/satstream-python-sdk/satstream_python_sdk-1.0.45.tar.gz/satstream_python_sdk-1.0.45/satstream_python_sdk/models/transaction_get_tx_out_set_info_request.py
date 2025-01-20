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

class TransactionGetTxOutSetInfoRequest(object):
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
        'hash_or_height': 'object',
        'hash_type': 'str',
        'use_index': 'bool'
    }

    attribute_map = {
        'hash_or_height': 'hash_or_height',
        'hash_type': 'hash_type',
        'use_index': 'use_index'
    }

    def __init__(self, hash_or_height=None, hash_type=None, use_index=None):  # noqa: E501
        """TransactionGetTxOutSetInfoRequest - a model defined in Swagger"""  # noqa: E501
        self._hash_or_height = None
        self._hash_type = None
        self._use_index = None
        self.discriminator = None
        if hash_or_height is not None:
            self.hash_or_height = hash_or_height
        if hash_type is not None:
            self.hash_type = hash_type
        if use_index is not None:
            self.use_index = use_index

    @property
    def hash_or_height(self):
        """Gets the hash_or_height of this TransactionGetTxOutSetInfoRequest.  # noqa: E501

        Block hash or height  # noqa: E501

        :return: The hash_or_height of this TransactionGetTxOutSetInfoRequest.  # noqa: E501
        :rtype: object
        """
        return self._hash_or_height

    @hash_or_height.setter
    def hash_or_height(self, hash_or_height):
        """Sets the hash_or_height of this TransactionGetTxOutSetInfoRequest.

        Block hash or height  # noqa: E501

        :param hash_or_height: The hash_or_height of this TransactionGetTxOutSetInfoRequest.  # noqa: E501
        :type: object
        """

        self._hash_or_height = hash_or_height

    @property
    def hash_type(self):
        """Gets the hash_type of this TransactionGetTxOutSetInfoRequest.  # noqa: E501

        Which UTXO set hash should be calculated  # noqa: E501

        :return: The hash_type of this TransactionGetTxOutSetInfoRequest.  # noqa: E501
        :rtype: str
        """
        return self._hash_type

    @hash_type.setter
    def hash_type(self, hash_type):
        """Sets the hash_type of this TransactionGetTxOutSetInfoRequest.

        Which UTXO set hash should be calculated  # noqa: E501

        :param hash_type: The hash_type of this TransactionGetTxOutSetInfoRequest.  # noqa: E501
        :type: str
        """

        self._hash_type = hash_type

    @property
    def use_index(self):
        """Gets the use_index of this TransactionGetTxOutSetInfoRequest.  # noqa: E501

        Whether to use coinstatsindex  # noqa: E501

        :return: The use_index of this TransactionGetTxOutSetInfoRequest.  # noqa: E501
        :rtype: bool
        """
        return self._use_index

    @use_index.setter
    def use_index(self, use_index):
        """Sets the use_index of this TransactionGetTxOutSetInfoRequest.

        Whether to use coinstatsindex  # noqa: E501

        :param use_index: The use_index of this TransactionGetTxOutSetInfoRequest.  # noqa: E501
        :type: bool
        """

        self._use_index = use_index

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
        if issubclass(TransactionGetTxOutSetInfoRequest, dict):
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
        if not isinstance(other, TransactionGetTxOutSetInfoRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
