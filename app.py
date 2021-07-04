from flask import Flask, render_template
import pandas as pd
import numpy as np
from collections import defaultdict

app = Flask(__name__)


@app.route('/')
def hello_world():
    df = pd.read_csv('WhatAppDataforDash.csv')
    message_list = list(df['Message'])
    totalmsgs = len(message_list)
    media = np.sum(df['MediaCount'])
    wordcount = np.sum(df['Words'])
    touse = df.copy()

    # <-----------Top Messages10  in the Group--------------->

    user_list = list(df['Person'])
    user_dicto = defaultdict(list)
    for person, message in zip(user_list, message_list):
        user_dicto[person].append(message)

    user_dicto1 = dict(user_dicto)
    message_map = {}
    for key, value in user_dicto1.items():
        message_map[key] = len(value)

    message_map = dict(
        sorted(message_map.items(), key=lambda x: x[1], reverse=True))

    top10user = list(message_map.keys())[:10]
    msg10count = list(message_map.values())[:10]

    # <---------------------------Messages End------------------------------>

    # <---------------------------Average Words per message by most active users----->

    user_list = list(df['Person'])
    user_map = {}
    for user in user_list:
        dummydf = df[df['Person'] == user]
        msgcount = np.sum(dummydf['Words'])/df.shape[0]
        user_map[user] = msgcount

    user_map = dict(sorted(user_map.items(), key=lambda x: x[1], reverse=True))
    useravgword = list(user_map.keys())[:10]
    useravgwordcount = list(user_map.values())[:10]
    useravgwordcount = [i*10 for i in useravgwordcount]

    # <---------------------------Average Words per message by most active users End----->

    # <-----------------------------Messages sent each day of week--------------------->

    days = list(df['Day'].unique())
    weekmap = {}
    for day in days:
        dummydf = df[df['Day'] == day]
        weekmap[day] = dummydf['Day'].value_counts()[0]

    # <-----------------------------Messages sent each day of week end--------------------->

    # <-----------------------------Top10 Media Contributors--------------------->

    userlist = list(df['Person'])
    mediadict = {}
    for user in userlist:

        dummy = touse[touse['Person'] == user]
        mediadict[user] = np.sum(dummy['MediaCount'])

    mediadict = dict(
        sorted(mediadict.items(), key=lambda x: x[1], reverse=True))
    mediauser = list(mediadict.keys())[:10]
    mediacount = list(mediadict.values())[:10]

    # <-----------------------------Top10 Media Contributors End--------------------->

    # <----------------------------Time when the Group was highly Active-------------->

    timelist = list(touse['Time'])
    time_map = {}
    for time in timelist:
        dummy = touse[touse['Time'] == time]
        time_map[time] = dummy.shape[0]

    time_map = dict(sorted(time_map.items(), key=lambda x: x[1], reverse=True))
    time = list(time_map.keys())[:10]
    timecount = list(time_map.values())[:10]

    # <----------------------------Time when the Group was highly Active end-------------->

    # <----------------------------Most Active year and month-------------->

    def getyeardf(year):
        return touse[touse['Year'] == year]

    df_2018 = getyeardf(2018)
    df_2019 = getyeardf(2019)
    df_2020 = getyeardf(2020)
    df_2021 = getyeardf(2021)
    df_2018 = dict(df_2018['Month'].value_counts())
    df_2019 = dict(df_2019['Month'].value_counts())
    df_2020 = dict(df_2020['Month'].value_counts())
    df_2021 = dict(df_2021['Month'].value_counts())

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def getformatteddict(data):
        returndict = {}
        for month in months:
            if month in data.keys():
                returndict[month] = data[month]

            else:
                returndict[month] = 0

        return returndict

    df_2018 = getformatteddict(df_2018)
    df_2019 = getformatteddict(df_2019)
    df_2020 = getformatteddict(df_2020)

    df_18_month = list(df_2018.keys())
    df_18_count = list(df_2018.values())
    df_19_count = list(df_2019.values())
    df_20_count = list(df_2020.values())
    df_21_count = list(df_2021.values())
    touse_month = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul']
    send_map = {}
    for month in touse_month:
        if month in df_2021.keys():
            send_map[month] = df_2021[month]
        else:
            send_map[month] = 0

    send_count = list(send_map.values())

    # <----------------------------Most Active year and month-------------->

    return render_template('index.html', total_msg=totalmsgs,
                           top10user=top10user, msg10count=msg10count, totaluser=len(
                               list(set(user_list))), media=media, words=wordcount, avguser=useravgword,
                           avguserword=useravgwordcount, days=list(weekmap.keys()), msgday=sorted(list(weekmap.values()), reverse=True), mediauser=mediauser, mediacount=mediacount, time=time, timecount=timecount,
                           df_18_month=df_18_month,
                           df_18_count=df_18_count,
                           df_19_count=df_19_count,
                           df_20_count=df_20_count,
                           df_21_count=send_count)


if __name__ == '__main__':
    app.run(debug=True)
