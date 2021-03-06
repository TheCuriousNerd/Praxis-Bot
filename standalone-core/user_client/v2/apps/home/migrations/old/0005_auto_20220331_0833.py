# Generated by Django 3.2.12 on 2022-03-31 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20220330_1649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chyron_entry',
            old_name='isEnabled',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='allowedGroups',
            new_name='allowed_groups',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='allowedServices',
            new_name='allowed_services',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='allowedUsers',
            new_name='allowed_users',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='coolDownLength',
            new_name='cooldown_length',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='isEnabled',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='isRestricted',
            new_name='is_restricted',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0',
            old_name='lastUsed',
            new_name='last_used',
        ),
        migrations.RenameField(
            model_name='praxisbot_commands_v0_savedvariables',
            old_name='isEnabled',
            new_name='is_enabled',
        ),
        migrations.RenameField(
            model_name='praxisbot_eventlog',
            old_name='sourceService',
            new_name='source_service',
        ),
        migrations.RemoveField(
            model_name='praxisbot_commands_v0_savedvariables',
            name='lastUpdated',
        ),
        migrations.AddField(
            model_name='praxisbot_commands_v0_savedvariables',
            name='last_used',
            field=models.IntegerField(default=0),
        ),
    ]
