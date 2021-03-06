# Generated by Django 3.1.2 on 2020-11-30 08:30

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
            name='Event',
            fields=[
                ('event_id', models.AutoField(db_column='eventId', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('desciption', models.TextField()),
                ('date', models.DateField()),
                ('user_id', models.ForeignKey(db_column='userId', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
