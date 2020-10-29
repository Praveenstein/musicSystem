# -*- coding: utf-8 -*-
"""
ORM CLASSES FOR MUSIC SERVICE
===================================

Main module consisting of ORM classes for a music as a service system

This script contains all the class details required to perform the
orm_queries based SQL operations, it contains the following classes

    * TimestampMixin
    * GenreTable
    * MediaTypeTable
    * ArtistTable
    * AlbumTable
    * TracksTable
    * EmployeeTable
    * CustomerTable
    * InvoiceTable
    * InvoiceLineTable
    * PlaylistTable
    * PlaylistTrackTable

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries

"""

# External imports
from sqlalchemy import text, ForeignKey
from sqlalchemy.schema import FetchedValue
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER, NUMERIC, NVARCHAR, TIMESTAMP, DATETIME
from sqlalchemy.orm import relationship, backref

BASE = declarative_base()


class TimestampMixin:
    """
    Class to be inherited by other classes to get user trail attributes
    such as created_on and last_updated_on

    :ivar created_by: User who created this row
    :vartype created_by: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

    :ivar created_on: Timestamp for creation time
    :vartype created_on: class:`sqlalchemy.dialects.mysql.types.TIMESTAMP`

    :ivar last_updated_by: User who last updated the record
    :vartype last_updated_by: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

    :ivar last_updated_on: Timestamp for last updation
    :vartype: last_updated_on: class:`sqlalchemy.dialects.mysql.types.TIMESTAMP`

    """
    __table_args__ = {'mysql_engine': 'InnoDB'}

    created_by = Column(NVARCHAR(250), default="SYSTEM", nullable=False)
    created_on = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    last_updated_by = Column(NVARCHAR(250), default="SYSTEM", nullable=False)
    last_updated_on = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                             server_onupdate=FetchedValue(), nullable=False)


class GenreTable(TimestampMixin, BASE):
    """
    ORM class for the genre table

    :ivar genre_id: Primary key of Genre Table
    :vartype genre_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

    :ivar name: Name of genre
    :vartype name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

    :ivar tracks: List of all tracks that belongs to this genre
    :vartype tracks: list

    """

    __tablename__ = 'genre'

    genre_id = Column(INTEGER(unsigned=True), name="GenreId", primary_key=True, autoincrement=True, nullable=False)
    name = Column(NVARCHAR(120), name="Name")

    # Relationships
    tracks = relationship("TracksTable", backref=backref("genre"), cascade="all, delete, delete-orphan")


class MediaTypeTable(TimestampMixin, BASE):
    """
    ORM class for the Media Type table

    :ivar media_type_id: Primary key of MediaTypeId Table
    :vartype media_type_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

    :ivar name: Name of MediaTypeId
    :vartype name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

    :ivar tracks: List of all tracks that belongs to this MediaTypeId
    :vartype tracks: list

    """

    __tablename__ = 'mediatype'

    media_type_id = Column(INTEGER(unsigned=True), name="MediaTypeId", primary_key=True, autoincrement=True,
                           nullable=False)
    name = Column(NVARCHAR(120), name="Name")

    # Relationships
    tracks = relationship("TracksTable", backref=backref("media_type"), cascade="all, delete, delete-orphan")


class ArtistTable(TimestampMixin, BASE):
    """
    ORM class for the Artist table

    :ivar artist_id: Primary key of Artist Table
    :vartype artist_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

    :ivar name: Name of Artist
    :vartype name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

    :ivar albums: List of all albums that belongs to this Artist
    :vartype albums: list

    """

    __tablename__ = 'artist'

    artist_id = Column(INTEGER(unsigned=True), name="ArtistId", primary_key=True, autoincrement=True, nullable=False)
    name = Column(NVARCHAR(120), name="Name")

    # Relationships
    albums = relationship("AlbumTable", backref=backref("artist"), cascade="all, delete, delete-orphan")


class AlbumTable(TimestampMixin, BASE):
    """
    ORM class for the Album table

    :ivar album_id: Primary key of Album Table
    :vartype album_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

    :ivar title: Title of Album
    :vartype title: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

    :ivar artist_id: Foregin key representing the artist id involving in this album
    :vartype artist_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

    :ivar tracks: List of all tracks that belongs to this album
    :vartype tracks: list

    """

    __tablename__ = 'album'

    album_id = Column(INTEGER(unsigned=True), name="AlbumId", primary_key=True, autoincrement=True, nullable=False)
    title = Column(NVARCHAR(160), name="Title", nullable=False)

    # Foreign Key
    artist_id = Column(INTEGER(unsigned=True), ForeignKey('artist.ArtistId', onupdate="NO ACTION", ondelete="NO "
                                                                                                            "ACTION"),
                       name="ArtistId", nullable=False, index=True)

    # Relationships
    tracks = relationship("TracksTable", backref=backref("album"), cascade="all, delete, delete-orphan")


