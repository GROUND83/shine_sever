# Generated by Django 4.0.4 on 2022-04-17 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seats', '0008_delete_roomtype_delete_seattype_seat_room_cate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seat',
            name='room_cate',
        ),
    ]
