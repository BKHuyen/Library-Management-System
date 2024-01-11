# Generated by Django 4.2.7 on 2024-01-09 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lmsApp', '0005_remove_borrowdetail_book_remove_borrowdetail_borrow_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowing_date', models.DateField()),
                ('return_date', models.DateField()),
                ('quantity', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('1', 'Pending'), ('2', 'Returned')], default=1, max_length=2)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_id_fk', to='lmsApp.books')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id_fk', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Borrowing Transactions',
            },
        ),
    ]
