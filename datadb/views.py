# -*- coding: utf-8 -*-

import time
import os
import pyodbc

import signal
from contextlib import contextmanager

import urllib
from bs4 import BeautifulSoup

from datetime import datetime,timedelta
from django.utils import timezone
from django.views.generic import ListView
from datadb.models import DataModel
from datadb.models import Av
from datadb.models import RequestAv,RequestData
from datadb.models import Hour,GraphData,GraphDataBC
from datadb.models import AgsStation
from datadb.models import PlanAgsStation
from datadb.models import GStation
from table import HourTable
from table import AvTable
from django_tables2 import RequestConfig
from datadb.models import Station
from datadb.models import DataAnalys
from chartit import DataPool,Chart
from django.db.models import Max,Min
from django.shortcuts import get_object_or_404


from django.shortcuts import render, render_to_response


def getdata_request(id_station,fromv,tov):

    dt1 = fromv

    dt2 = tov

    minlevel=0

    try:
        cnxn = pyodbc.connect("DSN=MSSQL-PYTHON;UID=gmcreader;PWD=123",timeout=1)
        cnxn.autocommit = True
        cursor = cnxn.cursor()
        cursor.execute("""
                select min(data) from dbo._data
                where dt>=? and dt<=? and mid=1 and id=?
                group by cast(dt as date)
                order by cast(dt as date) asc
               """,dt1,dt2,id_station)
        minlev=cursor.fetchall()
        for level in minlev:
            minlevel=level[0]

        cursor = cnxn.cursor()
        cursor.execute("""
                select cast (dt as date),avg(data),min(data),max(data) from dbo._data
                where dt>=? and dt<=? and mid=1 and id=? and ((data < 1.5*?) and (data > ?*0.3))
                group by cast(dt as date)
                order by cast(dt as date) desc
               """,dt1,dt2,id_station,minlevel,minlevel)
        rows = cursor.fetchall()

        ags_station = get_object_or_404(AgsStation,station_id=id_station)

        level_zero= ags_station.value_zero
        level_brovka = ags_station.value_brovka

        # Create a tables from databases
        requestdat = RequestAv.objects.all()
        if requestdat.count()>0:
            RequestAv.objects.all().delete()

        for rowdata in rows:
            if rowdata[3]/rowdata[2]<=1.5:
                datatableR=RequestAv()
                datatableR.value_min=rowdata[2]
                datatableR.value_avg=rowdata[1]
                datatableR.value_max=rowdata[3]
                datatableR.date_observation=rowdata[0]
                datatableR.id_station=id_station
                datatableR.value_avgBCp=rowdata[1]/100 + level_zero
                datatableR.value_minBC=rowdata[2]/100+level_zero
                datatableR.value_maxBC=rowdata[3]/100+level_zero
                datatableR.value_avgBC=rowdata[1]/100+level_zero

                temp_value=rowdata[1]/100 + level_zero

                if temp_value < level_brovka:
                    datatableR.value_avgBC=temp_value
                    datatableR.value_avgBC1=0
                    datatableR.value_avgBC2=0
                    datatableR.value_avgBC3=0
                    datatableR.value_avgBC4=0
                    datatableR.value_avgBC50=0
                    datatableR.value_avgBC60=temp_value

                if temp_value>=level_brovka and temp_value<(level_brovka+0.5):
                    datatableR.value_avgBC1=temp_value
                    datatableR.value_avgBC=level_brovka
                    datatableR.value_avgBC2=0
                    datatableR.value_avgBC3=0
                    datatableR.value_avgBC4=0
                    datatableR.value_avgBC50=temp_value
                    datatableR.value_avgBC60=level_brovka

                if  temp_value >= level_brovka+0.5 and temp_value<(level_brovka+0.8):
                    datatableR.value_avgBC2=temp_value
                    datatableR.value_avgBC=level_brovka
                    datatableR.value_avgBC1=level_brovka+0.5
                    datatableR.value_avgBC3=0
                    datatableR.value_avgBC4=0
                    datatableR.value_avgBC50=level_brovka+0.5
                    datatableR.value_avgBC60=level_brovka

                if  temp_value>= level_brovka+0.8 and temp_value<level_brovka + 2:
                    datatableR.value_avgBC3=temp_value
                    datatableR.value_avgBC=level_brovka
                    datatableR.value_avgBC2=level_brovka+0.8
                    datatableR.value_avgBC1=level_brovka+0.5
                    datatableR.value_avgBC4=0
                    datatableR.value_avgBC50=level_brovka+0.5
                    datatableR.value_avgBC60=level_brovka

                if  temp_value>=(level_brovka+2):
                    datatableR.value_avgBC4=temp_value
                    datatableR.value_avgBC=level_brovka
                    datatableR.value_avgBC2=level_brovka+0.8
                    datatableR.value_avgBC1=level_brovka+0.5
                    datatableR.value_avgBC3=level_brovka+2
                    datatableR.value_avgBC50=level_brovka+0.5
                    datatableR.value_avgBC60=level_brovka

                datatableR.save()

        return datatableR

    except:
        return None



