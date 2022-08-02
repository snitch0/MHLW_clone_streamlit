from datetime import datetime

def format_date(dt: datetime):
    month_str = str(dt.month).zfill(2)
    day_str = str(dt.day).zfill(2)
    return f"{str(dt.year)}年{month_str}月{day_str}日"
    
    
def get_today():
    today = datetime.today()
    return format_date(today)