# app/models/models.py
from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=60)
    email = fields.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50)
    user = fields.ForeignKeyField("models.User", related_name="posts")

    def __str__(self):
        return self.title


class Comment(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    user = fields.ForeignKeyField("models.User", related_name="comments")

    def __str__(self):
        return self.text


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    posts = fields.ManyToManyField("models.Post", related_name="tags")

    def __str__(self):
        return self.name
