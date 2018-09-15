# Generated by Django 2.1.1 on 2018-09-15 13:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gold', models.PositiveIntegerField()),
                ('gold_production', models.PositiveIntegerField()),
                ('rock', models.PositiveIntegerField()),
                ('rock_production', models.PositiveIntegerField()),
                ('wood', models.PositiveIntegerField()),
                ('wood_production', models.PositiveIntegerField()),
                ('last_updated', models.DateTimeField()),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]