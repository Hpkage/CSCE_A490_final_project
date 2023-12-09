# Generated by Django 4.2.7 on 2023-12-09 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_remove_comment_headline'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='auction',
            name='image',
            field=models.ImageField(upload_to='auctions/images/'),
        ),
    ]