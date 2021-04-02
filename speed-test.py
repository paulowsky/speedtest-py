from datetime import datetime
from msvcrt import kbhit
import multiprocessing
import pandas as pd
import random
import speedtest
import time

def check_speed():
  while True:
    s = speedtest.Speedtest()
    df = pd.read_csv('results.csv',index_col='id')
    time_now = datetime.now().strftime('%H:%M-%d/%m/%Y')
    try:
      servers = s.get_servers()
      server = servers[list(servers.keys())[random.randint(0,len(servers)-1)]]
      s.set_mini_server(server)
      print(server)
      download = f'{round(s.download(threads=None)*(10**-6))}Mbps'
      upload = f'{round(s.upload(threads=None, pre_allocate=True)*(10**-6))}Mbps'
    except:
      continue
    df.loc[len(df)] = [time_now, download, upload]
    df.to_csv('results.csv')
    print(f'Data saved! Time:{time_now} - Download:{download} - Upload:{upload}')
    time.sleep(1)#(30*60) # *30 minutes

if __name__ == '__main__':
  print('\nInitializing speedtest...')
  print('Press any key anytime to exit!\n')
  task_speed = multiprocessing.Process(target=check_speed)
  task_speed.start()
  while(not kbhit()):
    time.sleep(1)
  task_speed.kill()
