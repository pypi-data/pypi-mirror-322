from celery.schedules import crontab
import logging
from allianceauth.crontab.models import CronOffset
from django.db import ProgrammingError


logger = logging.getLogger(__name__)


def offset_cron(schedule: crontab) -> crontab:
    """Take a crontab and apply a series of precalculated offsets to spread out tasks execution on remote resources

    Args:
        schedule (crontab): celery.schedules.crontab()

    Returns:
        crontab: A crontab with offsetted Minute and Hour fields
    """

    try:
        cron_offset = CronOffset.get_solo()
        new_minute = [(m + (round(60 * cron_offset.minute))) % 60 for m in schedule.minute]
        new_hour = [(m + (round(24 * cron_offset.hour))) % 24 for m in schedule.hour]

        return crontab(
            minute=",".join(str(m) for m in sorted(new_minute)),
            hour=",".join(str(h) for h in sorted(new_hour)),
            day_of_month=schedule._orig_day_of_month,
            month_of_year=schedule._orig_month_of_year,
            day_of_week=schedule._orig_day_of_week)

    except ProgrammingError as e:
        # If this is called before migrations are run hand back the default schedule
        # These offsets are stored in a Singleton Model,
        logger.error(e)
        return schedule

    except Exception as e:
        # We absolutely cant fail to hand back a schedule
        logger.error(e)
        return schedule
