from datetime import datetime, timedelta
import shutil

date = datetime.now()
yesterday = date - timedelta(days=1)
y_date = yesterday.strftime('%d.%m')

shutil.move(f'internet_history_{y_date}.txt', f'internet_history/internet_history_{y_date}.txt')
shutil.move(f'speed_history_{y_date}.txt', f'speed_history/speed_history_{y_date}.txt')
