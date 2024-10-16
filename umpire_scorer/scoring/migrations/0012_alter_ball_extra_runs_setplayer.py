# Generated by Django 5.1 on 2024-08-21 15:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0011_ball_extra_runs_ball_is_byes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ball',
            name='extra_runs',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='SetPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_striker_batsman', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='non_strike_batsman', to='scoring.player')),
                ('opening_bowler', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='opeing_bowler', to='scoring.player')),
                ('striker_batsman', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='strike_batsman', to='scoring.player')),
            ],
        ),
    ]
