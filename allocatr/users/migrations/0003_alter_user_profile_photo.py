# Generated by Django 4.0.10 on 2023-03-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_name_user_first_name_user_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(default='https://eu2.contabostorage.com/84d43e83142241f5a2d61d2b3486c2bb:allocatr/media/profile_default.png', upload_to='', verbose_name='profile photo'),
        ),
    ]