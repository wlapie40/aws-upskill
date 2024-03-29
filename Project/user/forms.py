from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[InputRequired(),
                                       Length(min=4, max=15)])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email',
                        validators=[InputRequired(),
                                    Email(message='Invalid email'),
                                    Length(max=50)],
                        default='test@gmail.com')
    username = StringField('username',
                           validators=[InputRequired(),
                                       Length(min=4, max=15)])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         Length(min=8, max=80)])


class NewBucketForm(FlaskForm):
    bucket_name = StringField('Bucket name', default='anowak-bucket-name', validators=[InputRequired(), Length(min=4, max=80)])
