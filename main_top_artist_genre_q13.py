# -*- coding: utf-8 -*-
"""
Top Artist Who have Most Distinct Genres Main
========================================================

Main for reading records from the database to get the Top Artist Who have Most Distinct Genres

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to perform read operation with the database to get the Top Artist Who have
             Most Distinct Genres
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
    Main function to read records from the database to get the Top Artist Who have Most Distinct Genres

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

        db_aggregate.get_top_artist_genre(session, helper.ARGUMENTS.number)
    except AttributeError as err:
        LOGGER.error(err)


if __name__ == '__main__':
    main()
