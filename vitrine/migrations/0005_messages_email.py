# Generated by Django 4.0.6 on 2022-08-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vitrine', '0004_messages_raison_messages_telephone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='email',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
