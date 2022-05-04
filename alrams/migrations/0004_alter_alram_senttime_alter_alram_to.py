# Generated by Django 4.0.3 on 2022-04-10 03:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alrams', '0003_rename_subtitle_alram_contents_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alram',
            name='senttime',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='발송시간'),
        ),
        migrations.AlterField(
            model_name='alram',
            name='to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='유져', to=settings.AUTH_USER_MODEL, verbose_name='대상자'),
        ),
    ]
