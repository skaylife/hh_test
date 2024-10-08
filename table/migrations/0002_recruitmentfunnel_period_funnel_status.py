# Generated by Django 5.0.7 on 2024-07-25 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruitmentFunnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(verbose_name='Месяц')),
                ('year', models.IntegerField(verbose_name='Год')),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='table.recruitmentfunnel')),
            ],
        ),
        migrations.CreateModel(
            name='Funnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_name', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funnel_stages', to='table.recruitmentfunnel')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='table.recruitmentfunnel')),
            ],
        ),
    ]
