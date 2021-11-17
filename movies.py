"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Directors, Movies, MoviesSchema


def read_all():

    # Query the database for all the notes
    movies = Movies.query.order_by(Movies.id).all()

    # Serialize the list of notes from our data
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data

def get_popularity():

    # Query the database for all the notes
    movies = Movies.query.order_by(db.desc(Movies.popularity)).all()

    # Serialize the list of notes from our data
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data

def get_budget():

    # Query the database for all the notes
    movies = Movies.query.order_by(db.desc(Movies.budget)).all()

    # Serialize the list of notes from our data
    movies_schema = MoviesSchema(many=True)
    data = movies_schema.dump(movies)
    return data

def get_name(initial):

    # Query the database for all the notes
    movies = Movies.query.filter(Movies.original_title.like(initial+'%')).all()

    if movies is not None:
        # Serialize the list of notes from our data
        movies_schema = MoviesSchema(many=True)
        data = movies_schema.dump(movies)
        return data
    else:
        abort(404, f"Movies dengan initial {initial} not found")
        
def read_one(directors_id, movies_id):

    # Query the database for the note
    note = (
        Movies.query.join(Directors, Directors.id == Movies.director_id)
        .filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Was a note found?
    if note is not None:
        note_schema = MoviesSchema()
        data = note_schema.dump(note)
        return data

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"movies not found for Id: {movies_id}")


def create(directors_id, movies):
    
    # get the parent person
    person = Directors.query.filter(Directors.id == directors_id).one_or_none()

    # Was a person found?
    if person is None:
        abort(404, f"Person not found for Id: {directors_id}")

    # Create a note schema instance
    schema = MoviesSchema()
    new_note = schema.load(movies, session=db.session)

    # Add the note to the person and database
    person.movies.append(new_note)
    db.session.commit()

    # Serialize and return the newly created note in the response
    data = schema.dump(new_note)

    return data, 201


def update(directors_id, movies_id, movies):

    update_note = (
        Movies.query.filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # Did we find an existing note?
    if update_note is not None:

        # turn the passed in note into a db object
        schema = MoviesSchema()
        update = schema.load(movies, session=db.session)

        # Set the id's to the note we want to update
        update.id = update_note.id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated note in the response
        data = schema.dump(update_note)

        return data, 200

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Note not found for Id: {movies_id}")


def delete(directors_id, movies_id):

    # Get the note requested
    note = (
        Movies.query.filter(Directors.id == directors_id)
        .filter(Movies.id == movies_id)
        .one_or_none()
    )

    # did we find a note?
    if note is not None:
        db.session.delete(note)
        db.session.commit()
        return make_response(
            f"movies {movies_id} deleted", 200
        )

    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Note not found for Id: {movies_id}")