def getdatafromhtml(urlname):
    url = urlname
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html,"html.parser")

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)


    tar=[]
    k=0
    zk=1
    ml=''

    rus_text_new = 'Толщина льда, см'

    rus_text_old='Изменение уровня воды, см'

    rus_text='Толщина льда, см'

    print text

    rr_txt=0

    rr_txt = text.find(rus_text_new.decode("utf-8"))
    if rr_txt==-1:
        rus_text = 'Изменение уровня воды, см'



    while k<len(text):
        if text[k]=='\n':
            tar.append(ml)
            zk=zk+1
            ml=''
        else:
            ml=ml+text[k]

        k=k+1

    findel=1

    for i in range(len(tar)):
        ind=tar[i].find(rus_text.decode("utf-8"))
        if ind<>-1:
            findel=i

    res_list=[]

    res_list.insert(0,tar[findel+1])
    res_list.insert(1,tar[findel+2])
    if len(tar[findel+3])<=4:
        res_list.insert(2,tar[findel+3])
    else:
        res_list.insert(2,tar[findel+4])


    return  res_list

def ping(host):
    """
    Returns True if host responds to a ping request
    """
    import os, platform

    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0


def getdata_last(id_station):

    minlevel=0

    print 'Try to connect to external database ..'

    t1  = time.time()

    print t1

    try:
        cnxn = pyodbc.connect("DSN=MSSQL-PYTHON;UID=gmcreader;PWD=123;Trusted_Connection=True")

        cnxn.autocommit = False
        cnxn.timeout = 3

        cursor = cnxn.cursor()

        cursor.execute("""
                select min(data) from dbo._data
                where dt>getdate()-1 and mid=1 and id=?
                group by cast(dt as date)
                order by cast(dt as date) desc
               """,id_station)


        minlev=cursor.fetchall()
        for level in minlev:
            minlevel=level[0]

        cursor = cnxn.cursor()
        cursor.execute("""
                select dt,data from dbo._data
                where (id = ?) and (mid = 1) and dt>dateadd(HOUR ,-3, getdate()) and data < 2*? and data > ?*0.3
                ORDER BY dt DESC
               """,id_station,minlevel,minlevel)
        rows = cursor.fetchall()

        cursor = cnxn.cursor()
        cursor.execute("""
                select cast (dt as date),avg(data) from dbo._data
                where (id = ?) and (mid = 1) and dt>dateadd(HOUR ,-3, getdate()) and data < 2*? and data > ?*0.3
                GROUP BY cast(dt as date)
                ORDER BY cast(dt as date) DESC
                """,id_station,minlevel,minlevel)
        rows_av = cursor.fetchall()

        for av_level in rows_av:

            av_data=av_level[1]

        time_list=[]
        data_list=[]

        for level in rows:

            time_list.append(level[0])
            data_list.append(level[1])

        value_last=data_list[-1]
        time_last=time_list[-1]
        value_first=data_list[0]
        time_first=time_list[0]

        level_status=0

        if value_first>av_data:
            level_status=1
        if value_first<av_data:
            level_status=2

        ags=AgsStation.objects.get(station_id=id_station)
        ags.value_level=value_first
        ags.status_level=level_status
        ags.datetime_text=time_first
        ags.value_bc=ags.value_zero+value_first*0.01
        ags.save()

        return rows

    except pyodbc.Error as ex:
        print("Could not connect to database.")
        sqlstate = ex.args[0]
        if sqlstate == '08001':
            pass


    t2 = time.time()
    print t2-t1

    return None


