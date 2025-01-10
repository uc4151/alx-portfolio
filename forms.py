from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, URL

# WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    body = TextAreaField("Blog Content", validators=[DataRequired()])
    image = FileField("Upload Image")
    category = SelectField("Category", choices=[('Lifestyle', 'Lifestyle'), ('Wellbeing', 'Wellbeing'), ('Entertainment', 'Entertainment'), ('World News', 'World News'), ('Sports', 'Sports')], validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField("Enter your email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EmailForm(FlaskForm):
    email = EmailField("Your email", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio")
    profile_picture = FileField("Upload Profile Picture")
    submit = SubmitField("Update Profile")