# Generated by Django 5.0.6 on 2024-11-05 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_remove_mail_attachments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='attachments',
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachments/')),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='mail.mail')),
            ],
        ),
    ]
