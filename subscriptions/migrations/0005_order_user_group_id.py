# Generated by Django 3.0.3 on 2020-02-25 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userfeedback_subject'),
        ('subscriptions', '0004_auto_20200224_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user_group_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.UserGroup'),
        ),
    ]
