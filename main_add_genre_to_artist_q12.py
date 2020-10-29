# -*- coding: utf-8 -*-
"""
Module to Add Genre Tags to Artist Main
===============================================

Main Module for reading records from the database to create a pandas dataframe to add Genre Tags to Artist

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to add Genre Tags to Artist
"""
# Standard imports
import logging

# User Imports
import mservice.utils as helper
import mservice.connections as connections
import mservice.aggregate_operation as db_aggregate

LOGGER = logging.getLogger(__name__)


def main():
    """
    Main function to to add Genre Tags to Artist

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

        db_aggregate.add_genre_to_artist(engine, helper.ARGUMENTS.number)
    except AttributeError as err:
        LOGGER.error(err)


if __name__ == '__main__':
    main()
