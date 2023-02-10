# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movie_schema = MovieSchema()
director_schema = DirectorSchema()
genre_schema = GenreSchema()


@app.route('/')
def main_page():
    return 'Главная страница', 200


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        request_director_id = request.args.get('director_id')
        request_genre_id = request.args.get('genre_id')
        print(request_director_id, request_genre_id)
        if not request.args:
            movies = movie_schema.dump(Movie.query.all(), many=True)
        elif request_director_id and request_genre_id:
            movies = movie_schema.dump(Movie.query.filter(
                Movie.director_id == request_director_id,
                Movie.genre_id == request_genre_id).all(), many=True)
        elif request_director_id:
            movies = movie_schema.dump(Movie.query.filter(Movie.director_id == request_director_id).all(), many=True)
        elif request_genre_id:
            movies = movie_schema.dump(Movie.query.filter(Movie.genre_id == request_genre_id).all(), many=True)
        return movies

    def post(self):
        post_data = request.json
        new_movie = Movie(**post_data)
        db.session.add(new_movie)
        db.session.commit()
        return '', 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        movie = movie_schema.dump(Movie.query.get(mid))
        return movie

    def put(self, mid):
        movie_data = Movie.query.get(mid)
        new_data = request.json
        movie_data.title = new_data['title']
        movie_data.description = new_data['description']
        movie_data.trailer = new_data['trailer']
        movie_data.year = new_data['year']
        movie_data.rating = new_data['rating']
        movie_data.genre_id = new_data['genre_id']
        movie_data.director_id = new_data['director_id']
        db.session.add(movie_data)
        db.session.commit()
        return '', 201

    def delete(self, mid):
        db.session.query(Movie).filter(Movie.id == mid).delete()
        db.session.commit()
        return '', 201


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = director_schema.dump(Director.query.all(), many=True)
        return directors

    def post(self):
        post_data = request.json
        new_director = Director(**post_data)
        db.session.add(new_director)
        db.session.commit()
        return '', 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        director = director_schema.dump(Director.query.get(did))
        return director

    def put(self, did):
        director_data = Director.query.get(did)
        new_data = request.json
        director_data.name = new_data['name']
        db.session.add(director_data)
        db.session.commit()
        return '', 201

    def delete(self, did):
        db.session.query(Director).filter(Director.id == did).delete()
        db.session.commit()
        return '', 201


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = genre_schema.dump(Genre.query.all(), many=True)
        return genres

    def post(self):
        post_data = request.json
        new_genre = Genre(**post_data)
        db.session.add(new_genre)
        db.session.commit()
        return '', 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        genre = genre_schema.dump(Genre.query.get(gid))
        return genre

    def put(self, gid):
        genre_data = Genre.query.get(gid)
        new_data = request.json
        genre_data.name = new_data['name']
        db.session.add(genre_data)
        db.session.commit()
        return '', 201

    def delete(self, gid):
        db.session.query(Genre).filter(Genre.id == gid).delete()
        db.session.commit()
        return '', 201

if __name__ == '__main__':
    app.run(debug=True)
