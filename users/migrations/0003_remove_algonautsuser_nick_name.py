# Generated by Django 3.0.1 on 2020-01-17 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_algonautsuser_nick_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='algonautsuser',
            name='nick_name',
        ),
    ]
