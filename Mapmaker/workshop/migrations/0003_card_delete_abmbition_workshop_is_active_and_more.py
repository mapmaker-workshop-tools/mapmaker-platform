# Generated by Django 4.1.6 on 2023-02-25 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workshop', '0002_abmbition_workshop_date_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('cardtype', models.CharField(choices=[('ambition', 'Ambition'), ('challenge', 'Challenge'), ('idea', 'Idea'), ('pro', 'Pro'), ('con', 'Con')], max_length=20)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('followers', models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Abmbition',
        ),
        migrations.AddField(
            model_name='workshop',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='card',
            name='workshop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workshop', to='workshop.workshop'),
        ),
    ]