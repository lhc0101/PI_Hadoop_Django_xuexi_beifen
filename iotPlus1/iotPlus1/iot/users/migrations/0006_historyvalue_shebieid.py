# Generated by Django 2.0 on 2019-05-16 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190506_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyvalue',
            name='shebieid',
            field=models.CharField(default=2, max_length=32),
            preserve_default=False,
        ),
    ]
