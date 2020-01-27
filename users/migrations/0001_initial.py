# Generated by Django 3.0.1 on 2020-01-27 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgonautsUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_no', models.CharField(max_length=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('algo_credits', models.IntegerField()),
                ('trail', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReferralOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_time', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ug_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=128)),
                ('max_members', models.IntegerField()),
                ('min_members', models.IntegerField()),
                ('standard_group', models.BooleanField(blank=True, default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroupMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_added', models.DateTimeField(auto_now=True)),
                ('time_removed', models.DateTimeField(blank=True, default=users.models.end_date_time, null=True)),
                ('group_admin', models.BooleanField(default=False)),
                ('user_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ugm_user_group_id', to='users.UserGroup')),
                ('user_profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ugm_user_profile_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='usergroup',
            name='memb',
            field=models.ManyToManyField(through='users.UserGroupMapping', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='user_group_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ug_user_group_type_id', to='users.UserGroupType'),
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_code', models.IntegerField()),
                ('referral_time', models.DateTimeField()),
                ('referral_offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_referral_offer_id', to='users.ReferralOffer')),
                ('referred_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_referred_by', to=settings.AUTH_USER_MODEL)),
                ('referred_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_reffered_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
