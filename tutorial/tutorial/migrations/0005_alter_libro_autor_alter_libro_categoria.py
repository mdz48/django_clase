# Generated by Django 5.1.5 on 2025-02-09 02:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0004_libro_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.usuario'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='categoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutorial.categoria'),
        ),
    ]
