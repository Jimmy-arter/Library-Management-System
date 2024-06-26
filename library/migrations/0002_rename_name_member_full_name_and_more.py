# Generated by Django 5.0.6 on 2024-06-06 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='member',
            name='outstanding_debt',
        ),
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='member',
            name='date_of_birth',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AddField(
            model_name='member',
            name='phone_number',
            field=models.CharField(default='', max_length=15),
        ),
    ]
