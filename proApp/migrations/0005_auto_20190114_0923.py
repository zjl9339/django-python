# Generated by Django 2.1.3 on 2019-01-14 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proApp', '0004_auto_20190109_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='bookCover',
            field=models.ImageField(upload_to='icons'),
        ),
        migrations.AlterField(
            model_name='book',
            name='fileMore',
            field=models.FileField(default='', upload_to='files/%Y%m%d'),
        ),
    ]