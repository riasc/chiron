from datetime import datetime

def get_current_time():
    current_time = datetime.now().strftime('[%Y-%m-%d %H:%M:%S] ')
    return current_time
