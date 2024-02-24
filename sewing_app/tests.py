import os
import unittest
import app

from datetime import datetime, date
from sewing_app.extensions import app, db, bcrypt
from sewing_app.models import Fabric, Pattern, User, PatternCategory

"""
Run these tests with the command:
python -m unittest sewing_app.tests

Run specific test example:
python -m unittest sewing_app.tests.MainTests.test_homepage_logged_out
"""

#################################################
# Setup
#################################################


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def new_fabric():
    f1 = Fabric(
        name='green canvas',
        color='green',
        quantity=2.75,
        photo_url='https://i0.wp.com/fabriccraftsupply.com/wp-content/uploads/2017/08/brilliantafabriccloth4047-1.jpg?w=370&ssl=1'
        # ,pattern=p1
    )
    db.session.add(f1)

    # p2 = Pattern(name='cute jumpsuit')
    # f2 = Fabric(name='purple fabric', pattern=p2)
    # db.session.add(f2)
    # db.session.commit()


def create_user():
    # Creates a user with username 'timtam' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='timtam', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################


class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the fabrics show up on the homepage."""
        # Set up
        new_fabric()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains what is expected on home page
        response_text = response.get_data(as_text=True)
        self.assertIn('green canvas', response_text)
        self.assertIn('green', response_text)
        self.assertIn('Login', response_text)
        self.assertIn('Signup', response_text)

        # Check that the page doesn't contain what is not expected on home page
        # (what only logged in users should see)
        self.assertNotIn('New Fabric', response_text)
        self.assertNotIn('New Pattern', response_text)
        self.assertNotIn('timtam', response_text)

    def test_homepage_logged_in(self):
        """Test that the fabrics show up on the homepage."""
        # Set up
        new_fabric()
        create_user()
        login(self.app, 'timtam', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains what is expected on home page
        response_text = response.get_data(as_text=True)
        self.assertIn('green canvas', response_text)
        self.assertIn('green', response_text)
        self.assertIn('timtam', response_text)
        self.assertIn('New Fabric', response_text)
        self.assertIn('New Pattern', response_text)

        # Check that the page doesn't contain what is not expected on home page
        # (what only logged out users should see)
        self.assertNotIn('Login', response_text)
        self.assertNotIn('Signup', response_text)

    def test_fabric_detail_logged_out(self):
        # Use helper functions to create fabric, user
        new_fabric()
        create_user()

        # Make a GET request to the URL /fabric/1, check to see that the
        # status code is 200
        response = self.app.get('/fabric/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the Log In page text
        response_text = response.get_data(as_text=True)
        self.assertIn("<h1>Log In</h1>", response_text)
        self.assertIn("User Name", response_text)

        # Check that the response does NOT contain the fabric details
        # (it should only be shown to logged in users)
        self.assertNotIn("Created By", response_text)
        self.assertNotIn("Add to Fabrics List", response_text)

    def test_fabric_detail_logged_in(self):
        """Test that the fabric appears on its detail page."""
        # Use helper functions to create fabrics, patterns, user, & to log in
        new_fabric()
        create_user()
        login(self.app, 'timtam', 'password')

        # Make a GET request to the URL /fabric/1, check to see that the
        # status code is 200
        response = self.app.get('/fabric/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the fabric's name and color
        response_text = response.get_data(as_text=True)
        # Check for the fabric name
        self.assertIn('green canvas', response_text)

        # Check for the fabric color
        expected_fabric_color = "green"
        self.assertIn(expected_fabric_color, response_text)

        # Check that the response contains the 'Add to Fabrics List' button
        self.assertIn('Add to Fabrics List', response_text)
