# Generated by Django 3.2 on 2023-09-21 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagesize',
            old_name='heihgt',
            new_name='height',
        ),
    ]