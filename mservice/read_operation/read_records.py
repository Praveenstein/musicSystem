# -*- coding: utf-8 -*-
"""
Module to perform Read operation
========================================

Module for reading records from the database

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * perform_read_join - Function to perform read operation with the database using inner joins
"""
# Standard Imports
import logging

import sqlalchemy
from tabulate import tabulate

# External Imports
from sqlalchemy.orm.exc import NoResultFound

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def perform_read_join(session, records):
    """
    Function to perform read operation with the database

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :param records: The number of records to return from the query
    :type records: int

    :return: Nothing
    :rtype: None
    """
    try:

        if not issubclass(type(session), sqlalchemy.orm.session.Session):
            raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

        if not issubclass(type(records), int) or records < 1:
            raise AttributeError("number of records should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        # Selecting the Invoice Id, Customer Id, Invoice Date, Invoice Total, Customer Name, Employee Name,
        # Employee Title, Track Name
        query = session.query(models.InvoiceTable.invoice_id, models.InvoiceTable.customer_id,
                              models.InvoiceTable.invoice_date, models.InvoiceTable.total,
                              models.CustomerTable.first_name,
                              models.EmployeeTable.first_name.label("Employee_Name"), models.EmployeeTable.title,
                              models.TracksTable.name)

        # Joining Invoice Table, Customer Table, Invoice Line, Employee, Tracks Table
        query = query.join(models.CustomerTable, models.InvoiceTable.customer_id == models.CustomerTable.customer_id)
        query = query.join(models.InvoiceLineTable,
                           models.InvoiceTable.invoice_id == models.InvoiceLineTable.invoice_id)
        query = query.join(models.EmployeeTable,
                           models.CustomerTable.support_rep_id == models.EmployeeTable.employee_id)
        query = query.join(models.TracksTable, models.InvoiceLineTable.track_id == models.TracksTable.track_id)

        # Sorting by Invoice Id
        query = query.order_by(models.InvoiceTable.invoice_id)

        results = query.limit(records).all()

        if not results:
            raise NoResultFound("No Records Found")

        LOGGER.info("\n\nThe %s Invoice Records Are", records)

        print("\n\n")
        print("====" * 50)
        print("\n\n")

        LOGGER.info("\n\n %s", tabulate(results, headers=["Invoice ID", "Customer ID", "Invoice Date", "Invoice Total",
                                                          "Customer Name", "Support Rep Name", "Support Rep Title",
                                                          "Track"], tablefmt="grid"))

        print("\n\n")
        print("====" * 50)
        print("\n\n")
    except AttributeError as err:
        LOGGER.error(err)
    except NoResultFound as err:
        LOGGER.error(err)
    finally:
        session.close()
