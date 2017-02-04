__author__ = 'alex'

      # make 0


        rural_zero=Settlements.objects.all()

        for rur_o in rural_zero:

            rur_o.alarm=0
            rur_o.description=''
            rur_o.save()


        river_obj = Rivers.objects.get(name=selected_river)

        print selected_river

        print river_obj.river_code

        rural=Settlements.objects.all().filter(idriver=river_obj.river_code)

        print rural

        dists=[]
        name_r=[]
        al1=[]
        al2=[]
        dal1=[]
        dal2=[]
        descr1 = " "
        descr2 = " "

        for rural_obj in rural:

            dist_rural_first = rural_obj.start
            dist_rural_end = rural_obj.end

            level_rural_first = rural_obj.start_alarm
            level_rural_end = rural_obj.end_alarm


            name_rural = rural_obj.name

            level_start = get_level_map(map_id,dist_rural_first)
            level_end = get_level_map(map_id,dist_rural_end)

           # print dist_rural_first,level_start
           # print dist_rural_end,level_end

            value_alarm_first=0
            value_alarm_end=0

            if float(level_start)<float(level_rural_first):
                value_alarm_first=1
                descr1="Нет угрозы затопления"
            elif float(level_start)<float(level_rural_first)+0.4 and float(level_start)>float(level_rural_first):
                value_alarm_first=2
                descr1="угроза затопления территории н.п. до 0.4 м. Низкий риск"
            elif float(level_start)<float(level_rural_first)+1 and float(level_start)>float(level_rural_first)+0.4:
                value_alarm_first=3
                descr1="угроза затопления территории н.п. от 0.4 до 1 м. Повышенный риск"
            elif float(level_start)>float(level_rural_first)+1:
                value_alarm_first=4
                descr1="угроза затопления территории н.п. свыше 1 м. Критический риск"


            if float(level_end)<float(level_rural_end):
                value_alarm_first=1
                descr2="Нет угрозы затопления"
            elif float(level_end)<float(level_rural_end)+0.4 and float(level_end)>float(level_rural_end):
                value_alarm_end=2
                descr2="угроза затопления территории н.п. до 0.4 м. Низкий риск"
            elif float(level_end)<float(level_rural_end)+1 and float(level_end)>float(level_rural_end)+0.4:
                value_alarm_end=3
                descr2="угроза затопления территории н.п. от 0.4 до 1 м. Повышенный риск"

            elif float(level_end)>float(level_rural_end)+1:
                value_alarm_end=4
                descr2="угроза затопления территории н.п. свыше 1 м. Критический риск"

            name_r.append(name_rural)
            dists.append(dist_rural_first)
            al1.append(value_alarm_first)
            al2.append(value_alarm_end)
            dal1.append(descr1)
            dal2.append(descr2)


        t=0

        while t<len(name_r):

            rur_obj = Settlements.objects.get(name=name_r[t],idriver=river_obj.river_code)
            if al1[t]>al2[t]:
                rur_obj.alarm=int(al1[t])
                rur_obj.description=dal1[t]
                rur_obj.save()

            if al1[t]<al2[t]:
                rur_obj.alarm=int(al2[t])
                rur_obj.description=dal2[t]
                rur_obj.save()

            if al1[t] == al2[t]:
                rur_obj.alarm=int(al1[t])
                rur_obj.description=dal1[t]
                rur_obj.save()

            t=t+1




  {'options':{
                 'source': rural},
                 'terms': ['start','end']
                 },




                {'options':{
                   'type': 'line',
                   },
                'terms':{
                  'distance_float': [
                  'start']
                  }},












