# Generated by Django 4.0.3 on 2022-04-11 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seats', '0005_alter_seat_is_clean_alter_seat_is_light_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='seat_title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='좌석타이틀'),
        ),
    ]
