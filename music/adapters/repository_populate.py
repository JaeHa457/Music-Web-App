from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import create_track_object, create_artist_object, create_album_object, extract_genres, TrackCSVReader, load_users


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load articles and tags into the repository.

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.