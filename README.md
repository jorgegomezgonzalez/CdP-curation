# CdP-curation
#-*- coding: utf-8 -*-
"""
Created on Wed Oct 19 16:53:54 2016

@author: Jorge Gomez Gonzalez
"""

###Import packages pandas and matplotlib###
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
###Folder that contain the files###
folder= '/Users/jorge/Desktop/PracticasIFCA/csvFiles/%s.csv'
###Program that read a specific file with format csv and put how index the date
def load_data(title):
    data=pd.read_csv(folder%title)
    data.index=pd.to_datetime(data.pop('date'))
    return data
###Read the file AMT.csv to analyze the water temperature (ºC)
AMT=load_data('AMT')
###Create a new table deleting the rows that have profile 1
AMT= AMT[AMT.profile == 0]
list_temp=AMT.temp##Create a list with data from the water temperature with profile 0
##list_temp.plot()
list_temp['2014-08-01'].between_time('12:00','14:00')
AMT.depth['2014-08-01'].between_time('12:00','14:00')
###Now we create a new table where the depth is between 3.5 and 4.5 m and profile is 0
###because in the previous plot can see that in some data with profile 0 the depth is very big
AMT2= AMT[(AMT.depth>=3.5) & (AMT.depth<=4.5)]###AMT0 is the data table that we use to study the water teperature around 4 m

plt.figure(1)
AMT2['2014'].groupby(lambda x:x.month).temp.agg(['count']).plot(style='o')
plt.legend(['2014'],loc=2)
plt.xlabel('Month')
plt.ylabel('Size')
AMT2['2015'].groupby(lambda x:x.month).temp.agg(['count']).plot(style='^')
plt.legend(['2015'])
plt.xlabel('Month')
plt.ylabel('Size')

dates=[]###Create a list with the days that have some data with profile 0
for h in ['2014-11','2015-02','2015-03']:
    a=AMT2[h].index.strftime('%Y-%m-%d')
    for i in a:
        if i not in dates:
            dates.append(i)
list1=[]        
for i in dates:
    AMTday=AMT2[i]###Table with data for each day in dates
    l=len(AMTday)###Number of rows in AMTday
    if l>100:
        c=AMTday.index[0]
        b=AMTday.index[-1]
        for i in AMTday.index:
            if i not in pd.date_range(c,b,freq='15T'):
                list1.append(i)
AMT0=AMT2.drop(list1)###Delete the rows that not satisfy the coditions

plt.figure(2)
plt.hist([AMT0.temp,AMT2.temp], bins=25 , histtype='bar',normed=1,label=['AMT0','AMT2'])
plt.legend()
plt.xlabel('Temp')
plt.ylabel('Probability')

len(AMT0)
AMT0.name='AMT0'
list_temp0=AMT0.temp
print(list_temp0)
list_temp0.plot()
AMT.insert(12,'curate',None)
for t in AMT.index:
    if t not in AMT0.index:
        AMT.loc[t,'curate']='Warning'
AMT.to_csv('AMT_profile0.csv')
###Now separate 2014-2015 for months and compute the mean to each month and the general mean
def analysismeanmonth(data):
    mean2014=data['2014'].groupby(lambda x:x.month).temp.agg(['mean'])
    mean2015=data['2015'].groupby(lambda x:x.month).temp.agg(['mean'])
    generalmean=[np.NaN]                  
    for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
        date2014='2014-'+month
        date2015='2015-'+month
        if (date2014 in data.index) & (date2015 in data.index):
            data_month2014=data.temp[date2014]
            data_month2015=data.temp[date2015]
            data_month=data_month2014.append(data_month2015)
            generalmean.append(data_month.mean())
        else:
            generalmean.append(np.NaN)
    plt.figure(3)
    plt.plot(mean2014, 'bs',mean2015, 'g^',generalmean,'r--')
    plt.legend(['2014', '2015','2014-2015'],loc=2)
    plt.xlabel('Month')
    plt.ylabel('Temp')
    return  mean2014,mean2015,generalmean
    
##################################################################################################
###Compare with other station
###Program that read a specific file with format csv, change the column labels and put how index the date
def load_data2(title,columns):
    data=pd.read_csv(folder%title)
    data['FECHA'] = pd.to_datetime(data.FECHA,dayfirst=True)
    data=data.sort_values('FECHA')
    data.columns=columns
    data=data.set_index('date')
    return data
###################################################################################################
###Read the file DU07_DUERO_waterTemp2.csv to analyze the water temperature (ºC)
Duero=load_data2('DU07_DUERO_waterTemp2',['date','temp','unit'])
Duero.name='Duero'
plt.figure(4)
Duero.temp.plot()
plt.ylabel('Temp')
####################################################################################################
###Read the file Revinuesa_waterTemp2.csv to analyze the water temperature (ºC)
Revi=pd.read_csv(folder%'Revinuesa_waterTemp2')
Revi['FECHA'] = pd.to_datetime(Revi.FECHA,dayfirst=True)##Put the date with format YEAR-MONTH-DAY HOUR:MIN:SEC
Revi=Revi.sort_values('FECHA')##Order the data by date
plt.figure(5)
Revi.VALOR.plot()
plt.ylabel('Temp')
##Change the values >=30 
for i in range(0,len(Revi)):
    j=Revi.VALOR[i]
    if j>=30:
        Revi.loc[i,'VALOR']=j*0.1
