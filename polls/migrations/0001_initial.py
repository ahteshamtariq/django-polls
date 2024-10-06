# -*- coding: utf-8 -*-
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'polls_poll',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('poll', models.ForeignKey(on_delete=models.CASCADE, to='polls.Poll')),
                ('choice', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'polls_choice',
            },
        ),
    ]