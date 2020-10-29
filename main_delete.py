# -*- coding: utf-8 -*-
"""
Delete Operation Main
========================

Main Module for deleting records in the chinook database in genre table, which would also result in delete cascade of
related objects

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to call appropriate functions to perform the delete operation
"""

# Standard imports
import logging

# User Imports
import mservice.utils as helper
import mservice.connections as connections
import mservice.delete_operation as db_delete

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
    session = session_factory()

    db_delete.perform_delete(session)


if __name__ == '__main__':
    main()
