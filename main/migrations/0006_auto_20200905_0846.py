# Generated by Django 3.1.1 on 2020-09-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_group_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]