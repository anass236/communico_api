import json

from bson import json_util

from api.models.post import Post
from api.utils.database import db
from datetime import datetime
from mongoengine import signals
from flask_bcrypt import generate_password_hash, check_password_hash


class Followers(db.Document):
    added_by = db.ReferenceField('User')
    follower_username = db.ReferenceField('User')


class User(db.Document):
    username = db.StringField(unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    birth_date = db.DateTimeField()
    created_on = db.DateTimeField(default=datetime.utcnow)
    update_on = db.DateTimeField(default=datetime.utcnow)
    followers = db.ListField(db.ReferenceField('Followers', reverse_delete_rule=db.PULL))
    followings = db.ListField(db.ReferenceField('Followers', reverse_delete_rule=db.PULL))
    posts = db.ListField(db.ReferenceField('Post', reverse_delete_rule=db.PULL))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_on = datetime.utcnow()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        data = self.to_mongo()

        post = dict()
        l_post = []
        for key, value in enumerate(data["posts"]):
            post["title"] = self.posts[key].title
            post["content"] = self.posts[key].content
            post["comments"] = [{"comment": self.posts[key].comments[k].content,
                                 "username": self.posts[key].comments[k].added_by.username} for k, v in
                                enumerate(self.posts[key].comments)]
            l_post.append(post)
        data["posts"] = l_post
        data["followers"] = [
            {"username": self.followers[key].follower_username.username} for key, value in enumerate(data["followers"])]

        data["followings"] = [
            {"username": self.followings[k].added_by.username} for k, v in enumerate(data["followings"])]

        return json.loads(json_util.dumps(data))


signals.pre_save.connect(User.pre_save, sender=User)
User.register_delete_rule(Post, 'added_by', db.CASCADE)