##Change the values in inter
inter = (Revi.FECHA > '2014-12-01') & (Revi.FECHA <= '2015-04-01')
Revi_inter=Revi.loc[inter]
for i in Revi_inter.index:
    j=Revi.VALOR[i]
    if j>=10:
        Revi.loc[i,'VALOR']=j*0.1
Revi.columns=['date','temp','unit']##New columns label
Revi=Revi.set_index('date')##New index
Revi.name='Revinuesa'
plt.figure(6)
Revi.temp.plot()
plt.ylabel('Temp')
##################################################################################
Pita=load_data2('E08_Boya_Playa_Pita_waterTemp2',['date','temp','unit'])
Pitapress=load_data2('E08_Boya_Playa_Pita_waterPressure2',['date','press','unit'])
Pita.temp.plot()
for i in Pitapress.index:
    if i not in Pita.index:
        Pitapress.drop(i,inplace=True)
for i in Pita.index:
    if i not in Pitapress.index:
        Pita.drop(i,inplace=True)
Pita2=pd.concat([Pita, Pitapress], axis=1)
plt.figure(7)
Pita2[(Pita2.press>=0.32) & (Pita2.press<=0.34) & (Pita2.index>'2015-02-04') & (Pita2.index<'2015-08-14')].temp.plot()
plt.ylabel('Temp')

Pita2[(Pita2.index>'2015-02-04') & (Pita2.index<'2015-03-26')].temp.plot()
Pita2[(Pita2.index>'2015-05-07') & (Pita2.index<'2015-05-16')].temp.plot()
Pita2[(Pita2.index>'2015-07-16') & (Pita2.index<'2015-08-14')].temp.plot()

Pita3=Pita2[(Pita2.index<='2015-02-04') | ((Pita2.index>='2015-03-26') & (Pita2.index<='2015-05-07')) | ((Pita2.index>='2015-05-16') & (Pita2.index<='2015-07-16')) | (Pita2.index>='2015-08-14')]
plt.figure(8)
Pita3.temp.plot()
plt.ylabel('Temp')
Pita3.name='Playa Pita'

AMT0pita=AMT0[(AMT0.index<='2015-02-04') | ((AMT0.index>='2015-03-26') & (AMT0.index<='2015-05-07')) | ((AMT0.index>='2015-05-16') & (AMT0.index<='2015-07-16')) | (AMT0.index>='2015-08-14')]
AMT0pita.name='AMT0p'
##############################################################################
##############################################################################
##Kolmogorov-Smirnov Test
def contrast(data1,data2,variable):##Example contrast(AMT0,Duero,'temp')
    label1=data1.name
    label2=data2.name
    data1=data1[variable]
    data2=data2[variable]
    ##Take the same range by date
    if data1.index[0]<data2.index[0]:
        index0=data2.index[0]
    else:
        index0=data1.index[0]
    if data1.index[-1]<data2.index[-1]:
        index1=data1.index[-1]
    else:
        index1=data2.index[-1]
    data1=data1[(data1.index>=index0) & (data1.index<=index1)]       
    data2=data2[(data2.index>=index0) & (data2.index<=index1)]
    ## Plot the temperature by date. data1 with color blue and data2 with color green
    plt.figure(9)
    plt.plot(data1,'b',label=label1)
    plt.plot(data2,'g',label=label2)
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel(variable)
    ###Histogram for each data
    if data1.max()>data2.max(): 
        listbins=range(int(data1.max())+1)
    else:
        listbins=range(int(data2.max())+1)
    plt.figure(10)
    plt.hist([data1,data2], listbins, histtype='bar',normed=1,label=[label1,label2])
    plt.legend()
    plt.xlabel(variable)
    plt.ylabel('Probability')
    ###Kolmogorov-Smirnov Test
    ###Cumulative distribution function data1
    plt.figure(11)
    b=len(data1)
    h=np.sort(data1)
    a=np.searchsorted(h,h,side='right') / (1.0*b)
    plt.step(h,a,label=label1) 
    ###Cumulative distribution function data2
    b2=len(data2)
    h2=np.sort(data2)
    a2=np.searchsorted(h2,h2,side='right') / (1.0*b2)
    plt.step(h2,a2,label=label2)
    plt.legend(loc=4)
    plt.xlabel(variable)
    plt.ylabel('Probability')
    plt.title('Cumulative distribution function')
    return stats.ks_2samp(data1,data2)

contrast(AMT0,Duero,'temp')
contrast(AMT0,Revi,'temp')
contrast(AMT0pita,Pita3,'temp')
