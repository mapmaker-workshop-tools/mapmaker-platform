# Generated by Django 4.1.6 on 2023-02-25 09:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abmbition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]