# Generated by Django 4.2.7 on 2023-12-10 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='istockphoto-1337144146-612x612.jpg', null=True, upload_to='auctions/static/images/'),
        ),
    ]
