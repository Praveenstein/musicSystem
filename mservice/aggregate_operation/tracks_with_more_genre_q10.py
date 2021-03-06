# -*- coding: utf-8 -*-
"""
Module to Get Tracks with More than One Genre
==================================================

Module for reading records from the database to Get Tracks with More than One Genre

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_tracks_with_more_genre - Function to perform read operation with the database to Get Tracks with
                                  More than One Genre
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, distinct
from sqlalchemy.orm.exc import NoResultFound
from tabulate import tabulate

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_tracks_with_more_genre(session, number_of_tracks):
    """
    Function to perform read operation with the database to Get Tracks with More than One Genre

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :param number_of_tracks: The number of tracks to be returned from the query
    :type number_of_tracks: int

    :return: Nothing
    :rtype: None

    """
    try:

        if not issubclass(type(session), sqlalchemy.orm.session.Session):
            raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

        if not issubclass(type(number_of_tracks), int) or number_of_tracks < 1:
            raise AttributeError("number of tracks should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        # Creating a subquery that returns the name of tracks which is associated with more the one genre
        stmt = session.query(models.TracksTable.name).group_by(models.TracksTable.name)
        stmt = stmt.having(func.count(distinct(models.TracksTable.genre_id)) > 1).subquery()

        # Selecting the Track Name, Genre Name
        query = session.query(distinct(models.TracksTable.name).label("track_name"),
                              models.GenreTable.name.label("genre_name"))

        # Filtering the query to return only tracks that are returned from the subquery
        query = query.filter(models.TracksTable.name.in_(stmt))

        # Joining tracks table and genre table
        query = query.join(models.GenreTable, models.TracksTable.genre_id == models.GenreTable.genre_id)

        # Sorting by Tracks Name
        query = query.order_by(models.TracksTable.name)

        results = query.limit(number_of_tracks).all()

        if not results:
            raise NoResultFound("No Records Found")

        LOGGER.info("\n\n%s Tracks, That Are Part Of More Than One Genre", number_of_tracks)

        print("\n\n")
        print("===" * 50)
        print("\n\n")

        LOGGER.info("\n\n %s", tabulate(results, headers=["Track Name", "Genre Name"], tablefmt="grid"))

        print("\n\n")
        print("===" * 50)
        print("\n\n")
    except AttributeError as err:
        LOGGER.error(err)
    except NoResultFound as err:
        LOGGER.error(err)
    finally:
        session.close()
