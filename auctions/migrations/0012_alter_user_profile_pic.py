# Generated by Django 4.2.7 on 2023-12-10 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='auctions/static/images/default-profile.jpg', null=True, upload_to='auctions/static/images/'),
        ),
    ]
