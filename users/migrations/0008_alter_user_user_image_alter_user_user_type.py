# Generated by Django 4.0.3 on 2022-04-03 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_is_black'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='users/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('관리자', '관리자'), ('일반', '일반'), ('샤인학원생', '샤인학원생')], max_length=50, null=True, verbose_name='회원타입'),
        ),
    ]
