# Generated by Django 3.1.6 on 2021-02-17 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogdetailpage_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogdetailpage',
            old_name='blog_image',
            new_name='banner_image',
        ),
    ]