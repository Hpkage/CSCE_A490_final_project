# Generated by Django 4.2.7 on 2023-12-09 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='auctions/static/images/default-profile.jpg', null=True, upload_to=''),
        ),
    ]
