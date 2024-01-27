# Generated by Django 5.0.1 on 2024-01-27 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='Ник')),
                ('text', models.TextField(verbose_name='Текст')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')),
            ],
        ),
    ]
