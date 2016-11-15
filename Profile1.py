# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 10:23:56 2016

@author: jorge
"""


###Importamos los paquetes pandas y matplotlib###
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
###Folder that contain the files###
folder= '/Users/jorge/Desktop/PracticasIFCA/csvFiles/%s.csv'
###Program that read a specific file with format csv and put how index the date
def load_data(title):
    data=pd.read_csv(folder%title)
    data.index=pd.to_datetime(data.pop('date'))
    return data
###Read the file AMT.csv to analyze the water temperature (ºC)    
AMT=load_data('AMT')
###Create a new table deleting the rows that have profile 0
AMT1= AMT[AMT.profile == 1]
AMT1.insert(12,'curate',None)
###Program cleanP1() delete the rows where steel cage is going down                     
def cleanP1():
    a=AMT1.index.strftime('%Y-%m-%d')
    dates=[]###Create a list with the days that have some data with profile 1
    for i in a:
        if i not in dates:
            dates.append(i)
    list1=[]###Empty list that is going to contain the row indices to delete
    list2=[]###Empty list that is going to contain the row indices to profiles with few elements
    for i in dates:
        AMTday=AMT1[i]###Table with data for each day in dates
        l=len(AMTday)###Number of rows in AMTday
        if l>=10:###If AMTday has lees than 10 rows give problems in this program 
            for j in range(0,5):###Take the first five indices
                if (AMTday.depth[j]<AMTday.depth[j+1] and abs(AMTday.depth[j]-AMTday.depth[j+1])>=0.2) or AMTday.depth[j]<=5:
                    print(AMTday.index[j],'Warning')
                    list1.append(AMTday.index[j])
            for p in range(-5,-1):###Take the last five indices
                if AMTday.depth[p]<AMTday.depth[p+1] and abs(AMTday.depth[p]-AMTday.depth[p+1])>=0.2:
                    print(AMTday.index[p+1],'Warning')
                    list1.append(AMTday.index[p+1])
        else:
            for k in range(0,l):
                print(AMTday.index[k],'Few elements this day')
                list2.append(AMTday.index[k])
    AMTF=AMT1.drop(list1)###Delete the rows that not satisfy the coditions
    for t in list1:
        AMT1.loc[t,'curate']='Warning'
    for t in list2:
        AMT1.loc[t,'curate']='Few elements this day'
    return AMTF,AMT1###Return new table without wrong values
AMTF,AMT1 =cleanP1()
AMT1.to_csv('AMT_profile1.csv')
###############################################################################
def fitprofile(day):
    x=AMTF[day].temp##Temperature data specific day
    y=AMTF[day].depth##Depth data specific day
    def fdepth(y,alpha,n):##Function f(y)=((Te-Th)/((1+(alpha*y)**n)**m))+Th
        m=1-(1/n)
        Th=x.min()
        Te=x.max()
        return ((Te-Th)/((1+(alpha*y)**n)**m))+Th
    values,a=curve_fit(fdepth,y,x)
    print('alpha=',values[0],'\n','n=',values[1])
    Ftemp=fdepth(y,values[0],values[1])
    plt.figure()
    plt.gca().invert_yaxis()
    plt.scatter(x,y,label='Real')
    plt.plot(Ftemp,y,'r',label='Fit')
    plt.legend(loc=4)
    plt.xlabel('Temp')
    plt.ylabel('Depth')
    return

fitprofile('2014-08-17')
plt.figure()
plt.gca().invert_yaxis()
AMTF['2014-08-17'].depth.plot(style='o')
AMT1['2014-08-17'].depth