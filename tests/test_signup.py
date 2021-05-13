import unittest
import json

from main import app
from api.utils.database import db


class SignupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()

    def test_successful_signup(self):
        payload = json.dumps({})
