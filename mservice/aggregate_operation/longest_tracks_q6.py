# -*- coding: utf-8 -*-
"""
Module to Get Longest Tracks
=================================

Module for reading records from the database to get the longest tracks based on playtime of tracks

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_longest_tracks - Function to perform read operation with the database to get the longest tracks
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import desc

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_longest_tracks(session, number_of_tracks):
    """
    Function to perform read operation with the database to get the longest tracks

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

    # Selecting the Album id, Album Title, and count of distinct invoice IDs
    query = session.query(models.TracksTable.track_id, models.TracksTable.name, models.TracksTable.milliseconds)

    # Sorting by milliseconds and track id
    query = query.order_by(desc(models.TracksTable.milliseconds), models.TracksTable.track_id)

    results = query.limit(number_of_tracks)

    # Setting first variable as true, which could be used inside the for loop to print some line the first time
    # The loop is being run
    first = True

    for result in results:

        if first:

            # If it is the first time inside the loop, then some new lines and special characters are printed
            # And first is set to false
            print("\n\n")
            print("==" * 50)
            print("\n\n")
            first = False
            print("Track ID \t\tName\t\tPlayTime\n")

        print(f"{result.track_id},\t\t {result.name},\t\t {result.milliseconds}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()
