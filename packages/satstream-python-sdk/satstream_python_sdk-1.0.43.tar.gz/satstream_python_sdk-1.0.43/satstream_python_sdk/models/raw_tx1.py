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

class RawTx1(object):
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
        'blockhash': 'str',
        'blocktime': 'int',
        'confirmations': 'int',
        'hash': 'str',
        'hex': 'str',
        'locktime': 'int',
        'size': 'int',
        'time': 'int',
        'txid': 'str',
        'version': 'int',
        'vin': 'list[TxVin1]',
        'vout': 'list[Vout]',
        'vsize': 'int',
        'weight': 'int'
    }

    attribute_map = {
        'blockhash': 'blockhash',
        'blocktime': 'blocktime',
        'confirmations': 'confirmations',
        'hash': 'hash',
        'hex': 'hex',
        'locktime': 'locktime',
        'size': 'size',
        'time': 'time',
        'txid': 'txid',
        'version': 'version',
        'vin': 'vin',
        'vout': 'vout',
        'vsize': 'vsize',
        'weight': 'weight'
    }

    def __init__(self, blockhash=None, blocktime=None, confirmations=None, hash=None, hex=None, locktime=None, size=None, time=None, txid=None, version=None, vin=None, vout=None, vsize=None, weight=None):  # noqa: E501
        """RawTx1 - a model defined in Swagger"""  # noqa: E501
        self._blockhash = None
        self._blocktime = None
        self._confirmations = None
        self._hash = None
        self._hex = None
        self._locktime = None
        self._size = None
        self._time = None
        self._txid = None
        self._version = None
        self._vin = None
        self._vout = None
        self._vsize = None
        self._weight = None
        self.discriminator = None
        if blockhash is not None:
            self.blockhash = blockhash
        if blocktime is not None:
            self.blocktime = blocktime
        if confirmations is not None:
            self.confirmations = confirmations
        if hash is not None:
            self.hash = hash
        if hex is not None:
            self.hex = hex
        if locktime is not None:
            self.locktime = locktime
        if size is not None:
            self.size = size
        if time is not None:
            self.time = time
        if txid is not None:
            self.txid = txid
        if version is not None:
            self.version = version
        if vin is not None:
            self.vin = vin
        if vout is not None:
            self.vout = vout
        if vsize is not None:
            self.vsize = vsize
        if weight is not None:
            self.weight = weight

    @property
    def blockhash(self):
        """Gets the blockhash of this RawTx1.  # noqa: E501


        :return: The blockhash of this RawTx1.  # noqa: E501
        :rtype: str
        """
        return self._blockhash

    @blockhash.setter
    def blockhash(self, blockhash):
        """Sets the blockhash of this RawTx1.


        :param blockhash: The blockhash of this RawTx1.  # noqa: E501
        :type: str
        """

        self._blockhash = blockhash

    @property
    def blocktime(self):
        """Gets the blocktime of this RawTx1.  # noqa: E501


        :return: The blocktime of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._blocktime

    @blocktime.setter
    def blocktime(self, blocktime):
        """Sets the blocktime of this RawTx1.


        :param blocktime: The blocktime of this RawTx1.  # noqa: E501
        :type: int
        """

        self._blocktime = blocktime

    @property
    def confirmations(self):
        """Gets the confirmations of this RawTx1.  # noqa: E501


        :return: The confirmations of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._confirmations

    @confirmations.setter
    def confirmations(self, confirmations):
        """Sets the confirmations of this RawTx1.


        :param confirmations: The confirmations of this RawTx1.  # noqa: E501
        :type: int
        """

        self._confirmations = confirmations

    @property
    def hash(self):
        """Gets the hash of this RawTx1.  # noqa: E501


        :return: The hash of this RawTx1.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this RawTx1.


        :param hash: The hash of this RawTx1.  # noqa: E501
        :type: str
        """

        self._hash = hash

    @property
    def hex(self):
        """Gets the hex of this RawTx1.  # noqa: E501


        :return: The hex of this RawTx1.  # noqa: E501
        :rtype: str
        """
        return self._hex

    @hex.setter
    def hex(self, hex):
        """Sets the hex of this RawTx1.


        :param hex: The hex of this RawTx1.  # noqa: E501
        :type: str
        """

        self._hex = hex

    @property
    def locktime(self):
        """Gets the locktime of this RawTx1.  # noqa: E501


        :return: The locktime of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._locktime

    @locktime.setter
    def locktime(self, locktime):
        """Sets the locktime of this RawTx1.


        :param locktime: The locktime of this RawTx1.  # noqa: E501
        :type: int
        """

        self._locktime = locktime

    @property
    def size(self):
        """Gets the size of this RawTx1.  # noqa: E501


        :return: The size of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this RawTx1.


        :param size: The size of this RawTx1.  # noqa: E501
        :type: int
        """

        self._size = size

    @property
    def time(self):
        """Gets the time of this RawTx1.  # noqa: E501


        :return: The time of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this RawTx1.


        :param time: The time of this RawTx1.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def txid(self):
        """Gets the txid of this RawTx1.  # noqa: E501


        :return: The txid of this RawTx1.  # noqa: E501
        :rtype: str
        """
        return self._txid

    @txid.setter
    def txid(self, txid):
        """Sets the txid of this RawTx1.


        :param txid: The txid of this RawTx1.  # noqa: E501
        :type: str
        """

        self._txid = txid

    @property
    def version(self):
        """Gets the version of this RawTx1.  # noqa: E501


        :return: The version of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this RawTx1.


        :param version: The version of this RawTx1.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def vin(self):
        """Gets the vin of this RawTx1.  # noqa: E501


        :return: The vin of this RawTx1.  # noqa: E501
        :rtype: list[TxVin1]
        """
        return self._vin

    @vin.setter
    def vin(self, vin):
        """Sets the vin of this RawTx1.


        :param vin: The vin of this RawTx1.  # noqa: E501
        :type: list[TxVin1]
        """

        self._vin = vin

    @property
    def vout(self):
        """Gets the vout of this RawTx1.  # noqa: E501


        :return: The vout of this RawTx1.  # noqa: E501
        :rtype: list[Vout]
        """
        return self._vout

    @vout.setter
    def vout(self, vout):
        """Sets the vout of this RawTx1.


        :param vout: The vout of this RawTx1.  # noqa: E501
        :type: list[Vout]
        """

        self._vout = vout

    @property
    def vsize(self):
        """Gets the vsize of this RawTx1.  # noqa: E501


        :return: The vsize of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._vsize

    @vsize.setter
    def vsize(self, vsize):
        """Sets the vsize of this RawTx1.


        :param vsize: The vsize of this RawTx1.  # noqa: E501
        :type: int
        """

        self._vsize = vsize

    @property
    def weight(self):
        """Gets the weight of this RawTx1.  # noqa: E501


        :return: The weight of this RawTx1.  # noqa: E501
        :rtype: int
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this RawTx1.


        :param weight: The weight of this RawTx1.  # noqa: E501
        :type: int
        """

        self._weight = weight

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
        if issubclass(RawTx1, dict):
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
        if not isinstance(other, RawTx1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
