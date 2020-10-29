# -*- coding: utf-8 -*-
"""
Module to perform Read operation to get the Customers
=========================================================

Module for reading records from the database to get the list of customers who are from brazil and
have spent more then 30.

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * perform_read_join - Function to perform read operation with the database using inner joins
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc, literal_column

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_customer(session):
    """
    Function to perform read operation with the database

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Performing Read Operation")

    # Selecting the customer id, customer country, customer name, and sum of all total of the invoices
    query = session.query(models.InvoiceTable.customer_id, models.CustomerTable.country,
                          func.concat(models.CustomerTable.first_name, " ", models.CustomerTable.last_name).
                          label("name"), func.sum(models.InvoiceTable.total).label("total_sale"))

    # Joining customer table with invoice table
    query = query.join(models.CustomerTable, models.InvoiceTable.customer_id == models.CustomerTable.customer_id)

    # Filtering customers from brazil
    query = query.filter(models.CustomerTable.country == "Brazil")

    # Grouping by customer Id
    query = query.group_by(models.InvoiceTable.customer_id)

    # Filtering the final result whose total_sale value is greater than 30
    query = query.having(literal_column("total_sale") > 30)

    # Sorting by total_sale in descending order
    query = query.order_by(desc("total_sale"))

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

        print(f"{result.customer_id},{result.country}, {result.name}, {result.total_sale}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()
