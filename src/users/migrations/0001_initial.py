# Generated by Django 4.1.7 on 2023-04-28 09:50

from django.db import migrations, models
import django.utils.timezone
import pathlib


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('linkedin', models.CharField(blank=True, max_length=300)),
                ('organisation', models.CharField(blank=True, max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('avatar_url', models.CharField(blank=True, default='https://api.dicebear.com/5.x/pixel-art/svg?seed=430', max_length=500)),
                ('zoom_level', models.CharField(blank=True, default=0, max_length=1)),
                ('avatar', models.FileField(blank=True, default=pathlib.PurePosixPath('/Users/pvandoorn/Documents/Programming/mapmaker/src/staticfiles/images/avatar.jpg'), null=True, upload_to='media/avatars/')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
