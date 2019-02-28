import sys
import time
from datetime import datetime
import requests

import Adafruit_DHT

# パラメータ1: データ入力PIN番号  例: 4
# パラメータ2： POST送信URL  例: https:aaa.com/api
# パラメータ3： インターバル時間（分） 例: 10

if len(sys.argv) < 3 :
    print('arg 1 => Gpio number of pin ) thisfile.py 4')
    sys.exit(1)

# センサーのデータ出力GPIO番号および、種類、計測間隔を指定
pin = sys.argv[1]
sensor = Adafruit_DHT.DHT22
url    = sys.argv[2]
minute = int(sys.argv[3]) if (len(sys.argv) >= 4 and sys.argv[3].isdigit()) else 30
SENSOR_ID = 1

while True:
    # 温度・湿度の取得
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # 現在時刻の取得
    ct = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    if humidity is not None and temperature is not None:
        try :
            # データの送信
            data = {
                'sensor_id':SENSOR_ID,
                'humidity': round(humidity, 1),
                'temp': round(temperature, 1),
                'inspected_at': ct,
            }
            res = requests.post(url, json=data)
            if res.status_code != 200 :
                print(res.text)
        except BaseException as e:
            print(e.message)
    else:
        print('{0}: Failed to get reading. Try again!'.format(ct))
    time.sleep( 60 * minute)

