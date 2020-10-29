# -*- coding: utf-8 -*-
"""
Module to perform Read operation to get Top Tracks
=======================================================

Module for reading records from the database to get the top sold tracks

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_tracks - Function to perform read operation with the database to get the top records
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_tracks(session):
    """
    Function to perform read operation with the to get the top tracks

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Performing Read Operation")

    # Selecting the track id, and sum of all quantities of the track id in all invoices
    query = session.query(models.InvoiceLineTable.track_id, func.sum(models.InvoiceLineTable.quantity).
                          label("total_sales"))

    # Using group by to find the total sales per track
    query = query.group_by(models.InvoiceLineTable.track_id)

    # Ordering the values by total_sales
    query = query.order_by(desc("total_sales"), models.InvoiceLineTable.track_id)

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

        print(f"{result.track_id}, {result.total_sales}")

    print("\n\n")
    print("==" * 50)

    session.close()
