from apscheduler.scheduler import Scheduler

from divvy import sync, fetch


def poll(datadir):
    scheduler = Scheduler()
    scheduler.start()

    @scheduler.interval_schedule(minutes=1)
    def fetch_job():
        fetch.fetch(datadir)
        scheduler.print_jobs()

    @scheduler.interval_schedule(hours=6)
    def push_job():
        sync.git_commit_push(datadir)
        scheduler.print_jobs()
