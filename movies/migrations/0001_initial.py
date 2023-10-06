# Generated by Django 4.2.5 on 2023-10-06 17:13

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
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('director', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('Select Genre', 'Select Genre'), ('Action', 'Action'), ('Comedy', 'Comedy'), ('Drama', 'Drama'), ('Romance', 'Romance'), ('Science Fiction', 'Science Fiction'), ('Horror', 'Horror')], default='Select Genre', max_length=100)),
                ('personal_rating', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]