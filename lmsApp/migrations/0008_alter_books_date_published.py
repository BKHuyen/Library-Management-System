# Generated by Django 4.2.7 on 2024-01-11 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsApp', '0007_alter_books_date_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='date_published',
            field=models.CharField(max_length=20),
        ),
    ]
