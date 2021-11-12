from datetime import datetime


def reformat_str_data(date: str, format_from: str, format_to) -> str:
    date = datetime.strptime(date, format_from).date()
    return date.strftime(format_to)