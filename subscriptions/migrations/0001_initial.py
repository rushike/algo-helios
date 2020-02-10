# Generated by Django 3.0.1 on 2020-02-04 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=20)),
                ('offer_start_date', models.DateTimeField()),
                ('offer_end_date', models.DateTimeField()),
                ('offer_desc', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=50)),
                ('price_per_month', models.PositiveIntegerField()),
                ('price_per_year', models.PositiveIntegerField()),
                ('entry_time', models.DateTimeField()),
                ('expiry_time', models.DateTimeField()),
                ('user_group_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroupType')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_start', models.DateTimeField()),
                ('subscription_end', models.DateTimeField()),
                ('payment_id', models.IntegerField(default=0)),
                ('is_trial', models.BooleanField(default=False)),
                ('offer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='subscriptions.Offer')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan')),
                ('user_group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroup')),
            ],
        ),
        migrations.CreateModel(
            name='PlanOfferMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Offer')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan')),
            ],
        ),
        migrations.CreateModel(
            name='OfferPrerequisites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan')),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='offer_preqreq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.OfferPrerequisites'),
        ),
    ]
