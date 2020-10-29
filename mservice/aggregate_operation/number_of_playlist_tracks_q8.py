# -*- coding: utf-8 -*-
"""
Module to Find the Number of Playlists a Track has been Added to
=======================================================================

Module for reading records from the database to get the number of playlist a track has been added to

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_number_of_playlist_tracks - Function to perform read operation with the database to get the number of
                                      playlist a track has been added to
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import desc, func
from tabulate import tabulate

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_number_of_playlist_tracks(session, number_of_tracks):
    """
    Function to perform read operation with the database to get the number of playlist a track has been added to

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :param number_of_tracks: The number of tracks to be returned from the query
    :type number_of_tracks: int

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(number_of_tracks), int) or number_of_tracks < 1:
        raise AttributeError("number of tracks should be integer and greater than 0")

    LOGGER.info("Performing Read Operation")

    # Selecting the Track Id, Track Name, and Count of playlist IDs
    query = session.query(models.PlaylistTrackTable.track_id, models.TracksTable.name,
                          func.count(models.PlaylistTrackTable.play_list_id).label("number_of_playlist"))

    # Joining tracks table and playlisttrack table
    query = query.join(models.TracksTable, models.PlaylistTrackTable.track_id == models.TracksTable.track_id)

    # Grouping by Track Id
    query = query.group_by(models.PlaylistTrackTable.track_id)

    # Sorting by number_of_playlist and track id
    query = query.order_by(desc("number_of_playlist"), models.PlaylistTrackTable.track_id)

    results = query.limit(number_of_tracks).all()

    LOGGER.info("\n\nThe Top %s Tracks, Based On Number Of Playlist It Is Added To", number_of_tracks)

    print("\n\n")
    print("===" * 50)
    print("\n\n")

    print(tabulate(results, headers=["Track ID", "Track Name", "Number Of Playlist"], tablefmt="grid"))

    print("\n\n")
    print("===" * 50)
    print("\n\n")

    session.close()
