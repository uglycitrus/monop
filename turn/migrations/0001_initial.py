# Generated by Django 3.0.5 on 2020-04-25 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deck', '0001_initial'),
        ('game', '0004_auto_20200425_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deck.Card')),
            ],
            options={
                'db_table': 'move',
            },
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.NullBooleanField(default=None)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turns', to='game.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'turn',
                'unique_together': {('game', 'is_active')},
            },
        ),
        migrations.CreateModel(
            name='SlyDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='turn.Move')),
                ('received', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sly_deal_received', to='deck.Card')),
                ('requested', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sly_deal_requested', to='deck.Card')),
            ],
            options={
                'db_table': 'sly_deal',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('move', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='turn.Move')),
                ('received', models.ManyToManyField(to='deck.Card')),
                ('victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='move',
            name='turn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='turn.Turn'),
        ),
        migrations.CreateModel(
            name='ForcedDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='turn.Move')),
                ('offered', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forced_deal_offered', to='deck.Card')),
                ('requested', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forced_deal_requested', to='deck.Card')),
            ],
            options={
                'db_table': 'forced_deal',
            },
        ),
        migrations.CreateModel(
            name='DealBreaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='turn.Move')),
                ('received', models.ManyToManyField(related_name='deal_breaker_received', to='deck.Card')),
                ('requested', models.ManyToManyField(related_name='deal_breaker_requested', to='deck.Card')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='move',
            unique_together={('turn', 'index')},
        ),
    ]
