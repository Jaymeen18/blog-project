# Generated by Django 4.2.3 on 2023-09-12 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Deleted', 'Deleted')], default='Pending', max_length=10),
        ),
    ]
