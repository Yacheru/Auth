import schedule
import time

def job():
    print("I'm working...")

schedule.every(3).seconds.do(job)

while True:
    schedule.run_pending()
