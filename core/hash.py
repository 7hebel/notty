""" Contains functionalities to use hashing in project. """

from dataclasses import dataclass
import hashlib

SHORT_LENGTH = 5


@dataclass
class Hash:
    """ Represents hashed data using SHA256 algorithm.
    It contains two object generator functions:
    >>> generate(data: str) -> Hash
    >>> generate_from_full(full_hash: str) -> Hash
    and two magic methods:
    >>> __eq__: Check if a string is equal to short or full form.
    >>> __str__: return this Hash's data in "(short) full" form.

    Generated object has two attributes:
    >>> full: Full, generated SHA256 hash
    >>> short: First characters of full hash. Amount of characters
               is predefined and assigned to SHORT_LENGTH variable.
    """

    full: str
    short: str

    @staticmethod
    def generate(data: str) -> "Hash":
        """ Generate new Hash object based on given data. """
        full_hash = hashlib.sha256(data.encode()).hexdigest()
        short_hash = full_hash[:SHORT_LENGTH]
        return Hash(full_hash, short_hash)

    @staticmethod
    def generate_from_full(full_hash: str) -> "Hash":
        """ Generate new Hash object basing on full hash of an object. """
        short_hash = full_hash[:SHORT_LENGTH]
        return Hash(full_hash, short_hash)

    def __eq__(self, value: object) -> bool:
        """ Check if given value is equal to either full or short hash representation. """
        if not isinstance(value, str):
            raise TypeError("Hash.__eq__ requires string as value.")
        return str(value).strip().lower() in (self.full.lower(), self.short.lower())

    def __str__(self) -> str:
        """ Return readable version of Hash object. """
        return f"({self.short}) {self.full}"
