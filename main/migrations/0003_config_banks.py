# Generated by Django 3.1.6 on 2021-07-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_config_iteration'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='banks',
            field=models.CharField(default='halyk', max_length=200),
            preserve_default=False,
        ),
    ]
