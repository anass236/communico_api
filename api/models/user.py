from api.utils.database import db
from datetime import datetime
from mongoengine import signals
from flask_bcrypt import generate_password_hash, check_password_hash


class Followers(db.EmbeddedDocument):
    follower_username = db.StringField()


class Followings(db.EmbeddedDocument):
    following_username = db.StringField()


class User(db.Document):
    username = db.StringField(unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    birth_date = db.DateTimeField()
    created_on = db.DateTimeField(default=datetime.utcnow)
    update_on = db.DateTimeField(default=datetime.utcnow)
    followers = db.ListField(db.EmbeddedDocumentField(Followers))
    followings = db.ListField(db.EmbeddedDocumentField(Followings))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_on = datetime.utcnow()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


signals.pre_save.connect(User.pre_save, sender=User)
