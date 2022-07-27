import json
from datetime import date, datetime
from flask import flash, render_template, redirect, request, url_for
from werkzeug.utils import secure_filename

from fyyur import appFlask, db
from fyyur.models import Venues, Showss, Artistss
from fyyur.forms import AddArtist, AddVenueForm, ArtistSearchForm, CreateShowForm, VenueSearchForm, EditArtist, EditVenue






# routes that have to do with artists
# routes that have to do with artists
@appFlask.route('/')
def index():
    return render_template('index.html')


@appFlask.route('/artists')
def artists():
    all_artists = Artistss.query.all()

    for gen in all_artists:
        gen.genre = list(json.loads(gen.genre))

    return render_template('list_artists.html', artists=all_artists)


@appFlask.route('/artists/<int:artist_id>')
def view_artist(artist_id):
    get_artist = Artistss.query.get_or_404(artist_id)
    genres_1 = json.loads(get_artist.genre)
    genres_2 = list(genres_1)

    past_shows = db.session.query(Artistss).join(Showss).join(Venues).with_entities(Venues.id, Venues.name, Venues.image, Showss.start_time, Artistss.name).filter(Showss.start_time <= datetime.now(), Artistss.id==artist_id).all()

    upcoming_shows = db.session.query(Artistss).join(Showss).join(Venues).with_entities(Venues.id, Venues.name, Venues.image, Showss.start_time, Artistss.name).filter(Showss.start_time >= datetime.now(), Artistss.id==artist_id).all()

    return render_template('view_artist.html', artist=get_artist, genres=genres_2, past_shows=past_shows, upcoming_shows=upcoming_shows, upcoming_shows_count=len(upcoming_shows), past_shows_count=len(past_shows))


@appFlask.route('/artists/delete/<int:artist_id>')
def delete_artist(artist_id):
    get_artist = Artistss.query.get_or_404(artist_id)
    db.session.delete(get_artist)
    db.session.commit()
    flash('Artist successfully deleted', 'success')
    return redirect('http://127.0.0.1:5000/artists')



@appFlask.route('/artists/update/<int:artist_id>', methods=['GET', 'POST'])
def update_artist(artist_id):
    form = EditArtist()
    get_artist = Artistss.query.get_or_404(artist_id)

    if request.method == 'POST':
        if form.validate_on_submit():

            currently_seeking = form.currently_seeking.data
            #check if artist is currently seeking
            if currently_seeking == "":
                seeking = False
            else:
                seeking = True

            get_artist.name = form.name.data
            get_artist.email = form.email.data
            get_artist.genre = json.dumps(form.genre.data)
            get_artist.website = form.website.data
            get_artist.facebook = form.facebook.data
            get_artist.phone = form.phone.data
            get_artist.seeking_venue = seeking
            get_artist.currently_seeking = currently_seeking

            #commit to db
            db.session.commit()
            flash('Artist successfully updated', 'success')
            return redirect('http://127.0.0.1:5000/artists')
        else:
            flash('Failed to update artist', 'success')
            return redirect('http://127.0.0.1:5000/artists')

    form.name.data = get_artist.name
    form.email.data = get_artist.email
    form.genre.data = get_artist.genre
    form.website.data = get_artist.website
    form.facebook.data = get_artist.facebook
    form.phone.data = get_artist.phone
    form.currently_seeking.data = get_artist.currently_seeking

    return render_template('edit_artist.html', form=form)

            


@appFlask.route('/artists/add_artist', methods=['GET', 'POST'])
def add_artist():
    form = AddArtist()

    if request.method == 'POST':
        if form.validate_on_submit():
            
            name = form.name.data 
            email = form.email.data
            image = secure_filename(form.photo.data.filename)
            genre = json.dumps(form.genre.data)

            state = form.state.data
            city = form.city.data
            website = form.website.data
            facebook = form.facebook.data
            phone = form.phone.data
            currently_seeking = form.currently_seeking.data

            #check the currently seeking description and know wether he is seeking venue or not
            if currently_seeking == "":
                seeking = False
            else:
                seeking = True

            #upload photo
            form.photo.data.save('static/uploads/' + image)
            
            #artis object to add is in transient state
            artist_to_add = Artistss(name=name, email=email, image=image, state=state, city=city, website=website, facebook=facebook, phone=phone, currently_seeking=currently_seeking, seeking_venue=seeking, genre=genre)

            db.session.add(artist_to_add)
            db.session.commit()
            
            flash('Artist successfully added', 'success')
            return redirect(url_for('add_artist'))

    return render_template('add_artist.html', form=form)


@appFlask.route('/artists/search', methods=['GET', 'POST'])
def search_page():
    form = ArtistSearchForm()
    if form.validate_on_submit():

        #get form data
        search_by = form.search_by.data
        search = form.search.data

        #check search by and search according to value
        if search_by == 'state':
            search_text = "%{}%".format(search)
            results_q = Artistss.query.filter(Artistss.state.ilike(search_text)).all()
            print(results_q)
            return render_template('search.html', form=form, results=results_q)


        elif search_by == 'name':
            search_text = "%{}%".format(search)
            results_q = Artistss.query.filter(Artistss.name.ilike(search_text)).all()
            print(results_q)
            return render_template('search.html', form=form, results=results_q)

        else:
            return render_template('search.html', form=form)

    return render_template('search.html', form=form)


















#routes that deal with venues
#routes that deal with venues
@appFlask.route('/venues')
def venues():
    all_venues = Venues.query.all()
    all_states = []

    #loop through to convert string back to python lists
    for gen in all_venues:
        gen.genre = list(json.loads(gen.genre))

    #check for all the states in the venue so that we can group
    for ven in all_venues:
        all_states.append(ven.state)

    #convert all the states gotten to set(so that we can eliminate duplicates)
    convert_state_to_set = set(all_states)


    return render_template('venues.html', venues=all_venues, state_choices=convert_state_to_set)


