# Generated by Django 3.2.15 on 2022-09-02 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_us', '0002_rename_file_feedback_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='image',
            field=models.ImageField(null=True, upload_to='contact_us/'),
        ),
    ]