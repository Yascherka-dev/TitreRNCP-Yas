"""
Scheduler APScheduler — tourne dans le process gunicorn.
Lance sync_livescores toutes les 60 secondes quand SCHEDULER_ENABLED=1.
"""
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

logger = logging.getLogger(__name__)


def _sync_livescores_job():
    from datetime import timedelta
    from django.utils import timezone
    from apps.matches.models import Match
    from apps.matches.sports_api import fetch_livescores

    _LIVE = ['1H', '2H', 'HT', 'ET', 'P', 'BT']
    cutoff = timezone.now() - timedelta(hours=3)
    Match.objects.filter(statut__in=_LIVE, date_heure__lt=cutoff).update(statut='FT')

    updates = fetch_livescores()
    count = 0
    for upd in updates:
        updated = Match.objects.filter(external_id=upd['external_id']).update(
            statut=upd['statut'],
            score_a=upd['score_a'],
            score_b=upd['score_b'],
        )
        if updated:
            count += 1
    if count:
        logger.info('Livescores: %d score(s) mis à jour.', count)


def start():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(
        _sync_livescores_job,
        trigger=IntervalTrigger(seconds=60),
        id='sync_livescores',
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=30,
    )
    scheduler.start()
    logger.info('Scheduler démarré — sync_livescores toutes les 60s.')
