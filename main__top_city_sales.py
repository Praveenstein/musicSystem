# -*- coding: utf-8 -*-
"""
Read Operation Top Customers Main
=====================================

Main Module for reading records in the chinook database to get the top customers

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to call appropriate functions to get top customers
"""
# Standard imports
import logging

# User Imports
import mservice.utils as helper
import mservice.connections as connections
import mservice.read_operation as db_read

LOGGER = logging.getLogger(__name__)


def main():
    """
    Main function to read records from the database using join operations

    :return: Nothing
    :rtype: None
    """

    # Getting the path for logging config using arparse
    log_config_file = helper.ARGUMENTS.logfile

    # Configuring logging
    helper.configure_logging(log_config_file)

    try:
        # Getting a new engine
        engine = connections.create_new_engine(helper.ARGUMENTS.dialect, helper.ARGUMENTS.driver,
                                               helper.ARGUMENTS.user, helper.ARGUMENTS.password,
                                               helper.ARGUMENTS.host, helper.ARGUMENTS.database)

        # Getting a session factory binded to previously created engine
        session_factory = connections.get_session_factory(engine)
        session_1 = session_factory()
        session_2 = session_factory()

        # Calling function to get the top city based on number of invoices
        db_read.get_top_city_sales(session_1)
        print("\n\n")

        # calling function to get top city based on invoice total
        db_read.get_top_city_profit(session_2)
    except AttributeError as err:
        LOGGER.error(err)


if __name__ == '__main__':
    main()
