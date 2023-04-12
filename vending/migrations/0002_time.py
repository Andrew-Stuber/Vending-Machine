# Generated by Django 4.1.6 on 2023-02-19 18:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vending', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('item', models.TextField(null=True)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vending.vendingmachine')),
            ],
        ),
    ]