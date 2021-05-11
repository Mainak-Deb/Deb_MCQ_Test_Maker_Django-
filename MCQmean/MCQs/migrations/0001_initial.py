# Generated by Django 3.0.8 on 2021-05-08 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Examset',
            fields=[
                ('name', models.CharField(max_length=90)),
                ('qid', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=90)),
                ('topic', models.CharField(max_length=200)),
                ('time', models.IntegerField(default=60)),
                ('fm', models.IntegerField(default=0)),
            ],
        ),
    ]