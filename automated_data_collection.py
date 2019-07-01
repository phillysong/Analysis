import pandas as pd


from secrets import oanda_p_acc_token,oanda_p_acc_id
import secrets
import json
from datetime import datetime,timedelta
import oandapyV20.endpoints.instruments as instruments
import oandapyV20

accountID, access_token = oanda_p_acc_id,oanda_p_acc_token
api = oandapyV20.API(access_token=access_token)

#SQL setup
import sqlite3
from sqlite3 import Error

def create_connection(db):
    try:
        conn=sqlite3.connect(db)
    except Error as e:
        print(e)
    finally:
        conn.close()


def create_table(table_name):
    conn=sqlite3.connect(r'A:\Programming files\Python scripts\Oanda\phase2.db')
    c=conn.cursor()
    
    query = """ CREATE TABLE IF NOT EXISTS {} (
        -- id integer PRIMARY KEY,
        time datetime,
        open float,
        high float,
        low float,
        close float
        );""".format("'{}'").format(table_name)
    
    c.execute(query).fetchall()
    conn.commit()
    conn.close()
    return None

#create db
# path=r'A:\Programming files\Python scripts\Oanda\phase2.db'
# create_connection(path)
# #execute creation of tables
# pairs_list=['M1_EUR_USD','M1_GBP_USD','M1_USD_JPY','M1_EUR_JPY','M1_GBP_JPY','M1_USD_CAD','M5_EUR_USD','M5_GBP_USD','M5_USD_JPY','M5_EUR_JPY','M5_GBP_JPY','M5_USD_CAD','M15_EUR_USD','M15_GBP_USD','M15_USD_JPY','M15_EUR_JPY','M15_GBP_JPY','M15_USD_CAD','M30_EUR_USD','M30_GBP_USD','M30_USD_JPY','M30_EUR_JPY','M30_GBP_JPY','M30_USD_CAD','H1_EUR_USD','H1_GBP_USD','H1_USD_JPY','H1_EUR_JPY','H1_GBP_JPY','H1_USD_CAD','H4_EUR_USD','H4_GBP_USD','H4_USD_JPY','H4_EUR_JPY','H4_GBP_JPY','H4_USD_CAD','D_EUR_USD','D_GBP_USD','D_USD_JPY','D_EUR_JPY','D_GBP_JPY','D_USD_CAD']
# for i in pairs_list:
#     create_table(i)

def insert_stuff(table_name,query_args):
    conn=sqlite3.connect(r'A:\Programming files\Python scripts\Oanda\phase2.db')
    query='''INSERT INTO {} (time,open,high,low,close)
            values (?,?,?,?,?)'''.format("'{}'").format(table_name)
    c=conn.cursor()
    c.execute(query,query_args)
    conn.commit()
    conn.close()
    return c.lastrowid

def time_query_check(table_name,time):
    conn=sqlite3.connect(r'A:\Programming files\Python scripts\Oanda\phase2.db')
    # conn=sqlite3.connect(r'A:\Programming files\Python scripts\dbbackups\phase2.db')
    query="""SELECT time
    FROM {}
    WHERE time = {}""".format("'{}'".format(table_name),"'{}'".format(time))
    c=conn.cursor()
    c.execute(query)
    return c.fetchall()

def insert_new_into_table(trading_pair,time_frame):
    added_times=[]
    #request data from oanda
    params={
    'granularity': time_frame
    }
    r=instruments.InstrumentsCandles(instrument=trading_pair,
                                    params=params)
    requested_data=api.request(r)
    
    #prep data to push
    no_of_candles=len(requested_data['candles'])
    for i in range(no_of_candles):
        if requested_data['candles'][i]['complete'] == True:
            raw_time=requested_data['candles'][i]['time']
            formatted_time=datetime.strptime(raw_time,'%Y-%m-%dT%H:%M:%S.000000000Z')
            formatted_time=formatted_time+timedelta(hours=3)
            temp=str(formatted_time)[:-3]
            formatted_time=temp.replace('-','.')

            table_name='{}_{}'.format(time_frame,trading_pair)
            #check if time needs to be added
            if time_query_check(table_name,formatted_time) == []:
                raw_data=requested_data['candles'][i]['mid']
                o=raw_data['o']
                h=raw_data['h']
                l=raw_data['l']
                c=raw_data['c']
                insert_stuff(table_name,(formatted_time,o,h,l,c))        
                added_times.append(formatted_time)
    return added_times

dc_trading_pairs=['EUR_USD','GBP_USD','USD_JPY','EUR_JPY','GBP_JPY','USD_CAD']
dc_time_frames=['M1','M5','M15','M30','H1','H4','D']
if datetime.today().weekday()>=0 and datetime.today().weekday() <=3:
    for pair in dc_trading_pairs:
        for tf in dc_time_frames:
            print('checking data for {} {}'.format(tf,pair))
            insert_new_into_table(pair,tf)
elif datetime.today().weekday() == 4 and datetime.now().hour <17:
    for pair in dc_trading_pairs:
        for tf in dc_time_frames:
            print('checking data for {} {}'.format(tf,pair))
            insert_new_into_table(pair,tf)
# if sunday
elif datetime.today().weekday() == 6 and datetime.now().hour >16:
    for pair in dc_trading_pairs:
        for tf in dc_time_frames:
            print('checking data for {} {}'.format(tf,pair))
            insert_new_into_table(pair,tf)
else:
    print("not running")
