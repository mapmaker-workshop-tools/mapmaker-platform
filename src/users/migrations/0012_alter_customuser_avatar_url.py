# Generated by Django 4.1.7 on 2023-03-29 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_customuser_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar_url',
            field=models.CharField(blank=True, default='https://api.dicebear.com/5.x/pixel-art/svg?seed=249', max_length=300),
        ),
    ]
