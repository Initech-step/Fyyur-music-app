from fyyur import db


class Artistss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=True)
    city = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    facebook = db.Column(db.String(), nullable=True)
    website = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)
    currently_seeking = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean())
    genre = db.Column(db.String(900), nullable=False)
    shows = db.relationship('Showss', backref='artists', lazy=True, cascade='all, delete')
    dummy = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'Artist {self.name}'


class Venues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=True)
    state = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    genre = db.Column(db.String(500), nullable=False)
    address = db.Column(db.String(), nullable=True)
    facebook = db.Column(db.String(), nullable=True)
    currently_seeking = db.Column(db.String(), nullable=True)
    shows = db.relationship('Showss', backref='show', lazy=True, cascade='all, delete')

    def __repr__(self):
        return f'Venues {self.name}'


class Showss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    artist = db.Column(db.Integer, db.ForeignKey('artistss.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=True)

    def __repr__(self):
        return f'Shows {self.venue}, artist {self.artist}'

