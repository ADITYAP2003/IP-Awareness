import unittest
from flask import Flask, request
from flask_testing import TestCase
from app import app, db, User, contact_form_submissions, authenticate_user
from datetime import datetime

class FlaskTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:sanky25032003@localhost/test_intellectual_playground'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()
            user = User(
                fullname='Test User',
                dob=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
                email='testuser@example.com',
                gender='Male',
                username='testuser',
                password='testpassword'
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign Up', response.data)

    def test_login_success(self):
        response = self.client.post('/login', data=dict(username='testuser', password='testpassword'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Main Page', response.data)

    def test_login_incorrect_password(self):
        response = self.client.post('/login', data=dict(username='testuser', password='wrongpassword'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect Password', response.data)

    def test_login_user_not_found(self):
        response = self.client.post('/login', data=dict(username='nonexistentuser', password='somepassword'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username not found', response.data)

    def test_user_authentication(self):
        result = authenticate_user('testuser', 'testpassword')
        self.assertEqual(result, 'success')

        result = authenticate_user('testuser', 'wrongpassword')
        self.assertEqual(result, 'incorrect_password')

        result = authenticate_user('nonexistentuser', 'somepassword')
        self.assertEqual(result, 'user_not_found')

    def test_user_registration(self):
        response = self.client.post('/submit', data=dict(
            fullname='New User',
            dob='1990-05-15',
            email='newuser@example.com',
            gender='Female',
            username='newuser',
            password='newpassword'
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/success', response.location)

        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')

    def test_contact_form_submission(self):
        response = self.client.post('/contact-submit', data=dict(
            fullname='Contact User',
            email='contactuser@example.com',
            subject='Testing',
            message='This is a test message.'
        ))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/success', response.location)

        contact = contact_form_submissions.query.filter_by(email='contactuser@example.com').first()
        self.assertIsNotNone(contact)
        self.assertEqual(contact.subject, 'Testing')


if __name__ == '__main__':
    unittest.main()
