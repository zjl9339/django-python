# Generated by Django 2.1.3 on 2019-01-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proApp', '0007_auto_20190114_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='head_img',
            field=models.ImageField(default='', upload_to='media/icons'),
        ),
    ]
