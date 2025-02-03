from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    # Initialize the scheduler
    scheduler = BackgroundScheduler()
    # Schedule the task to run daily at 12:00 PM
    # scheduler.add_job(
    #     send_auto_pay_reminders,
    #     CronTrigger(hour=9, minute=9),  # Runs every day at 12:00 PM
    # )
    scheduler.start()