@appFlask.route('/venues/<int:venue_id>')
def view_venue(venue_id):
    get_venue = Venues.query.get_or_404(venue_id)
    #process info about the genre
    genres_1 = list(json.loads(get_venue.genre))

    past_shows = db.session.query(Venues).join(Showss).join(Artistss).with_entities(Venues.id, Venues.name, Venues.image, Showss.start_time, Artistss.name, Artistss.id).filter(Showss.start_time <= datetime.now(), Venues.id==venue_id).all()

    upcoming_shows = db.session.query(Venues).join(Showss).join(Artistss).with_entities(Venues.id, Venues.name, Venues.image, Showss.start_time, Artistss.name, Artistss.id).filter(Showss.start_time >= datetime.now(), Venues.id==venue_id).all()

    for show in past_shows:
        print('past ', show)

    for show in upcoming_shows:
        print('past ', show)


    return render_template('view_venue.html', venue=get_venue, genres=genres_1, upcoming_shows=upcoming_shows, past_shows=past_shows, upcoming_shows_count=len(upcoming_shows), past_shows_count=len(past_shows))



@appFlask.route('/venues/delete/<int:venue_id>')
def delete_venue(venue_id):
    get_venue = Venues.query.get_or_404(venue_id)
    db.session.delete(get_venue)
    db.session.commit()
    flash('venue successfully deleted', 'success')
    return redirect('http://127.0.0.1:5000/venues')



@appFlask.route('/venues/add_venue', methods=['GET', 'POST'])
def add_venue():
    form = AddVenueForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            
            name = form.name.data 
            state = form.state.data
            city = form.city.data
            currently_seeking = form.currently_seeking.data

            image = secure_filename(form.photo.data.filename)
            address = form.address.data
            phone = form.phone.data
            facebook = form.facebook.data
            genre = json.dumps(form.genre.data)

            #save uploaded file
            form.photo.data.save('static/uploads/' + image)

            #add data to db, transient
            venue_to_add = Venues(name=name, state=state, city=city, currently_seeking=currently_seeking, image=image, address=address, phone=phone, facebook=facebook, genre=genre )

            db.session.add(venue_to_add)
            db.session.commit()
            
            flash('Venue successfully added', 'success')
            return redirect(url_for('add_venue'))

    return render_template('add_venue.html', form=form)


@appFlask.route('/venue/update/<int:venue_id>', methods=['GET', 'POST'])
def update_venue(venue_id):
    form = EditVenue()
    get_venue = Venues.query.get_or_404(venue_id)

    if request.method == 'POST':
        if form.validate_on_submit():

            currently_seeking = form.currently_seeking.data
            #check if artist is currently seeking
            if currently_seeking == "":
                seeking = False
            else:
                seeking = True

            get_venue.name = form.name.data
            get_venue.address = form.address.data
            get_venue.genre = json.dumps(form.genre.data)
      
            get_venue.facebook = form.facebook.data
            get_venue.phone = form.phone.data
            get_venue.seeking_venue = seeking
            get_venue.state = form.state.data
            get_venue.city = form.city.data

            #commit to db
            db.session.commit()
            flash('Venue successfully updated', 'success')
            return redirect('http://127.0.0.1:5000/venues')
        else:
            flash('Error updating venue', 'danger')
            return redirect('http://127.0.0.1:5000/venues')

    form.name.data = get_venue.name
    form.genre.data = get_venue.genre
    form.facebook.data = get_venue.facebook
    form.phone.data = get_venue.phone
    form.state.data = get_venue.phone
    form.city.data = get_venue.phone
    form.address.data = get_venue.phone
    form.currently_seeking.data = get_venue.currently_seeking

    return render_template('edit_venue.html', form=form)



@appFlask.route('/venue/search', methods=['GET', 'POST'])
def search_venue():
    form = VenueSearchForm()
    if form.validate_on_submit():

        #get form data
        search_by = form.search_by.data
        search = form.search.data

        #check search by and search according to value
        if search_by == 'name':
            search_text = "%{}%".format(search)
            results_q = Venues.query.filter(Venues.name.ilike(search_text)).all()
            print(results_q)
            return render_template('search_venue.html', form=form, results=results_q)

        elif search_by == 'state':
            search_text = "%{}%".format(search)
            results_q = Venues.query.filter(Venues.state.ilike(search_text)).all()
            print(results_q)
            return render_template('search_venue.html', form=form, results=results_q)

        elif search_by == 'city':
            search_text = "%{}%".format(search)
            results_q = Venues.query.filter(Venues.city.ilike(search_text)).all()
            print(results_q)
            return render_template('search_venue.html', form=form, results=results_q)

        else:
            return render_template('search_venue.html', form=form)

    return render_template('search_venue.html', form=form)











#routes that deal with shows
#routes that deal with shows
#routes that deal with shows



@appFlask.route('/shows')
def shows():
    all_shows = Showss.query.all()
    return render_template('shows.html', shows=all_shows)


@appFlask.route('/shows/add_show', methods=['GET', 'POST'])
def add_show():
    form = CreateShowForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            venue = form.venue_id.data
            artist = form.artist_id.data
            date = form.date.data

            show_to_add = Showss(venue=venue, artist=artist, start_time=date)
            db.session.add(show_to_add)
            db.session.commit()

            flash('Show successfully added', 'success')
            return redirect(url_for('add_show'))

        flash('Show was not added', 'danger')
        return redirect(url_for('add_show'))

    return render_template('add_show.html', form=form)

