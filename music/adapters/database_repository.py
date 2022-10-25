from abc import ABC
from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from music.domainmodel.track import User, Track, Review
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre import Genre
from music.domainmodel.playlist import PlayList
from music.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User.user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def get_album_by_id(self, album_id):
        albums = self._session_cm.session.query(Album).filter(Album.album_id.in_(album_id))
        return albums

    def get_artist_by_id(self, artist_id):
        artist = self._session_cm.session.query(Artist).filter(Artist.artist_id.in_(artist_id))
        return artist

    def get_number_of_tracks(self) -> int:
        num = self._session_cm.session.query(Track).count()
        return num

    def get_number_of_users(self):
        num = self._session_cm.session.query(User).count()
        return num

    def get_reviews(self):
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def get_track_by_id(self, track_id):
        track = self._session_cm.query(Track).filter(Track.track_id.in_(track_id))
        return track

    def get_tracks(self):
        tracks = self._session_cm.session.query(Track).all()
        return tracks

