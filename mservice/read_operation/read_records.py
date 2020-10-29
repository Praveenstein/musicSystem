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

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def perform_read_join(session):
    """
    Function to perform read operation with the database

    :param session: The session to work with
    :type session: sqlalchemy.orm.session.Session

    :return: Nothing
    :rtype: None
    """

    LOGGER.info("Performing Read Operation")

    # Selecting the Invoice Id, Customer Id, Invoice Date, Invoice Total, Customer Name, Employee Name,
    # Employee Title, Track Name
    query = session.query(models.InvoiceTable.invoice_id, models.InvoiceTable.customer_id,
                          models.InvoiceTable.invoice_date, models.InvoiceTable.total, models.CustomerTable.first_name,
                          models.EmployeeTable.first_name.label("Employee_Name"), models.EmployeeTable.title,
                          models.TracksTable.name)

    # Joining Invoice Table, Customer Table, Invoice Line, Employee, Tracks Table
    query = query.join(models.CustomerTable, models.InvoiceTable.customer_id == models.CustomerTable.customer_id)
    query = query.join(models.InvoiceLineTable, models.InvoiceTable.invoice_id == models.InvoiceLineTable.invoice_id)
    query = query.join(models.EmployeeTable, models.CustomerTable.support_rep_id == models.EmployeeTable.employee_id)
    query = query.join(models.TracksTable, models.InvoiceLineTable.track_id == models.TracksTable.track_id)

    # Sorting by Invoice Id
    query = query.order_by(models.InvoiceTable.invoice_id)

    results = query.limit(20)

    print("\n\n")
    print("==" * 50)

    for result in results:
        print(f"{result.invoice_id}, {result.customer_id}, {result.invoice_date}, {result.total}, {result.first_name},"
              f"{result.Employee_Name}, {result.name}, {result.title}")

    print("\n\n")
    print("==" * 50)

    session.close()
