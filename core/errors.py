""" This module contains error classes. """

class RepositoryError(Exception):
    """ This errors occurs when there is an problem with REPO. """

class SaveError(Exception):
    """ It is used for example when save is not found. """

class HashError(Exception):
    """ This exception is raised when an Hash is wrong. (e.g it's length) """