class TracksTable(TimestampMixin, BASE):
    """
     ORM class for the Tracks table

     :ivar track_id: Primary key of Track Table
     :vartype track_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar name: Name of Track
     :vartype name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar composer: Name of composer
     :vartype composer: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar milliseconds: Length of track in milliseconds
     :vartype milliseconds: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar bytes: size of tracks in bytes
     :vartype bytes: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar unit_price: unit price of track
     :vartype unit_price: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar album_id: Foregin key representing the album id this track belongs to
     :vartype album_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar media_type_id: Foregin key representing the mediatype this track belongs to
     :vartype media_type_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar genre_id: Foregin key representing the GenreId this track belongs to
     :vartype genre_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     """

    __tablename__ = 'track'

    track_id = Column(INTEGER(unsigned=True), name="TrackId", primary_key=True, autoincrement=True, nullable=False)

    # NVARCHAR types
    name = Column(NVARCHAR(200), name="Name", nullable=False)
    composer = Column(NVARCHAR(220), name="Composer")

    # Numeric and Integer Types
    milliseconds = Column(INTEGER(unsigned=True), name="Milliseconds", nullable=False)
    bytes = Column(INTEGER(unsigned=True), name="Bytes")
    unit_price = Column(NUMERIC(10, 2), name="UnitPrice", nullable=False)

    # Foreign Key Columns
    album_id = Column(INTEGER(unsigned=True), ForeignKey('album.AlbumId', onupdate="NO ACTION", ondelete="NO ACTION"),
                      name="AlbumId", nullable=False, index=True)
    media_type_id = Column(INTEGER(unsigned=True), ForeignKey('mediatype.MediaTypeId', onupdate="NO ACTION",
                                                              ondelete="NO ACTION"), name="MediaTypeId",
                           nullable=False, index=True)

    genre_id = Column(INTEGER(unsigned=True), ForeignKey('genre.GenreId', onupdate="NO ACTION", ondelete="NO ACTION"),
                      name="GenreId")


class EmployeeTable(TimestampMixin, BASE):
    """
     ORM class for the Employee Table

     :ivar employee_id: Primary key of Employee Table
     :vartype employee_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar last_name: Last Name of employee
     :vartype last_name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar first_name: First name of employee
     :vartype first_name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar title: Title of employee
     :vartype title: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar address: Address of employee
     :vartype address: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar city: City of employee
     :vartype city: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar state: State of employee
     :vartype state: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar country: Country of employee
     :vartype country: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar postal_code: PostalCode of employee
     :vartype postal_code: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar phone: Phone of employee
     :vartype phone: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar fax: Fax of employee
     :vartype fax: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar email: Email of employee
     :vartype email: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar birth_date: Birthdate of empolyee
     :vartype birth_date: class:`sqlalchemy.dialects.mysql.types.DATETIME`

     :ivar hire_date: HireDate of empolyee
     :vartype hire_date: class:`sqlalchemy.dialects.mysql.types.DATETIME`

     :ivar reports_to: Foregin Key representing the Manager to whom the emplyee reports to
     :vartype reports_to: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar manages: List of all employee the manager manages
     :vartype manages: list

     :ivar customer: List of customers the employee handles
     :vartype customer: list

     """

    __tablename__ = 'employee'

    employee_id = Column(INTEGER(unsigned=True), name="EmployeeId", primary_key=True, autoincrement=True,
                         nullable=False)

    # NVARCHAR data type
    last_name = Column(NVARCHAR(20), name="LastName", nullable=False)
    first_name = Column(NVARCHAR(20), name="FirstName", nullable=False)
    title = Column(NVARCHAR(30), name="Title")
    address = Column(NVARCHAR(70), name="Address")
    city = Column(NVARCHAR(40), name="City")
    state = Column(NVARCHAR(40), name="State")
    country = Column(NVARCHAR(40), name="Country")
    postal_code = Column(NVARCHAR(10), name="PostalCode")
    phone = Column(NVARCHAR(24), name="Phone")
    fax = Column(NVARCHAR(24), name="Fax")
    email = Column(NVARCHAR(24), name="Email")

    # DATETIME data type
    birth_date = Column(DATETIME, name="BirthDate")
    hire_date = Column(DATETIME, name="HireDate")

    # Foreign Key
    reports_to = Column(INTEGER(unsigned=True), ForeignKey("employee.EmployeeId", onupdate="NO ACTION",
                                                           ondelete="NO ACTION"), name="ReportsTo", index=True)

    # Relationships
    manages = relationship("EmployeeTable", backref=backref("manager", remote_side=[employee_id]))

    customers = relationship("CustomerTable", backref=backref("support_rep"), cascade="all, delete, delete-orphan")


