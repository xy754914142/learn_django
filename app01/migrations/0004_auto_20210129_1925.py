# Generated by Django 3.1.5 on 2021-01-29 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_userdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='class_id',
            new_name='classes',
        ),
        migrations.CreateModel(
            name='Teacher2Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.classes')),
                ('t_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.teacher')),
            ],
        ),
    ]
