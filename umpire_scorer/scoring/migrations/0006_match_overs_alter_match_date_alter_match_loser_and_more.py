# Generated by Django 5.1 on 2024-08-19 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0005_remove_match_venue_match_loser_match_score_team1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='overs',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches_lost', to='scoring.teamstats'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches_won', to='scoring.teamstats'),
        ),
    ]
