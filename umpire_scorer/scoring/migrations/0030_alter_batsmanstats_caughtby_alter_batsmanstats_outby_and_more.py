# Generated by Django 5.1 on 2024-09-10 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoring', '0029_batsmanstats_caughtby_batsmanstats_outby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batsmanstats',
            name='caughtBy',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='batsmanstats',
            name='outBy',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='batsmanstats',
            name='outType',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
