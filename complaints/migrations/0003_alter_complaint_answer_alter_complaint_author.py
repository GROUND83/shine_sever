# Generated by Django 4.0.3 on 2022-04-11 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('complaints', '0002_complaint_answer_complaint_complaintype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='answer',
            field=models.TextField(blank=True, null=True, verbose_name='답변'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='회원'),
        ),
    ]
