# Generated by Django 3.1.5 on 2021-01-30 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='target',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='se_done', to='diary.done', verbose_name='紐つぐ記事'),
        ),
    ]