def request_page(request):

    from_value=''
    to_value=''
    fromv1=''
    tov1=''
    showgr='no'

    index_id=0

    stations=Station.objects.all()

    selected_value=''

    if 'from_' in request.POST:

        from_value=request.POST['from_']

        if from_value == '':
            fromv1=''
        else:
            fromv1='666'

    if 'to_' in request.POST:

        to_value=request.POST['to_']

        if to_value == '':
            tov1=''
        else:
            tov1='666'

    if 'river_list' in request.POST:

        selected_value = request.POST['river_list']

        for k in stations:
            if k.description==selected_value and fromv1=='666' and tov1=='666':
                getdata_request(k.id_station,from_value,to_value)
                index_id=k.id_station

        if  fromv1=='666' and tov1=='666':
            showgr='ok'
        else:
            showgr='no'

        min_level=[]
        max_level=[]

        min_level1=[]
        max_level1=[]


        ags_station = get_object_or_404(AgsStation,station_id=index_id)

        level_zero= ags_station.value_zero
        level_brovka = ags_station.value_brovka

        level_zerol=0
        level_brovkal=(level_brovka-level_zero)*100

        print level_brovkal,level_zero

        levelb05=level_brovka+0.5
        levelb08=level_brovka+0.8
        levelb20=level_brovka+2.0

        min_levelBC=[]
        max_levelBC=[]

        min_levelBC1=[]
        max_levelBC1=[]

        max_level = RequestAv.objects.all().filter(id_station=index_id).aggregate(Max('value_max'))
        min_level = RequestAv.objects.all().filter(id_station=index_id).aggregate(Min('value_min'))

        max_levelBC = RequestAv.objects.all().filter(id_station=index_id).aggregate(Max('value_maxBC'))
        min_levelBC = RequestAv.objects.all().filter(id_station=index_id).aggregate(Min('value_minBC'))

        max_level1 = RequestAv.objects.all().filter(id_station=index_id).aggregate(Max('value_avg'))
        min_level1 = RequestAv.objects.all().filter(id_station=index_id).aggregate(Min('value_avg'))

        max_levelBC1 = RequestAv.objects.all().filter(id_station=index_id).aggregate(Max('value_avgBCp'))
        min_levelBC1 = RequestAv.objects.all().filter(id_station=index_id).aggregate(Min('value_avgBCp'))

        print max_level1,max_levelBC1,min_level1,min_levelBC1

        ds=\
                    DataPool(
                    series=
                    [{'options': {
                    'source':RequestAv.objects.all().order_by('date_observation') },
                    'terms': [
                    ('date_observation', lambda d: time.mktime(d.timetuple())),
                    'value_avg','value_min','value_max']}
                    ])

        cht = Chart(
                    datasource=ds,
                    series_options=
                [{'options':{
                  'type': 'areaspline',
                  'stacking': False},'minorTickInterval':'auto',
                  'terms':{
                  'date_observation': [
                  'value_avg']
                  }},

                    {'options':{
                   'type': 'spline',
                   },
                'terms':{
                  'date_observation': [
                  'value_min','value_max']
                  }},

                ],
        chart_options=
                    {'chart':
                    {
                    'zoomType': 'x'
                    },
                    'title':
                    {
                    'text': 'Измеренный уровень воды, см  ' + ' || станция AГС: '+ selected_value.encode('utf-8')
                    },
                      'colors': ['#34ffff','#349aff','#ff9a34','#ff3434','#35ff34','#9aff34'],

                     'yAxis':
                    {
                    'title' : {'text': ' см '},
                    'min': min_level.values(),
                    'max' :max_level.values(),
                    },
                     'navigation': {
                'buttonOptions': {
                'height': 48,
                'width': 48,
                'symbolSize': 24,
                'symbolX': 23,
                'symbolY': 21,
                'symbolStrokeWidth': 2,
                'minorTickInterval':'auto',
            },
                     },

                    'xAxis':
                    {
                    'title' : {'text': ' Дата '},
                    'labels':
                        {'step': 24, 'rotation': 0, 'align': 'bottom'},
                    'minRange': 5
                    },
                    'credits':
                    {
                    'enabled': True
                    },
                    'plotOptions': {
                   'series':

                    {
                     'fillOpacity':1
                    },
                  'spline': {
                  'id':'1',
                  'index':2,
                  'legendIndex':1,
                  'lineWidth': 10,
                  'marker': {
                    'lineWidth': 0,
                    'radius': 0.1,
                    'lineColor': '#666666'
                     },
                  },
                 },
                     'plotOptions': {'minorTickInterval':'auto',
                   'series':

                    {'minorTickInterval':'auto',
                     'fillOpacity':0.5,

                    },

                  'areaspline': {
                  'id':'0',
                  'index':1,
                  'legendIndex':2,
                  'lineWidth': 0.0,
                  'marker': {
                    'lineWidth': 0.0,
                    'radius': 0.1,
                    'lineColor': '#666666'
                     },
                    },
                 },
                },

        x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime(" %Y-%m-%d"), False))

        val_count=RequestAv.objects.all().count()

        stepval=int(val_count/7)

        ds1=\
            DataPool(
            series=
                [{'options': {
                'source':RequestAv.objects.all().order_by('date_observation') },
                'terms': [
                    ('date_observation', lambda d: time.mktime(d.timetuple())),
                    'value_avgBCp']}
                  ])
        cht1 = Chart(
            datasource=ds1,
            series_options=
              [
               {'options':{
                'type': 'area',
                   'xAxis':0,
                   'yAxis':0,
                   'zIndex':1},

               'terms':{'date_observation':['value_avgBCp']}},

               ],

            chart_options=
               {'chart':
                    {
                    'zoomType': 'x',
                    'alignTicks': False,

                    },



                'colors': ['#058DC7', '#64E572', '#FFF263', '#ED561B', '#8085e9',
                '#f15c80', '#e4d354', '#2b908f', '#f45b5b', '#91e8e1'],

                  'title':
                    {
                    'text': 'Измеренный уровень воды, м  ' + ' || станция AГС: '+ selected_value.encode('utf-8')
                    },
                    'subtitle': {
                                'text': '* см (от 0 поста АГС ) ',
                                'align': 'right',
                                'x': -100
                             },

                      'tooltip':{
                      'shared': True,
                      'useHTML': True,
                      'headerFormat': '<small> {point.key}</small><table>',
                       'pointFormat': '<tr><td style="color: {series.color}">{series.name}: </td>' +
                         '<td style="text-align: right"> <b> {point.y}  </b></td></tr>',
                        'footerFormat': '</table>',
                        'valueDecimals': 2
                       },

                 'yAxis':

                    [
                      {
                       'opposite': False,
                       'gridZIndex': 3,
                       'min': min_levelBC.values(),
                       'max': max_levelBC.values(),
                       'title' : {'text': ' м '},



                      'plotLines': [{
                       'value': levelb05,
                       'color': '#CB66FE',
                       'zIndex':5,
                       'width': 2,
                       'label': {
                       'text': '0.5м - yровень опасности ',
                       'align': 'left',
                       'style': {
                       'color': 'black'
                         }
                         }
                      },
                       {
                       'value': levelb08,
                       'color': '#D334FC',
                       'zIndex':4,
                       'width': 3,
                       'label': {
                       'text': '0.8м - уровень опасности ',
                       'align': 'left',
                       'style': {
                       'color': 'black'
                        }
                       }
                      },
                        {
                       'value': levelb20,
                       'color': '#610060',
                       'zIndex':3,
                       'width': 4,
                       'label': {
                       'text': '2м - уровень опасности ',
                       'align': 'left',
                       'style': {
                       'color': 'black'
                        }
                       }
                      },
                       ]},

                     {
                    'title' : {'text': ' cм (*) '},
                    'min': min_level.values(),
                    'max': max_level.values(),
                    'opposite' : True,
                    'tickColor':'#349aff',
                    'minTickInterval':5,
                    'gridZIndex':4,
                    'maxPadding': 0.1,
                     }
                    ],

                 'navigation': {
                'buttonOptions': {
                'height': 40,
                'width': 48,
                'symbolSize': 24,
                'symbolX': 23,
                'symbolY': 21,
                'symbolStrokeWidth': 2
                           },
                     },


                'xAxis':
                    [{
                    'title' : {'text': '  '},
                    'labels':
                        {'step': stepval,  'rotation': 0, 'align': 'top'},
                    'gridLineWidth': 0.25,
                    'gridZIndex': 1,
                    'gridLineColor': "#FFFFFF",
                    'gridLineDashStyle': "Solid",
                    'minorTickLength':10,
                    'minorTickInterval':'auto',
                    },
                    ],

                 'plotOptions': {

                  'column': {
                  'fillOpacity':0.2,
                  'lineWidth': 3,
                  'marker': {
                    'lineWidth': 0,
                    'radius': 0,
                    'lineColor': '#666666'
                     },
                  },
                    'area': {
                   'fillOpacity':0.5,
                  'lineWidth': 2,
                  'showInLegend':True,
                  'marker': {
                    'lineWidth': 0,
                    'radius': 0,
                    'lineColor': '#666666'
                     },
                  },
                   'spline': {
                   'fillOpacity':0.00,
                   'enableMouseTracking': True,

                   'stickyTracking': False,
                   'dashStyle': "ShortDot",
                   'lineWidth': 0.0,
                  'marker': {
                    'lineWidth': 0,
                    'radius': 0,
                    'lineColor': '#666666'
                     },
                  },


                 },


                   'legend':{

                    'reversed': True},

                   'credits':
                    {
                    'enabled': True
                    },
               },
            x_sortf_mapf_mts = (None,lambda i: datetime.fromtimestamp(i).strftime(" %Y-%m-%d") , False))


        ds4=\
            DataPool(
            series=
               [{
                'options': {
               'source':RequestAv.objects.all().order_by('date_observation')  },
              'terms': [
                ('date_observation', lambda d: time.mktime(d.timetuple())),
                'value_avgBC2','value_avgBC3','value_avgBC4']},
                { 'options': {
               'source':RequestAv.objects.all().order_by('date_observation')  },
              'terms': [
                ('date_observation', lambda d: time.mktime(d.timetuple())),
                'value_avgBC','value_avgBC1','value_avgBC50']},

                ])

        cht4 = Chart(
                datasource=ds4,
                series_options=
              [
                   {'options':{
                   'type': 'areaspline',
                   },
                'terms':{
                  'date_observation': [
                  'value_avgBC','value_avgBC2','value_avgBC3','value_avgBC4']
                  }},

                     {'options':{
                   'type': 'line',
                   },
                'terms':{
                  'date_observation': [
                  'value_avgBC50']
                  }},

                 ],
                chart_options=
               {'chart':
                    {
                    'zoomType': 'x',
                     },

                'title':
                    {
                    'text': 'Измеренный уровень воды в абсолютных отметках БС,м'  + ' || станция AГС: '+ selected_value.encode('utf-8')
                    },

                 'yAxis':
                    {
                    'title' : {'text': ' м '},
                    'min': min_levelBC.values(),
                    'max' :max_levelBC.values(),

                     'plotLines': {
                       'value': 132.8,
                       'color': '#CB66FE',
                       'width': 2,
                       'label': {
                       'text': '0.5м - yровень опасности ',
                       'align': 'left',
                       'style': {
                       'color': 'black'
                         }
                         }
                     },

                    },
                'navigation': {
                'buttonOptions': {
                'height': 40,
                'width': 48,
                'symbolSize': 24,
                'symbolX': 23,
                'symbolY': 21,
                'symbolStrokeWidth': 2
                           },
                     },

                'xAxis':
                    {
                    'title' : {'text': ' Дата '},
                    'labels':
                        {'step': 24, 'rotation': 0, 'align': 'bottom'},
                    'minRange': 5
                    },
                'colors': ['#ff9a34','#ffff81','#349aff','#ff3434','#35ff34','#9aff34'],

                'credits':
                    {
                    'enabled': True
                    },
                 'legend':
                     {
                      'reversed':'true'
                     },
                    'plotOptions': {
                   'series':

                    {
                     'fillOpacity':1
                    },
                  'line': {
                  'id':'1',
                  'index':2,
                  'legendIndex':1,
                  'lineWidth': 10,
                  'marker': {
                    'lineWidth': 0,
                    'radius': 0,
                    'lineColor': '#666666'
                     },
                  },
                 },
                     'plotOptions': {
                   'series':

                    {
                     'fillOpacity':1,

                    },

                  'areaspline': {
                  'id':'0',
                  'index':1,
                  'legendIndex':2,
                  'lineWidth': 1,
                  'marker': {
                    'lineWidth': 0.0,
                    'radius': 0.0,
                    'lineColor': '#666666'

                     },

                  },
                 },

                },
                x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%Y-%m-%d"), False))



        ds=\
                    DataPool(
                    series=
                   [{
                   'options': {
                   'source':RequestAv.objects.all().order_by('date_observation')},
                   'tergetdams': [
                   ('date_observation', lambda d: time.mktime(d.timetuple())),
                    'value_avg']},
                   { 'options': {
                   'source':RequestAv.objects.all().order_by('date_observation')},
                   'terms': [
                   ('date_observation', lambda d: time.mktime(d.timetuple())),
                    'value_avgBCp']},
                         ])
        cht2 = Chart(
                    datasource=ds,
                    series_options=
                [{'options':{
                  'type': 'line',
                  'xAxis': 0,
                  'yAxis': 0,
                  'zIndex': 1},
                  'terms':{
                  'date_observation': ['value_avgBCp']
                  }},
                 ],
        chart_options=
                    {'chart':
                    {
                    'zoomType': 'x'
                    },
                      'tooltip':{
                      'shared': True,
                      'useHTML': True,
                      'headerFormat': '<small> {point.key}</small><table>',
                       'pointFormat': '<tr><td style="color: {series.color}">{series.name}: </td>' +
                         '<td style="text-align: right"> <b> {point.y}  </b></td></tr>',
                        'footerFormat': '</table>',
                        'valueDecimals': 2
                       },

                    'title':
                    {
                    'text': 'Измеренный уровень воды, м  ' + ' || станция AГС: '+ selected_value.encode('utf-8')
                    },
                    'subtitle': {
                                'text': '* см (от 0 поста АГС ) ',
                                'align': 'right',
                                'x': -100
                             },


                      'colors': ['#3596f6','#349aff','#ff9a34','#ff3434','#35ff34','#9aff34'],

                     'yAxis':[
                    {
                    'title' : {'text': ' м '},
                    'minorTickInterval':0.02,
                    'minorTickLength': 0.5,
                    'minorGridLineWidth': 0.5,
                    'gridLineWidth': 2,
                    'tickColor':'#349aff',
                    'ceiling':max_levelBC1.values(),
                    'maxPadding': 0.1,

                    },

                   {
                    'title' : {'text': ' cм (*) '},
                    'floor':  min_level1.values(),
                    'ceiling' : max_level1.values(),
                    'min': min_level1.values(),
                    'max': max_level1.values(),
                    'opposite' : True,
                    'startOnTick': True,
                    'maxPadding': 1,
                    'tickinterval':10,
                    'tickColor':'#349aff',
                    'tickamount':10,
                    'gridZIndex':4,
                     }


                     ],
                     'navigation': {
                'buttonOptions': {
                'height': 40,
                'width': 48,
                'symbolSize': 24,
                'symbolX': 23,
                'symbolY': 21,
                'symbolStrokeWidth': 2
                     },
                     },

                    'xAxis':[
                    {
                    'title' : {'text': ' Дата '},
                    'labels':
                        {'step': 6, 'rotation': 0, 'align': 'bottom'},
                    'minRange': 2
                    }
                    ],
                    'credits':
                    {
                    'enabled': True
                    },
                    'plotOptions': {
                   'series':

                    {
                     'fillOpacity':0.5
                    },
                  'line': {
                  'id':'1',
                  'index':1,
                  'legendIndex':1,
                  'lineWidth': 10,
                 'marker': {
                    'lineWidth': 1,
                    'radius': 0.1,
                    'lineColor': '#666666'
                     },
                   },
                 },
                     'plotOptions': {
                   'series':
                    {
                    'fillOpacity':1,
                    },
                  'line': {
                  'id':'0',

                  'legendIndex':0,
                  'lineWidth': 2.0,
                  'marker': {
                    'lineWidth': 0.0,
                    'radius': 0.1,
                    'lineColor': '#666666'
                     },
                    },
                 },
                },

         x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime(" %Y-%m-%d"), False))


        return render(request,'request.html',{'dtchart':[cht1],'stations':stations,'selvalue':selected_value,'showgr':showgr,'fromv':from_value,'tvalue':to_value,'fromv1':fromv1,'tov1':tov1})

    else:

        selected_value=''

        print stations

        showgr = 'no'

        return render(request,'request.html',{'stations':stations,'selvalue':selected_value,'fromv':from_value,'tvalue':to_value,'fromv1':fromv1,'tov1':tov1,'showgr':showgr})



