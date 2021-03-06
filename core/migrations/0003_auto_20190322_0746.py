# Generated by Django 2.1.7 on 2019-03-22 12:46

from django.db import migrations
from django.conf import settings
# from django.contrib.auth.models import User
import os.path
import csv

def load_comments(apps, schema_editor):
    """Read CSV file of comment data and add it to the posts"""
    Post = apps.get_model('core', 'Post')
    Comment = apps.get_model('core', 'Comment')
    User = apps.get_model('auth', 'User')

    datapath = os.path.join(settings.BASE_DIR, 'initial_data')
    datafile = os.path.join(datapath, 'comments.csv')

    with open(datafile) as file:
        reader = csv.DictReader(file)
        for row in reader:

            users_who_favorited = []
            for user_string in row['users_who_favorited'].split('/'):
                favorite_user, _ = User.objects.get_or_create(username=user_string)
                users_who_favorited.append(favorite_user)

            comment_author, _ = User.objects.get_or_create(username=row['author'])

            post = Post.objects.filter(title = row['post_title'])[0]

            comment = post.comments.create(                
                content = row['content'],
                author = comment_author,
            )

            # comment = Comment(
            #     author = comment_author,
            #     content = row['content'],
            #     post = post,
            # )
            # comment.save()

            for fav_user in users_who_favorited:
                comment.favorited_by.add(fav_user) 

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190322_0744'),
    ]

    operations = [migrations.RunPython(load_comments)
    ]
