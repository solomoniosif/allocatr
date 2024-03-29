# Generated by Django 4.0.10 on 2023-03-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0010_transaction_is_planned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='is_recurring',
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_recurrent',
            field=models.BooleanField(default=False, verbose_name='Is recurrent'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='currency',
            field=models.CharField(choices=[('AUD', 'Australia Dollar'), ('CAD', 'Canada Dollar'), ('RMB', 'China Yuan Renminbi'), ('EUR', 'Euro Member Countries'), ('RON', 'Romania Leu'), ('GBP', 'United Kingdom Pound'), ('USD', 'United States Dollar')], default='USD', max_length=3),
        ),
    ]
