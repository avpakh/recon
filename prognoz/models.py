# -*- coding: utf-8 -*-
from django.db import models

from djgeojson.fields import PolygonField
from django.contrib.gis.db import models as gismodels

class Settlements(gismodels.Model):

    name = models.CharField("Название населенного пункта", max_length=50)
    idriver=models.SmallIntegerField("Rivercode")
    alarm = models.SmallIntegerField("Угроза вначале")
    alarm_end = models.SmallIntegerField("Угроза вконце")
    bereg = models.CharField("Берег", max_length=20)
    start = models.DecimalField("Расстояние по реке - начало, км",max_digits=6,decimal_places=2)
    start_brovka = models.DecimalField("Отметка бровки - начало, м БС",max_digits=6,decimal_places=2)
    start_alarm = models.DecimalField("Отметка опасности - начало, м БС",max_digits=6,decimal_places=2)
    end = models.DecimalField("Расстояние по реке - конец, км",max_digits=6,decimal_places=2)
    end_brovka = models.DecimalField("Отметка бровки - конец, м БС",max_digits=6,decimal_places=2)
    end_alarm = models.DecimalField("Отметка опасности - конец, м БС",max_digits=6,decimal_places=2)
    description=models.CharField("Описание риска",max_length=100)

    geom = PolygonField()

    @property
    def popupContent(self):
      return self.alarm,self.name,self.description


    def __unicode__(self):
		return u" %s %s %s %s %s" % (self.name,self.description,self.alarm,self.start,self.bereg)




class Rivers(models.Model):
    id_river=models.AutoField(primary_key=True)
    river_code=models.SmallIntegerField('Уникальный код реки')
    name_ags=models.TextField('Название станции',max_length=60)
    name= models.TextField('Название реки')
    riverfile=models.TextField('Файл реки')
    uroven=models.DecimalField('Отметка БС',max_digits=6,decimal_places=2)
    data_avaliable=models.BooleanField('Наличие оперативной информации')
    data_url=models.TextField()

    class Meta:
        managed = True
        db_table = u'Rivers'

    def __str__(self):
        return u" %s %s %s" % (self.id_river,self.name,self.riverfile)

    def __unicode__(self):
        return u" %s %s %s" % (self.id_river,self.name,self.riverfile)

class FloodClassification(models.Model):
    id_class=models.AutoField(primary_key=True)
    map_index=models.SmallIntegerField('Код карты')
    description=models.TextField('Классификация наводнений',max_length=120)

    class Meta:
        managed = True
        db_table = u'FloodClassification'

    def __str__(self):
        return u" %s %s " % (self.map_index,self.description)

    def __unicode__(self):
        return u" %s %s" % (self.map_index,self.description)


class Maps(models.Model):
    id_maps=models.AutoField(primary_key=True)
    river=models.ForeignKey(Rivers)
    map_level=models.DecimalField('Расчетный уровень',max_digits=6,decimal_places=2)
    map_index=models.SmallIntegerField('Код карты')


    class Meta:
        managed = True
        db_table = u'Maps'

class Site_New(models.Model):
    river=models.ForeignKey(Rivers)
    distance=models.FloatField('Расстояние до устья')
    explanation=models.TextField('Объект')
    xaxis =models.SmallIntegerField('z')

    class Meta:
        managed = True
        db_table = u'Site_New'

    def __unicode__(self):
        return u" %s %s " % (self.distance,self.explanation)

    def __str__(self):
        return u" %s %s " % (self.distance,self.explanation)



