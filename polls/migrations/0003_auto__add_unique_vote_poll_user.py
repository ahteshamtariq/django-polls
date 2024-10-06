# -*- coding: utf-8 -*-
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto__add_vote__add_field_poll_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('poll', 'user')},
        ),
    ]