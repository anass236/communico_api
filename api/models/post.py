from bson import json_util

from api.utils.database import db
from datetime import datetime
from mongoengine import signals
from .Comment import Comment


class Post(db.Document):
    added_by = db.ReferenceField('User')
    title = db.StringField(required=True)
    content = db.StringField(min_length=50)
    comments = db.ListField(db.ReferenceField('Comment', reverse_delete_rule=db.PULL))
    # change to text for simplicity
    # audioPost = db.FileField()
    # audioFileName = ''.join(random.choice(string.ascii_lowercase) for i in range(8)) + '.mp3'
    tags = db.ListField(db.StringField(max_length=30))
    created_on = db.DateTimeField(default=datetime.utcnow)
    update_on = db.DateTimeField(default=datetime.utcnow)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_on = datetime.utcnow()

    def to_result(self):
        data = self.to_mongo()
        data["added_by"] = {"User": self.added_by.username}
        data["comments"] = [{"username": self.comments[key].added_by.username, "content": self.comments[key].content}
                            for
                            key, content in enumerate(data["comments"])]
        return json_util.dumps(data)


signals.pre_save.connect(Post.pre_save, sender=Post)
Post.register_delete_rule(Comment, 'post_in', db.CASCADE)
