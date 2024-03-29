# Generated by Django 4.1.6 on 2023-04-28 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0003_alter_workshop_legend_hex_color_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='legend_icon_1',
            field=models.CharField(default='flag-solid.svg', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_icon_3',
            field=models.CharField(default='mountain-solid.svg', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_icon_4',
            field=models.CharField(default='lightbulb-solid.svg', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_icon_5',
            field=models.CharField(default='thumbs-down-solid.svg', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_label_1',
            field=models.CharField(default='Ambition', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_label_2',
            field=models.CharField(default='Pro', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_label_3',
            field=models.CharField(default='Challenge', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_label_4',
            field=models.CharField(default='Idea', max_length=40),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='legend_label_5',
            field=models.CharField(default='Con', max_length=40),
        ),
    ]
