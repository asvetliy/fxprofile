from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import close_expired_blockchain_transactions


class Updater(object):
    @staticmethod
    def start():
        scheduler = BackgroundScheduler()
        scheduler.add_job(close_expired_blockchain_transactions, 'interval', minutes=1)
        scheduler.start()
