# Generated by Django 2.1 on 2018-09-28 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='confirmation',
            field=models.CharField(default='Pending', max_length=12),
        ),
    ]
