```markdown
# Introduction:

This blog site was created by EGBUAGU LINDA UCHENNA, as a solo project for her final portfolio project as a Back-end software programmer in the Prestigious ALX program.

# About this Project:

Intel-Vibez Blog is a simple blogging platform built with Flask. Users can register, log in, create posts, categorize posts, and search for posts by title. The platform also includes a sidebar profile and a responsive design.

## Features

- User authentication (register, log in, log out)
- Create, read, update, and delete posts
- Categorize posts (Lifestyle, Wellbeing, Entertainment, World News, Sports)
- Search posts by title
- Sidebar profile with user information
- Responsive design

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-WTF
- CKEditor
- Bootstrap

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/uc4151/my-alx-blog.git
   cd my-alx-blog
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the environment variables:**

   Create a 

.env

 file in the root directory and add the following:

   ```env
   SECRET_KEY=your_secret_key
   ```

5. **Initialize the database:**

   ```sh
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application:**

   ```sh
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000`.

## Usage

1. **Register a new user:**

   Go to `http://127.0.0.1:5000/register` and create a new account.

2. **Log in:**

   Go to `http://127.0.0.1:5000/login` and log in with your credentials.

3. **Create a new post:**

   Go to `http://127.0.0.1:5000/create-post` and fill out the form to create a new post. You can select a category and upload an image.

4. **View posts:**

   Go to `http://127.0.0.1:5000/` to view all posts. You can filter posts by category and search for posts by title.

5. **Edit your profile:**

   Click on the "Profile" link in the navigation bar to view and edit your profile information.

## Project Structure

```
intel-vibez-blog/
├── migrations/          # Database migrations
├── static/              # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── uploads/
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── header.html
│   ├── footer.html
│   ├── register.html
│   ├── login.html
│   ├── make-post.html
│   ├── profile.html
│   └── user_profile.html
├── .env                 # Environment variables
├── .gitignore           # Git ignore file
├── README.md            # Project README file
├── app.py               # Flask application
├── forms.py             # Flask-WTF forms
├── models.py            # SQLAlchemy models
├── requirements.txt     # Python dependencies
└── config.py            # Configuration file
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
```

