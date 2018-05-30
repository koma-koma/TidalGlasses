import urllib.request
import math
import time
from datetime import datetime
from bs4 import BeautifulSoup
import stepperMotorL6470 as sm 
import wiringpi as wp

def getLatestDataLists(location):
    url =  "http://www1.kaiho.mlit.go.jp/KANKYO/TIDE/real_time_tide/images/tide_real/" + location + "Today.txt"

    txt = urllib.request.urlopen(url)
    data = txt.read()

    data = data.decode(errors='replace') # bytesからstrにデコード
    data = data.split('\n') # 改行で区切る
    del data[:11] # 1~11行目を削除
    data.pop()

    data_list = []

    for i in data:
        d = {
            'location':location,
            'year':int(i[:4]),
            'month':int(i[5:7]),
            'date':int(i[8:10]),
            'hour':int(i[11:13]),
            'minute':int(i[14:16]),
            'cm':int(i[-4:])
        }
        data_list.append(d)

    return data_list

def interpolate(target_val, init_val, duration):
    print(str(init_val) + ' -> ' + str(target_val))
    if target_val != init_val:
        d = (target_val - init_val)
        print("speed %d" % (d*500))
        sm.L6470_run(0, int(d*500))
        d = d / duration
        val = init_val
        for i in range(duration):
            print(i, val)
            val = val + d
            time.sleep(1)
    else:
        sm.L6470_softstop(0)
        time.sleep(60)

if __name__=="__main__":
    try:
        sm.L6470_init(0)
        time.sleep(1)
        while True:
            tokyo_data = getLatestDataLists('tokyoM')

            t = datetime.now()
            index = t.hour * 12 + math.floor(t.minute / 5) - 1

            while tokyo_data[index]['cm'] == 9999:
                if index <= 0 :
                    break
                index = index - 1
            latest = tokyo_data[index]

            interpolate(tokyo_data[index]['cm'], tokyo_data[index-1]['cm'], 300)

            print(latest)

    except KeyboardInterrupt:
       sm.L6470_softstop(0) 
       sm.L6470_softhiz(0)
