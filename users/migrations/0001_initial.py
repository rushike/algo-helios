# Generated by Django 3.0.3 on 2020-02-18 11:36

from django.conf import settings
import django.core.validators
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
                ('algo_credits', models.IntegerField(default=0)),
                ('referral_code', models.CharField(default=users.models.get_unique_referral_code, max_length=8, validators=[django.core.validators.MinLengthValidator(4)])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'unique_together': {('referral_code',)},
            },
        ),
        migrations.CreateModel(
            name='ReferralOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('offer_credits_to', models.IntegerField()),
                ('offer_credits_by', models.IntegerField()),
                ('offer_start', models.DateTimeField(auto_now=True)),
                ('offer_end', models.DateTimeField(blank=True)),
                ('offer_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_time', models.DateTimeField(auto_now=True)),
                ('multiplier', models.IntegerField(default=1)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ug_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=128)),
                ('max_members', models.IntegerField(default=1)),
                ('min_members', models.IntegerField(default=1)),
                ('standard_group', models.BooleanField(blank=True, default=True)),
                ('eligible_for_trial', models.BooleanField(default=True)),
            ],
            options={
                'unique_together': {('type_name', 'max_members', 'min_members')},
            },
        ),
        migrations.CreateModel(
            name='UserGroupMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_added', models.DateTimeField(auto_now=True)),
                ('time_removed', models.DateTimeField(default=users.models.end_date)),
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
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_message', models.CharField(max_length=1024)),
                ('category_name', models.CharField(max_length=20)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usergroup',
            unique_together={('user_group_type_id', 'admin')},
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_code', models.CharField(max_length=8)),
                ('referral_time', models.DateTimeField()),
                ('referral_offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_referral_offer_id', to='users.ReferralOffer')),
                ('referred_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_referred_by', to=settings.AUTH_USER_MODEL)),
                ('referred_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='r_reffered_to', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('referred_to',)},
            },
        ),
    ]
