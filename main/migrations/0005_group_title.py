# Generated by Django 3.1.1 on 2020-09-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200905_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(default='ab', max_length=250),
            preserve_default=False,
        ),
    ]
