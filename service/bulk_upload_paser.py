
from datetime import date
from datetime import datetime
import random


def generate_temp_filename():
    today = date.today()
    now = datetime.now()
    l = random.randint(1, 26) + 96
    return today.strftime("%m%d%Y") + now.strftime("%H%M%S") + "_" + chr(l)

