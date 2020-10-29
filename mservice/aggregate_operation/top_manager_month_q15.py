# -*- coding: utf-8 -*-
"""
Module to Find Top Manager with Highest Total Revenue in a Month
======================================================================

Module for reading records from the database to Find Top Manager with Highest Revenue in a Month

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * get_top_manager_revenue - Function to perform read operation with the database to Find Top Manager with
                             Highest Total Revenue in a Month
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm
from sqlalchemy import desc, func, extract
from sqlalchemy.orm import aliased

# User Imports
from tabulate import tabulate

import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def get_top_manager_revenue(session, number_of_manager):
    """
    Function to perform read operation with the database to Find Top Manager with Highest Total Revenue in a Month

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :param number_of_manager: The number of managers to be returned from the query
    :type number_of_manager: int

    :return: Nothing
    :rtype: None

    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(number_of_manager), int) or number_of_manager < 1:
        raise AttributeError("number of Managers should be integer and greater than 0")

    LOGGER.info("Performing Read Operation")

    # Creating an alias for manager and employee Since they both are from same table and needs to self reference
    manager = aliased(models.EmployeeTable)
    employee = aliased(models.EmployeeTable)

    # Selecting the Manager Id, Manager Name, And his Total Revenue, By summing all his invoice total
    query = session.query(employee.reports_to.label("manager_id"),
                          func.concat(manager.first_name, " ", manager.last_name).label("manager_name"),
                          func.sum(models.InvoiceTable.total).label("total_revenue"))

    # Joining the customer table with invoice table, and with the previously aliased employee and manager table
    query = query.join(models.CustomerTable, models.InvoiceTable.customer_id == models.CustomerTable.customer_id)
    query = query.join(employee, models.CustomerTable.support_rep_id == employee.employee_id)
    query = query.join(manager, employee.reports_to == manager.employee_id)

    # Filtering out the invoices which occurred in month 8 and year 2012
    query = query.filter(extract('month', models.InvoiceTable.invoice_date) == 8,
                         extract('year', models.InvoiceTable.invoice_date) == 2012)

    # Grouping by Manager Id
    query = query.group_by("manager_id")

    # Sorting By total revenue
    query = query.order_by(desc("total_revenue"))

    results = query.limit(number_of_manager).all()

    LOGGER.info("\n\nThe Top %s Manager with Most Sales in Year: 2012 and Month: 08", number_of_manager)

    print("\n\n")
    print("===" * 50)
    print("\n\n")

    print(tabulate(results, headers=["Manager ID", "Manager Name", "Total Revenue"], tablefmt="grid"))

    print("\n\n")
    print("===" * 50)
    print("\n\n")

    session.close()
