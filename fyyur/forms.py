from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, EmailField, PasswordField, StringField, SelectField, TextAreaField, IntegerField, DateTimeField, SelectMultipleField, URLField
from flask_wtf import file
from wtforms.validators import DataRequired, Email, Length



state_choices = [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]

genre_choices = [
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]


class AddArtist(FlaskForm):
    name = StringField('Artist name', validators=[DataRequired(), Length(min=2, max=30)])
    photo = file.FileField('Image', validators=[DataRequired()])
    state = SelectField('State (ctrl+click)', validators=[DataRequired()], choices=state_choices)
    city = StringField('City', validators=[DataRequired()])
    facebook = URLField('Facebook profile link', validators=[DataRequired()])
    website = URLField('Website', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11)], render_kw={'placeholder': 'XXX XXX XXX XX'})
    genre = SelectMultipleField('Genre', validators=[DataRequired(), Length(min=1, max=850)], choices=genre_choices)
    currently_seeking = StringField('Currently seeking?', render_kw={'placeholder':'Leave blank if not currently seeking venues.'})
    submit = SubmitField('Add artist')


class EditArtist(FlaskForm):
    name = StringField('Artist name', validators=[DataRequired(), Length(min=2, max=30)])
    facebook = URLField('Facebook profile link', validators=[DataRequired()])
    website = URLField('Website', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11)], render_kw={'placeholder': 'XXX XXX XXX XX'})
    genre = SelectMultipleField('Genre', validators=[DataRequired(), Length(min=1, max=850)], choices=genre_choices)
    currently_seeking = StringField('Currently seeking?', render_kw={'placeholder':'Leave blank if not currently seeking venues.'})
    submit = SubmitField('Update artist')


class ArtistSearchForm(FlaskForm):
    search_by = SelectField('Search by', validators=[DataRequired()], 
    choices=[('state', 'Artist state'), 
            ('name', 'Artist name')]
    )
    search = StringField('What you want to search', validators=[DataRequired()], render_kw={'placeholder':'Search is case insensitive'})
    submit = SubmitField('search artist')


class AddVenueForm(FlaskForm):
    name = StringField('venue name', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()], choices=state_choices)
    genre = SelectMultipleField('Genre', validators=[DataRequired(), Length(min=1, max=500)], choices=genre_choices)
    photo = file.FileField('Image', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    currently_seeking = StringField('Currently seeking talent?', render_kw={'placeholder':'Leave blank if not currently seeking talent.'})
    facebook = URLField('Facebook profile link', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11)], render_kw={'placeholder': 'XXX XXX XXX XX'})
    submit = SubmitField('Add venue')


class EditVenue(FlaskForm):
    name = StringField('venue name', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()], choices=state_choices)
    genre = SelectMultipleField('Genre', validators=[DataRequired()], choices=genre_choices)
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=500)])
    currently_seeking = StringField('Currently seeking talent?', render_kw={'placeholder':'Leave blank if not currently seeking talent.'})
    facebook = URLField('Facebook profile link', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11)], render_kw={'placeholder': 'XXX XXX XXX XX'})
    submit = SubmitField('Edit venue')


class VenueSearchForm(FlaskForm):
    search_by = SelectField('Search by', validators=[DataRequired()], 
    choices=[('name', 'venue name'), 
            ('state', 'venue state'),    
            ('city', 'venue city')]
    )
    search = StringField('search', validators=[DataRequired()], render_kw={'placeholder':'Search is case insensitive'})
    submit = SubmitField('search venue')


class CreateShowForm(FlaskForm):
    artist_id = IntegerField('Artist Id', validators=[DataRequired()])
    venue_id = IntegerField('Venue Id', validators=[DataRequired()])
    date = DateTimeField('Date & time', validators=[DataRequired()], default=datetime.today())
    submit = SubmitField('Add show')