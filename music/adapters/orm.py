from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel import album, artist, genre, playlist, track

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('user_name', String(255), unique=True, nullable=False),
                    Column('password', String(255), nullable=False)
                    )

reviews_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('track_id', ForeignKey('tracks.id')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False),
)

tracks_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('artist_id', Integer, ForeignKey('artists.id')),
    Column('duration', Integer, nullable=False),
    Column('url', String(255), nullable=False),
    Column('album', String(255), nullable=False)
)

albums_table = Table(
    'albums', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release year', Integer, nullable=False),
    Column('album url', String(255), nullable=False),
    Column('type', String(255), nullable=False)
)

artists_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False)
)


def map_model_to_tables():
    mapper(track.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__user_id': users_table.c.id
    })
    mapper(track.Review, reviews_table, properties={
        '_Review__review_text': reviews_table.c.comment,
        '_Review__review_track': relationship(track.Track, backref='_tracks__title')
    })
    mapper(track.Track, tracks_table, properties={
        '_Track__track_id': tracks_table.c.id,
        '_Track__title': tracks_table.c.title,
        '_Track__artist': tracks_table.c.artist_id,
        '_Track__track_url': tracks_table.c.url,
        '_Track__album': tracks_table.c.album
    })
    mapper(album.Album, albums_table, properties={
        '_Album__album_id': albums_table.c.id,
        '_Album__title': albums_table.c.title,
        '_Album__album_type': albums_table.c.type
    })
    mapper(artist.Artist, artists_table, properties={
        '_Artist__artist_id': artists_table.c.id,
        '_Artist__full_name': artists_table.c.name
    })
