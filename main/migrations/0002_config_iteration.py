# Generated by Django 3.1.6 on 2021-07-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='iteration',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
