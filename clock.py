from modules.twitter_user import TwitterUser
from apscheduler.schedulers.blocking import BlockingScheduler
from __init__ import generate_csv_report

sched = BlockingScheduler()
@sched.scheduled_job('interval', days=5)
def generate_reports():
    print("Generating reports...")
    generate_csv_report()
    print("Done ")

sched.start()