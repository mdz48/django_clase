# Generated by Django 5.1.5 on 2025-02-10 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0005_alter_libro_autor_alter_libro_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorial.autor'),
        ),
    ]
