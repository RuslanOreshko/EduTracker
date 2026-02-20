from datetime import date


def academic_year_start(for_date: date) -> date:
    year = for_date.year if for_date.month >= 9 else for_date.year - 1
    return date(year, 9, 1)