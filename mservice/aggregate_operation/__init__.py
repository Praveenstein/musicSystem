# -*- coding: UTF-8 -*-
"""
Initialization For Read Records for aggregate_operation Package
===================================================================


This is an initialization module for aggregate operataions
"""

# Importing necessary modules and functions to be used by modules using this package
from mservice.aggregate_operation.top_album_tracks_q1 import get_top_album_tracks
from mservice.aggregate_operation.top_artist_tracks_q2 import get_top_artist_tracks
from mservice.aggregate_operation.top_customer_amount_q3 import get_top_customers
from mservice.aggregate_operation.top_album_purchases_q4 import get_top_album_purchases
from mservice.aggregate_operation.top_tracks_for_genre_q5 import get_top_tracks_for_genre
from mservice.aggregate_operation.longest_tracks_q6 import get_longest_tracks
from mservice.aggregate_operation.longest_album_q7 import get_longest_album
from mservice.aggregate_operation.number_of_playlist_tracks_q8 import get_number_of_playlist_tracks
from mservice.aggregate_operation.number_of_playlist_album_q9 import get_number_of_playlist_album
from mservice.aggregate_operation.top_artist_distinct_genre_q13 import get_top_artist_genre
from mservice.aggregate_operation.top_employee_month_q14 import get_top_employee_sales
from mservice.aggregate_operation.top_manager_month_q15 import get_top_manager_revenue
from mservice.aggregate_operation.add_genre_to_album_q11 import add_genre_to_album
from mservice.aggregate_operation.add_genre_to_artist_q12 import add_genre_to_artist
from mservice.aggregate_operation.tracks_with_more_genre_q10 import get_tracks_with_more_genre
