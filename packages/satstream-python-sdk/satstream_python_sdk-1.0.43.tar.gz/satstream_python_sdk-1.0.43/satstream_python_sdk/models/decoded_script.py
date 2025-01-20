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

class DecodedScript(object):
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
        'asm': 'str',
        'desc': 'str',
        'p2sh': 'str',
        'segwit': 'AllOfDecodedScriptSegwit',
        'type': 'str'
    }

    attribute_map = {
        'address': 'address',
        'asm': 'asm',
        'desc': 'desc',
        'p2sh': 'p2sh',
        'segwit': 'segwit',
        'type': 'type'
    }

    def __init__(self, address=None, asm=None, desc=None, p2sh=None, segwit=None, type=None):  # noqa: E501
        """DecodedScript - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._asm = None
        self._desc = None
        self._p2sh = None
        self._segwit = None
        self._type = None
        self.discriminator = None
        if address is not None:
            self.address = address
        if asm is not None:
            self.asm = asm
        if desc is not None:
            self.desc = desc
        if p2sh is not None:
            self.p2sh = p2sh
        if segwit is not None:
            self.segwit = segwit
        if type is not None:
            self.type = type

    @property
    def address(self):
        """Gets the address of this DecodedScript.  # noqa: E501

        The Bitcoin address (only if well-defined)  # noqa: E501

        :return: The address of this DecodedScript.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this DecodedScript.

        The Bitcoin address (only if well-defined)  # noqa: E501

        :param address: The address of this DecodedScript.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def asm(self):
        """Gets the asm of this DecodedScript.  # noqa: E501

        Script public key  # noqa: E501

        :return: The asm of this DecodedScript.  # noqa: E501
        :rtype: str
        """
        return self._asm

    @asm.setter
    def asm(self, asm):
        """Sets the asm of this DecodedScript.

        Script public key  # noqa: E501

        :param asm: The asm of this DecodedScript.  # noqa: E501
        :type: str
        """

        self._asm = asm

    @property
    def desc(self):
        """Gets the desc of this DecodedScript.  # noqa: E501

        Inferred descriptor for the script  # noqa: E501

        :return: The desc of this DecodedScript.  # noqa: E501
        :rtype: str
        """
        return self._desc

    @desc.setter
    def desc(self, desc):
        """Sets the desc of this DecodedScript.

        Inferred descriptor for the script  # noqa: E501

        :param desc: The desc of this DecodedScript.  # noqa: E501
        :type: str
        """

        self._desc = desc

    @property
    def p2sh(self):
        """Gets the p2sh of this DecodedScript.  # noqa: E501

        P2SH address wrapping this redeem script  # noqa: E501

        :return: The p2sh of this DecodedScript.  # noqa: E501
        :rtype: str
        """
        return self._p2sh

    @p2sh.setter
    def p2sh(self, p2sh):
        """Sets the p2sh of this DecodedScript.

        P2SH address wrapping this redeem script  # noqa: E501

        :param p2sh: The p2sh of this DecodedScript.  # noqa: E501
        :type: str
        """

        self._p2sh = p2sh

    @property
    def segwit(self):
        """Gets the segwit of this DecodedScript.  # noqa: E501

        Witness script details  # noqa: E501

        :return: The segwit of this DecodedScript.  # noqa: E501
        :rtype: AllOfDecodedScriptSegwit
        """
        return self._segwit

    @segwit.setter
    def segwit(self, segwit):
        """Sets the segwit of this DecodedScript.

        Witness script details  # noqa: E501

        :param segwit: The segwit of this DecodedScript.  # noqa: E501
        :type: AllOfDecodedScriptSegwit
        """

        self._segwit = segwit

    @property
    def type(self):
        """Gets the type of this DecodedScript.  # noqa: E501

        The output type  # noqa: E501

        :return: The type of this DecodedScript.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DecodedScript.

        The output type  # noqa: E501

        :param type: The type of this DecodedScript.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(DecodedScript, dict):
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
        if not isinstance(other, DecodedScript):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
