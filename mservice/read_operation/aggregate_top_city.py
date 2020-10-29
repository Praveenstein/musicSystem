# -*- coding: utf-8 -*-
"""
Module to perform Read operation to Get Top City
===================================================

Module for reading records from the database to get the top cities

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_city_sales - Function to get top city based on number of invoices
    * get_top_city_profit - Function to get top city based on total of invoices
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_city_sales(session):
    """
    Function to perform read operation with the database to get the total number of invoices (sales) for all city

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Performing Read Operation")

    # Getting the Billing city, and count of invoices for the city
    query = session.query(models.InvoiceTable.billing_city,
                          func.count(models.InvoiceTable.invoice_id).label("number_of_sales"))

    # Removing any city which has null value
    query = query.filter(models.InvoiceTable.billing_city is not None)

    # Getting count of invoices for all billing city using group by
    query = query.group_by(models.InvoiceTable.billing_city)

    # Sorting by number of sales
    query = query.order_by(desc("number_of_sales"), models.InvoiceTable.billing_city)

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

        print(f"{result.billing_city}, {result.number_of_sales}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()


def get_top_city_profit(session):
    """
    Function to perform read operation with the database to get the total profit from all cities

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Performing Read Operation")

    # Getting the Billing city, and Sum of invoices Total for the city
    query = session.query(models.InvoiceTable.billing_city,
                          func.sum(models.InvoiceTable.total).label("total_sales"))

    # Removing any city which has null value
    query = query.filter(models.InvoiceTable.billing_city is not None)

    # Getting Sum of invoices total for all billing city using group by
    query = query.group_by(models.InvoiceTable.billing_city)

    # Sorting by number of sales
    query = query.order_by(desc("total_sales"), models.InvoiceTable.billing_city)

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

        print(f"{result.billing_city}, {result.total_sales}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()
