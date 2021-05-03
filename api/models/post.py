from api.utils.database import db
from datetime import datetime
from mongoengine import signals
import random
import string


class Post(db.Document):
    title = db.StringField(required=True)
    audioPost = db.FileField()
    audioFileName = ''.join(random.choice(string.ascii_lowercase) for i in range(8)) + '.mp3'
    tags = db.ListField(db.StringField(max_length=30))
    created_on = db.DateTimeField(default=datetime.utcnow)
    update_on = db.DateTimeField(default=datetime.utcnow)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_on = datetime.utcnow()


signals.pre_save.connect(Post.pre_save, sender=Post)
