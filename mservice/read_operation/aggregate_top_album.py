# -*- coding: utf-8 -*-
"""
Module to perform Read operation to get the top Albums
==========================================================

Module for reading records from the database to get the top albums

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_album - Function to perform read operation with the database to get the top albums
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_album(session):
    """
    Function to perform read operation with the database to get the top albums

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Performing Read Operation")

    # Selecting the Album id, Album Title, and sum of all quantities of the track id in all invoices
    query = session.query(models.AlbumTable.album_id, models.AlbumTable.title,
                          func.sum(models.InvoiceLineTable.quantity).label("total_sales"))

    # Joining tracks table, album table, with the invoiceline table
    query = query.join(models.TracksTable, models.InvoiceLineTable.track_id == models.TracksTable.track_id)
    query = query.join(models.AlbumTable, models.TracksTable.album_id == models.AlbumTable.album_id)

    # Grouping by Album Id
    query = query.group_by(models.AlbumTable.album_id)

    # Sorting by total_sales
    query = query.order_by(desc("total_sales"), models.AlbumTable.album_id)

    results = query.limit(20)

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

        print(f"{result.album_id}, {result.title}, {result.total_sales}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()
