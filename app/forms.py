from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, SelectField, PasswordField, TextAreaField, EmailField
from wtforms.validators import InputRequired, Optional, EqualTo, Email, Length, Regexp, ValidationError
from app import db
from app.models import User, Property
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from urllib.parse import quote
from datetime import datetime as dt

class PropertyForm(FlaskForm):
    filename = ""
    title = StringField('Property Title', validators=[InputRequired()], render_kw = {'placeholder':'Enter property title'}) 
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=10, max=255)], render_kw = {'placeholder':'Property description...'})
    bedrooms = StringField('No. of Rooms', validators=[InputRequired()], render_kw = {'placeholder':'3'}) #
    bathrooms = StringField('No. of Bathrooms', validators=[InputRequired()], render_kw = {'placeholder':'2'}) #Regexp(regex=r'^\d{1,3}$', message="Number of bathrooms must be a number - no other characters allowed!")
    price  = StringField('Price', validators=[InputRequired()], render_kw = {'placeholder':'150,000.00'}) #Regexp(regex=r'^(\d){1,3}(,{0,1}\d{3}){0,3}(\.\d{2}){0,1}$', message="Price is required and must be at least 0 in value. It must be formatted without the dollar sign ($) and only contain numbers. It MAY be comma-separated, but this is not required. It MAY contain at most one decimal point (.) and two digits after the decimal point if a decimal point is entered. i.e. '150,000.00'")
    property_type = SelectField('Type', choices=[('apartment','Apartment'), ('house','House')], validators=[InputRequired()])
    location  = StringField('Location', validators=[InputRequired()], render_kw = {'placeholder':'10 Waterloo Road'}) 
    photo = FileField('Photo', validators=[FileRequired(), FileSize(max_size=8000000), FileAllowed(["jpg", "jpeg", "png"], message="Image Files Only!")])
    
    def filter_price(self, price):
        if price is not None:
            return float(price.replace(",", ""))
    
    
    def create_filename(self):
        photo = self.photo.data
        normalized = str(photo.filename).split(".")
        filename = normalized[0]
        ftype = normalized[-1]
        replace1 = dt.now().isoformat().replace(".","_")
        replace2 = replace1.replace(":","_")
        self.filename = secure_filename(quote(filename)) + "_" + replace2 + "." + ftype
        return self.filename
    
    def save(self):
        ppty = Property(self.title.data, self.bedrooms.data, self.bathrooms.data, self.location.data, self.price.data, self.property_type.data, self.description.data, self.filename)
        db.session.add(ppty)
        db.session.commit()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[InputRequired()])
    
    def validate_authentication(self):
        user = User.query.filter_by(username=self.username.data).first() or db.session.execute(db.select(User).filter_by(username=self.username.data)).scalar()
        if user is None or not check_password_hash(user.password, self.password):
            self.username = ""
            self.password = ""
            raise ValidationError('Invalid username or password. Try again or contact the System Administrator.')


class RegistrationForm(FlaskForm):
    role = SelectField('Role', choice=[('user','User'), ('admin','Admin')], validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=25, message="Username must be 4 to 25 characters in length!")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25, message="Password must be 8 to 25 characters in length!")])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message="Passwords do not match!")])
    
    def validate_username(self):
        user = User.query.filter_by(username=self.username.data).first() or db.session.execute(db.select(User).filter_by(username=self.username.data)).scalar()
        if user is not None:
            raise ValidationError('That username already exists. Choose another.')