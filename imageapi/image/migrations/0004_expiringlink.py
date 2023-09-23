# Generated by Django 3.2.10 on 2023-09-23 12:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_auto_20230923_0849'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiringLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('expires_at', models.DateTimeField()),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image.image')),
            ],
        ),
    ]
