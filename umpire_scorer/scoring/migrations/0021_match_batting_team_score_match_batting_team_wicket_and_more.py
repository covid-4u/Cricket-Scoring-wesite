# Generated by Django 5.1 on 2024-09-04 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0020_remove_ball_team_over_match_over_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='batting_team_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='batting_team_wicket',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='total_overs',
            field=models.FloatField(default=10),
        ),
    ]
