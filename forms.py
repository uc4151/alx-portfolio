from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, EqualTo
from flask_ckeditor import CKEditorField


# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    email = EmailField("Enter your email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirmation = PasswordField("Confirm your password", validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    name = StringField("Enter your name", validators=[DataRequired()])
    submit = SubmitField("Sign me up")


class LoginForm(FlaskForm):
    email = StringField("Enter your email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log me in")


class CommentForm(FlaskForm):
    comments = CKEditorField("Comments")
    submit = SubmitField("Submit Comment")

class EmailForm(FlaskForm):
    email = EmailField("Your email", validators=[DataRequired()])
    message = CKEditorField("Message")
    submit = SubmitField("Submit Comment")
