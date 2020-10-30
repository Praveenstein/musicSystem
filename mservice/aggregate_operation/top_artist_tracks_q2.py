# -*- coding: utf-8 -*-
"""
Module to Get Top Artist Based On Number of Tracks
==========================================================

Module for reading records from the database to get the top artist based on number of tracks they have composed

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_artist_tracks - Function to perform read operation with the database to get the top artist
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc
from sqlalchemy.orm.exc import NoResultFound
from tabulate import tabulate

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_artist_tracks(session, number_of_artist):
    """
    Function to perform read operation with the database to get the top artist

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :param number_of_artist: The number of artist to be returned from the query
    :type number_of_artist: int

    :return: Nothing
    :rtype: None
    """
    try:
        if not issubclass(type(session), sqlalchemy.orm.session.Session):
            raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

        if not issubclass(type(number_of_artist), int) or number_of_artist < 1:
            raise AttributeError("number of artist should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        # Selecting the Artist id, Artist Name, and count of track id
        query = session.query(models.AlbumTable.artist_id, models.ArtistTable.name,
                              func.count(models.TracksTable.track_id).label("number_of_tracks"))

        # Joining tracks table and album table
        query = query.join(models.AlbumTable, models.TracksTable.album_id == models.AlbumTable.album_id)
        query = query.join(models.ArtistTable, models.AlbumTable.artist_id == models.ArtistTable.artist_id)

        # Grouping by Artist Id
        query = query.group_by(models.AlbumTable.artist_id)

        # Sorting by number_of_tracks and artist id
        query = query.order_by(desc("number_of_tracks"), models.AlbumTable.artist_id)

        results = query.limit(number_of_artist).all()

        if not results:
            raise NoResultFound("No Records Found")

        LOGGER.info("\n\nThe Top %s Artist based on number of tracks are", number_of_artist)

        print("\n\n")
        print("===" * 50)
        print("\n\n")

        print(tabulate(results, headers=["Artist ID", "Artist Name", "Number Of Tracks"], tablefmt="grid"))

        print("\n\n")
        print("===" * 50)
        print("\n\n")
    except AttributeError as err:
        LOGGER.error(err)
    except NoResultFound as err:
        LOGGER.error(err)
    finally:
        session.close()
