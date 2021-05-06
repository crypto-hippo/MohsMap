import time


def now():
    return time.time()

jinja_vars = {
    "now": now 
}