# Generated by Django 2.1.7 on 2019-03-20 00:17

from django.db import migrations
from django.conf import settings
import os.path
import csv

def load_comments(apps, schema_editor):
    """Read CSV file of comment data and add it to the posts"""
    Post = apps.get_model('core', 'Post')
    Author = apps.get_model('core', 'Author')
    Comment = apps.get_model('core', 'Comment')

    datapath = os.path.join(settings.BASE_DIR, 'initial_data')
    datafile = os.path.join(datapath, 'comments.csv')

    with open(datafile) as file:
        reader = csv.DictReader(file)
        for row in reader:

            authors_who_favorited = []
            for author_string in row['authors_who_favorited'].split('/'):
                favorite_author, _ = Author.objects.get_or_create(name=author_string)
                authors_who_favorited.append(favorite_author)

            comment_author, _ = Author.objects.get_or_create(name=row['author'])

            print(row['post_title'])
            post = Post.objects.get(title = row['post_title'])

            comment = Comment(
                author = comment_author,
                content = row['content'],
                post = post,
            )
            comment.save()

            for fav_author in authors_who_favorited:
                comment.favorited_by.add(fav_author)    

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190319_1335'),
    ]

    operations = [
        migrations.RunPython(load_comments),
    ]
