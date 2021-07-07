from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from collections import defaultdict

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/mv1249/WhatsappTextAnalysis/main/WhatAppDataforDash.csv')
    df1 = pd.read_csv(
        'https://raw.githubusercontent.com/mv1249/WhatsappTextAnalysis/main/WhatsAppuserdata.csv')
    dates = pd.read_csv(
        'https://raw.githubusercontent.com/mv1249/WhatsappTextAnalysis/main/YearMonth.csv')

    rep1 = pd.read_csv(
        'https://raw.githubusercontent.com/mv1249/WhatsappTextAnalysis/main/WhatsAppReplierList.csv')

    finaldf = pd.read_csv(
        'https://raw.githubusercontent.com/mv1249/WhatsappTextAnalysis/main/TopRepliesfromX.csv')

    user_list = len(df['Person'].unique())
    years = sorted(list((set(list(dates['Year'])))))

    order = ['MessageCount', 'Avgcount',
             'Msgsentperweek', 'Media', 'ActiveTime']
    message_list = list(df['Message'])
    totalmsgs = len(message_list)
    media = np.sum(df['MediaCount'])
    wordcount = np.sum(df['Words'])
    touse = df.copy()

    # <-----------Top Messages10  in the Group--------------->

    message_map = df1[df1['Purpose'] == order[0]]
    top10user = list(message_map['User'])
    msg10count = list(message_map['Message'])

    # <---------------------------Messages End------------------------------>

    # <---------------------------Average Words per message by most active users----->

    user_map = df1[df1['Purpose'] == order[1]]
    useravgword = list(user_map['User'])
    useravgwordcount = list(user_map['Message'])

    # <---------------------------Average Words per message by most active users End----->

    # <-----------------------------Messages sent each day of week--------------------->

    dummydf = df1[df1['Purpose'] == order[2]]
    weekday = list(dummydf['User'])
    weekcount = list(dummydf['Message'])

    # <-----------------------------Messages sent each day of week end--------------------->

    # <-----------------------------Top10 Media Contributors--------------------->

    mediadict = df1[df1['Purpose'] == order[3]]
    mediauser = list(mediadict['User'])
    mediacount = list(mediadict['Message'])

    # <-----------------------------Top10 Media Contributors End--------------------->

    # <----------------------------Time when the Group was highly Active-------------->

    time_map = df1[df1['Purpose'] == order[4]]
    time = list(time_map['User'])
    timecount = list(time_map['Message'])

    # <----------------------------Time when the Group was highly Active end-------------->

    # <----------------------------Most Active year and month-------------->

    mapper = {'Jan': 0, 'Feb': 0, 'Mar': 0,
              'Apr': 0, 'May': 0, 'Jun': 0, 'Jul': 0}
    mapper1 = {'Aug': 470, 'Sep': 238, 'Oct': 179, 'Nov': 227, 'Dec': 73}
    finalmapper = mapper | mapper1
    finalmapper

    df_18_month = list(finalmapper.keys())
    df_18_count = list(finalmapper.values())

    # df_2019

    dummy1 = dates[dates['Year'] == years[1]]
    df_19_count = list(dummy1['Count'])

    # df_2020

    dummy2 = dates[dates['Year'] == years[2]]
    df_20_count = list(dummy2['Count'])

    # df_2021

    mapper30 = {'Jan': 154, 'Feb': 57, 'Mar': 234,
                'Apr': 570, 'Jun': 243, 'Jul': 70}
    mapper31 = {'Aug': 0, 'Sep': 0, 'Oct': 0, 'Nov': 0, 'Dec': 0}
    mapper_mix = mapper30 | mapper31
    send_count = list(mapper_mix.values())

    # <----------------------------Most Active year and month-------------->

    # <------------------------------------Replier list------------------>

    # 2018

    rep_18 = rep1[rep1['Year'] == 2018]
    user_18 = list(rep_18['User'])
    user_18_count = list(rep_18['Reply Count'])

    mapper_18 = dict(zip(user_18, user_18_count))

    # 2019

    rep_19 = rep1[rep1['Year'] == 2019]
    user_19 = list(rep_19['User'])
    user_19_count = list(rep_19['Reply Count'])

    mapper_19 = dict(zip(user_19, user_19_count))

    # 2020

    rep_20 = rep1[rep1['Year'] == 2020]
    user_20 = list(rep_20['User'])
    user_20_count = list(rep_20['Reply Count'])
    mapper_20 = dict(zip(user_20, user_20_count))

    # 2021

    rep_21 = rep1[rep1['Year'] == 2021]
    user_21 = list(rep_21['User'])
    user_21_count = list(rep_21['Reply Count'])

    mapper_21 = dict(zip(user_21, user_21_count))

    combination = user_18+user_19+user_20+user_21
    combination_set = list(set(combination))

    user_18_map = {}
    user_19_map = {}
    user_20_map = {}
    user_21_map = {}

    # 2018
    for i in combination_set:
        if i in user_18:
            user_18_map[i] = mapper_18[i]
        else:
            user_18_map[i] = 20

    # 19 map

    for i in combination_set:
        if i in user_19:
            user_19_map[i] = mapper_19[i]
        else:
            user_19_map[i] = 20

    # 20 map

    for i in combination_set:
        if i in user_20:
            user_20_map[i] = mapper_20[i]
        else:
            user_20_map[i] = 20

    # 21 map
    for i in combination_set:
        if i in user_21:
            user_21_map[i] = mapper_21[i]

        else:
            user_21_map[i] = 20

    user_18 = list(user_18_map.keys())
    user_18_count = list(user_18_map.values())
    user_19_count = list(user_19_map.values())
    user_20_count = list(user_20_map.values())
    user_21_count = list(user_21_map.values())

    # <---------------------------TopRepliersfrom X-------------------------------------->

    def getdetails(detaillist, replierlist):

        names = [detaillist[i][0] for i in range(len(detaillist))]
        values = [detaillist[i][1] for i in range(len(detaillist))]

        returnmap = dict(zip(names, values))
        finalmap = {}
        for i in range(len(replierlist)):
            if replierlist[i] in returnmap.keys():
                finalmap[replierlist[i]] = returnmap[replierlist[i]]

            else:
                finalmap[replierlist[i]] = 25

        return finalmap

    senderlist = list(finaldf['Sender'])
    replierlist = list(finaldf['Replier'])
    repliercount = list(finaldf['Count'])

    finalreply = []
    for i in replierlist:
        if i not in finalreply:
            finalreply.append(i)

    finalmapper = defaultdict(list)

    for sender, replier, count in zip(senderlist, replierlist, repliercount):

        finalmapper[sender].append((replier, count))

    finalmapper = dict(finalmapper)
    finalkeys = list(finalmapper.keys())

    # user_1

    user1keys = list(getdetails(finalmapper[finalkeys[0]], finalreply).keys())

    user1vals = list(getdetails(
        finalmapper[finalkeys[0]], finalreply).values())

    # user2

    user2vals = list(getdetails(
        finalmapper[finalkeys[1]], finalreply).values())

    # user3

    user3vals = list(getdetails(
        finalmapper[finalkeys[2]], finalreply).values())

    # user4

    user4vals = list(getdetails(
        finalmapper[finalkeys[3]], finalreply).values())

    # user5
    user5vals = list(getdetails(
        finalmapper[finalkeys[4]], finalreply).values())

    return render_template('index.html', total_msg=totalmsgs,
                           top10user=top10user, msg10count=msg10count, totaluser=user_list, media=media, words=wordcount, avguser=useravgword,
                           avguserword=useravgwordcount, days=weekday, msgday=weekcount, mediauser=mediauser, mediacount=mediacount, time=time, timecount=timecount,
                           df_18_month=df_18_month,
                           df_18_count=df_18_count,
                           df_19_count=df_19_count,
                           df_20_count=df_20_count,
                           df_21_count=send_count, user_18=user_18, user_18_count=user_18_count,
                           user_19_count=user_19_count, user_20_count=user_20_count,
                           user_21_count=user_21_count,
                           user1keys=user1keys,
                           user1vals=user1vals,
                           user2vals=user2vals,
                           user3vals=user3vals,
                           user4vals=user4vals,
                           user5vals=user5vals,
                           topsenders=finalkeys)


if __name__ == '__main__':
    app.run(debug=True)
