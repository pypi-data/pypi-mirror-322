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

class Output(object):
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
        'script_pubkey': 'str',
        'value': 'int'
    }

    attribute_map = {
        'script_pubkey': 'script_pubkey',
        'value': 'value'
    }

    def __init__(self, script_pubkey=None, value=None):  # noqa: E501
        """Output - a model defined in Swagger"""  # noqa: E501
        self._script_pubkey = None
        self._value = None
        self.discriminator = None
        if script_pubkey is not None:
            self.script_pubkey = script_pubkey
        if value is not None:
            self.value = value

    @property
    def script_pubkey(self):
        """Gets the script_pubkey of this Output.  # noqa: E501


        :return: The script_pubkey of this Output.  # noqa: E501
        :rtype: str
        """
        return self._script_pubkey

    @script_pubkey.setter
    def script_pubkey(self, script_pubkey):
        """Sets the script_pubkey of this Output.


        :param script_pubkey: The script_pubkey of this Output.  # noqa: E501
        :type: str
        """

        self._script_pubkey = script_pubkey

    @property
    def value(self):
        """Gets the value of this Output.  # noqa: E501


        :return: The value of this Output.  # noqa: E501
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Output.


        :param value: The value of this Output.  # noqa: E501
        :type: int
        """

        self._value = value

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
        if issubclass(Output, dict):
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
        if not isinstance(other, Output):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
