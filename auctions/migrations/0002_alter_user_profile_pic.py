# Generated by Django 4.2.7 on 2023-12-11 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='istockphoto-1337144146-612x612.jpg', null=True, upload_to='auctions/static/images/'),
        ),
    ]
