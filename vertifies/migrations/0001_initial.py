# Generated by Django 4.0.3 on 2022-03-27 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vertifie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='phone')),
                ('code', models.CharField(max_length=4, null=True, verbose_name='code')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
