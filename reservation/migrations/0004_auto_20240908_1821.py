# Generated by Django 3.1.14 on 2024-09-08 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_remove_room_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='view',
        ),
        migrations.AddField(
            model_name='room',
            name='view',
            field=models.CharField(choices=[('SEA', 'SEA View'), ('Lake', 'Lake View'), ('City', 'City View'), ('Mountain', 'Mountain View'), ('Jungle', 'Jungle View')], default='Lake', max_length=20),
        ),
    ]
