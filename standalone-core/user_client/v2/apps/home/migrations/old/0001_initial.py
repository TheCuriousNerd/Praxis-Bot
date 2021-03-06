# Generated by Django 3.2.11 on 2022-03-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chyron_Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('prefix', models.CharField(blank=True, default='', max_length=500)),
                ('text', models.CharField(blank=True, default='', max_length=1000)),
                ('tag', models.CharField(max_length=200)),
                ('isEnabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PraxisBot_Commands_v0',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('command', models.CharField(max_length=200)),
                ('response', models.CharField(max_length=500)),
                ('isEnabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PraxisBot_Commands_v0_SavedVariables',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('data', models.TextField(max_length=1000)),
                ('lastUpdated', models.DateTimeField(auto_now_add=True)),
                ('isEnabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PraxisBot_EventLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event', models.CharField(max_length=300)),
                ('eventType', models.CharField(max_length=300)),
                ('sourceService', models.CharField(max_length=300)),
                ('user', models.CharField(max_length=300)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PraxisBot_Settings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('initialSetup', models.BooleanField(default=False)),
            ],
        ),
    ]
