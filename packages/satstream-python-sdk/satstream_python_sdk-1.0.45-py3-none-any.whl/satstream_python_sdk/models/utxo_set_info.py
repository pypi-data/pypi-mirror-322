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

class UTXOSetInfo(object):
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
        'block_info': 'AllOfUTXOSetInfoBlockInfo',
        'bogosize': 'int',
        'disk_size': 'int',
        'hash_serialized_2': 'str',
        'height': 'int',
        'muhash': 'str',
        'total_amount': 'float',
        'total_unspendable_amount': 'float',
        'transactions': 'int',
        'txouts': 'int'
    }

    attribute_map = {
        'bestblock': 'bestblock',
        'block_info': 'block_info',
        'bogosize': 'bogosize',
        'disk_size': 'disk_size',
        'hash_serialized_2': 'hash_serialized_2',
        'height': 'height',
        'muhash': 'muhash',
        'total_amount': 'total_amount',
        'total_unspendable_amount': 'total_unspendable_amount',
        'transactions': 'transactions',
        'txouts': 'txouts'
    }

    def __init__(self, bestblock=None, block_info=None, bogosize=None, disk_size=None, hash_serialized_2=None, height=None, muhash=None, total_amount=None, total_unspendable_amount=None, transactions=None, txouts=None):  # noqa: E501
        """UTXOSetInfo - a model defined in Swagger"""  # noqa: E501
        self._bestblock = None
        self._block_info = None
        self._bogosize = None
        self._disk_size = None
        self._hash_serialized_2 = None
        self._height = None
        self._muhash = None
        self._total_amount = None
        self._total_unspendable_amount = None
        self._transactions = None
        self._txouts = None
        self.discriminator = None
        if bestblock is not None:
            self.bestblock = bestblock
        if block_info is not None:
            self.block_info = block_info
        if bogosize is not None:
            self.bogosize = bogosize
        if disk_size is not None:
            self.disk_size = disk_size
        if hash_serialized_2 is not None:
            self.hash_serialized_2 = hash_serialized_2
        if height is not None:
            self.height = height
        if muhash is not None:
            self.muhash = muhash
        if total_amount is not None:
            self.total_amount = total_amount
        if total_unspendable_amount is not None:
            self.total_unspendable_amount = total_unspendable_amount
        if transactions is not None:
            self.transactions = transactions
        if txouts is not None:
            self.txouts = txouts

    @property
    def bestblock(self):
        """Gets the bestblock of this UTXOSetInfo.  # noqa: E501

        The hash of the block at which these statistics are calculated  # noqa: E501

        :return: The bestblock of this UTXOSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._bestblock

    @bestblock.setter
    def bestblock(self, bestblock):
        """Sets the bestblock of this UTXOSetInfo.

        The hash of the block at which these statistics are calculated  # noqa: E501

        :param bestblock: The bestblock of this UTXOSetInfo.  # noqa: E501
        :type: str
        """

        self._bestblock = bestblock

    @property
    def block_info(self):
        """Gets the block_info of this UTXOSetInfo.  # noqa: E501

        Info on amounts in the block at this height  # noqa: E501

        :return: The block_info of this UTXOSetInfo.  # noqa: E501
        :rtype: AllOfUTXOSetInfoBlockInfo
        """
        return self._block_info

    @block_info.setter
    def block_info(self, block_info):
        """Sets the block_info of this UTXOSetInfo.

        Info on amounts in the block at this height  # noqa: E501

        :param block_info: The block_info of this UTXOSetInfo.  # noqa: E501
        :type: AllOfUTXOSetInfoBlockInfo
        """

        self._block_info = block_info

    @property
    def bogosize(self):
        """Gets the bogosize of this UTXOSetInfo.  # noqa: E501

        Database-independent metric indicating the UTXO set size  # noqa: E501

        :return: The bogosize of this UTXOSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._bogosize

    @bogosize.setter
    def bogosize(self, bogosize):
        """Sets the bogosize of this UTXOSetInfo.

        Database-independent metric indicating the UTXO set size  # noqa: E501

        :param bogosize: The bogosize of this UTXOSetInfo.  # noqa: E501
        :type: int
        """

        self._bogosize = bogosize

    @property
    def disk_size(self):
        """Gets the disk_size of this UTXOSetInfo.  # noqa: E501

        The estimated size of the chainstate on disk  # noqa: E501

        :return: The disk_size of this UTXOSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._disk_size

    @disk_size.setter
    def disk_size(self, disk_size):
        """Sets the disk_size of this UTXOSetInfo.

        The estimated size of the chainstate on disk  # noqa: E501

        :param disk_size: The disk_size of this UTXOSetInfo.  # noqa: E501
        :type: int
        """

        self._disk_size = disk_size

    @property
    def hash_serialized_2(self):
        """Gets the hash_serialized_2 of this UTXOSetInfo.  # noqa: E501

        The serialized hash (only for hash_serialized_2)  # noqa: E501

        :return: The hash_serialized_2 of this UTXOSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._hash_serialized_2

    @hash_serialized_2.setter
    def hash_serialized_2(self, hash_serialized_2):
        """Sets the hash_serialized_2 of this UTXOSetInfo.

        The serialized hash (only for hash_serialized_2)  # noqa: E501

        :param hash_serialized_2: The hash_serialized_2 of this UTXOSetInfo.  # noqa: E501
        :type: str
        """

        self._hash_serialized_2 = hash_serialized_2

    @property
    def height(self):
        """Gets the height of this UTXOSetInfo.  # noqa: E501

        The block height of the returned statistics  # noqa: E501

        :return: The height of this UTXOSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this UTXOSetInfo.

        The block height of the returned statistics  # noqa: E501

        :param height: The height of this UTXOSetInfo.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def muhash(self):
        """Gets the muhash of this UTXOSetInfo.  # noqa: E501

        The serialized hash (only for muhash)  # noqa: E501

        :return: The muhash of this UTXOSetInfo.  # noqa: E501
        :rtype: str
        """
        return self._muhash

    @muhash.setter
    def muhash(self, muhash):
        """Sets the muhash of this UTXOSetInfo.

        The serialized hash (only for muhash)  # noqa: E501

        :param muhash: The muhash of this UTXOSetInfo.  # noqa: E501
        :type: str
        """

        self._muhash = muhash

    @property
    def total_amount(self):
        """Gets the total_amount of this UTXOSetInfo.  # noqa: E501

        The total amount of coins in the UTXO set  # noqa: E501

        :return: The total_amount of this UTXOSetInfo.  # noqa: E501
        :rtype: float
        """
        return self._total_amount

    @total_amount.setter
    def total_amount(self, total_amount):
        """Sets the total_amount of this UTXOSetInfo.

        The total amount of coins in the UTXO set  # noqa: E501

        :param total_amount: The total_amount of this UTXOSetInfo.  # noqa: E501
        :type: float
        """

        self._total_amount = total_amount

    @property
    def total_unspendable_amount(self):
        """Gets the total_unspendable_amount of this UTXOSetInfo.  # noqa: E501

        Total amount permanently excluded from UTXO set  # noqa: E501

        :return: The total_unspendable_amount of this UTXOSetInfo.  # noqa: E501
        :rtype: float
        """
        return self._total_unspendable_amount

    @total_unspendable_amount.setter
    def total_unspendable_amount(self, total_unspendable_amount):
        """Sets the total_unspendable_amount of this UTXOSetInfo.

        Total amount permanently excluded from UTXO set  # noqa: E501

        :param total_unspendable_amount: The total_unspendable_amount of this UTXOSetInfo.  # noqa: E501
        :type: float
        """

        self._total_unspendable_amount = total_unspendable_amount

    @property
    def transactions(self):
        """Gets the transactions of this UTXOSetInfo.  # noqa: E501

        The number of transactions with unspent outputs  # noqa: E501

        :return: The transactions of this UTXOSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        """Sets the transactions of this UTXOSetInfo.

        The number of transactions with unspent outputs  # noqa: E501

        :param transactions: The transactions of this UTXOSetInfo.  # noqa: E501
        :type: int
        """

        self._transactions = transactions

    @property
    def txouts(self):
        """Gets the txouts of this UTXOSetInfo.  # noqa: E501

        The number of unspent transaction outputs  # noqa: E501

        :return: The txouts of this UTXOSetInfo.  # noqa: E501
        :rtype: int
        """
        return self._txouts

    @txouts.setter
    def txouts(self, txouts):
        """Sets the txouts of this UTXOSetInfo.

        The number of unspent transaction outputs  # noqa: E501

        :param txouts: The txouts of this UTXOSetInfo.  # noqa: E501
        :type: int
        """

        self._txouts = txouts

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
        if issubclass(UTXOSetInfo, dict):
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
        if not isinstance(other, UTXOSetInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
