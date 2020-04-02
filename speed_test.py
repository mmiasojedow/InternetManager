import datetime

import speedtest

s = speedtest.Speedtest()
s.get_best_server()
s.download()
s.upload()
results = s.results
d = round((results.download / 1000000), 2)
u = round((results.upload / 1000000), 2)
p = round(results.ping, 2)

t = datetime.datetime.now().strftime('%d/%m %H:%M')
date = datetime.datetime.now().strftime('%d.%m')

file = f'./speed_history/speed_history_{date}.txt'
f = open(file, "a+")
f.write(f'{t} - D: {d} / U: {u} / P: {p}\n')
f.close()
