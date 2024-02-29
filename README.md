# Final Project
## Sewing App
This sewing app helps users keep track of their fabric stash and sewing pattern collection. Users can create new fabrics or sewing pattern records and add them to their fabric lists or patterns lists.

### Technologies Used:
- **Python**: the primary programming language used for backend development.
- **Flask**: a micro web framework used to build the web application.[(source)](https://flask.palletsprojects.com/en/3.0.x/)
- **WTForms**:  a flexible forms validation and rendering library for Python web development.[(source)](https://wtforms.readthedocs.io/en/3.1.x/)
- **Flask-WTF**: integration of Flask and WTForms, including CSRF. The `crsf_token` is included in forms to prevent Cross-Site Request Forgery (CSRF) attacks. [(source)](https://flask-wtf.readthedocs.io/en/1.2.x/)
- **SQLAlchemy**: Python SQL toolkit and Object Relational Mapper. [(source)](https://www.sqlalchemy.org/)
- **Flask-Login**: provides user session management for Flask, such as logging in and logging out. [(source)](https://flask-login.readthedocs.io/en/latest/)


### Set up

To run this app locally, clone the repo.

In the parent directory, open a terminal to create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

To install dependencies, run:

```bash
pip3 install -r requirements.txt
```

Then rename the `.env.example` file as `.env`:

This command copies the file `.env.example` to a new file named `.env`
Use this when you want to keep both files, both `.env.example` and `.env`
```bash
cp .env.example .env
```

Use `mv .env.example .env` when you want to rename the file.

Then you can run the server:

```bash
python app.py
```

When you are finished coding, simply close the terminal or type `deactivate` to terminate the virtual environment.

Setup instructions adapted from [Grocery Store Homework](https://github.com/Tech-at-DU/ACS-1220-Grocery-Store-Homework).