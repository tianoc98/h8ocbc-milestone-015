from datetime import datetime
from config import db, ma
from marshmallow import fields

class Directors(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    gender = db.Column(db.Integer)
    uid = db.Column(db.Integer)
    department = db.Column(db.String(32))
    movies = db.relationship(
        'Movies',
        backref='directors',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Movies.id)'
    )

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(32))
    budget = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.Date)
    revenue =  db.Column(db.Integer)
    title = db.Column(db.String(32))
    vote_average =  db.Column(db.Float())
    overview =  db.Column(db.String(32))
    tagline = db.Column(db.String(32))
    uid = db.Column(db.Integer)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))
    
class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Directors
        sqla_session = db.session
        load_instance = True

    movies = fields.Nested('DirectorsMoviesSchema', default=[], many=True)

class DirectorsMoviesSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    original_title = fields.Str()
    budget = fields.Int()
    popularity = fields.Int()
    release_date = fields.Str()
    revenue =  fields.Int()
    title = fields.Str()
    vote_average =  fields.Int()
    overview =  fields.Str()
    tagline = fields.Str()
    uid = fields.Int()
    director_id = fields.Int()


class MoviesSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Movies
        sqla_session = db.session
        load_instance = True


class MoviesDirectorSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    name = fields.Str()
    gender = fields.Str()
    uid = fields.Int()
    department = fields.Str()