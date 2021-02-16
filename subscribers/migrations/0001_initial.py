# Generated by Django 3.1.6 on 2021-02-16 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subsciribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(help_text='Email Adresse', max_length=100)),
                ('full_name', models.CharField(help_text='First and Last Name', max_length=100)),
            ],
        ),
    ]