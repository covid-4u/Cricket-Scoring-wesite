# Generated by Django 5.1 on 2024-08-20 12:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0006_match_overs_alter_match_date_alter_match_loser_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Score',
            new_name='ScoreBoard',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='eco_rate',
            new_name='economy_rate',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='thiries',
            new_name='total_30s',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='fifties',
            new_name='total_50s',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='overs',
            new_name='total_overs_bowled',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='batting_runs',
            new_name='total_runs',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='bowling_runs',
            new_name='total_runs_given',
        ),
        migrations.RenameField(
            model_name='player',
            old_name='wickets',
            new_name='total_wickets',
        ),
        migrations.RemoveField(
            model_name='match',
            name='loser',
        ),
        migrations.RemoveField(
            model_name='match',
            name='overs',
        ),
        migrations.RemoveField(
            model_name='match',
            name='score_team1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='score_team2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner',
        ),
        migrations.AddField(
            model_name='match',
            name='batting_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batting_matches', to='scoring.teamstats'),
        ),
        migrations.AddField(
            model_name='match',
            name='bowling_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bowling_matches', to='scoring.teamstats'),
        ),
        migrations.AddField(
            model_name='match',
            name='match_status',
            field=models.CharField(default='ongoing', max_length=20),
        ),
        migrations.AddField(
            model_name='match',
            name='total_balls',
            field=models.IntegerField(default=120),
        ),
        migrations.AddField(
            model_name='match',
            name='total_overs',
            field=models.FloatField(default=20),
        ),
        migrations.AddField(
            model_name='player',
            name='total_4s',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='total_6s',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='total_balls_faced',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='total_dot_balls',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BatsmanStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runs', models.IntegerField(default=0)),
                ('balls_faced', models.IntegerField(default=0)),
                ('fours', models.IntegerField(default=0)),
                ('sixes', models.IntegerField(default=0)),
                ('strike_rate', models.FloatField(default=0.0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoring.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoring.player')),
            ],
        ),
        migrations.CreateModel(
            name='BowlerStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overs_bowled', models.FloatField(default=0.0)),
                ('runs_given', models.IntegerField(default=0)),
                ('dot_balls', models.IntegerField(default=0)),
                ('wickets', models.IntegerField(default=0)),
                ('economy_rate', models.FloatField(default=0.0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoring.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scoring.player')),
            ],
        ),
        migrations.DeleteModel(
            name='IndividualScore',
        ),
    ]
