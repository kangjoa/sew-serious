import os
import unittest
import app

from datetime import datetime, date
from soup_app.extensions import app, db, bcrypt
from soup_app.models import Fabric, Pattern, User, PatternCategory

"""
Run these tests with the command:
python -m unittest soup_app.main.tests

Run specific test:
python -m unittest soup_app.tests.MainTests.test_homepage_logged_out
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
    p1 = Pattern(name='Perfect Pants')
    f1 = Fabric(
        name='Light Linen',
        color='Lavender',
        quantity=1,
        photo_url='testurl',
        pattern=p1
    )
    db.session.add(f1)

    p2 = Pattern(name='Summer Shirt')
    f2 = Fabric(name='Soft Silk', pattern=p2)
    db.session.add(f2)
    db.session.commit()


def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
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
        """Test that the books show up on the homepage."""
        # Set up
        new_fabric()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Light Linen', response_text)
        self.assertIn('Summer Shirt', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('New Fabric', response_text)
        self.assertNotIn('New Pattern', response_text)

    def test_homepage_logged_in(self):
        """Test that the books show up on the homepage."""
        # Set up
        new_fabric()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Light Linen', response_text)
        self.assertIn('Summer Shirt', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('New Fabric', response_text)
        self.assertIn('New Pattern', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_fabric_detail_logged_out(self):
        # Use helper functions to create books, authors, user
        new_fabric()
        create_user()

        # Make a GET request to the URL /book/1, check to see that the
        # status code is 200
        response = self.app.get('/book/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the book's name, publish date,
        # and pattern's name
        response_text = response.get_data(as_text=True)
        self.assertIn("<h1>Light Linen</h1>", response_text)
        self.assertIn("Harper Lee", response_text)

        # Check that the response does NOT contain the 'Favorite' button
        # (it should only be shown to logged in users)
        self.assertNotIn("Favorite This Fabric", response_text)

    def test_fabric_detail_logged_in(self):
        """Test that the book appears on its detail page."""
        # Use helper functions to create books, authors, user, & to log in
        new_fabric()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request to the URL /book/1, check to see that the
        # status code is 200
        response = self.app.get('/book/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the book's name, publish date,
        # and pattern's name
        response_text = response.get_data(as_text=True)
        # Check for the book name
        self.assertIn('Light Linen', response_text)

        # Check for the publish date
        expected_publish_date = "July 11, 1960"
        self.assertIn(expected_publish_date, response_text)

        # Check that the response contains the 'Favorite' button
        self.assertIn('Favorite This Fabric', response_text)

    def test_update_fabric(self):
        """Test updating a book."""
        # Set up
        new_fabric()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Tequila Mockingbird',
            'publish_date': '1960-07-12',
            'pattern': 1,
            'audience': 'CHILDREN',
            'genres': []
        }
        self.app.post('/book/1', data=post_data)

        # Make sure the book was updated as we'd expect
        book = Fabric.query.get(1)
        self.assertEqual(book.name, 'Tequila Mockingbird')
        self.assertEqual(book.publish_date, date(1960, 7, 12))
        self.assertEqual(book.audience, PatternCategory.CHILDREN)

    def test_create_book(self):
        """Test creating a book."""
        # Set up
        new_fabric()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Go Set a Watchman',
            'publish_date': '2015-07-14',
            'pattern': 1,
            'audience': 'ADULT',
            'genres': []
        }
        self.app.post('/create_book', data=post_data)

        # Make sure book was updated as we'd expect
        created_book = Fabric.query.filter_by(name='Go Set a Watchman').one()
        self.assertIsNotNone(created_book)
        self.assertEqual(created_book.pattern.name, 'Harper Lee')

    def test_create_book_logged_out(self):
        """
        Test that the user is redirected when trying to access the create book 
        route if not logged in.
        """
        # Set up
        new_fabric()
        create_user()

        # Make GET request
        response = self.app.get('/create_book')

        # Make sure that the user was redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_book', response.location)

    def test_create_author(self):
        """Test creating an pattern."""
        # Create a user & login (so that the user can access the route)
        create_user()
        login(self.app, 'me1', 'password')

        # Make a POST request to the /create_author route
        post_data = {
            'name': 'New Pattern',
            'biography': 'New pattern biography'
        }
        self.app.post('/create_author', data=post_data)

        # Verify that the pattern was updated in the database
        created_author = Pattern.query.filter_by(name='New Pattern').first()
        self.assertIsNotNone(created_author)
        self.assertEqual(created_author.name, 'New Pattern')
        self.assertEqual(created_author.biography, 'New pattern biography')

    # def test_create_genre(self):
    #     # Create a user & login (so that the user can access the route)
    #     create_user()
    #     login(self.app, 'me1', 'password')

    #     # Make a POST request to the /create_genre route,
    #     post_data = {
    #         'name': 'New Genre'
    #     }
    #     self.app.post('/create_genre', data=post_data)

    #     # Verify that the genre was updated in the database
    #     created_genre = Genre.query.filter_by(name='New Genre').first()
    #     self.assertIsNotNone(created_genre)
    #     self.assertEqual(created_genre.name, 'New Genre')

    def test_profile_page(self):
        # Set up to create a user and commit to database
        create_user()

        # Make a GET request to the /profile/me1 route
        response = self.app.get('/profile/me1', follow_redirects=True)

        # Verify that the response shows the appropriate user info
        self.assertEqual(response.status_code, 200)

    def test_favorite_book(self):
        # Set up to create a book and a user
        new_fabric()
        create_user()

        # Login as the user me1
        login(self.app, 'me1', 'password')

        # Make a POST request to the /favorite/1 route
        post_data = {
            'book_id': 1
        }
        self.app.post('/favorite/1', data=post_data)

        # Verify that the book with id 1 was added to the user's favorites
        # Look for first user with username me1
        created_user = User.query.filter_by(username='me1').first()
        favorite_books = created_user.favorite_books

        # Check if book with id 1 is in the user's favorites
        books_in_favorites = any(book.id == 1 for book in favorite_books)
        self.assertTrue(books_in_favorites,
                        "Fabric with id 1 was not found in the user's favorites")

    def test_unfavorite_book(self):
        # Set up to create a book and a user
        new_fabric()
        create_user()

        # Login as the user me1, and add book with id 1 to me1's favorites
        login(self.app, 'me1', 'password')

        # Make a POST request to the /unfavorite/1 route
        post_data = {
            'book_id': 1
        }
        self.app.post('/unfavorite/1', data=post_data)

        # Verify that the book with id 1 was removed from the user's
        # favorites
        # Look for first user with username me1
        created_user = User.query.filter_by(username='me1').first()
        favorite_books = created_user.favorite_books

        # Check if book with id 1 is in the user's favorites
        books_in_favorites = any(book.id == 1 for book in favorite_books)
        self.assertFalse(books_in_favorites,
                         "Fabric with id 1 was found in the user's favorites")