def map_page(request):

    stations_id=[4,7] # list of id_stations
    if ping("pinhmc.pogoda.by:1433")==True:
        for idsta in stations_id:
            tt = getdata_last(idsta)
            print 'result',tt


    ags_spot=AgsStation.objects.all()

    pags_spot=PlanAgsStation.objects.all()

    g_spot = GStation.objects.all()

    for gs in g_spot:
        mrlist=getdatafromhtml(gs.urlname)
        print mrlist
        gs.value_level=float(mrlist.pop(2))
        gs.txtdata=mrlist.pop(0)
        gs.value_bc=gs.value_zero+gs.value_level/100
        gs.save()

    return render(request,'map.html',{'ags_spot':ags_spot,'g_spot':g_spot,'pags_spot':pags_spot})


def graphs_page(request,pk):

    min_level=[]
    max_level=[]

    max_level = GraphData.objects.all().filter(id_station=pk).aggregate(Max('value_avg'))
    min_level = GraphData.objects.all().filter(id_station=pk).aggregate(Min('value_avg'))

    name_ags=''

    station = get_object_or_404(Station, id_station=pk)

    ags_station = get_object_or_404(AgsStation,station_id=pk)

    level_zero= ags_station.value_zero

    max_levelBC = float(max_level.values()[0]/100) + level_zero

    val_brovka  = ags_station.value_brovka

    min_levelBC = float(min_level.values()[0]/100) + level_zero

    if min_levelBC> val_brovka:
        min_levelBC=val_brovka-0.005

    stations=Station.objects.all()

    #['#57db15','#f07420','#ffff34','#7cb5ec','#f63535'],

    name_ags=station

    ds=\
            DataPool(
            series=
                [{'options': {
               'source':GraphData.objects.all().order_by('dt_observation').filter(id_station=pk) },
              'terms': [
                ('dt_observation', lambda d: time.mktime(d.timetuple())),
                'value_avg']}
                ])

    cht = Chart(
                datasource=ds,
                series_options=
              [{'options':{
                  'type': 'area',
                  'stacking': False},
                'terms':{
                  'dt_observation': [
                  'value_avg']
                  }}


              ],
                chart_options=
               {'chart':
                    {
                    'zoomType': 'x'
                    },
                'title':
                    {
                    'text': 'Измеренный уровень воды, см  '
                    },

                 'yAxis':
                    {
                    'title' : {'text': ' см '},
                    'min': min_level.values(),
                    'max' :max_level.values(),
                    },

                'xAxis':
                    {
                    'title' : {'text': ' Дата '},
                    'labels':
                        {'step': 24, 'rotation': 0, 'align': 'bottom'},
                    'minRange': 5
                    },
                'credits':
                    {
                    'enabled': True
                    }
               },
                x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%H:%M %Y-%m-%d"), False))

    ds1=\
            DataPool(
            series=
               [{
                'options': {
               'source':GraphData.objects.all().order_by('dt_observation').filter(id_station=pk) },
              'terms': [
                ('dt_observation', lambda d: time.mktime(d.timetuple())),
                'value_avgBC2','value_avgBC3','value_avgBC4']},
                { 'options': {
               'source':GraphData.objects.all().order_by('dt_observation').filter(id_station=pk) },
              'terms': [
                ('dt_observation', lambda d: time.mktime(d.timetuple())),
                'value_avgBC','value_avgBC1','value_avgBC50']},

                ])

    cht1 = Chart(
                datasource=ds1,
                series_options=
              [


                   {'options':{
                   'type': 'areaspline',
                   },
                'terms':{
                  'dt_observation': [
                  'value_avgBC','value_avgBC2','value_avgBC3','value_avgBC4']
                  }},

                     {'options':{
                   'type': 'line',
                   },
                'terms':{
                  'dt_observation': [
                  'value_avgBC50']
                  }},

                 ],
                chart_options=
               {'chart':
                    {
                    'zoomType': 'x',
                     },

                'title':
                    {
                    'text': 'Измеренный уровень воды в абсолютных отметках БС,м'
                    },

                 'yAxis':
                    {
                    'title' : {'text': ' м '},
                    'min': min_levelBC,
                    'max' :max_levelBC,
                    },

                'xAxis':
                    {
                    'title' : {'text': ' Дата '},
                    'labels':
                        {'step': 24, 'rotation': 0, 'align': 'bottom'},
                    'minRange': 5
                    },
                'colors': ['#ff9a34','#ffff81','#349aff','#ff3434','#35ff34','#9aff34'],

                'credits':
                    {
                    'enabled': True
                    },
                 'legend':
                     {
                      'reversed':'true'
                     },
                    'plotOptions': {
                   'series':

                    {
                     'fillOpacity':1
                    },
                  'line': {
                  'id':'1',
                  'index':2,
                  'legendIndex':1,
                  'lineWidth': 10,
                  'marker': {
                    'lineWidth': 0,
                    'radius': 0,
                    'lineColor': '#666666'

                     },

                  },
                 },
                     'plotOptions': {
                   'series':

                    {
                     'fillOpacity':1,

                    },

                  'areaspline': {
                  'id':'0',
                  'index':1,
                  'legendIndex':2,
                  'lineWidth': 1,
                  'marker': {
                    'lineWidth': 0.0,
                    'radius': 0.0,
                    'lineColor': '#666666'

                     },

                  },
                 },

                },
                x_sortf_mapf_mts=(None, lambda i: datetime.fromtimestamp(i).strftime("%H:%M %Y-%m-%d"), False))


    return render(request,'graphs.html', {'dtchart':[cht,cht1],'ags':name_ags,'stations':stations})



def graph_page(request):

    stations=Station.objects.all()

    return render(request,'graph_basic.html',{'stations':stations})


def table_page(request):

    table = AvTable(Av.objects.all())

    stations=Station.objects.all()

    tableav=True

    RequestConfig(request,paginate={"per_page":10}).configure(table)

    return render(request,'table_basic.html',{'table':table,'stations':stations,'tableav':tableav})

def showdetail(request,pk):

    table = AvTable(Av.objects.all().filter(id_station=pk))

    table2 = HourTable(Hour.objects.all().filter(id_station=pk))

    stations=Station.objects.all()

    analys_types=DataAnalys.objects.all()

    visiblestations=Station.objects.all().filter(id_station=pk)

    last_date=Av.objects.first()

    tableav=True

    RequestConfig(request,paginate={"per_page":11}).configure(table)

    RequestConfig(request,paginate={"per_page":13}).configure(table2)

    return render(request,'table.html',{'table':table,'table2':table2,'stations':stations,'tableav':tableav,'name':visiblestations,'ld':last_date,'analys':analys_types },)


def showtypes(request,pk):

    table = AvTable(Av.objects.all().filter(id_station=pk))

    stations=Station.objects.all()

    visiblestations=Station.objects.all().filter(id_station=pk)

    last_date=Av.objects.first()

    tableav=True

    RequestConfig(request,paginate={"per_page":10}).configure(table)

    return render(request,'table.html',{'table':table,'stations':stations,'tableav':tableav,'name':visiblestations,'ld':last_date},)


     #init_Tables10(request)# Create a tables from databases
    dat10 = Av.objects.all()
    if dat10.count()>0:
        Av.objects.all().delete()

    stations_id=[4,7] # list of id_stations
    for idsta in stations_id:
        row10=getdata_table10(idsta)
        for rowdata in row10:
            datatableav10=Av()
            datatableav10.value_min=rowdata[2]
            datatableav10.value_avg=rowdata[1]
            datatableav10.value_max=rowdata[3]
            datatableav10.date_observation=rowdata[0]
            datatableav10.id_station=idsta
            datatableav10.save()

    return datatableav10


def getdata_table10(id_station):
    cnxn = pyodbc.connect("DSN=MSSQL-PYTHON;UID=gmcreader;PWD=123",timeout=1)
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    cursor.execute("""
                select min(data) from dbo._data
                where dt> getdate()-10 and mid=1 and id=?
                group by cast(dt as date)
                order by cast(dt as date) desc
               """,id_station)
    minlev=cursor.fetchall()
    for level in minlev:
        minlevel=level[0]

    cursor = cnxn.cursor()
    cursor.execute("""
                select cast (dt as date),avg(data),min(data),max(data) from dbo._data
                where dt> getdate()-10 and mid=1 and id=? and data < 2*? and data>0.3*?
                group by cast(dt as date)
                order by cast(dt as date) desc
               """,id_station,minlevel,minlevel)
    rows = cursor.fetchall()
    return rows

def getdata_table5(id_station):
    cnxn = pyodbc.connect("DSN=MSSQL-PYTHON;UID=gmcreader;PWD=123",timeout=1)
    cnxn.autocommit = True
    cursor = cnxn.cursor()
    cursor.execute("""
                select min(data) from dbo._data
                where dt> getdate()-5 and mid=1 and id=?
                group by cast(dt as date)
                order by cast(dt as date) desc
               """,id_station)
    minlev=cursor.fetchall()
    for level in minlev:
        minlevel=level[0]

    cursor = cnxn.cursor()
    cursor.execute("""
                select cast(dt as date) as expr1, datepart(hh, DT) as expr2, avg(data) as expr3,
                min(data) as expr4, max(data)as expr5 from dbo._data
                where (id = ?) and (mid = 1) and dt>dateadd(day, - 5, getdate()) and data < 1.5*? and data > 0.3*?
                group by cast(dt as date), datepart(hh, dt)
                ORDER BY Expr1 DESC, Expr2 DESC
               """,id_station,minlevel,minlevel)
    rows = cursor.fetchall()
    return rows

def init_Tables10(request):

# Create a tables from databases
    dat10 = Av.objects.all()
    if dat10.count()>0:
        Av.objects.all().delete()

    stations_id=[4,7] # list of id_stations
    for idsta in stations_id:
        row10=getdata_table10(idsta)
        for rowdata in row10:
            datatableav10=Av()
            datatableav10.value_min=rowdata[2]
            datatableav10.value_avg=rowdata[1]
            datatableav10.value_max=rowdata[3]
            datatableav10.date_observation=rowdata[0]
            datatableav10.id_station=idsta
            datatableav10.save()

    return datatableav10

def init_Tables5(request):

# Create a tables from databases

    if Hour.objects.all().count()>0:
        Hour.objects.all().delete()

    if GraphData.objects.all().count()>0:
        GraphData.objects.all().delete()

    stations_id=[4,7] # list of id_stations
    for idsta in stations_id:
        row5=getdata_table5(idsta)
        for rowdat in row5:
            datatable5=Hour()
            datatable5.value_min=rowdat[3]
            datatable5.value_avg=rowdat[2]
            datatable5.value_max=rowdat[4]
            datatable5.date_observation=rowdat[0]
            datatable5.hour=rowdat[1]
            datatable5.id_station=idsta
            datatable5.save()

    timezone.now()
    stations_id=[4,7] # list of id_stations

    level_brovka=0
    level_zero=0
    for idsta in stations_id:

        ags_station = get_object_or_404(AgsStation,station_id=idsta)

        level_zero= ags_station.value_zero
        level_brovka = ags_station.value_brovka

        graph5=getdata_table5(idsta)
        for rowdat in graph5:
            datatable5=GraphData()
            datatable5.value_min=rowdat[3]
            datatable5.value_max=rowdat[4]
            datatable5.date_observation=rowdat[0]
            my_hour=int(rowdat[1])

            my_date=datetime.strptime(rowdat[0], "%Y-%m-%d")
            my_new_date=my_date+timedelta(hours=my_hour)

            datatable5.dt_observation=my_new_date
            datatable5.hour=rowdat[1]
            datatable5.id_station=idsta

            datatable5.value_avg=rowdat[2]

            temp_value=rowdat[2]/100 + level_zero

            if temp_value < level_brovka:
                datatable5.value_avgBC=temp_value
                datatable5.value_avgBC1=0
                datatable5.value_avgBC2=0
                datatable5.value_avgBC3=0
                datatable5.value_avgBC4=0
                datatable5.value_avgBC50=0
                datatable5.value_avgBC60=temp_value

            if temp_value>=level_brovka and temp_value<(level_brovka+0.5):
                datatable5.value_avgBC1=temp_value
                datatable5.value_avgBC=level_brovka
                datatable5.value_avgBC2=0
                datatable5.value_avgBC3=0
                datatable5.value_avgBC4=0
                datatable5.value_avgBC50=temp_value
                datatable5.value_avgBC60=level_brovka

            if  temp_value >= level_brovka+0.5 and temp_value<(level_brovka+0.8):
                datatable5.value_avgBC2=temp_value
                datatable5.value_avgBC=level_brovka
                datatable5.value_avgBC1=level_brovka+0.5
                datatable5.value_avgBC3=0
                datatable5.value_avgBC4=0
                datatable5.value_avgBC50=level_brovka+0.5
                datatable5.value_avgBC60=level_brovka

            if  temp_value>= level_brovka+0.8 and temp_value<level_brovka + 2:
                datatable5.value_avgBC3=temp_value
                datatable5.value_avgBC=level_brovka
                datatable5.value_avgBC2=level_brovka+0.8
                datatable5.value_avgBC1=level_brovka+0.5
                datatable5.value_avgBC4=0
                datatable5.value_avgBC50=level_brovka+0.5
                datatable5.value_avgBC60=level_brovka

            if  temp_value>=(level_brovka+2):
                datatable5.value_avgBC4=temp_value
                datatable5.value_avgBC=level_brovka
                datatable5.value_avgBC2=level_brovka+0.8
                datatable5.value_avgBC1=level_brovka+0.5
                datatable5.value_avgBC3=level_brovka+2
                datatable5.value_avgBC50=level_brovka+0.5
                datatable5.value_avgBC60=level_brovka



            datatable5.save()



    return datatable5




class ListStatus(ListView):
    model = DataModel
    template_name = 'get_data.html'

def list_status(request):

    table = HourTable(Hour.objects.all())

    RequestConfig(request,paginate={"per_page":10}).configure(table)

    return render(request,'get_data.html',{'table':table})

def index_view(request):
    template_name = "index.html"

    return render(request, template_name)


def mains(request):
    return render(request,'index.html')


def update_page(request):

    init_Tables10(request)

    init_Tables5(request)

    stations=Station.objects.all()

    return render(request,'graph_basic.html',{'stations':stations},)

 #   table = AvTable(Av.objects.all())

 #   table2 = HourTable(Hour.objects.all())

 #   analys_types=DataAnalys.objects.all()

 #    visiblestations=Station.objects.all()

 #   last_date=Av.objects.first()

 #   tableav=True

 #   RequestConfig(request,paginate={"per_page":11}).configure(table)

 #   RequestConfig(request,paginate={"per_page":13}).configure(table2)



