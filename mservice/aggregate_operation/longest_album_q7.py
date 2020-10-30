# -*- coding: utf-8 -*-
"""
Module to Get Longest Album
=================================

Module for reading records from the database to get the longest Albums based on playtime of its tracks

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_longest_album - Function to perform read operation with the database to get the longest albums
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import desc, func
from sqlalchemy.orm.exc import NoResultFound
from tabulate import tabulate

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_longest_album(session, number_of_albums):
    """
    Function to perform read operation with the database to get the longest albums

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :param number_of_albums: The number of albums to be returned from the query
    :type number_of_albums: int

    :return: Nothing
    :rtype: None
    """
    try:
        if not issubclass(type(session), sqlalchemy.orm.session.Session):
            raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

        if not issubclass(type(number_of_albums), int) or number_of_albums < 1:
            raise AttributeError("number of albums should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        # Selecting the Album id, Album Title, and sum of playtime
        query = session.query(models.TracksTable.album_id, models.AlbumTable.title,
                              func.sum(models.TracksTable.milliseconds).label("total_playtime"))

        # Joining tracks table and album table
        query = query.join(models.AlbumTable, models.TracksTable.album_id == models.AlbumTable.album_id)

        # Grouping by Album Id
        query = query.group_by(models.TracksTable.album_id)

        # Sorting by milliseconds and track id
        query = query.order_by(desc("total_playtime"), models.TracksTable.album_id)

        results = query.limit(number_of_albums).all()

        if not results:
            raise NoResultFound("No Records Found")

        LOGGER.info("\n\nThe %s Longest Albums Based On Playtime Of Its Tracks", number_of_albums)

        print("\n\n")
        print("===" * 50)
        print("\n\n")

        print(tabulate(results, headers=["Album ID", "Album Title", "Total PlayTime (Milli Seconds)"], tablefmt="grid"))

        print("\n\n")
        print("===" * 50)
        print("\n\n")
    except AttributeError as err:
        LOGGER.error(err)
    except NoResultFound as err:
        LOGGER.error(err)
    finally:
        session.close()
