# Generated by Django 3.2.10 on 2021-12-22 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_techpost_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='economypost',
            name='source',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='marketpost',
            name='source',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='sportspost',
            name='source',
            field=models.URLField(max_length=500),
        ),
    ]
