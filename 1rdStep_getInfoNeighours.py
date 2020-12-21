# -*- coding: utf-8 -*-
"""
本程序流程
1 读取 'trafficMetaData.csv' 文件
2 Traite函数负责将取得起始点，结束点之间均值
3 distance 计算两地之间距离
4 PointDeControleVille 根据所选城市，提取出此城市的观测点
5 TousLesVoisin 按照规则（距离，最小小邻居数目）获取本观测点和其邻居的信息
6 将5中结果存储在 'tousLesVoisinsDeTouslesPionts.npy'
"""

'''
本次关键参数：
'''
#fileDetrafficMetaData = 'trafficMetaData_simple.csv' #这是改过的，只含有11个观测点
fileDetrafficMetaData = 'trafficMetaData.csv' 
villeChoisie = "Aarhus"
distanceEntreVoision = 1000
miniNumVoisin = 4


'''
读取 'trafficMetaData.csv' 文件
lecture de metadat de traffice
'''
import csv
metaDataTraffice = []
with open(fileDetrafficMetaData) as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
        metaDataTraffice.append(row) 

'''
fonction Traite 
将监测路段经度/纬度处理，从文本到浮点型可以接收的范围，然后算个均值
'''
def Traite(X,Y):
    if len(X) >= 15:
        X = X[0:16]
    else: 
        for c in (0,16-len(X)):
            X+"0"
    if len(Y) >= 15:
        Y = Y[0:16]
    else: 
        for c in (0,16-len(Y)):
            Y+"0"
    return 0.5*(float(X)+float(Y))

'''
distance 输入两地经纬度，计算距离 输出单位 米
'''
import math
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6378.137 # km
 
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c*1000
    return d
'''
根据所选城市，提取出所有监控点的位置
输出【ID，LA，LN】
'''
def PointDeControleVille(metaDataTraffice,ville):
    metaDataVille = []
    for c in range(0,len(metaDataTraffice)):
        if metaDataTraffice[c][16] ==ville:
#        print(metaDataTraffice[c][25]+","+metaDataTraffice[c][12]+","+metaDataTraffice[c][19]+","+metaDataTraffice[c][13]+","+metaDataTraffice[c][5])
            metaDataVille.append([metaDataTraffice[c][20],metaDataTraffice[c][12],metaDataTraffice[c][19],metaDataTraffice[c][13],metaDataTraffice[c][5]])
    F = lambda a:(a[0],Traite(a[1],a[3]),Traite(a[2],a[4]))
    re = F(metaDataVille)
#    metaDataVille = map(lambda (a):([int(a[0]),Traite(a[1],a[3]),Traite(a[2],a[4])]),metaDataVille)
    return re

ponitTraffic = PointDeControleVille(metaDataTraffice,villeChoisie)


'''
输入 moi 自己所在点【ID，LA，LN】，
输入 Doc 即监控点ID和位置信息
输入 邻居范围
输出 邻居列表 【ID，LA，LN】 
第一个位置表示自己， 即 自己 + 邻居
'''
def VoisinDePoint(moi,Doc,Dis):
    MoiLA = 0
    MoiLON = 0
    listVoisin = []
    for c in range(0,len(Doc)):
        if Doc[c][0] == moi:
                MoiLA = Doc[c][1]
                MoiLON = Doc[c][2]
                listVoisin.append([moi,MoiLA,MoiLON])
    for c in range(0,len(Doc)):
        if Doc[c][0] != moi and distance([MoiLA,MoiLON],[Doc[c][1],Doc[c][2]])<Dis:
            listVoisin.append(Doc[c])
    return listVoisin


'''
输入 pt 即所有节点信息，对应 ponitTraffic
输入 dis 距离
输出　[本节点,+若干邻居节点列表]
'''
def TousLesVoisin(pt,dis):
    resultat = []
    for c in range(0,len(pt)):
        temp = VoisinDePoint(pt[c][0],ponitTraffic,dis)
        if len(temp[1:]) <= miniNumVoisin:
            temp = VoisinDePoint(pt[c][0],ponitTraffic,dis*3)
        if len(temp[1:]) <= miniNumVoisin:
            print (temp[0])
#        resultat.append([temp[0][0],dis,len(temp[1:]),map(lambda a:a[0],temp[1:])])
        resultat.append(map(lambda a:a[0],temp))
    return resultat
        
tousLesVoisinsDeTouslesPionts = TousLesVoisin(ponitTraffic,distanceEntreVoision)


'''
需要描述一些邻居节点信息
1 多少观察节点，
2 邻居数据均值,最大值，最小值
'''
def discription(info):
    numVoisions = map(lambda a:len(a),info)
    chiffre = [len(numVoisions),np.average(numVoisions),np.max(numVoisions),np.min(numVoisions)]
    print ['nombreux','moyenne','max','min']
    print (chiffre)
    
discription(tousLesVoisinsDeTouslesPionts)
    
'''
#X,Y 黑点表示，全部Aarhus的点
#'''
#X = map(lambda (a):(a[1]-56),ponitTraffic)
#Y = map(lambda (a):(a[2]-10),ponitTraffic)
#'''
#lvX lvY自己和邻居的点 红色 蓝色
#'''
#lvX = map(lambda (a):(a[1]-56),listVoisin)
#lvY = map(lambda (a):(a[2]-10),listVoisin)
#import matplotlib.pyplot as plt
#
#plt.xlim()
#
#plt.xlim(min(X)*0.99, max(X)*1.01)
#plt.ylim(min(Y)*0.99, max(Y)*1.01)
#
#plt.plot(X,Y,'ko')
#plt.plot(lvX[1:],lvY[1:],'bo')
#plt.plot(lvX[0],lvY[0],'ro')
##plt.plot(listVoisin[2:][1],listVoisin[2:][2],'bo',label="point")
##plt.plot(listVoisin[0][1],listVoisin[0][2],'ro',label="point")
#plt.legend()
#plt.show()

'''

'''
import numpy as np
import csv
#csvfile = file('listVoisin.csv', 'wb') 
#writer = csv.writer(csvfile)
#writer.writerow(['rapportID','LA','LON'])
#writer.writerows(listVoisin)
#csvfile.close()


np.save('tousLesVoisinsDeTouslesPionts.npy',tousLesVoisinsDeTouslesPionts) 








