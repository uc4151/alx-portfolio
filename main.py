from flask import Flask, render_template, render_template_string, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, PostForm, CommentForm, EmailForm, ProfileForm
from functools import wraps
from flask import abort
import hashlib
from dotenv import load_dotenv
from email_sender import EmailSender
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
import time
import os
import uuid

load_dotenv()
email_sender = EmailSender()

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRETKEY')
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)
# Add 'wtf' global for Jinja2
app.jinja_env.globals['wtf'] = FlaskForm

@app.context_processor
def inject_time():
    return dict(time=time)

# CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/blogpost.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'blogpost.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    profile_picture = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.Text, nullable=True) 
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship("User", back_populates="posts")
    date = db.Column(db.String(100), nullable=False)

    #***************Parent Relationship*************#
    comments = relationship("Comment", back_populates="parent_post")

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment_author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    parent_post = relationship("Post", back_populates="comments")
    comment_author = relationship("User", back_populates="comments")

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.is_authenticated and current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def get_all_posts():
    category = request.args.get('category')
    search = request.args.get('search')
    if category:
        posts = Post.query.filter_by(category=category).all()
    elif search:
        posts = Post.query.filter(Post.title.contains(search)).all()
    else:
        posts = Post.query.all()
    csrf_token = generate_csrf()
    return render_template("index.html", all_posts=posts, current_user=current_user, csrf_token=csrf_token)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if User.query.filter_by(email=form.email.data).first():
            return redirect(url_for('login', flash=flash("Email already exist, login instead")))
        print(form.password.data)
        if form.password.data == form.confirm_password.data:
            p_word = generate_password_hash(form.password.data, "pbkdf2:sha256", 8)
        else:
            flash("Passwords don't match, please try again.")
            return redirect(url_for("register"))
        new_user = User(
            name=form.username.data,
            email=form.email.data,
            password=p_word
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


def gravatar_url(email, size=200):
    email_hash = hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s={size}"


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            text=form.text.data,
            post_id=post.id,
            comment_author_id=current_user.id
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    return render_template("post.html", post=post, form=form, current_user=current_user)

@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = EmailForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        email_sender.send_email(
            sender_email=form.email.data,
            sender_name=current_user.name,
            subject=f"Message from {current_user.name}",
            body=form.message.data
        )
        flash("Your message has been sent!")
        return redirect(url_for("contact"))
    elif not current_user.is_authenticated:
        flash("You need to login to send email!")
        return redirect(url_for("login"))
    return render_template("contact.html", form=form, current_user=current_user)


@app.route("/new-post", methods=['GET', 'POST'])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            author=current_user,
            date=datetime.now().strftime("%B %d, %Y %H:%M:%S")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_user=current_user)

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(app.root_path, 'static/uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            image_url = url_for('static', filename='uploads/' + filename)
        else:
            image_url = None

        new_post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            image_url=image_url,
            category=form.category.data,  # Save the category
            author=current_user,
            date=datetime.now().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        print("Post created successfully")  # Debug statement
        return redirect(url_for('get_all_posts'))
    else:
        print("Form validation failed")  # Debug statement
        print(form.errors)  # Debug statement
    return render_template('make-post.html', form=form, current_user=current_user)

@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.id != 1:
        abort(403)
    form = CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.body = form.body.data
        post.category = form.category.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            upload_folder = os.path.join(app.root_path, 'static/uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_path = os.path.join(upload_folder, filename)
            form.image.data.save(image_path)
            post.image_url = url_for('static', filename='uploads/' + filename)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.body.data = post.body
        form.category.data = post.category
    return render_template('make-post.html', form=form, current_user=current_user, post=post)


@app.route("/delete-post/<int:post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.id != 1:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/delete-comment/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)
    db.session.delete(comment_to_delete)
    db.session.commit()
    return redirect(url_for('show_post', post_id=comment_to_delete.post_id))

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    profile_picture = None  # Initialize the variable

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        profile_picture = form.profile_picture.data

        if profile_picture:
            # Generate a unique filename to prevent overwriting
            unique_filename = str(uuid.uuid4()) + "_" + secure_filename(profile_picture.filename)
            upload_folder = os.path.join(app.root_path, 'static/uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            profile_picture_path = os.path.join(upload_folder, unique_filename)
            profile_picture.save(profile_picture_path)
            current_user.profile_picture = 'uploads/' + unique_filename
            print(f"Profile picture saved at: {profile_picture_path}")  # Debug statement
            
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('get_all_posts'))

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template('profile.html', form=form, current_user=current_user, time=time)

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user, current_user=current_user)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True, extra_files=["templates/", "static/"])