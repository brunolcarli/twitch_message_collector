# Generated by Django 2.1.4 on 2022-12-14 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_datetime', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('username', models.CharField(max_length=300)),
            ],
        ),
    ]
