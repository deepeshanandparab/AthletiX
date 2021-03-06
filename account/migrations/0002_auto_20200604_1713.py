# Generated by Django 2.2.4 on 2020-06-04 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='batting_hand',
            field=models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right')], default='Not Mentioned', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='batting_order',
            field=models.CharField(blank=True, choices=[('opener', 'Opener'), ('middle', 'middle Order'), ('finish', 'Finisher'), ('tail', 'Tail Ender')], default='Not Mentioned', max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bowling_hand',
            field=models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right')], default='Not Mentioned', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bowling_type',
            field=models.CharField(blank=True, choices=[('RAF', 'Right Arm Fast'), ('RAM', 'Right Arm Medium'), ('LAF', 'Left Arm Fast'), ('LAM', 'Left Arm Medium'), ('RAFS', 'Right Arm Finger Spin'), ('RAWS', 'Right Arm Wrist Spin'), ('LAFS', 'Left Arm Finger Spin'), ('LAWS', 'Left Arm Wrist Spin')], default='Not Mentioned', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='Not Mentioned', max_length=10, null=True),
        ),
    ]
