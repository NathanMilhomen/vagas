# Generated by Django 3.2.4 on 2021-06-15 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0002_auto_20210615_0953'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companys'},
        ),
        migrations.RenameField(
            model_name='jobvacancy',
            old_name='name',
            new_name='description',
        ),
        migrations.AddField(
            model_name='jobvacancy',
            name='number_of_candidates',
            field=models.IntegerField(default=0),
        ),
    ]