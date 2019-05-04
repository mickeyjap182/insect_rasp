import sys
import os
import traceback
import time
from datetime import datetime, timedelta
import requests

import Adafruit_DHT

from data import Date, Data, Notify
from modules.link.line import Subscriber

### データの蓄積を行う###
# パラメータ1: データ入力PIN番号  例: 4
# パラメータ2： LINEAPIトークン  例: xxxxx
# パラメータ3： インターバル時間（分） 例: 10
if len(sys.argv) < 3 :
    print('arg 1 => Gpio number of pin ) thisfile.py 4')
    sys.exit(1)

# センサーのデータ出力GPIO番号および、種類、計測間隔を指定
pin = sys.argv[1]
sensor = Adafruit_DHT.DHT22
token    = sys.argv[2]
minute = int(sys.argv[3]) if (len(sys.argv) >= 4 and sys.argv[3].isdigit()) else 30

while True:
    # 温度・湿度の取得
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # 現在時刻の取得
    ct = datetime.now()
    if humidity is not None and temperature is not None:
        try :
            # file_name = ct.strftime("%Y/%m/%d %H:%M:%S") + '.csv'
            save_csv = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'files', Date.get_target_date(ct) + '.csv')

            # アラート
            Notify.alert(ct, humidity, temperature, token)
            # データの蓄積
            Data.store(ct, humidity, temperature, save_csv)
        except BaseException as e:
            message = 'ERROR:' + str(e) + str(traceback.format_exc())
            
            s = Subscriber(token)
            s.send(message)

    else:
        print('{0}: Failed to get reading. Try again!'.format(ct))
    time.sleep( 60 * minute)

