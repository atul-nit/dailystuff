# Generated by Django 2.2 on 2020-01-25 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20200125_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicereviews',
            name='service_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicecatalog.ServiceProduct'),
        ),
    ]