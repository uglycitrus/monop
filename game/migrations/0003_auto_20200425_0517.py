# Generated by Django 3.0.5 on 2020-04-25 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_player_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='is_winner',
            field=models.NullBooleanField(default=None),
        ),
    ]
