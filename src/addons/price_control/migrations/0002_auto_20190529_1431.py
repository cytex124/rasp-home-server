# Generated by Django 2.2.1 on 2019-05-29 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('price_control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pages', to='price_control.Product'),
        ),
    ]
