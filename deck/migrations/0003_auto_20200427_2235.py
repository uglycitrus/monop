# Generated by Django 3.0.5 on 2020-04-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deck', '0002_auto_20200426_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='color',
            field=models.CharField(choices=[('brown', 'brown'), ('blue', 'blue'), ('lightgreen', 'lightgreen'), ('lightblue', 'lightblue'), ('orange', 'orange'), ('pink', 'pink'), ('black', 'black'), ('red', 'red'), ('yellow', 'yellow'), ('green', 'green')], max_length=255),
        ),
        migrations.AlterField(
            model_name='card',
            name='secondary_color',
            field=models.CharField(choices=[('brown', 'brown'), ('blue', 'blue'), ('lightgreen', 'lightgreen'), ('lightblue', 'lightblue'), ('orange', 'orange'), ('pink', 'pink'), ('black', 'black'), ('red', 'red'), ('yellow', 'yellow'), ('green', 'green')], max_length=255),
        ),
    ]
