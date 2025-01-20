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

class DecodedPSBTOutput(object):
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
        'bip32_derivs': 'list[PSBTBip32Deriv]',
        'redeem_script': 'AllOfDecodedPSBTOutputRedeemScript',
        'unknown': 'AllOfDecodedPSBTOutputUnknown',
        'witness_script': 'AllOfDecodedPSBTOutputWitnessScript'
    }

    attribute_map = {
        'bip32_derivs': 'bip32_derivs',
        'redeem_script': 'redeem_script',
        'unknown': 'unknown',
        'witness_script': 'witness_script'
    }

    def __init__(self, bip32_derivs=None, redeem_script=None, unknown=None, witness_script=None):  # noqa: E501
        """DecodedPSBTOutput - a model defined in Swagger"""  # noqa: E501
        self._bip32_derivs = None
        self._redeem_script = None
        self._unknown = None
        self._witness_script = None
        self.discriminator = None
        if bip32_derivs is not None:
            self.bip32_derivs = bip32_derivs
        if redeem_script is not None:
            self.redeem_script = redeem_script
        if unknown is not None:
            self.unknown = unknown
        if witness_script is not None:
            self.witness_script = witness_script

    @property
    def bip32_derivs(self):
        """Gets the bip32_derivs of this DecodedPSBTOutput.  # noqa: E501

        The BIP32 derivation paths  # noqa: E501

        :return: The bip32_derivs of this DecodedPSBTOutput.  # noqa: E501
        :rtype: list[PSBTBip32Deriv]
        """
        return self._bip32_derivs

    @bip32_derivs.setter
    def bip32_derivs(self, bip32_derivs):
        """Sets the bip32_derivs of this DecodedPSBTOutput.

        The BIP32 derivation paths  # noqa: E501

        :param bip32_derivs: The bip32_derivs of this DecodedPSBTOutput.  # noqa: E501
        :type: list[PSBTBip32Deriv]
        """

        self._bip32_derivs = bip32_derivs

    @property
    def redeem_script(self):
        """Gets the redeem_script of this DecodedPSBTOutput.  # noqa: E501

        The redeem script  # noqa: E501

        :return: The redeem_script of this DecodedPSBTOutput.  # noqa: E501
        :rtype: AllOfDecodedPSBTOutputRedeemScript
        """
        return self._redeem_script

    @redeem_script.setter
    def redeem_script(self, redeem_script):
        """Sets the redeem_script of this DecodedPSBTOutput.

        The redeem script  # noqa: E501

        :param redeem_script: The redeem_script of this DecodedPSBTOutput.  # noqa: E501
        :type: AllOfDecodedPSBTOutputRedeemScript
        """

        self._redeem_script = redeem_script

    @property
    def unknown(self):
        """Gets the unknown of this DecodedPSBTOutput.  # noqa: E501

        Unknown fields  # noqa: E501

        :return: The unknown of this DecodedPSBTOutput.  # noqa: E501
        :rtype: AllOfDecodedPSBTOutputUnknown
        """
        return self._unknown

    @unknown.setter
    def unknown(self, unknown):
        """Sets the unknown of this DecodedPSBTOutput.

        Unknown fields  # noqa: E501

        :param unknown: The unknown of this DecodedPSBTOutput.  # noqa: E501
        :type: AllOfDecodedPSBTOutputUnknown
        """

        self._unknown = unknown

    @property
    def witness_script(self):
        """Gets the witness_script of this DecodedPSBTOutput.  # noqa: E501

        The witness script  # noqa: E501

        :return: The witness_script of this DecodedPSBTOutput.  # noqa: E501
        :rtype: AllOfDecodedPSBTOutputWitnessScript
        """
        return self._witness_script

    @witness_script.setter
    def witness_script(self, witness_script):
        """Sets the witness_script of this DecodedPSBTOutput.

        The witness script  # noqa: E501

        :param witness_script: The witness_script of this DecodedPSBTOutput.  # noqa: E501
        :type: AllOfDecodedPSBTOutputWitnessScript
        """

        self._witness_script = witness_script

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
        if issubclass(DecodedPSBTOutput, dict):
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
        if not isinstance(other, DecodedPSBTOutput):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
