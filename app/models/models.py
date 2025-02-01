# app/models/models.py
from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=60)
    email = fields.CharField(max_length=50, unique=True)
    permissions = fields.CharField(max_length=50, default="user")

    posts: fields.ReverseRelation["Post"]
    liked_posts: fields.ManyToManyRelation["Post"]
    favorited_posts: fields.ManyToManyRelation["Post"]
    comments: fields.ReverseRelation["Comment"]
    liked_comments: fields.ReverseRelation["Comment"]

    def __str__(self):
        return self.name


class Post(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=50, unique=True, index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True)
    likes_count = fields.BigIntField(default=0)
    favorites_count = fields.BigIntField(default=0)
    summary = fields.TextField(null=True)

    user = fields.ForeignKeyField("models.User", related_name="posts")
    likes = fields.ManyToManyField(
        "models.User", related_name="liked_posts", through="post_likes"
    )
    favorites = fields.ManyToManyField(
        "models.User", related_name="favorited_posts", through="post_favorites"
    )

    comments: fields.ReverseRelation["Comment"]

    def __str__(self):
        return self.title


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

    def __str__(self):
        return f"Comment by {self.user.name} on {self.post.title}"


class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    posts = fields.ManyToManyField("models.Post", related_name="tags")

    def __str__(self):
        return self.name
