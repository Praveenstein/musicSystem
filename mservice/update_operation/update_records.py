# -*- coding: utf-8 -*-
"""
Module to perform Update operations
========================================

Module for updating records from the database

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * perform_update - Function to perform update operation with the database
"""
# Standard Imports
import logging

# User Imports
import sqlalchemy.orm

import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def perform_update(session):
    """
    Function to perform update operation with the database

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :return: Nothing
    :rtype: None
    """
    try:
        if not issubclass(type(session), sqlalchemy.orm.session.Session):
            raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")
        LOGGER.info("Performing Update Operation")

        session.query(models.TracksTable).update({models.TracksTable.unit_price: 0.99})

        session.commit()
    except AttributeError as err:
        LOGGER.error(err)
    finally:
        session.close()
