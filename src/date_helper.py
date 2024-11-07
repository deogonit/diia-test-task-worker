from datetime import datetime


def get_previous_quarter():
    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1
    previous_year = now.year if quarter > 1 else now.year - 1
    previous_quarter = quarter - 1 if quarter > 1 else 4
    return previous_year, previous_quarter
