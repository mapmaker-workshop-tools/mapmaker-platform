# Generated by Django 4.1.6 on 2023-04-16 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0061_alter_customuser_avatar_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar_url',
            field=models.CharField(blank=True, default='https://api.dicebear.com/5.x/pixel-art/svg?seed=153', max_length=500),
        ),
    ]
