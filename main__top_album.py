# -*- coding: utf-8 -*-
"""
Read Operation Top Album Main
================================

Main Module for reading records in the chinook database to get the top albums

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to call appropriate functions to perform the read operation to get the top albums
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
    Main function to read records from the database to get the top albums

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
        session = session_factory()

        db_read.get_top_album(session)
    except AttributeError as err:
        LOGGER.error(err)


if __name__ == '__main__':
    main()
