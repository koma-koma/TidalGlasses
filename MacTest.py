import urllib.request
import math
import time
from datetime import datetime
from bs4 import BeautifulSoup

import osc

location = "tokyoM"

def openUrlData(location):
    url =  "http://www1.kaiho.mlit.go.jp/KANKYO/TIDE/real_time_tide/images/tide_real/" + location + "Today.txt"

    txt = urllib.request.urlopen(url)

    data = txt.read()
    data = data.decode(errors='replace') # bytesからstrにデコード
    data = data.split('\n') # 改行で区切る

    return data

def getLocationDataDict(data):
    loc_data = {"location": data[2][18:],
                "longtitude": data[3][18:],
                "latitude": data[4][19:],
                "timezone": data[5][18:]}

    return loc_data

def getLatestDataLists(data):
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
        # sm.L6470_run(0, int(d*500))
        d = d / duration
        val = init_val
        for i in range(duration):
            print(i, val)
            osc.sendString("/data", val)
            val = val + d
            time.sleep(1)
    else:
        # sm.L6470_softstop()
        d = (target_val - init_val)
        print("speed %d" % (d*500))
        d = d / duration
        val = init_val
        for i in range(60):
            print(i, val)
            osc.sendString("/data", val)
            val = val + d
            time.sleep(1)
        # time.sleep(60)

if __name__=="__main__":
    try:
        print("type location")
        location = input()
        # sm.L6470_init()
        time.sleep(1)

        data = openUrlData(location)
        location_dict = getLocationDataDict(data)
        li = []
        for key in location_dict.keys():
            li.append(location_dict[key])
        osc.sendList("/location", li)

        while True:
            data = openUrlData(location)
            tide_data = getLatestDataLists(data)

            t = datetime.now()
            index = t.hour * 12 + math.floor(t.minute / 5) - 1

            while tide_data[index]['cm'] == 9999:
                if index <= 0 :
                    break
                index = index - 1
            latest = tide_data[index]
            
            datatime = []
            datatime.append(str(latest["year"]) + "-" + str(latest["month"]) + "-" + str(latest["date"]))
            datatime.append(str(latest["hour"]) + ":" + str(latest["minute"]))
            osc.sendList("/time", datatime)
            print(latest)

            interpolate(tide_data[index]['cm'], tide_data[index-1]['cm'], 300)


    except KeyboardInterrupt:
    #    sm.L6470_softstop() 
    #    sm.L6470_softhiz()
        print("")