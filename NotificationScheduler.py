from plyer import notification
from apscheduler.schedulers.background import BackgroundScheduler

from Utils.DataBaseOperations import DBHandler, Query
from datetime import datetime


class Notification:
    scheduled_lst = []

    @classmethod
    def _notify(cls, title='title', msg='message'):
        notification.notify(title=title, message=msg, timeout=30, app_icon=r"Resources/Remainder_icon.ico")

    @classmethod
    def schedule(cls, date_time, title, message):
        sched = BackgroundScheduler(daemon=True)
        sched.add_job(cls._notify, 'date', run_date=date_time, id=str(sched), args=[title, message])

        # sched = Job(cls._notify, trigger='date', run_date=date_time, args=[title, message])

        sched.start()
        # sched.remove_job()
        cls.scheduled_lst.append(sched)

    @classmethod
    def remove_all_schedules(cls):
        print("REMOVING2")
        for sched in cls.scheduled_lst:
            sched.remove_job(job_id=str(sched))

    @classmethod
    def load_from_db(cls):
        data = DBHandler.get_data(Query.schedule_for_notification, fetch_size=10)

        print("First")

        cls.remove_all_schedules()

        print("REMOVING")

        for value in data:
            event_type, event_tag, date_time, message = value
            date, time = date_time.split()
            year, month, day = list(map(int, date.split('-')))
            hours, minutes, _ = list(map(int, time.split(':')))
            date_time_object = datetime(year=year, month=month, day=day, hour=hours, minute=minutes)
            if date_time_object > datetime.now():
                cls.schedule(date_time_object, f"{event_type} ({event_tag})", message)

    @classmethod
    def db_changed(cls):
        cls.load_from_db()
