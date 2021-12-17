import os
import numpy as np
import cv2
from threading import Thread
import time
import math
from pathlib import Path

# Veri seti secildikten sonra kullaniciya gore uzerinde uygulanacak islemler
def DatasetOperations(CSVFile, columnOperation, rawOperation, methodsOperation):

    # column bazli silme
    if columnOperation!="Not":

        for i in CSVFile:

            nan=0

            for j in CSVFile[i]:

                if str(j) == "nan":

                    nan+=1


            yuzdelik = 100 * (nan/len(CSVFile[i]))
            if yuzdelik > float(columnOperation[1:]):

                CSVFile.drop("{}".format(i), axis=1, inplace=True)

    # satir bazli silme
    if rawOperation!="Not":

        columns = CSVFile.columns

        for index, row in CSVFile.iterrows():

            nan = 0

            for cl in range(0,len(columns)):

                if str(row[cl])=="nan":

                    nan+=1

            if nan > int(rawOperation):

                CSVFile = CSVFile.drop([int(index)])

    # doldurma yontemleri
    if methodsOperation!="Not":

        if methodsOperation == "Mean":

            for i in CSVFile:

                count = 0
                toplam = 0

                for j in CSVFile[i]:

                    if str(j) != "nan":

                        toplam += int(j)
                        count+=1

                deger = toplam/count
                deger = int(deger)

                for z, j in enumerate(CSVFile[i]):

                    if str(j) == "nan":

                        CSVFile[i][z] = deger

        elif methodsOperation == "Mode":

            for i in CSVFile:

                dtta = []
                dttb = []

                for j in CSVFile[i]:

                    if str(j) == "nan":

                        continue

                    flag = None

                    for k, z in enumerate(dtta):

                        if j==z:

                            flag=True
                            dttb[k] = dttb[k]+1
                            break

                    if flag==None:

                        dtta.append(j)
                        dttb.append(1)


                maxValue = max(dttb)
                mode = -99

                for k,j in enumerate(dttb):

                    if j==maxValue:

                        mode = dtta[k]

                mode = int(mode)

                for z, j in enumerate(CSVFile[i]):

                    if str(j) == "nan":

                        CSVFile[i][z] = mode


        elif methodsOperation == "Median":


            for name in CSVFile:

                vektor = []

                for j in CSVFile[name]:

                    if str(j) != "nan":

                        vektor.append(j)
 
                vektor = sorted(vektor)
                veriAdedi = len(vektor)
                deger = -99

                if veriAdedi % 2 == 1:

                    deger = vektor[veriAdedi // 2]

                else:

                    i = veriAdedi // 2
                    deger = (vektor[i - 1] + vektor[i]) / 2


                deger = int(deger)

                for z, j in enumerate(CSVFile[name]):

                    if str(j) == "nan":

                        CSVFile[name][z] = deger

    return CSVFile

def Mean(dicta, CSVFile, deger):

    ind = deger.index("Mean")
    degTemp = deger[0]
    deger[0] = "Mean"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Mean":[]}

    for i in CSVFile:

        top = 0
        count = 0

        for j in CSVFile[i]:

            count += 1
            top += j

        dicta["Column Name"].append(i)
        dicta["Mean"].append(top/count)

    return dicta, CSVFile, deger


def Median(dicta, CSVFile, deger):

    ind = deger.index("Median")
    degTemp = deger[0]
    deger[0] = "Median"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Median":[]}

    for name in CSVFile:

        vektor = sorted(CSVFile[name])
        veriAdedi = len(vektor)

        if veriAdedi % 2 == 1:

            dicta["Median"].append(vektor[veriAdedi // 2])

        else:

            i = veriAdedi // 2
            dicta["Median"].append((vektor[i - 1] + vektor[i]) / 2)

        dicta["Column Name"].append(name)

    return dicta, CSVFile, deger


def Mode(dicta, CSVFile, deger):

    ind = deger.index("Mode")
    degTemp = deger[0]
    deger[0] = "Mode"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Mode":[]}

    for i in CSVFile:

        dtta = []
        dttb = []

        for j in CSVFile[i]:

            flag = None

            for k, z in enumerate(dtta):

                if j==z:

                    flag=True
                    dttb[k] = dttb[k]+1
                    break

            if flag==None:

                dtta.append(j)
                dttb.append(1)

        maxValue = max(dttb)
        mode = []

        for k,j in enumerate(dttb):

            if j==maxValue:

                mode.append(dtta[k])

        dicta["Mode"].append(mode)

        dicta["Column Name"].append(i)

    return dicta, CSVFile, deger


def IQR(dicta, CSVFile, deger):

    ind = deger.index("Interquartile range value (IQR)")
    degTemp = deger[0]
    deger[0] = "Interquartile range value (IQR)"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Interquartile range value (IQR)":[]}

    for i in CSVFile:

        IQR = np.percentile(CSVFile[i], 75) - np.percentile(CSVFile[i], 25)

        dicta["Column Name"].append(i)
        dicta["Interquartile range value (IQR)"].append(IQR)


    return dicta, CSVFile, deger


def Outliers(dicta, CSVFile, deger):

    ind = deger.index("Outliers")
    degTemp = deger[0]
    deger[0] = "Outliers"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Outliers":[]}

    for i in CSVFile:

        q1 = np.percentile(CSVFile[i], 25)
        q3 = np.percentile(CSVFile[i], 75)
        IQR = q3-q1
        degerler = []

        minn = q1 - IQR*1.5
        maxx = q3 + IQR*1.5

        for j in CSVFile[i]:

            if j<minn or j>maxx:

                degerler.append(j)

        strr = "Min: "+str(minn)+", Max: "+str(maxx)+", Aykiri Degerler: "+str(degerler)

        dicta["Column Name"].append(i)
        dicta["Outliers"].append(strr)


    return dicta, CSVFile, deger


def FiveNumber(dicta, CSVFile, deger):

    ind = deger.index("Five number summary")
    degTemp = deger[0]
    deger[0] = "Five number summary"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Five number summary":[]}

    for i in CSVFile:

        q1 = np.percentile(CSVFile[i], 25)
        q3 = np.percentile(CSVFile[i], 75)
        minn = min(CSVFile[i])
        maxx = max(CSVFile[i])

        vektor = sorted(CSVFile[i])
        veriAdedi = len(vektor)
        median = -99

        if veriAdedi % 2 == 1:

            median = vektor[veriAdedi // 2]

        else:

            x = veriAdedi // 2
            median = (vektor[x - 1] + vektor[x]) / 2

 
        strr = "Min: "+str(minn)+", Q1: "+str(q1)+", Median: "+str(median)+", Q3: "+str(q3)+", Max: "+str(maxx)

        dicta["Column Name"].append(i)
        dicta["Five number summary"].append(strr)

    return dicta, CSVFile, deger


def VarianceStandardDeviation(dicta, CSVFile, deger):

    ind = deger.index("Variance and standard deviation")
    degTemp = deger[0]
    deger[0] = "Variance and standard deviation"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Variance and standard deviation":[]}

    for i in CSVFile:

        varianceD = variance(CSVFile[i])
        stdevD = stdev(CSVFile[i])

        strr = "Variance: "+str(varianceD)+", Standard Deviation: "+str(stdevD)

        dicta["Column Name"].append(i)
        dicta["Variance and standard deviation"].append(strr)

    return dicta, CSVFile, deger


def BoxChart(CSVFile, deger, dt_string):

    ind = deger.index("Box Chart")
    degTemp = deger[0]
    deger[0] = "Box Chart"
    deger[ind] = degTemp

    img_np = []

    for i in CSVFile:

        q1 = np.percentile(CSVFile[i], 25)
        q3 = np.percentile(CSVFile[i], 75)

        vektor = sorted(CSVFile[i])
        veriAdedi = len(vektor)

        if veriAdedi % 2 == 1:

            median = vektor[veriAdedi // 2]

        else:

            x = veriAdedi // 2
            median = (vektor[x - 1] + vektor[x]) / 2

        # resimler ayri bir fonksiyonda cizdirilir ve saklanir
        img_np.append(CreateBoxChartImage([min(CSVFile[i]),q1,median, q3, max(CSVFile[i])], i))


    # resimler cift halinde yatay sekilde birlestirilir
    img_cift = []
    for k, img in enumerate(img_np):

        # ilk resim saklanir, ikinci resimle birlestirmek icin
        if k%2==0:

            new_image = img

            # eger sutun sayisi tek ise beyaz bir resim olusturulur ve birlesitirlir
            if len(img_np)%2==1 and k==len(img_np)-1:

                temp = np.zeros((img.shape[0],img.shape[1],img.shape[2]), np.uint8)
                temp[:,:] = [255,255,255]
                new_image = np.concatenate((new_image, temp), axis=1)

                img_cift.append(new_image)

        # ilk resim ile ikinci resim yatayda birlestirilir ve liste de saklanır
        else:

            new_image = np.concatenate((new_image, img), axis=1)

            img_cift.append(new_image)


    # yatay da birlestirilen resimler dikeyde birlestirilir
    cs = 0
    for img in img_cift:

        # ilk resim saklanır
        if cs==0:

            final_image = img
            cs=1

        # ilk ve diger resimler birlestirilir
        else:

            final_image = np.concatenate((final_image, img), axis=0)


    # resim uniq bir sekilde kaydedilir.
    img = os.path.join('static', 'imagesBoxChart/{}.png'.format(dt_string))
    cv2.imwrite(img, final_image)

    # ayri bir thred ile silinir, depolama icin tutmadim, server de sikinti cikartir
    Thread(target=Check, args=(img,)).start()

    return img, CSVFile, deger



def CreateBoxChartImage(dtt, name):

    # boyutlar ve cizim icin gereklilikler
    width = 500
    height = 600
    chanel = 3
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 1

    # bos beyaz sayfa
    image  = np.zeros((width,height,chanel), np.uint8)
    image[:,:] = [255,255,255]

    # yatay duz cizgi
    image = cv2.line(image, (20,360), (500,360), color, 2)

    # column name yazdirma
    temp = (400-len(name))//2
    image = cv2.putText(image, name, (temp, 40), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

    # min-max normalizasyonu icin degerler
    new_min = 50
    new_max = 450
    minn = min(dtt)
    maxx = max(dtt)

    q1_q3 = []

    # bos beyaz sayfaya cizim yaptigim dongu
    for i in range(len(dtt)):

        # min-max normalizasyonu
        bl = (dtt[i]-minn)/(maxx-minn)
        deg = int(bl*(new_max-new_min)+new_min)

        # degerleri yuvarlak ile cizdim
        image = cv2.circle(image, (deg,360), 2, color, 2)

        # degerleri yazdim
        image = cv2.putText(image, str(dtt[i]), (deg-5, 390), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

        # min max degerleri icin duz cizgi
        if i==0 or i==4:

            image = cv2.line(image, (deg,175), (deg,225), color, 2)

        # min max dan q1 ve q3 'e duz cizgi
        if i==1 or i==3:

            if i==1:

                image = cv2.line(image, (new_min,200), (int(deg),200), color, 1)

            else:

                image = cv2.line(image, (new_max,200), (int(deg),200), color, 1)

            q1_q3.append(deg)


        # median
        if i==2:

            image = cv2.line(image, (deg,150), (deg,250), (0,0,139), 2)

    # dikdörtgen, q1 ve q3 e gore cizilir
    image = cv2.rectangle(image, (q1_q3[0],150), (q1_q3[1],250), color, thickness)


    return image

def Frequency(dicta, CSVFile, deger, dt_string):

    ind = deger.index("Frequency")
    degTemp = deger[0]
    deger[0] = "Frequency"
    deger[ind] = degTemp

    dicta = {"Column Name":[],"Frequency":[]}
    img_np = []

    # frekans hesaplanir
    for i in CSVFile:

        dtt = []

        for j in CSVFile[i]:

            flag = None

            for k, z in enumerate(dtt):

                if j==z[0]:

                    flag=True
                    dtt[k][1] = dtt[k][1]+1
                    break

            if flag==None:

                dtt.append([j,1])

        dicta["Column Name"].append(i)
        dicta["Frequency"].append(dtt)

        # resim ayri bir fonksiyonda cizdirilir ve bu listede depolanir
        img_np.append(CreateFrekansImage(dtt, i))


    # resimler cift halinde yatayda birlestirilir ve liste de saklanilir 
    img_cift = []
    for k, img in enumerate(img_np):

        # ilk resim saklanir ve ikinci resimle birlesitirmek icin tutulur
        if k%2==0:

            new_image = img

            # eger sutunumuz tek ise bos beyaz resim olusturulur ve birlestirilir
            if len(img_np)%2==1 and k==len(img_np)-1:

                temp = np.zeros((img.shape[0],img.shape[1],img.shape[2]), np.uint8)
                temp[:,:] = [255,255,255]
                new_image = np.concatenate((new_image, temp), axis=1)

                img_cift.append(new_image)

        # sutunumuz cift ise ilk resimle birlestirilir ve listede depolanir
        else:

            new_image = np.concatenate((new_image, img), axis=1)

            img_cift.append(new_image)


    # olusturdugumuz yatayda ki cift resimleri dikey sekilde birlestiriyoruz
    cs = 0
    for img in img_cift:

        # ilk resim
        if cs==0:

            final_image = img
            cs=1

        # ilk resim ve diger resimlerin birlestirilmesi
        else:

            final_image = np.concatenate((final_image, img), axis=0)

    # uniq bir sekilde bu konuma resim yazdirilir
    img = os.path.join('static', 'imagesFrequency/{}.png'.format(dt_string))
    cv2.imwrite(img, final_image)

    # ayri bir thred ile silinir, depolama icin tutmadim, server de sikinti cikartir
    Thread(target=Check, args=(img,)).start()

    return dicta, img, CSVFile, deger


def CreateFrekansImage(dtt, name):

    # boyutlar ve cizim icin gereklilikler
    width = 500
    height = 600
    chanel = 3
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 0)
    thickness = 1

    # bos beyaz sayfa
    image  = np.zeros((width,height,chanel), np.uint8)
    image[:,:] = [255,255,255]

    # kordinat duzlemi icin dikeyde ve yatayda cizgi
    image = cv2.line(image, (40,40), (40,360), color, 2)
    image = cv2.line(image, (40,360), (500-30,360), color, 2)

    # column name
    temp = (400-len(name))//2
    image = cv2.putText(image, name, (temp, 20), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

    # values ekseni
    image = cv2.putText(image, "Values", (480, 365), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

    # frekans ekseni
    image = cv2.putText(image, "FREQ", (15, 20), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

    # ayni frekans degerlerini sürekli cizdirmemek icin sadece bir kere aldim
    listDeger = []
    for i in range(0, len(dtt)):

        flag = None

        for j in listDeger:

            if dtt[i][1]==j:

                flag=True
                break

        if flag!=True:

            listDeger.append(dtt[i][1])

    listDeger = sorted(listDeger)

    # frekanslarin esit bir sekilde yazdirilmasi icin
    adim = 350/(len(listDeger))
    count = adim

    temp = []

    for i in listDeger:

        # frekans yazdirma
        image = cv2.putText(image, str(i), (0, int(400-count)), font, 
                        fontScale, color, thickness, cv2.LINE_AA)

        # frekans yazilimi belli olsun diye ufak daire
        image = cv2.circle(image, (40,int(400-(count+4))), 3, color, 2)

        # bu degeri tutuyorum cunki, daha sonra buraya kadar cizgi cekecegiz
        temp.append([i, int(400-(count+3))])

        count+=adim

    # degerler icin olceklenebilir adim
    adim = 375/(len(dtt))
    count = adim

    for i in range(0, len(dtt)):

        # deger adi yazdirilir
        image = cv2.putText(image, str(dtt[i][0]), (int(450-count), 385), font, 
                    fontScale, color, thickness, cv2.LINE_AA)

        # bu deger konumundan frekansa kadar kalin kirmizi cizgi cekilir
        for z in temp:

            if z[0]==dtt[i][1]:

                image = cv2.line(image, (int(450-(count-7)), 360), (int(450-(count-7)),z[1]), (0,0,139), 15)

        count+=adim

    return image


def variance(data):

    n = len(data)
    mean = sum(data) / n
    return sum((x - mean) ** 2 for x in data) / (n - 1)

def stdev(data):

    var = variance(data)
    std_dev = math.sqrt(var)
    return std_dev

def Check(img):

    for i in range(0,999999999999999):

        my_file = Path(img)
        if my_file.is_file():

            time.sleep(5)

            os.system("rm {}".format(img))

            break