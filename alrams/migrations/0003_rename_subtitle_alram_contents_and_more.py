# Generated by Django 4.0.3 on 2022-04-09 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alrams', '0002_alram_to'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alram',
            old_name='subTitle',
            new_name='contents',
        ),
        migrations.RenameField(
            model_name='alram',
            old_name='title',
            new_name='headings',
        ),
        migrations.AddField(
            model_name='alram',
            name='sented',
            field=models.BooleanField(default=False, verbose_name='발송'),
        ),
        migrations.AddField(
            model_name='alram',
            name='senttime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='alram',
            name='subtitle',
            field=models.CharField(max_length=200, null=True, verbose_name='서브타이틀'),
        ),
    ]
