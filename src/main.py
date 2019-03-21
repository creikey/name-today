import random
import datetime
import coloredlogs, logging
import os.path
from enum import Enum, auto

coloredlogs.install(level="DEBUG")


class Day(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


day_files = {
    Day.SUNDAY: "sunday-saturday.txt",
    Day.MONDAY: "monday.txt",
    Day.TUESDAY: "tuesday.txt",
    Day.WEDNESDAY: "wednesday.txt",
    Day.THURSDAY: "thursday.txt",
    Day.FRIDAY: "friday.txt",
    Day.SATURDAY: "sunday-saturday.txt",
}

for d in day_files.keys():
    if not os.path.isfile(day_files[d]):
        logging.critical("Could not find file {} for day {}!".format(day_files[d], d))


def get_today() -> Day:
    now = datetime.datetime.now()
    return Day(now.strftime("%A"))


def get_word(day: Day) -> str:
    with open(day_files[day], "r") as f:
        return random.choice(f.readlines()).capitalize().rstrip()


today = get_today()
logging.info("Today is {} {}!".format(get_word(today), today.value))
