# -*- coding: utf-8 -*-
"""
Module to Find the Number of Playlists An album has been Added to
=====================================================================

Module for reading records from the database to get the number of playlist an album has been added to

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_number_of_playlist_album - Function to perform read operation with the database to get the number of
                                      playlist an album has been added to
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import desc, func, distinct
from sqlalchemy.orm.exc import NoResultFound
from tabulate import tabulate

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_number_of_playlist_album(session, number_of_albums):
    """
    Function to perform read operation with the database to get the number of playlist a track has been added to

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :param number_of_albums: The number of albums to be returned from the query
    :type number_of_albums: int

    :return: Nothing
    :rtype: None
    """
    try:
        if not issubclass(type(session), sqlalchemy.orm.session.Session):
            raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

        if not issubclass(type(number_of_albums), int) or number_of_albums < 1:
            raise AttributeError("number of tracks should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        # Selecting the Album Id, Album title, and Count of Distinct playlist IDs
        query = session.query(models.TracksTable.album_id, models.AlbumTable.title,
                              func.count(distinct(models.PlaylistTrackTable.play_list_id)).label("number_of_playlist"))

        # Joining tracks table, playlisttrack table and album table
        query = query.join(models.TracksTable, models.PlaylistTrackTable.track_id == models.TracksTable.track_id)
        query = query.join(models.AlbumTable, models.TracksTable.album_id == models.AlbumTable.album_id)

        # Grouping by Album Id
        query = query.group_by(models.TracksTable.album_id)

        # Sorting by number_of_playlist and track id
        query = query.order_by(desc("number_of_playlist"), models.TracksTable.album_id)

        results = query.limit(number_of_albums).all()

        if not results:
            raise NoResultFound("No Records Found")

        LOGGER.info("\n\nThe Top %s Albums, Based On Number Of Playlist It Is Added To", number_of_albums)

        print("\n\n")
        print("===" * 50)
        print("\n\n")

        print(tabulate(results, headers=["Album ID", "Album Title", "Number Of Playlist"], tablefmt="grid"))

        print("\n\n")
        print("===" * 50)
        print("\n\n")
    except AttributeError as err:
        LOGGER.error(err)
    except NoResultFound as err:
        LOGGER.error(err)
    finally:
        session.close()
