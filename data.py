import sys, traceback
import time
from datetime import datetime, timedelta
import numpy as np
from modules.link.line import Subscriber
from modules.datahandler.csvfile import Formatter, Csv
from modules.imagehandler.graphhandler import Line, Bar, Graph


class Date():
    @staticmethod
    def get_target_date(date):
        h = int(date.strftime("%H"))
        # 7時未満は前日のデータあつかい
        day = date
        if h < 7 :
            day = Date.yesterday(date)
        return day.strftime("%Y_%m_%d")

    @staticmethod
    def get_yesterdate(date):
        day = Date.yesterday(date)
        return day.strftime("%Y_%m_%d")

    @staticmethod
    def yesterday(date):
        return date + timedelta(days=-1)

class Data():
    
    HEADER = ['time', 'humidity', 'temp']

    @staticmethod
    def store(date, humidity, temperature, file_path):
        f = Formatter()
        c = Csv(f)
        contents = [
            [int(date.strftime("%H")),round(humidity, 1), round(temperature, 1)],
        ]
        c.write(file_path, contents, headers=Data.HEADER)


    @staticmethod
    def create_report(target_date, csv_file, graph_file):
        # CSV読み込み
        c = Csv(Formatter())
        contents = c.read(csv_file, headers=Data.HEADER)
        multiarr = np.asarray(contents)
        col_time, col_hum, col_temp = (multiarr[:,0], multiarr[:,1], multiarr[:,2]) 
        
        # グラフ作成
        graph = Graph()
        graph.draw(Bar(y_label="humi(%)"), col_time, col_hum, color="royalblue")
        graph.draw(Line(title="{} report".format(target_date),x_label="time", y_label="temp(C)"), col_time, col_temp, color="red", linewidth=5, addtional=True)
        graph.save(graph.fig, graph_file)
    
class Notify():
    @staticmethod
    def alert(date, humidity, temperature, token):
        current = date.strftime("%Y/%m/%d %H:%M:%S")
        # まるめ
        humi = round(humidity, 1)
        temp = round(temperature, 1)
        
        message = ''
        if humi < 40:
            message = message + 'dry !!! humidity:{}%'.format(humi)
        if not (17 < temp < 25): 
            message = message + ' cold or hot !!! temperature:{}C'.format(temp)

        if message != '':
            try:
                message = current + ': ALERT ' + message
                s = Subscriber(token)
                s.send(message)
            except BaseException as e:
                print(str(e) + " alert:".format(message))
                traceback.print_exc()

    @staticmethod
    def send_report(date, report_file, token):
        try:
            current = date.strftime("%Y/%m/%d %H:%M:%S")
            message = current + ': yesterday report'
            s = Subscriber(token)
            s.send(message, report_file)
        except BaseException as e:
            print(str(e) + " alert:".format(message))
            traceback.print_exc()
