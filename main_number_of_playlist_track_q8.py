# -*- coding: utf-8 -*-
"""
Number of Playlist a Track has been Added to Main
========================================================

Main for reading records from the database to get the number of playlist a track has been added to

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function

    * main - main function to perform read operation with the database to get the number of playlist a track has
             been added to
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
    Main function to read records from the database to get the number of playlist a track has been added to

    :return: Nothing
    :rtype: None
    """

    # Getting the path for logging config using arparse
    log_config_file = helper.ARGUMENTS.logfile

    # Configuring logging
    helper.configure_logging(log_config_file)

    # Getting a new engine
    engine = connections.create_new_engine(helper.ARGUMENTS.dialect, helper.ARGUMENTS.driver,
                                           helper.ARGUMENTS.user, helper.ARGUMENTS.password,
                                           helper.ARGUMENTS.host, helper.ARGUMENTS.database)

    # Getting a session factory binded to previously created engine
    session_factory = connections.get_session_factory(engine)
    session = session_factory()

    db_aggregate.get_number_of_playlist_tracks(session, helper.ARGUMENTS.number)


if __name__ == '__main__':
    main()
