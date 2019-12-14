import random
import string
import hashlib
import datetime


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


def hash(text, size):
    return format(
        int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % 16 ** size, "x"
    )


def random_date():
    earliest = datetime.date(1910, 1, 1)
    latest = datetime.date(2018, 1, 1)
    delta = latest - earliest
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return earliest + datetime.timedelta(seconds=random_second)
