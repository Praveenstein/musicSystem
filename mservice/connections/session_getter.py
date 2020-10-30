# -*- coding: utf-8 -*-
""" Module for creating Engine and session maker factory

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries
"""
# Standard Imports
import logging

# External Imports
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

LOGGER = logging.getLogger(__name__)


def create_new_engine(dialect, driver, user, password, host, database):
    """
    Function to Create new engine from given input arguments

    :param dialect: The database dialect being used
    :type dialect: str

    :param driver: The driver used to connect to the give database dialect
    :type driver: str

    :param user: The user to login into the database
    :type user: str

    :param password: The password of the user to login into the database
    :type password: str

    :param host: The host ID
    :type host: str

    :param database: The database name to connect to
    :type database: str

    :return: New engine configured with given parameters
    :rtype: :class:`sqlalchemy.engine.create_engine`
    """
    try:

        if not all(map(lambda arg: True if issubclass(type(arg), str) else False, [dialect, driver, user, password,
                                                                                   host, database])):
            raise AttributeError("Invalid attribute type, should be string")

        connection_string = dialect + "+" + driver + "://" + user + ":" + password + "@" + host + "/" + database + \
                            "?charset=utf8mb4"

        engine = create_engine(connection_string, echo=True)
        return engine
    except AttributeError as err:
        LOGGER.error(err)
        raise


def get_session_factory(engine):
    """
    Function used to create and new session and return back

    :return: sessionmaker
    :rtype: :class:sqlalchemy.orm.sessionmaker
    """
    try:
        if not issubclass(type(engine), sqlalchemy.engine.base.Engine):
            raise AttributeError("Engine should be of type 'sqlalchemy.engine.base.Engine'")

        session_factory = sessionmaker(bind=engine)
        return session_factory
    except AttributeError as err:
        LOGGER.error(err)
        raise
