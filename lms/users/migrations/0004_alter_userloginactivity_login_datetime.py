# Generated by Django 3.2.17 on 2023-06-03 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_userloginactivity_login_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloginactivity',
            name='login_datetime',
            field=models.DateTimeField(),
        ),
    ]
