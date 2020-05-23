# Generated by Django 3.0.5 on 2020-04-27 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deck', '0003_auto_20200427_2235'),
        ('turn', '0005_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('move', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='turn.Move')),
                ('received', models.ManyToManyField(to='deck.Card')),
                ('victim', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'payment',
            },
        ),
    ]
