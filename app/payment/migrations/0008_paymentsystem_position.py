# Generated by Django 3.1.5 on 2021-06-06 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20210604_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentsystem',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
