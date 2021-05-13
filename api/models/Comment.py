from mongoengine import signals

from api.utils.database import db
from datetime import datetime


class Comment(db.Document):
    added_by = db.ReferenceField('User')
    content = db.StringField()
    post_in = db.ReferenceField('Post')
    created_on = db.DateTimeField(default=datetime.utcnow)
    update_on = db.DateTimeField(default=datetime.utcnow)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.update_on = datetime.utcnow()


signals.pre_save.connect(Comment.pre_save, sender=Comment)