class CustomerTable(TimestampMixin, BASE):
    """
     ORM class for the Customer Table

     :ivar customer_id: Primary key of Customer Table
     :vartype customer_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar last_name: Last Name of employee
     :vartype last_name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar first_name: First name of employee
     :vartype first_name: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar company: Company of employee
     :vartype company: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar address: Address of employee
     :vartype address: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar city: City of employee
     :vartype city: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar state: State of employee
     :vartype state: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar country: Country of employee
     :vartype country: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar postal_code: PostalCode of employee
     :vartype postal_code: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar phone: Phone of employee
     :vartype phone: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar fax: Fax of employee
     :vartype fax: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar email: Email of employee
     :vartype email: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

     :ivar support_rep_id: Foreign Key representing the Employee who handles this customer
     :vartype support_rep_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

     :ivar manages: List of all employee the manager manages
     :vartype manages: list

     :ivar invoices: List of invoices in which this customer was involved
     :vartype invoices: list

     """

    __tablename__ = 'customer'

    # Primary Key
    customer_id = Column(INTEGER(unsigned=True), name="CustomerId", primary_key=True, autoincrement=True,
                         nullable=False)

    # NVARCHAR data type
    last_name = Column(NVARCHAR(20), name="LastName", nullable=False)
    first_name = Column(NVARCHAR(40), name="FirstName", nullable=False)
    company = Column(NVARCHAR(80), name="Company")
    address = Column(NVARCHAR(70), name="Address")
    city = Column(NVARCHAR(40), name="City")
    state = Column(NVARCHAR(40), name="State")
    country = Column(NVARCHAR(40), name="Country")
    postal_code = Column(NVARCHAR(10), name="PostalCode")
    phone = Column(NVARCHAR(24), name="Phone")
    fax = Column(NVARCHAR(24), name="Fax")
    email = Column(NVARCHAR(60), name="Email", nullable=False)

    # Foreign Key
    support_rep_id = Column(INTEGER(unsigned=True), ForeignKey("employee.EmployeeId", onupdate="NO ACTION",
                                                               ondelete="NO ACTION"), name="SupportRepId", index=True)

    # Relationships
    invoices = relationship("InvoiceTable", backref=backref("customer"), cascade="all, delete, delete-orphan")


class InvoiceTable(TimestampMixin, BASE):
    """
      ORM class for the Invoice Table

      :ivar invoice_id: Primary key of Invoice Table
      :vartype invoice_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar billing_address: BillingAddress of invoice
      :vartype billing_address: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

      :ivar billing_city: BillingCity of invoice
      :vartype billing_city: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

      :ivar billing_state: BillingState of invoice
      :vartype billing_state: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

      :ivar billing_country: BillingCountry of invoice
      :vartype billing_country: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

      :ivar billing_postal_code: BillingPostalCode of invoice
      :vartype billing_postal_code: class:`sqlalchemy.dialects.mysql.types.NVARCHAR`

      :ivar invoice_date: Date of invoice
      :vartype invoice_date: class:`sqlalchemy.dialects.mysql.types.DATETIME`

      :ivar total: Total cost of invoice
      :vartype total: class:`sqlalchemy.dialects.mysql.types.NUMERIC`

      :ivar customer_id: Foreign key representing the customer involved in this invoive
      :vartype customer_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar purchased_tracks: List of tracks involved in this invoice
      :vartype purchased_tracks: list

      """

    __tablename__ = 'invoice'

    # Primary Key
    invoice_id = Column(INTEGER(unsigned=True), name="InvoiceId", primary_key=True, autoincrement=True, nullable=False)

    # NVARCHAR data type
    billing_address = Column(NVARCHAR(70), name="BillingAddress")
    billing_city = Column(NVARCHAR(40), name="BillingCity")
    billing_state = Column(NVARCHAR(40), name="BillingState")
    billing_country = Column(NVARCHAR(40), name="BillingCountry")
    billing_postal_code = Column(NVARCHAR(10), name="BillingPostalCode")

    # DATETIME data type
    invoice_date = Column(DATETIME, name="InvoiceDate", nullable=False)

    # Numeric Data Type
    total = Column(NUMERIC(10, 2), name="Total", nullable=False)

    # Foreign Key
    customer_id = Column(INTEGER(unsigned=True), ForeignKey("customer.CustomerId", onupdate="NO ACTION",
                                                            ondelete="NO ACTION"), name="CustomerId",
                         nullable=False, index=True)

    # Relationships
    purchased_tracks = relationship("TracksTable", backref=backref("invoices"), secondary="invoiceline")


