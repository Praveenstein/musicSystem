# -*- coding: utf-8 -*-
"""
Module to Get Top Tracks For each Genre
==================================================

Module for reading records from the database to Get Top Tracks For each Genre

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_tracks_for_genre - Function to perform read operation with the database to Get Top Tracks For
                                   each Genre
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


def get_top_tracks_for_genre(session, number_of_tracks):
    """
    Function to perform read operation with the database to Get Top Tracks For each Genre

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

        # Creating a subquery that returns the track id, track name, genre id, genre name, and number of purchases
        # Of the track and a rank for each track, the track with highest number of purchases will have the lowest rank
        # number, this is done using a row_number function, by partitioning over the genre Id
        genre_ranked_table = session.query(models.TracksTable.track_id.label("track_id"),
                                           models.TracksTable.name.label("track_name"),
                                           models.TracksTable.genre_id.label("genre_id"),
                                           models.GenreTable.name.label("genre_name"),
                                           func.count(models.InvoiceLineTable.invoice_id).label("number_of_purchases"),
                                           func.row_number().over(partition_by=models.TracksTable.genre_id,
                                                                  order_by=
                                                                  desc(func.count(models.InvoiceLineTable.invoice_id))).
                                           label("track_rank"))

        # Joining the invoiceline table and tracks table and Genre Table
        genre_ranked_table = genre_ranked_table.join(models.InvoiceLineTable,
                                                     models.TracksTable.track_id == models.InvoiceLineTable.track_id)

        genre_ranked_table = genre_ranked_table.join(models.GenreTable,
                                                     models.TracksTable.genre_id == models.GenreTable.genre_id)

        # Grouping By the Track Id and using that as a subquery
        genre_ranked_table = genre_ranked_table.group_by(models.TracksTable.track_id).subquery()

        # Selecting the Track ID, Track Name, Genre Id, Genre Name, Total Number Of Purchases from the Subquery
        # Table genre_ranked_table
        query = session.query(genre_ranked_table.c.track_id, genre_ranked_table.c.track_name,
                              genre_ranked_table.c.genre_id, genre_ranked_table.c.genre_name,
                              genre_ranked_table.c.number_of_purchases)

        # To get the top 2 tracks for all genre, the query is filtered for track_rank less than 3
        results = query.filter(genre_ranked_table.c.track_rank < number_of_tracks + 1).all()

        if not results:
            raise NoResultFound("No Records Found")

        LOGGER.info("\n\nThe Top %s Tracks For all Genre, Based On Number Of Purchases", number_of_tracks)

        print("\n\n")
        print("===" * 50)
        print("\n\n")

        LOGGER.info("\n\n %s", tabulate(results, headers=["Track ID", "Track Name", "Genre ID", "Genre Name",
                                                          "Number Of Purchases"], tablefmt="grid"))

        print("\n\n")
        print("===" * 50)
        print("\n\n")
    except AttributeError as err:
        LOGGER.error(err)
    except NoResultFound as err:
        LOGGER.error(err)
    finally:
        session.close()
