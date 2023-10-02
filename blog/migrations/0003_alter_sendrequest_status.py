# Generated by Django 4.2.3 on 2023-09-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_sendrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]
