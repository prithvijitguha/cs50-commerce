# Generated by Django 3.1.4 on 2020-12-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bidmodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=120)),
                ('displayname', models.CharField(max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='closedlistings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.CharField(max_length=120)),
                ('closed_date', models.DateTimeField(auto_now=True)),
                ('picture', models.URLField(null=True)),
                ('listingid', models.IntegerField()),
                ('seller', models.CharField(max_length=64)),
                ('buyer', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('listingid', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.CharField(max_length=120)),
                ('listed_date', models.DateTimeField(auto_now=True)),
                ('picture', models.URLField(null=True)),
                ('seller', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('listingid', models.IntegerField()),
            ],
        ),
    ]