class MapsBrovka(models.Model):
    distance_float=models.FloatField('Расстояние до устья реки')
    dist_km=models.IntegerField('Расстояние до устья реки, км')
    brovka_value=models.DecimalField('Уровень',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka_below=models.DecimalField('Ниже отметки 0 м бровки ',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka0_40=models.DecimalField('От 0  до 40 см превышения над бровкой ',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka40_1=models.DecimalField('От 40 см до 1 м превышения над бровкой',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka1_3=models.DecimalField('Свыше 1м превышения над бровкой',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka1=models.DecimalField('От 0 до 50 см превышения над бровкой',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka2=models.DecimalField('От 50 до 80 см превышения над бровкой',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka3=models.DecimalField('От 80 до 200 см превышения над бровкой',max_digits=5,decimal_places=2,blank=True,null=True)
    brovka4=models.DecimalField('Свыше 2 м превышения над бровкой',max_digits=5,decimal_places=2,blank=True,null=True)



    def __unicode__(self):
        return u" %s %s %s %s %s" % (self.distance_float,self.brovka_below,self.brovka0_40,self.brovka40_1,self.brovka1_3)

    def __str__(self):
        return u" %s %s %s %s %s " % (self.distance_float,self.brovka_below,self.brovka0_40,self.brovka40_1,self.brovka1_3)



    class Meta:
        managed = True
        db_table = u'MapsBrovka'


class MapsData(models.Model):
    river=models.ForeignKey(Rivers,blank=True)
    distance_float=models.FloatField('Расстояние до устья реки',blank=True,null=True)
    map_1=models.DecimalField('Высоковероятностный сценарий 25 %ВП (один раз в 4 года)',max_digits=5,decimal_places=2,blank=True,null=True)
    map_2=models.DecimalField('Высоковерояностный сценарий 10% ВП (один раз в 10 лет)',max_digits=5,decimal_places=2,blank=True,null=True)
    map_3=models.DecimalField('Высоковерояностный сценарий 5% ВП (один раз в 20 лет)',max_digits=5,decimal_places=2,blank=True,null=True)
    map_4=models.DecimalField('Низковероятностный сценарий 1% ВП (один раз в 100 лет)', max_digits=5,decimal_places=2,blank=True,null=True)
    map_5=models.DecimalField('Низковерояностный сценарий 0.5% ВП (один раз в 200 лет)',max_digits=5,decimal_places=2,blank=True,null=True)
    map_6=models.DecimalField('Нет существенного затопления',max_digits=5,decimal_places=2,blank=True,null=True)
    addF=models.TextField('AddF')
    class Meta:
        managed = True
        db_table = u'MapsData'


class Prognozdata(models.Model):

    map=models.ForeignKey(Maps)
    river=models.ForeignKey(Rivers)
    distance=models.DecimalField(' Расстояние до устья ' ,max_digits=12,decimal_places=6)
    distance_float=models.FloatField('Расстояние до устья реки')
    discharge=models.DecimalField('Расход реки',max_digits=12,decimal_places=6)
    level=models.DecimalField('Уровень реки',max_digits=12,decimal_places=6)
    dno=models.DecimalField('Отметка дна',max_digits=12,decimal_places=6)
    time60=models.DecimalField('Время в часах:минутах',max_digits=5,decimal_places=2)
    time100=models.DecimalField('Время в часах',max_digits=5,decimal_places=2)
    brovka=models.DecimalField('Превышение над бровкой',max_digits=5,decimal_places=2)
    distance_pr=models.SmallIntegerField('Привязка',null=True)

    class Meta:
        managed = True
        db_table = u'PrognozData'

    def __unicode__(self):
        return u" %s %s %s %s %s %s %s %s" % (self.distance_float,self.distance,self.discharge,self.level,self.dno,self.time60,self.time100,self.brovka)

    def __str__(self):
        return u" %s %s %s %s %s %s %s %s" % (self.distance_float,self.distance,self.discharge,self.level,self.dno,self.time60,self.time100,self.brovka)


class PrognozGraph(models.Model):

    dist_km=models.IntegerField(' Расстояние до устья, км ')
    distance=models.DecimalField(' Расстояние до устья ' ,max_digits=12,decimal_places=6)
    discharge=models.DecimalField('Расход реки, куб.м/с',max_digits=12,decimal_places=6)
    level=models.DecimalField('Уровень реки, м',max_digits=12,decimal_places=6)
    dno=models.DecimalField('Отметка дна',max_digits=12,decimal_places=6)
    time60=models.DecimalField('Время в часах:минутах',max_digits=5,decimal_places=2)
    time100=models.DecimalField('Время от начала прогноза, ч',max_digits=5,decimal_places=2)
    brovka=models.DecimalField(' Уровень относительно бровки, м',max_digits=5,decimal_places=2)
    brovka1=models.DecimalField('Уровень относительно бровки',max_digits=5,decimal_places=2)

    label=models.TextField('Шкала',max_length=120)

    class Meta:
        managed = True
        db_table = u'PrognozGraph'

    def __unicode__(self):
        return u" %s %s %s %s %s %s %s %s %s" % (self.dist_km,self.distance,self.discharge,self.level,self.dno,self.time60,self.time100,self.brovka,self.label)

    def __str__(self):
        return u" %s %s %s %s %s %s %s %s %s" % (self.dist_km,self.distance,self.discharge,self.level,self.dno,self.time60,self.time100,self.brovka,self.label)


class FloodSet(models.Model):
    dist_km=models.IntegerField(' Расстояние до устья, км ')
    distance=models.DecimalField(' Расстояние до устья,  ' ,max_digits=12,decimal_places=6)
    level=models.DecimalField('Уровень реки, м',max_digits=12,decimal_places=6,null=True)
    name=models.TextField('Название населенного пункта')
    level_danger=models.DecimalField(' Уровень опасности',max_digits=12,decimal_places=6,null=True)

    class Meta:
        managed = True
        db_table = u'FloodSet'

    def __unicode__(self):
        return u" %s %s %s %s %s " % (self.dist_km,self.distance,self.level,self.name,self.level_danger)

    def __str__(self):
        return u" %s %s %s %s %s" % (self.dist_km,self.distance,self.level,self.name,self.level_danger)

