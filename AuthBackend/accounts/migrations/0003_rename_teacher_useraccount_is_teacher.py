# Generated by Django 4.2.1 on 2023-05-24 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_useraccount_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useraccount',
            old_name='teacher',
            new_name='is_teacher',
        ),
    ]
