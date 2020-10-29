# -*- coding: utf-8 -*-
"""
Module to perform Create operation
========================================

Main Module for creating new records for the genre table, tracks, invoice and invoiceliine tables

This script requires the following modules be installed in the python environment
    * logging - to perform logging operations

This script contains the following function
    * create_new_genre - function to create a new genre record in the genre table
    * create_new_track - function to create a new track record in the track table, with the previously created genre
    * create_new_invoice - function to create a new invoice record in the invoice table
    * create_new_invoiceline - function to create a new invoiceline record in the invoiceline table, with previously
                               created track and invoice
    * perform_create - function to invokes all the above function
"""
# Standard Imports
import logging

# External imports
import sqlalchemy.orm

# User Imports
import mservice.database_model as models

LOGGER = logging.getLogger(__name__)


def create_new_genre(session):
    """
    Function to create a new genre record in the genre table

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :return: genre_id
    :rtype: int
    """

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Creating New Genre")

    new_genre = models.GenreTable(name="NEW_GENRE")

    session.add(new_genre)
    session.flush()
    genre_id = new_genre.genre_id
    session.commit()
    session.close()
    return genre_id


def create_new_track(session, genre_id):
    """
    Function to create a new track record in the track table, with the previously created genre

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :param genre_id: The genre Id to which the track has to associated with
    :type genre_id: int

    :return: track_id
    :rtype: int
    """
    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(genre_id), int):
        raise AttributeError("Genre Id is not of type Int")

    LOGGER.info("Creating New Track")

    new_track = models.TracksTable(name="For Those About To Rock (We Salute You)", album_id=1, media_type_id=1,
                                   genre_id=genre_id, composer="Angus Young, Malcolm Young, Brian Johnson",
                                   milliseconds=343719, bytes=11170334, unit_price=99)

    session.add(new_track)
    session.flush()
    track_id = new_track.track_id
    session.commit()
    session.close()
    return track_id


def create_new_invoice(session):
    """
    Function to create a new invoice record in the invoice table

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :return: invoice_id
    :rtype: int
    """
    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    LOGGER.info("Creating New Track")

    new_invoice = models.InvoiceTable(invoice_date="2020-10-22", total=1.98, customer_id=1)

    session.add(new_invoice)
    session.flush()
    invoice_id = new_invoice.invoice_id
    session.commit()
    session.close()
    return invoice_id


def create_new_invoiceline(session, track_id, invoice_id):
    """
    Function to create a new invoiceline record in the invoiceline table, with previously created track and invoice

    :param session: The session to work with
    :type session: :class:`sqlalchemy.orm.session.Session`

    :param track_id: The track id previously created, that needs to be added to the invoiceline
    :type track_id: int

    :param invoice_id: The invoice id previously craeted, that needs to be referenced in the invoiceline
    :type invoice_id: int

    :return: new_invoiceline_1_id, new_invoiceline_2_id - The id of newly created invoicelines
    :rtype: int
    """
    LOGGER.info("Creating New Track")

    if not issubclass(type(session), sqlalchemy.orm.session.Session):
        raise AttributeError("session not passed correctly, should be of type 'sqlalchemy.orm.session.Session' ")

    if not issubclass(type(track_id), int):
        raise AttributeError("Track Id is not of type Int")

    if not issubclass(type(invoice_id), int):
        raise AttributeError("Invoice Id is not of type Int")

    new_invoiceline_1 = models.InvoiceLineTable(unit_price=0.99, quantity=1, invoice_id=invoice_id, track_id=track_id)
    new_invoiceline_2 = models.InvoiceLineTable(unit_price=0.99, quantity=1, invoice_id=invoice_id, track_id=2)

    session.add_all([new_invoiceline_1, new_invoiceline_2])
    session.flush()
    new_invoiceline_2_id = new_invoiceline_2.invoice_line_id
    new_invoiceline_1_id = new_invoiceline_1.invoice_line_id
    session.commit()
    session.close()
    return new_invoiceline_1_id, new_invoiceline_2_id


def perform_create(session_factory):
    """
    Function to invokes all the above function to perform a set of create operations

    :param session_factory: The session factory used to create new session to be passed to other functions
    :type session_factory: :class:`sqlalchemy.orm.session.sessionmaker`

    :return: Nothing
    :rtype: None
    """

    if not issubclass(type(session_factory), sqlalchemy.orm.session.sessionmaker):
        raise AttributeError("Session Maker not passed properly, correct type 'sqlalchemy.orm.session.sessionmaker' ")

    session = session_factory()
    new_genre_id = create_new_genre(session)

    if not issubclass(type(new_genre_id), int):
        raise AttributeError("Returned Genre Id is not of type Int")

    session = session_factory()
    new_track_id = create_new_track(session, new_genre_id)

    if not issubclass(type(new_track_id), int):
        raise AttributeError("Returned Track Id is not of type Int")

    session = session_factory()
    new_invoice_id = create_new_invoice(session)

    if not issubclass(type(new_invoice_id), int):
        raise AttributeError("Returned Track Id is not of type Int")

    session = session_factory()
    new_invoiceline_1_id, new_invoiceline_2_id = create_new_invoiceline(session, new_track_id, new_invoice_id)

    if not issubclass(type(new_invoiceline_1_id), int) or not issubclass(type(new_invoiceline_2_id), int):
        raise AttributeError("Returned invoiceline Id is not of type Int")

    LOGGER.info("The ID of new Genre: %s", new_genre_id)
    LOGGER.info("The ID of new Track: %s", new_track_id)
    LOGGER.info("The ID of new Invoice: %s", new_invoice_id)
    LOGGER.info("The ID of new Invoiceline_1_id: %s", new_invoiceline_1_id)
    LOGGER.info("The ID of new Invoiceline_2_id: %s", new_invoiceline_2_id)
