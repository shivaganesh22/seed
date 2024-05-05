from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import *

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(movierulz_fcm, 'interval', minutes=30)
	scheduler.add_job(ibomma_fcm, 'interval', minutes=60)
	scheduler.start()