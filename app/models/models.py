# app/models/models.py
from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=60)
    email = fields.CharField(max_length=50, unique=True)


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, unique=True)
    user = fields.ForeignKeyField("models.User", related_name="posts")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    likes_count = fields.BigIntField(default=0)
    favorites_count = fields.BigIntField(default=0)
    likes = fields.ManyToManyField("models.User", related_name="liked_posts")
    favorites = fields.ManyToManyField("models.User", related_name="favorited_posts")
    summary = fields.TextField(null=True)


class Comment(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    time = fields.DatetimeField(auto_now=True)
    likes_count = fields.BigIntField(default=0)
    post = fields.ForeignKeyField("models.Post", related_name="comments")
    user = fields.ForeignKeyField("models.User", related_name="comments")
    liked_by = fields.ManyToManyField(
        "models.User", related_name="liked_comments"
    )  # 点赞用户


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    posts = fields.ManyToManyField("models.Post", related_name="tags")
