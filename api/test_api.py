from models import XRate, datetime

from config import logging, LOGGING

log = logging.getLogger("TestApi")
fh = logging.FileHandler(LOGGING["file"])
fh.setLevel(LOGGING["level"])
fh.setFormatter(LOGGING["formatter"])
log.addHandler(fh)
log.setLevel(LOGGING["level"])


def update_xrates(from_currency, to_currency):
    log.info("Started update for: %s=>%s" % (from_currency, to_currency))
    xrate = XRate.select().where(XRate.from_currency == from_currency,
                                 XRate.to_currency == to_currency).first()

    log.debug("rate before: %s", xrate.rate)
    xrate.rate += 0.01
    xrate.updated = datetime.now()
    xrate.save()

    log.debug("rate after: %s", xrate.rate)
    log.info("Finished update for: %s=>%s" % (from_currency, to_currency))
