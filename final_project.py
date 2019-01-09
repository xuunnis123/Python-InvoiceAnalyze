# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 21:16:30 2018
統計102/01~107/09統一發票特別獎1000萬與特獎200萬中獎(分開計算)在每個縣市出現次數。V
0.禁止先下載整理好的統一發票特別獎與特獎資料V
1.要使用thread，分別抓取不同時間網頁V
2.要使用matplotlib模組顯示相關資訊V
3.能夠指定任意102/01~107/09統計時間區間V
/店招、地址、類別、金額/
//多少區間中獎機會高//
1.使用tkinter模組(或其他GUI模組)設計GUI，讓使用者可以輕易操作你的程式V
2.程式還提供不同的統計(例如依照發票類別，如食品，停車費等)
@author: Ji-Yang Lin
"""
from bs4 import BeautifulSoup
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os 
import time
import concurrent.futures
from tkinter import Tk, Label,Text, Button, Entry, IntVar, END,W,E,N,S,messagebox,simpledialog,filedialog,Menu,Checkbutton,TOP,BOTTOM,LEFT,RIGHT,PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

locate1000={'基隆市':0,'臺北市':0,'新北市':0,'桃園市':0,'新竹市':0,'新竹縣':0,'苗栗縣':0,'臺中市':0,'彰化縣':0,'雲林縣':0,'南投縣':0,'嘉義縣':0,'嘉義市':0,'臺南市':0,'高雄市':0,'屏東縣':0,'宜蘭縣':0,'花蓮縣':0,'臺東縣':0,'澎湖縣':0,'金門縣':0,'連江縣':0}
locate200={'基隆市':0,'臺北市':0,'新北市':0,'桃園市':0,'新竹市':0,'新竹縣':0,'苗栗縣':0,'臺中市':0,'彰化縣':0,'雲林縣':0,'南投縣':0,'嘉義縣':0,'嘉義市':0,'臺南市':0,'高雄市':0,'屏東縣':0,'宜蘭縣':0,'花蓮縣':0,'臺東縣':0,'澎湖縣':0,'金門縣':0,'連江縣':0}
alldata1000=[]
alldata200=[]
short_1000company=[]
short_1000address=[]
short_1000item=[]
short_200company=[]
short_200address=[]
short_200item=[]
locate1000_count_data=[]
locate200_count_data=[]
shot1=""
shot2=""
devide_all1000={}
devide_all200={}
item_200set={}
item_1000set={}
doneitemlist1000=[]
doneitemlist200=[]

start=0
end=35
count=0
timechoose=['10201','10203','10205','10207','10209','10211','10301','10303','10305','10307','10309','10311','10401','10403','10405','10407','10409','10411','10501','10503','10505','10507','10509','10511','10601','10603','10605','10607','10609','10611','10701','10703','10705','10707','10709']
def collect_and_devide(shot,start,end):
    global alldata1000,alldata200,short_1000company,short_1000address,short_1000item,short_200company,short_200address,short_200item,count
    
    savee=shot
    #print(savee)
    urll='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+savee+'/'
    #print(urll)
    url=urll
    #url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_10709/'
    html = requests.get(url).content.decode('utf-8')
    sp = BeautifulSoup(html,'html.parser')
    table1000=sp.find('table',{'id':"fbonly"})
    table200=sp.find('table',{'id':"fbonly_200"})
    save1000=table1000.find_all('tr')

    
    save1000company=table1000.findAll('td',{'headers':'companyname'})
    save1000address=table1000.findAll('td',{'headers':'companyAddress'})
    save1000item=table1000.findAll('td',{'headers':'tranItem'})

    save200=table200.find_all('tr')
    save200company=table200.findAll('td',{'headers':'companyname2'})
    save200address=table200.findAll('td',{'headers':'companyAddress2'})
    save200item=table200.findAll('td',{'headers':'tranItem2'})
    #print("1000萬")
#devide data
#1000
    for row in save1000company:
    
        short_1000company.append(row.get_text())

    for row in save1000address:
        short_1000address.append(row.get_text())    
    
    for row in save1000item:
        short_1000item.append(row.get_text())    
#200    
    for row in save200company:
    
        short_200company.append(row.get_text())

    for row in save200address:
        short_200address.append(row.get_text())    
    
    for row in save200item:
        short_200item.append(row.get_text()) 

    #all data
    for idx,row in enumerate(save1000[1:]):
        alldata1000.append(row.get_text())
    
    #########
    #for _ in alldata1000:    
    #    print(_)
    
    #print(alldata[_])    
    #print("200萬")    
    for idx,row in enumerate(save200[1:]):
        alldata200.append(row.get_text())
    ####
    check=['0','1','2','3','4','5','6','7','8','9']
    ###項目整理
    doneitemlist1000.clear()
    doneitemlist200.clear()
    def delnumber(length,i):
        while(length):
          for _ in check:
                if i.find(_)!=-1:
                    i=i[0:i.find(_)]
          length-=1
        return i  
    for i in short_1000item:
        #字串整理
        if i.find("，")!=-1:
            i=i[0:i.find("，")]
            i=delnumber(len(i),i)
            print(i)   
           
        else:
            
            i=delnumber(len(i),i)
            print(i) 
            list(i)        
            
        doneitemlist1000.append(i)        
    #print("1000:",doneitemlist1000)        
    #doneitemlist1000.sort()
    #print("1000:",doneitemlist1000)        
    
    for i in short_200item:
        #字串整理
        if i.find("，")!=-1:
            i=i[0:i.find("，")]
            i=delnumber(len(i),i)
            print(i)   
           
        else:
            
            i=delnumber(len(i),i)
            print(i) 
            list(i)        
            
        doneitemlist200.append(i)  
                
    
    #print("200:",doneitemlist200)  
    
    ####建itiem key,values
    if start==end:
        for i in doneitemlist1000:
            #print(i)
            if i not in item_1000set.keys():
                item_1000set[i]=1
                print(i,item_1000set[i])
            else:
                item_1000set[i]+=1
                print(i,item_1000set[i])
        print("set:",item_1000set)   
        for i in doneitemlist200:
            #print(i)
            if i not in item_200set.keys():
                item_200set[i]=1
            else:
                item_200set[i]+=1
    #print("set:",item_200set)  
    ####sort
    #item_1000set=sorted(item_1000set.items(), key = lambda item:item[1],reverse=True)
    #item_200set=sorted(item_200set.items(), key = lambda item:item[1],reverse=True)
    
    Label(root,text="1000萬獎項交易項目：",bg="#FFFFBB").place(x=40,y=220)
          #T=Text(root,text=item_1000set,wraplength=160,justify='left',bg="#FFFFBB").place(x=40,y=250)
    finalitemlist1000=[]
    
    finalitemlist1000=(sorted(item_1000set.items(),key=lambda item:item[1],reverse=True))
       
    output1=""
    for i in finalitemlist1000:
        output1="{}:{}\n".format(i[0],i[1])
        T1.insert(END,output1)
    
    Label(root,text="200萬獎項交易項目：",bg="#FFFFBB").place(x=260,y=220)
    finalitemlist200=[]
    finalitemlist200=(sorted(item_200set.items(),key=lambda item:item[1],reverse=True))
    output2=""
    for i in finalitemlist200:
        output2="{}:{}\n".format(i[0],i[1])
        T2.insert(END,output2)
    count+=1
    #print("count:",count)
    if start==end:
        for thisrow in short_1000address:
            for i in locate1000:
                #改制
                if str(thisrow).find("桃園縣")!=-1:
                    locate1000['桃園市']+=1
                    #print("次數:",'桃園市',locate1000['桃園市'])
                    break
                if str(thisrow).find("臺北縣")!=-1:
                    locate1000['新北市']+=1    
                    break
                if str(thisrow).find("臺中縣")!=-1:
                    locate1000['臺中市']+=1 
                    break
                if str(thisrow).find("臺南縣")!=-1:
                    locate1000['臺南市']+=1 
                    break
                if str(thisrow).find("高雄縣")!=-1:
                    locate1000['高雄市']+=1   
                    break
                    
                #正常
                if str(thisrow).find(i) !=-1:
                    
                    locate1000[i]+=1
                    #print("1000萬次數:",i,locate1000[i])
        #print("1000萬地點：")
        #print(locate1000)
        
        for thisrow in short_200address:
            for i in locate200:
                if str(thisrow).find("桃園縣")!=-1:
                    locate200['桃園市']+=1
                    break
                if str(thisrow).find("臺北縣")!=-1:
                    locate200['新北市']+=1    
                    break
                if str(thisrow).find("臺中縣")!=-1:
                    locate200['臺中市']+=1 
                    break
                if str(thisrow).find("臺南縣")!=-1:
                    locate200['臺南市']+=1 
                    break
                if str(thisrow).find("高雄縣")!=-1:
                    locate200['高雄市']+=1   
                    break
                
                if str(thisrow).find(i) !=-1:
                    
                    locate200[i]+=1
                    #print("200萬次數:",i,locate200[i])
        ###印各縣市次數  
        """          
        print("200萬：")
        for i in locate200:
            print(i,locate200[i])
            
        print("1000萬：")
        for i in locate1000:
            print(i,locate1000[i])    
        """    
        show()           
    #print("200萬地點：")
    #print(locate200)
#collect_and_devide()
    
    return locate1000,locate200
    
    


###畫折線圖
def show():
    global locate1000,locate200
    font = FontProperties(fname=os.environ['WINDIR']+'\\Fonts\\simsun.ttc',size=10)
#整理ndarray
    for _ in locate1000:
    #print(locate1000['臺北市'])
        locate1000_count_data.append(locate1000[_])
    for _ in locate200:
        locate200_count_data.append(locate200[_])    
    #print("次數1000:",locate1000_count_data)   
#print("次數200:",locate200_count_data)
    data1000=np.array(locate1000_count_data)  
    maxdata1=max(data1000)
#print(maxdata1)
##[0 3 1 2 0 2 0 1 3 0 0 0 0 1 3 1 0 0 0 0 0 0]
    data200=np.array(locate200_count_data)
    maxdata2=max(data200) 
#print(maxdata2)
    maxdata=0
    if maxdata1>=maxdata2:
        maxdata=maxdata1
    else:
        maxdata=maxdata2 
    timenumber=[]
    for i in range(maxdata+1):
        
        timenumber.append(str(i))
        
    #print(timenumber)    
#[0 0 2 5 0 0 0 1 0 0 0 0 0 2 2 0 0 0 0 0 0 0]
    '''
    for i in locate1000:
        print(i)
        #print(data1000[i])
        plt.plot(data1000[len(i)],label=locate1000[i])
    
    #np.arange(data1000.shape[0]),
    '''
    label='1000萬特別獎中獎曲線'
    label2='200萬特獎中獎曲線'
    #aa=Tk()
    f=plt.figure(figsize=(12,5))
    plt.rcParams['axes.facecolor'] = '#FFFFBB'
    plt.plot(np.arange(data1000.shape[0]),data1000,label=label)
    plt.plot(np.arange(data200.shape[0]),data200,label=label2)
    plt.xticks(np.arange(data1000.shape[0]),['基隆市','臺北市','新北市','桃園市','新竹市','新竹縣','苗栗縣','臺中市','彰化縣','雲林縣','南投縣','嘉義縣','嘉義市','臺南市','高雄市','屏東縣','宜蘭縣','花蓮縣','臺東縣','澎湖縣','金門縣','連江縣'],fontproperties=font)    
    plt.yticks(np.arange(maxdata+1),timenumber,fontproperties=font)    
    #['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
    plt.legend(loc='upper right',prop=font)
    plt.title('各縣市中獎次數',fontproperties=font)
    plt.xlabel('縣市',fontproperties=font)
    plt.ylabel('次數',fontproperties=font)
    plt.savefig("final.png")
    plt.show()
    
    
    #im=PhotoImage(file="final.png")
    
    canvas =FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().place(x=440,y=40)
    # = Label(root, imag=im)
    #img_label.pack(row=11)
####

###視窗###
if __name__ == '__main__':
    root=Tk()
    root.geometry('1300x500')
    root.title("季陽統一發票統計系統")
    root.configure(background='#FFFFBB')
    
    def fun_shot1(add):
        global shot1,startlabel
        shot1=shot1+add
        Label(root,text="開始區間:{}".format(shot1),bg="#FFFFBB").place(x=40,y=40)
    def fun_shot2(add):
        global shot2
        shot2=shot2+add
        Label(root,text="結束區間:{}".format(shot2),bg="#FFFFBB").place(x=40,y=60)
    def sure(shot1,shot2):
        global devide_all1000,devide_all200
        global end,start
        for j in range(35):
            if timechoose[j]==shot1:
                #print(j,timechoose[j])
                start=j
        for i in range(35):
            if timechoose[i]==shot2:
                #print(i,timechoose[i])
                end=i
      
        begin=time.time()     
        while start<=end:   
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                 
                #devide_all1000,devide_all200=
                executor.map(collect_and_devide(timechoose[start],start,end))
                devide_all1000.update(devide_all1000)
                devide_all200.update(devide_all200)
  

            """
            devide_all1000,devide_all200=collect_and_devide(timechoose[start],start,end)
            devide_all200.update(devide_all200)
            devide_all1000.update(devide_all1000)
            """
            start+=1
        over=time.time()
        print("time:",over-begin)
    def reset():
        global shot1,shot2,locate1000,locate200,alldata1000,alldata200,short_1000company,short_1000address,short_1000item,short_200company,short_200address,short_200item,locate1000_count_data,locate200_count_data,devide_all200,devide_all1000,start,end,item_200set,item_1000set,doneitemlist1000,doneitemlist200
        shot1=""
        shot2=""
        locate1000={'基隆市':0,'臺北市':0,'新北市':0,'桃園市':0,'新竹市':0,'新竹縣':0,'苗栗縣':0,'臺中市':0,'彰化縣':0,'雲林縣':0,'南投縣':0,'嘉義縣':0,'嘉義市':0,'臺南市':0,'高雄市':0,'屏東縣':0,'宜蘭縣':0,'花蓮縣':0,'臺東縣':0,'澎湖縣':0,'金門縣':0,'連江縣':0}
        locate200={'基隆市':0,'臺北市':0,'新北市':0,'桃園市':0,'新竹市':0,'新竹縣':0,'苗栗縣':0,'臺中市':0,'彰化縣':0,'雲林縣':0,'南投縣':0,'嘉義縣':0,'嘉義市':0,'臺南市':0,'高雄市':0,'屏東縣':0,'宜蘭縣':0,'花蓮縣':0,'臺東縣':0,'澎湖縣':0,'金門縣':0,'連江縣':0}
        alldata1000=[]
        alldata200=[]
        short_1000company=[]
        short_1000address=[]
        short_1000item=[]
        short_200company=[]
        short_200address=[]
        short_200item=[]
        locate1000_count_data=[]
        locate200_count_data=[]
        devide_all1000={}
        devide_all200={}
        start=0
        end=35
        item_200set={}
        item_1000set={}
        doneitemlist1000=[]
        doneitemlist200=[]
        T1.delete(0.0,END)
        T2.delete(0.0,END)
        '''
        Label(root,text="1000萬獎項交易項目：",bg="#FFFFBB").place(x=40,y=220)
        Label(root,text="-----------",wraplength=160,justify='left',bg="#FFFFBB").place(x=40,y=250)
        Label(root,text="200萬獎項交易項目：",bg="#FFFFBB").place(x=260,y=220)
        Label(root,text="-----------",wraplength=160,justify='left',bg="#FFFFBB").place(x=260,y=250)
        '''
        
    first=Label(text="選出開始的區間:",bg="#FFFFBB")
    first.place(x=40, y= 80)    
        #Label(root,text="開始區間:{}".format(shot1)).pack(row=7,columnspan=8)
        #Label(root,text="結束區間:{}".format(shot2)).pack(row=8,columnspan=8)
    button102=Button(text="102",command=lambda:fun_shot1("102"),bg='#FF0088')
    button102.place(x=40, y= 100)
    button103=Button(text="103",command=lambda:fun_shot1("103"),bg='#FF3333')
    button103.place(x=70, y= 100)
    button104=Button(text="104",command=lambda:fun_shot1("104"),bg='#FF0088')
    button104.place(x=100, y= 100)
    button105=Button(text="105",command=lambda:fun_shot1("105"),bg='#FF3333')
    button105.place(x=130, y= 100)
    button106=Button(text="106",command=lambda:fun_shot1("106"),bg='#FF0088')
    button106.place(x=160, y= 100)
    button107=Button(text="107",command=lambda:fun_shot1("107"),bg='#FF3333')
    button107.place(x=190, y= 100)
    
    button01=Button(text="01",command=lambda:fun_shot1("01"),width=7,bg='#FFA488')
    button01.place(x=40, y= 140)
    button03=Button(text="03",command=lambda:fun_shot1("03"),width=7,bg='#FFA488')
    button03.place(x=100, y= 140)
    button05=Button(text="05",command=lambda:fun_shot1("05"),width=7,bg='#FFA488')
    button05.place(x=160, y= 140)
    button07=Button(text="07",command=lambda:fun_shot1("07"),width=7,bg='#FFA488')
    button07.place(x=40, y= 180)
    button09=Button(text="09",command=lambda:fun_shot1("09"),width=7,bg='#FFA488')
    button09.place(x=100, y= 180)
    button11=Button(text="11",command=lambda:fun_shot1("11"),width=7,bg='#FFA488')
    button11.place(x=160, y= 180)
    
    second=Label(text="選出結束的區間:",bg="#FFFFBB")
    second.place(x=260, y= 80)
    
    button102=Button(text="102",command=lambda:fun_shot2("102"),bg='#CCCCFF')
    button102.place(x=260, y= 100)
    button103=Button(text="103",command=lambda:fun_shot2("103"),bg='#5555FF')
    button103.place(x=290, y= 100)
    button104=Button(text="104",command=lambda:fun_shot2("104"),bg='#CCCCFF')
    button104.place(x=320, y= 100)
    button105=Button(text="105",command=lambda:fun_shot2("105"),bg='#5555FF')
    button105.place(x=350, y= 100)
    button106=Button(text="106",command=lambda:fun_shot2("106"),bg='#CCCCFF')
    button106.place(x=380, y= 100)
    button107=Button(text="107",command=lambda:fun_shot2("107"),bg='#5555FF')
    button107.place(x=410, y= 100)
    
    button01=Button(text="01",command=lambda:fun_shot2("01"),width=7,bg='#CCBBFF')
    button01.place(x=260, y= 140)
    button03=Button(text="03",command=lambda:fun_shot2("03"),width=7,bg='#CCBBFF')
    button03.place(x=320, y= 140)
    button05=Button(text="05",command=lambda:fun_shot2("05"),width=7,bg='#CCBBFF')
    button05.place(x=380, y= 140)
    button07=Button(text="07",command=lambda:fun_shot2("07"),width=7,bg='#CCBBFF')
    button07.place(x=260, y= 180)
    button09=Button(text="09",command=lambda:fun_shot2("09"),width=7,bg='#CCBBFF')
    button09.place(x=320, y= 180)
    button11=Button(text="11",command=lambda:fun_shot2("11"),width=7,bg='#CCBBFF')
    button11.place(x=380, y= 180)
    
    button_sure=Button(text="確認",command=lambda:sure(shot1,shot2),width=7,bg="#AAAAAA").place(x=260, y= 40)
    button_reset=Button(text="重置",command=lambda:reset(),width=7,bg="#888800").place(x=320, y= 40)
    button_reset=Button(text="離開",command=root.quit,width=7,bg="#886600").place(x=380, y= 40)
    T1=Text(root,height=15,width=20,bg="#FFFFBB")
    T1.place(x=40,y=250)
    T2=Text(root,height=15,width=20,bg="#FFFFBB")
    T2.place(x=260,y=250)
    menu=Menu(root)    
    filemenu=Menu(menu)
    menu.add_cascade(label="操作模式",menu=filemenu)
    filemenu.add_command(label="區間模式")
    filemenu.add_command(label="Exit",command=root.quit)
    
    root.config(menu=menu)
    
    root.mainloop()
    root.destroy()

###