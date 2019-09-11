import logging
from logging.config import dictConfig

from apscheduler.schedulers.blocking import BlockingScheduler

from models import XRate, config
import api

sched = BlockingScheduler()

dictConfig(config.LOGGING)
log = logging.getLogger("Tasks")


@sched.scheduled_job('interval', minutes=1)
def update_rates():
    log.info("Job started")
    xrates = XRate.select()
    for rate in xrates:
        try:
            api.update_rate(rate.from_currency, rate.to_currency)
            log.info("api updated")
        except Exception as e:
            log.exception(e)
    log.info("Job finished")


sched.start()

log.info("Scheduler started")
