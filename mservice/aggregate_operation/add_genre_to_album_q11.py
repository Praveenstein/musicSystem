# -*- coding: utf-8 -*-
"""
Module to Add Genre Tags to Albums
==========================================

Module for reading records from the database to create a pandas dataframe to add Genre Tags to Albums

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * add_genre_to_album - Function to add Genre Tags to Albums
"""
# Standard Imports
import logging

# External imports
import sqlalchemy
import pandas as pd

LOGGER = logging.getLogger(__name__)


def add_genre_to_album(engine, number_of_albums):
    """
    Function to to add Genre Tags to Albums

    :param engine: The engine to work with
    :type engine: :class:`sqlalchemy.engine.base.Engine`

    :param number_of_albums: The number of albums to be returned from the query
    :type number_of_albums: int

    :return: Nothing
    :rtype: None
    """
    try:
        if not issubclass(type(engine), sqlalchemy.engine.base.Engine):
            raise AttributeError("Engine not passed correctly, should be of type 'sqlalchemy.engine.base.Engine' ")

        if not issubclass(type(number_of_albums), int) or number_of_albums < 1:
            raise AttributeError("number of albums should be integer and greater than 0")

        LOGGER.info("Performing Read Operation")

        sql_stmt = f"""
                        SELECT DISTINCT
                            a.title AS album,
                            g.Name AS genre	  
                        FROM track t
                        INNER JOIN album a
                            ON t.AlbumId = a.AlbumId
                        INNER JOIN genre g
                            ON t.GenreId = g.GenreId
                        -- WHERE t.AlbumId = 102 OR t.AlbumId = 251 
                        ORDER BY t.AlbumId
                        LIMIT {number_of_albums}
                    """

        with engine.connect() as connection:
            albums_df = pd.read_sql(sql_stmt, connection)

        print("\n\n")
        print("==" * 50)

        print(albums_df)

        print("\n\n")
        print("==" * 50)
    except AttributeError as err:
        LOGGER.error(err)
