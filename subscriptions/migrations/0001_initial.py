# Generated by Django 3.0.1 on 2020-01-23 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=500)),
                ('price_per_month', models.PositiveIntegerField()),
                ('price_per_year', models.PositiveIntegerField()),
                ('entry_time', models.DateTimeField()),
                ('expiry_time', models.DateTimeField()),
                ('is_active', models.BooleanField(default=False)),
                ('user_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_start', models.DateTimeField()),
                ('subscription_end', models.DateTimeField()),
                ('subscription_active', models.BooleanField()),
                ('payment_id', models.IntegerField(default=0)),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan')),
                ('user_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroup')),
            ],
        ),
    ]
