# Generated by Django 5.1 on 2024-09-03 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0015_remove_bowlerstats_b'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bowlerstats',
            name='overs_bowled',
        ),
        migrations.AddField(
            model_name='bowlerstats',
            name='bowled',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bowlerstats',
            name='over',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
