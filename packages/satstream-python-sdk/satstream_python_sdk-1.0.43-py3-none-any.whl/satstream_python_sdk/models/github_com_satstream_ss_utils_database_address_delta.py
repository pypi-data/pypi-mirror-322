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

class GithubComSatstreamSsUtilsDatabaseAddressDelta(object):
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
        'address': 'str',
        'amount': 'int',
        'block_height': 'int'
    }

    attribute_map = {
        'address': 'address',
        'amount': 'amount',
        'block_height': 'block_height'
    }

    def __init__(self, address=None, amount=None, block_height=None):  # noqa: E501
        """GithubComSatstreamSsUtilsDatabaseAddressDelta - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._amount = None
        self._block_height = None
        self.discriminator = None
        if address is not None:
            self.address = address
        if amount is not None:
            self.amount = amount
        if block_height is not None:
            self.block_height = block_height

    @property
    def address(self):
        """Gets the address of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501


        :return: The address of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this GithubComSatstreamSsUtilsDatabaseAddressDelta.


        :param address: The address of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def amount(self):
        """Gets the amount of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501


        :return: The amount of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501
        :rtype: int
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this GithubComSatstreamSsUtilsDatabaseAddressDelta.


        :param amount: The amount of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501
        :type: int
        """

        self._amount = amount

    @property
    def block_height(self):
        """Gets the block_height of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501


        :return: The block_height of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501
        :rtype: int
        """
        return self._block_height

    @block_height.setter
    def block_height(self, block_height):
        """Sets the block_height of this GithubComSatstreamSsUtilsDatabaseAddressDelta.


        :param block_height: The block_height of this GithubComSatstreamSsUtilsDatabaseAddressDelta.  # noqa: E501
        :type: int
        """

        self._block_height = block_height

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
        if issubclass(GithubComSatstreamSsUtilsDatabaseAddressDelta, dict):
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
        if not isinstance(other, GithubComSatstreamSsUtilsDatabaseAddressDelta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
