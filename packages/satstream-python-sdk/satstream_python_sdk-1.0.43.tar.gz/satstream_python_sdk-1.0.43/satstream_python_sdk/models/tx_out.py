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

class TxOut(object):
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
        'bestblock': 'str',
        'coinbase': 'bool',
        'confirmations': 'int',
        'script_pub_key': 'AllOfTxOutScriptPubKey',
        'value': 'float'
    }

    attribute_map = {
        'bestblock': 'bestblock',
        'coinbase': 'coinbase',
        'confirmations': 'confirmations',
        'script_pub_key': 'scriptPubKey',
        'value': 'value'
    }

    def __init__(self, bestblock=None, coinbase=None, confirmations=None, script_pub_key=None, value=None):  # noqa: E501
        """TxOut - a model defined in Swagger"""  # noqa: E501
        self._bestblock = None
        self._coinbase = None
        self._confirmations = None
        self._script_pub_key = None
        self._value = None
        self.discriminator = None
        if bestblock is not None:
            self.bestblock = bestblock
        if coinbase is not None:
            self.coinbase = coinbase
        if confirmations is not None:
            self.confirmations = confirmations
        if script_pub_key is not None:
            self.script_pub_key = script_pub_key
        if value is not None:
            self.value = value

    @property
    def bestblock(self):
        """Gets the bestblock of this TxOut.  # noqa: E501

        The hash of the block at the tip of the chain  # noqa: E501

        :return: The bestblock of this TxOut.  # noqa: E501
        :rtype: str
        """
        return self._bestblock

    @bestblock.setter
    def bestblock(self, bestblock):
        """Sets the bestblock of this TxOut.

        The hash of the block at the tip of the chain  # noqa: E501

        :param bestblock: The bestblock of this TxOut.  # noqa: E501
        :type: str
        """

        self._bestblock = bestblock

    @property
    def coinbase(self):
        """Gets the coinbase of this TxOut.  # noqa: E501

        Whether this is a coinbase transaction  # noqa: E501

        :return: The coinbase of this TxOut.  # noqa: E501
        :rtype: bool
        """
        return self._coinbase

    @coinbase.setter
    def coinbase(self, coinbase):
        """Sets the coinbase of this TxOut.

        Whether this is a coinbase transaction  # noqa: E501

        :param coinbase: The coinbase of this TxOut.  # noqa: E501
        :type: bool
        """

        self._coinbase = coinbase

    @property
    def confirmations(self):
        """Gets the confirmations of this TxOut.  # noqa: E501

        The number of confirmations  # noqa: E501

        :return: The confirmations of this TxOut.  # noqa: E501
        :rtype: int
        """
        return self._confirmations

    @confirmations.setter
    def confirmations(self, confirmations):
        """Sets the confirmations of this TxOut.

        The number of confirmations  # noqa: E501

        :param confirmations: The confirmations of this TxOut.  # noqa: E501
        :type: int
        """

        self._confirmations = confirmations

    @property
    def script_pub_key(self):
        """Gets the script_pub_key of this TxOut.  # noqa: E501

        The public key script  # noqa: E501

        :return: The script_pub_key of this TxOut.  # noqa: E501
        :rtype: AllOfTxOutScriptPubKey
        """
        return self._script_pub_key

    @script_pub_key.setter
    def script_pub_key(self, script_pub_key):
        """Sets the script_pub_key of this TxOut.

        The public key script  # noqa: E501

        :param script_pub_key: The script_pub_key of this TxOut.  # noqa: E501
        :type: AllOfTxOutScriptPubKey
        """

        self._script_pub_key = script_pub_key

    @property
    def value(self):
        """Gets the value of this TxOut.  # noqa: E501

        The transaction value in BTC  # noqa: E501

        :return: The value of this TxOut.  # noqa: E501
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this TxOut.

        The transaction value in BTC  # noqa: E501

        :param value: The value of this TxOut.  # noqa: E501
        :type: float
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
        if issubclass(TxOut, dict):
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
        if not isinstance(other, TxOut):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
