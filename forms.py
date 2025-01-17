from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, URL
from flask_wtf.file import FileAllowed

# Form for creating new blog posts
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    body = TextAreaField("Blog Content", validators=[DataRequired()])
    image = FileField("Upload Image")
    # Dropdown menu to select the post category (required)
    category = SelectField("Category", choices=[('Lifestyle', 'Lifestyle'), ('Wellbeing', 'Wellbeing'), ('Entertainment', 'Entertainment'), ('World News', 'World News'), ('Sports', 'Sports')], validators=[DataRequired()])
    submit = SubmitField("Submit Post")

# Form for user registration
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Form for user login
class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

# Form for creating or editing a simple post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for submitting comments on blog posts
class CommentForm(FlaskForm):
    text = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Form for sending an email message (contact form)
class EmailForm(FlaskForm):
    email = EmailField("Your email", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")

# Form for updating user profile details
class ProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio")
    profile_picture = FileField("Upload Profile Picture", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Update Profile")