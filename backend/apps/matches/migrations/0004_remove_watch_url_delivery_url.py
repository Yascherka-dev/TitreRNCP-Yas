from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0003_add_league_id_venue_thumb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='watch_url',
        ),
        migrations.RemoveField(
            model_name='match',
            name='delivery_url',
        ),
    ]
