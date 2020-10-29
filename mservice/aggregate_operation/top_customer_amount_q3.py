# -*- coding: utf-8 -*-
"""
Module to Get Top Customers Based On Total amount
==========================================================

Module for reading records from the database to get the top customers based on total amount of purchase in history

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_customers - Function to perform read operation with the database to get the top customers
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import func, desc

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_customers(session, number_of_customers):
    """
    Function to perform read operation with the database to get the top customers

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :param number_of_customers: The number of customers to be returned from the query
    :type number_of_customers: int

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(number_of_customers), int) or number_of_customers < 1:
        raise AttributeError("number of customers should be integer and greater than 0")

    LOGGER.info("Performing Read Operation")

    # Selecting the Customer ID, Customer Full Name, Total amount customer spent
    query = session.query(models.InvoiceTable.customer_id, func.concat(models.CustomerTable.first_name, " ",
                                                                       models.CustomerTable.last_name).label("name"),
                          func.sum(models.InvoiceTable.total).label("total_amount"))

    # Joining customer table and invoice table
    query = query.join(models.CustomerTable, models.InvoiceTable.customer_id == models.CustomerTable.customer_id)

    # Grouping by Customer Id
    query = query.group_by(models.InvoiceTable.customer_id)

    # Sorting by total amount and customer Id
    query = query.order_by(desc("total_amount"), models.InvoiceTable.customer_id)

    results = query.limit(number_of_customers)

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
            print("Customer ID \t\tName\t\tTotal Amount\n")

        print(f"{result.customer_id},\t\t {result.name},\t\t {result.total_amount}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()