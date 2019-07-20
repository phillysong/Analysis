
# coding: utf-8

# In[13]:


# client_id='sft39r624yi158qxfcfx6l5o5r6lij'
# client_secret='ps3cp3qddnb3cispc3nt3c7j334eu8'
import pandas as pd
import numpy as np
from sqlite3 import Error
import requests,json,sqlite3,datetime
from secrets import client_id,client_secret


# In[14]:
db_file=r'A:\Programming files\Databases\twitch.db'
conn = sqlite3.connect(db_file)
conn.close()

headers = {'Accept' : 'application/vnd.twitchtv.v5+json','Client-ID' : client_id, 'Authorization' : client_secret}


# In[21]:


def create_featured_streamers_table():
    conn=sqlite3.connect(r'A:\Programming files\Databases\twitch.db')
    c=conn.cursor()
    
    query = """ CREATE TABLE if not exists featured_streamers (
        -- id integer PRIMARY KEY,
        time datetime,
        display_name int,
        channel_id int,
        channel_views int,
        channel_followers int,
        primary_streamer int
        );"""
    
    c.execute(query).fetchall()
    conn.commit()
    conn.close()
    return None        

def create_channel_info_table():
    conn=sqlite3.connect(r'A:\Programming files\Databases\twitch.db')
    c=conn.cursor()
    
    query = """ CREATE TABLE if not exists channel_info (
        -- id integer PRIMARY KEY,
        time datetime,
        display_name text,
        channel_id int,
        channel_views int,
        channel_followers int
        );"""
    
    c.execute(query).fetchall()
    conn.commit()
    conn.close()
    return None

create_featured_streamers_table()
create_channel_info_table()


# In[17]:


def get_time():
    now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return now


# In[18]:


def insert_featured_streams(display_name,channel_id,channel_views,channel_followers):
    conn=sqlite3.connect(r'A:\Programming files\Databases\twitch.db')
    c=conn.cursor()
    query=f'''
    INSERT INTO featured_streamers (time,display_name,channel_id,channel_views,channel_followers,primary_streamer)
    VALUES (?,?,?,?,?,?);
           '''
    for line in range(len(display_name)):
        if line==0:
            values=(get_time(),display_name[line],channel_id[line],channel_views[line],channel_followers[line],1)
        else:
            values=(get_time(),display_name[line],channel_id[line],channel_views[line],channel_followers[line],0)
        c.execute(query,values)
    conn.commit()
    conn.close()
    return None

def create_featured_dictionary(featured_request):
    display_name_list,channel_id_list,channel_views_list,channel_followers_list=[],[],[],[]
    for stream in featured_request:
        display_name_list.append(stream['stream']['channel']['display_name'])
        channel_id_list.append(stream['stream']['channel']['_id'])
        channel_views_list.append(stream['stream']['channel']['views'])
        channel_followers_list.append(stream['stream']['channel']['followers'])
    return display_name_list,channel_id_list,channel_views_list,channel_followers_list

def scrape_for_featured_streams():
    featured_url='https://api.twitch.tv/kraken/streams/featured?limit=9'
    featured_request=requests.get(featured_url, headers=headers).json()['featured']
    display_name,channel_id,channel_views,channel_followers=create_featured_dictionary(featured_request)
    insert_featured_streams(display_name,channel_id,channel_views,channel_followers)
    return None


# In[19]:


def import_data():
    conn=sqlite3.connect(r'A:\Programming files\Databases\twitch.db')
    df=pd.read_sql_query("SELECT distinct channel_id from featured_streamers",conn)
    conn.close()
    return df
 
def get_channel_info(df):
    channel_id_list=df['channel_id']
    live_channel_ids,display_name,channel_views_list,channel_followers_list=[],[],[],[]
    for channel in channel_id_list:
        url=r'https://api.twitch.tv/kraken/streams/{}?stream_type=all'.format(channel)
        channel_info=requests.get(url, headers=headers).json()
        if channel_info['stream']!=None:
            live_channel_ids.append(channel)
            display_name.append(channel_info['stream']['channel']['display_name'])
            channel_views_list.append(channel_info['stream']['channel']['views'])
            channel_followers_list.append(channel_info['stream']['channel']['followers'])
    return live_channel_ids,display_name,channel_views_list,channel_followers_list

def insert_channel_info(display_name,channel_id,channel_views,channel_followers):
    conn=sqlite3.connect(r'A:\Programming files\Databases\twitch.db')
    c=conn.cursor()
    query=f'''
    INSERT INTO channel_info (time,display_name,channel_id,channel_views,channel_followers)
    VALUES (?,?,?,?,?);
           '''
    for line in range(len(display_name)):
        values=(get_time(),display_name[line],channel_id[line],channel_views[line],channel_followers[line])
        c.execute(query,values)
    conn.commit()
    conn.close()
    return None

def scrape_for_channel_info():
    df=import_data()
    live_channel_ids,display_name,channel_views_list,channel_followers_list=get_channel_info(df)
    insert_channel_info(display_name,live_channel_ids,channel_views_list,channel_followers_list)
    return None


# In[ ]:


scrape_for_featured_streams()
scrape_for_channel_info()