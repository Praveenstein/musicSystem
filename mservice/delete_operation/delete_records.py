# -*- coding: utf-8 -*-
"""
Module to perform Delete operation
========================================

Module for deleting records for the genre table

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * perform_delete - Function to perform delete operation with the database
"""
# Standard Imports
import logging

# External Imports
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def perform_delete(session):
    """
    Function to perform delete operation with the database

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :return: Nothing
    :rtype: None
    """

    LOGGER.info("Performing Delete Operation")
    try:

        new_genre = session.query(models.GenreTable).filter(models.GenreTable.genre_id == 33).one()
        session.delete(new_genre)
        session.commit()
        LOGGER.info("Deleted New Media")
    except NoResultFound as err:
        LOGGER.error("No Results: %s", err)
        session.rollback()
    except MultipleResultsFound as err:
        LOGGER.error("Multiple Results: %s", err)
        session.rollback()
    except Exception as err:
        LOGGER.error("Error: %s", err)
        session.rollback()
    finally:
        session.close()
