# Generated by Django 4.0.3 on 2022-04-04 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seats', '0003_alter_seat_room_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='종료일'),
        ),
        migrations.AlterField(
            model_name='seat',
            name='lightId',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='조명 id'),
        ),
        migrations.AlterField(
            model_name='seat',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='회원', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seat',
            name='seat_title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='좌석타이틀'),
        ),
    ]