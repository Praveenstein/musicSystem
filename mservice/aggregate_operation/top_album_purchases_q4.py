# -*- coding: utf-8 -*-
"""
Module to Get Top Albums Based On Number of Purchases
==========================================================

Module for reading records from the database to get the top albums based on number of purchases

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_album_purchases - Function to perform read operation with the database to get the top albums
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc, distinct

# User Imports
from tabulate import tabulate

import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_album_purchases(session, number_of_albums):
    """
    Function to perform read operation with the database to get the top albums

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :param number_of_albums: The number of albums to be returned from the query
    :type number_of_albums: int

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(number_of_albums), int) or number_of_albums < 1:
        raise AttributeError("number of albums should be integer and greater than 0")

    LOGGER.info("Performing Read Operation")

    # Selecting the Album id, Album Title, and count of distinct invoice IDs
    query = session.query(models.TracksTable.album_id, models.AlbumTable.title,
                          func.count(distinct(models.InvoiceLineTable.invoice_id)).label("number_of_purchases"))

    # Joining tracks table and invoiceline table with album table
    query = query.join(models.TracksTable, models.InvoiceLineTable.track_id == models.TracksTable.track_id)
    query = query.join(models.AlbumTable, models.TracksTable.album_id == models.AlbumTable.album_id)

    # Grouping by Album Id
    query = query.group_by(models.TracksTable.album_id)

    # Sorting by number_of_purchases
    query = query.order_by(desc("number_of_purchases"), models.TracksTable.album_id)

    results = query.limit(number_of_albums).all()

    LOGGER.info("\n\nThe Top %s Albums based on Total Number of Purchases", number_of_albums)

    print("\n\n")
    print("===" * 50)
    print("\n\n")

    print(tabulate(results, headers=["Album ID", " Album Title", "Number Of Purchases"], tablefmt="grid"))

    print("\n\n")
    print("===" * 50)
    print("\n\n")

    session.close()
