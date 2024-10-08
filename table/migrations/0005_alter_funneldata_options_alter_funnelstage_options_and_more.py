# Generated by Django 5.0.7 on 2024-07-31 13:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0004_funnelstage_funneldata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='funneldata',
            options={'verbose_name': 'Модель столбцов', 'verbose_name_plural': 'Столбцы'},
        ),
        migrations.AlterModelOptions(
            name='funnelstage',
            options={'verbose_name': 'Модель строк', 'verbose_name_plural': 'Строки'},
        ),
        migrations.AlterField(
            model_name='funneldata',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='funneldata',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='funneldata',
            name='funnel_stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table.funnelstage', verbose_name='Название столбца'),
        ),
        migrations.AlterField(
            model_name='funnelstage',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название строки'),
        ),
        migrations.CreateModel(
            name='CallRows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rows', models.TextField(blank=True, verbose_name='Описание причины')),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_rows', to='table.recruitmentfunnel', verbose_name='Отчетный период')),
            ],
            options={
                'verbose_name': 'Модель строк при первом зконке',
                'verbose_name_plural': 'Строки при первых звонках',
            },
        ),
        migrations.CreateModel(
            name='CallColumns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('columns', models.IntegerField(default=0, verbose_name='Значение')),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruitment_funnel', to='table.recruitmentfunnel', verbose_name='Отчетный период')),
                ('rows', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='table.callrows', verbose_name='Название столбца')),
            ],
            options={
                'verbose_name': 'Модель столбцов',
                'verbose_name_plural': 'Столбцы',
            },
        ),
    ]
