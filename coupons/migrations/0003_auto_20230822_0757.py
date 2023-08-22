# Generated by Django 3.2.19 on 2023-08-22 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0002_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='image',
        ),
        migrations.AddField(
            model_name='ticket',
            name='file',
            field=models.FileField(default='hello', upload_to='tickets/'),
            preserve_default=False,
        ),
    ]