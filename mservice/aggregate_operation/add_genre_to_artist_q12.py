# -*- coding: utf-8 -*-
"""
Module to Add Genre Tags to Artist
==========================================

Module for reading records from the database to create a pandas dataframe to add Genre Tags to Artist

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * add_genre_to_artist - Function to add Genre Tags to Artist
"""
# Standard Imports
import logging

# External imports
import sqlalchemy
import pandas as pd

LOGGER = logging.getLogger(__name__)


def add_genre_to_artist(engine, number_of_artist):
    """
    Function to to add Genre Tags to Artist

    :param engine: The engine to work with
    :type engine: :class:`sqlalchemy.engine.base.Engine`

    :param number_of_artist: The number of albums to be returned from the query
    :type number_of_artist: int

    :return: Nothing
    :rtype: None
    """
    try:
        if not issubclass(type(engine), sqlalchemy.engine.base.Engine):
            raise AttributeError("Engine not passed correctly, should be of type 'sqlalchemy.engine.base.Engine' ")

        if not issubclass(type(number_of_artist), int) or number_of_artist < 1:
            raise AttributeError("number of artist should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        sql_stmt = f"""
                        SELECT DISTINCT 
                            art.Name AS artist ,
                            g.Name AS genre	   
                        FROM track t
                        INNER JOIN genre g
                            ON t.GenreId = g.GenreId
                        INNER JOIN album a
                            ON t.AlbumId = a.AlbumId
                        INNER JOIN artist art
                            ON a.ArtistId = art.ArtistId
                        -- WHERE a.ArtistId = 6 
                        ORDER BY a.ArtistId
                        LIMIT {number_of_artist}
                    """

        with engine.connect() as connection:
            artists_df = pd.read_sql(sql_stmt, connection)

        print("\n\n")
        print("==" * 50)

        LOGGER.info("\n\n %s", artists_df)

        print("\n\n")
        print("==" * 50)
    except AttributeError as err:
        LOGGER.error(err)
