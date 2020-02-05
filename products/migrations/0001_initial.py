# Generated by Django 3.0.1 on 2020-02-04 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscriptions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_details', models.CharField(max_length=200)),
                ('access_link', models.URLField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProductFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_attributes', models.CharField(max_length=200)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upf_product_id', to='products.Product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upf_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_product_category_id', to='products.ProductCategory'),
        ),
        migrations.CreateModel(
            name='PlanProductMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ppm_plan_id', to='subscriptions.Plan')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ppm_product_id', to='products.Product')),
            ],
            options={
                'unique_together': {('plan_id', 'product_id')},
            },
        ),
    ]
