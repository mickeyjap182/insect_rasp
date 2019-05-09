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
# パラメータ2： LINEAPIトークン  例: xxxxx
if len(sys.argv) < 2 :
    print('arg 1 => line token ) thisfile.py xxxxx')
    sys.exit(1)

# センサーのデータ出力GPIO番号および、種類、計測間隔を指定
sensor = Adafruit_DHT.DHT22
token    = sys.argv[1]

while True:
    try :

        # ファイル情報
        ct = datetime.now()
        if int(ct.strftime("%H") != 6:
            continue
        target_date = Date.get_yesterdate(ct)
        read_csv = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'files', target_date + '.csv')
        save_report = os.path.join( os.path.dirname(os.path.abspath(__file__)), 'report', target_date + '.png')

        # データの送信
        Data.create_report(target_date, read_csv, save_report)
        Notify.send_report(ct, save_report, token)
    except BaseException as e:
        message = 'ERROR:' + str(e) + str(traceback.format_exc())
        print(message)
        s = Subscriber(token)
        s.send(message)

    time.sleep( 58 * 60)
    
