# Generated by Django 3.0.3 on 2020-02-18 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriptions', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='user_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroup'),
        ),
        migrations.AddField(
            model_name='planoffermap',
            name='offer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Offer'),
        ),
        migrations.AddField(
            model_name='planoffermap',
            name='plan_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan'),
        ),
        migrations.AddField(
            model_name='plan',
            name='plan_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.PlanType'),
        ),
        migrations.AddField(
            model_name='plan',
            name='user_group_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroupType'),
        ),
        migrations.AddField(
            model_name='payment',
            name='subscription_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Subscription'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user_group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserGroup'),
        ),
        migrations.AddField(
            model_name='offerprerequisites',
            name='plan_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='subscriptions.Plan'),
        ),
        migrations.AddField(
            model_name='offer',
            name='offer_preqreq',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.OfferPrerequisites'),
        ),
        migrations.AlterUniqueTogether(
            name='plan',
            unique_together={('plan_name', 'user_group_type_id', 'plan_type_id')},
        ),
    ]
