# -*- coding: utf-8 -*-
"""
Create Operation Main
========================

Main Module for creating new records in the chinook database in genre, tracks, invoice and invoiceline table

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to call appropriate functions to perform the create operation
"""

# Standard imports
import logging

# User Imports
import mservice.utils as helper
import mservice.connections as connections
import mservice.create_operation as db_create

LOGGER = logging.getLogger(__name__)


def main():
    """
    Main function to perform the create operation

    :return: Nothing
    :rtype: None
    """

    # Getting the path for logging config using arparse
    log_config_file = helper.ARGUMENTS.logfile

    # Configuring logging
    helper.configure_logging(log_config_file)

    engine = connections.create_new_engine(helper.ARGUMENTS.dialect, helper.ARGUMENTS.driver,
                                           helper.ARGUMENTS.user, helper.ARGUMENTS.password,
                                           helper.ARGUMENTS.host, helper.ARGUMENTS.database)

    session_factory = connections.get_session_factory(engine)

    db_create.perform_create(session_factory)


if __name__ == '__main__':
    main()