class InvoiceLineTable(TimestampMixin, BASE):
    """
      ORM class for the InvoiceLine Table

      :ivar invoice_line_id: Primary key of InvoiceLine Table
      :vartype invoice_line_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar unit_price: unit price of tracks
      :vartype unit_price: class:`sqlalchemy.dialects.mysql.types.NUMERIC`

      :ivar quantity: quantity of purchase of given track
      :vartype quantity: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar invoice_id: Foreign key representing the invoice id
      :vartype invoice_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar track_id: Foreign key representing the track id involved
      :vartype track_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar invoice: The invoice which was involved in this invoice line
      :vartype invoice: :class:`mservice.database_model.ORMClasses.InvoiceTable`

      :ivar track: The track which was involved in this invoice line
      :vartype track: :class:`mservice.database_model.ORMClasses.TracksTable`

      """

    __tablename__ = 'invoiceline'

    # Primary key
    invoice_line_id = Column(INTEGER(unsigned=True), name="InvoiceLineId", primary_key=True, autoincrement=True,
                             nullable=False)

    # Numeric & Int type
    unit_price = Column(NUMERIC(10, 2), name="UnitPrice", nullable=False)
    quantity = Column(INTEGER(unsigned=True), name="Quantity", nullable=False)

    # Foreign Key
    invoice_id = Column(INTEGER(unsigned=True), ForeignKey("invoice.InvoiceId", onupdate="NO ACTION",
                                                           ondelete="NO ACTION"), name="InvoiceId",
                        nullable=False, index=True)

    track_id = Column(INTEGER(unsigned=True), ForeignKey("track.TrackId", onupdate="NO ACTION", ondelete="NO ACTION"),
                      name="TrackId", nullable=False, index=True)

    # Relationships
    invoice = relationship("InvoiceTable", backref=backref("track_associations", cascade="all, delete, delete-orphan"))
    track = relationship("TracksTable", backref=backref("invoice_associations", cascade="all, delete, delete-orphan"))


class PlaylistTable(TimestampMixin, BASE):
    """
      ORM class for the Playlist Table

      :ivar play_list_id: Primary key of Playlist Table
      :vartype play_list_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar name: The name of playlist
      :vartype name:`sqlalchemy.dialects.mysql.types.NVARCHAR`

      :ivar tracks_in_playlist: List of tracks in this playlist
      :vartype tracks_in_playlist: list

      """

    __tablename__ = 'playlist'

    play_list_id = Column(INTEGER(unsigned=True), name="PlaylistId", primary_key=True, autoincrement=True,
                          nullable=False)
    name = Column(NVARCHAR(120), name="Name")

    # Relationships
    tracks_in_playlist = relationship("TracksTable", backref=backref("playlist_involved"), secondary="playlisttrack")


class PlaylistTrackTable(TimestampMixin, BASE):
    """
      ORM class for the PlaylistTrack Table

      :ivar play_list_id: Primary key of PlaylistTrack Table, which is also a foreign key
      :vartype play_list_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar track_id: Primary key of PlaylistTrack Table, which is also a foreign key
      :vartype track_id: class:`sqlalchemy.dialects.mysql.types.INTEGER`

      :ivar playlist: The playlist which is involved in this playlist track table record
      :vartype playlist: :class:`mservice.database_model.ORMClasses.PlaylistTable`

      :ivar track: The track which was involved in this this playlist track table record
      :vartype track: :class:`mservice.database_model.ORMClasses.TracksTable`

      """

    __tablename__ = 'playlisttrack'

    play_list_id = Column(INTEGER(unsigned=True), ForeignKey("playlist.PlaylistId", onupdate="NO ACTION",
                                                             ondelete="NO ACTION"), name="PlaylistId",
                          nullable=False, primary_key=True)

    track_id = Column(INTEGER(unsigned=True), ForeignKey("track.TrackId", onupdate="NO ACTION", ondelete="NO ACTION"),
                      name="TrackId", nullable=False, primary_key=True, index=True)

    # Relationships
    playlist = relationship("PlaylistTable", backref=backref("track_association", cascade="all, delete, delete-orphan"))
    track = relationship("TracksTable", backref=backref("playlist_association", cascade="all, delete, delete-orphan"))
