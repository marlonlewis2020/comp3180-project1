"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db, login_manager
from flask import render_template, request, redirect, send_from_directory, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.models import User, Property
from app.forms import PropertyForm
from flask_paginate import Pagination
import locale
locale.setlocale(locale.LC_ALL,"")


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Marlon Lewis")


@app.route("/properties/<int:propertyid>", methods=["GET"])
def details(propertyid):
    """Render the website's about page."""
    unit = Property.query.filter_by(id=propertyid).first()
    return render_template('details.html', property=unit)

@app.route("/properties/create", methods=["POST", "GET"])
def add_property():
    """Render the website's page to add a new property."""
    html = "add_property.html"
    form = PropertyForm()
    if form.validate_on_submit():
        # form.validate()
        if len(form.errors) > 0:
            for k,v in form.errors.items():
                print(k,v)
            new_form = PropertyForm()
            flash_errors(form)
            return render_template(html, property = new_form, errors = form.errors.keys())
        
        form.filename = form.create_filename()
        photo = request.files['photo'] or form.photo.data
        file_path = app.config['UPLOAD_FOLDER']
        file_name = os.path.join(file_path, form.filename)
        try:
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            photo.save(file_name)
            form.save()
            form = PropertyForm()
            page = request.args.get('page', 1, type=int)
            ROWS_PER_PAGE = 6
            search = False
            q = request.args.get('q')
            if q:
                search = True
            properties = Property.query.order_by(Property.id.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
            total = Property.query.count()
            pagination = Pagination(page=page, total=total, search=search, record_name='properties')
            flash("New property added successfully!", 'success')
            return render_template("properties.html", properties = properties, pagination = pagination, total=total)
        except FileNotFoundError:
            if os.path.exists(file_name):
                os.remove(file_name)
            flash("Unable to save property image. Try again.", 'warning')
    return render_template(html, property = form)

@app.route("/properties", methods=["GET"])
def properties():
    page = request.args.get('page', 1, type=int)
    ROWS_PER_PAGE = 6
    search = False
    q = request.args.get('q')
    if q:
        search = True
        
    properties = Property.query.order_by(Property.id.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
    total = Property.query.count()
    pagination = Pagination(page=page, total=total, search=search, record_name='properties')
    flash("New property added successfully!", 'success')
    return render_template("properties.html", properties = properties, pagination = pagination, total=total)


@app.route("/properties/<filename>", methods=["GET"])
def get_image(filename):
    uploads = get_uploaded_images()
    print("FILENAME:", filename)
    for file, file_dir in uploads:
        print("NAME:", filename, "FILE:", file)
        if filename == file:
            print(file, file_dir)
            return send_from_directory(file_dir, file)
    return page_not_found("Image File Not Found!")




###
# The functions below should be applicable to all Flask apps.
###

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

def get_uploaded_images():
    photos = []
    for dir, subdirs, files in os.walk(os.getcwd() + app.config['UPLOAD_FOLDER']):
        for file in files:
            photos.append([file, dir])
            print(file, dir)
    return photos


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


def currency_format(value):
    return locale.currency(float(value), grouping=True)

app.jinja_env.filters['currency_format'] = currency_format
