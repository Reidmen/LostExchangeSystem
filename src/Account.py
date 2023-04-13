""""
Implements ABC account and member.

Author: Reidmen <r.rethmawn@gmail.com>
Date: 04/13/2023
"""
from datetime import datetime
from abc import ABC, abstractmethod


class Account(ABC):
    def __init__(
        self,
        id: str,
        password: str,
        name: str,
        address: str,
        email: str,
        phone: str,
        status=Status,
    ):

        self.__id = id
        self.__password = password
        self.__name = name
        self.__address = address
        self.__email = email
        self.__phone = phone
        self._status = status

    @property
    @abstractmethod
    def _password(self):
        return NotImplementedError("requires _password")

    @_password.setter
    def _password(self, value):
        return NotImplementedError("requires setter for password")

    @abstractmethod
    def _reset_password(self):
        return NotImplementedError("requires _reset_password")
