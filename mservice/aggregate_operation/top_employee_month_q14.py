# -*- coding: utf-8 -*-
"""
Module to Find Top Employee with Most Sales in a Month
=============================================================

Module for reading records from the database to Find Top Employee with Most Sales in a Month

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_employee_sales - Function to perform read operation with the database to Find Top Employee with
                             Most Sales in a Month
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import desc, func, extract

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_employee_sales(session, number_of_employee):
    """
    Function to perform read operation with the database to Find Top Employee with Most Sales in a Month

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :param number_of_employee: The number of albums to be returned from the query
    :type number_of_employee: int

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(number_of_employee), int) or number_of_employee < 1:
        raise AttributeError("number of Employee should be integer and greater than 0")

    LOGGER.info("Performing Read Operation")

    # Selecting the Employee Id, Employee Name, and Total Sales
    query = session.query(models.CustomerTable.support_rep_id.label("employee_id"),
                          func.concat(models.EmployeeTable.first_name, " ", models.EmployeeTable.last_name).
                          label("name"), func.count(models.InvoiceTable.invoice_id).label("total_sales"))

    # Joining Invoice, customer and employee Table
    query = query.join(models.CustomerTable, models.InvoiceTable.customer_id == models.CustomerTable.customer_id)
    query = query.join(models.EmployeeTable, models.CustomerTable.support_rep_id == models.EmployeeTable.employee_id)

    # Filtering the result For given year and month
    query = query.filter(extract('month', models.InvoiceTable.invoice_date) == 8,
                         extract('year', models.InvoiceTable.invoice_date) == 2012)

    # Grouping by Employee Id
    query = query.group_by(models.CustomerTable.support_rep_id)

    # Sorting by total_sales and employee id
    query = query.order_by(desc("total_sales"), models.CustomerTable.support_rep_id)

    results = query.limit(number_of_employee)

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
            print("Employee ID \t\tName\t\tTotal Sales\n")

        print(f"{result.employee_id},\t\t {result.name},\t\t {result.total_sales}")
        print("\n")

    print("\n\n")
    print("==" * 50)

    session.close()
