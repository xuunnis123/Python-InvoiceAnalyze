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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import os 
import time
import concurrent.futures
from tkinter import Tk, Label,Text, Button, Entry, IntVar, END,W,E,N,S,messagebox,simpledialog,filedialog,Menu,Checkbutton,TOP,BOTTOM,LEFT,RIGHT,PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 分出來的部分
from wintimes import Wintimes
from analyzeItem import AnalyzeItem

locate1000_count_data=[]
locate200_count_data=[]
shot1=""
shot2=""
devide_all1000={}
devide_all200={}

analyze_1000 = AnalyzeItem(1000)
analyze_200 = AnalyzeItem(200)
locate1000 = analyze_1000.locate()
locate200 = analyze_200.locate()

start=0
end=35
timechoose=['10201','10203','10205','10207','10209','10211','10301','10303','10305','10307','10309','10311','10401','10403','10405','10407','10409','10411','10501','10503','10505','10507','10509','10511','10601','10603','10605','10607','10609','10611','10701','10703','10705','10707','10709']

def reset():
    global shot1,shot2,locate1000,locate200,locate1000_count_data,locate200_count_data,devide_all1000,devide_all200,start,end
    shot1=""
    shot2=""
    locate1000_count_data=[]
    locate200_count_data=[]
    devide_all1000={}
    devide_all200={}
    start=0
    end=35
    T1.delete(0.0,END)
    T2.delete(0.0,END)

def collect_and_devide(shot,start,end):
    
    analyze_1000.update(shot)
    analyze_200.update(shot)
  
    # 視窗下面的項目table-------------------------------------
    Label(root,text="1000萬獎項交易項目：",bg="#FFFFBB").place(x=40,y=220)
    finalitemlist1000=list(sorted(analyze_1000.item().items(),key=lambda item:item[1],reverse=True))  
    output1=""
    for i in finalitemlist1000:
        output1="{}:{}\n".format(i[0],i[1])
        T1.insert(END,output1)
    
    Label(root,text="200萬獎項交易項目：",bg="#FFFFBB").place(x=260,y=220)
    finalitemlist200 = list(sorted(analyze_200.item().items(),key=lambda item:item[1],reverse=True))
    output2=""
    for i in finalitemlist200:
        output2="{}:{}\n".format(i[0],i[1])
        T2.insert(END,output2)  
    #--------------------------------------------------------
    # 計算每個縣市的中獎次數
    if start==end:
        analyze_1000.cal_locate_count()
        analyze_200.cal_locate_count()
        # 畫折線圖
        show()           
    return locate1000.count(), locate200.count()
    
### 畫折線圖 ###
def show():

    font = FontProperties(fname='./STHeiti Medium.ttc',size=10)
    #整理ndarray
    for _ in locate1000.count():
    #print(locate1000['臺北市'])
        locate1000_count_data.append(locate1000.getCount(_))
    for _ in locate200.count():
        locate200_count_data.append(locate200.getCount(_))    
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

    label='1000萬特別獎中獎曲線'
    label2='200萬特獎中獎曲線'
    #aa=Tk()
    f=plt.figure(figsize=(12,5))
    plt.rcParams['axes.facecolor'] = '#FFFFBB'
    plt.plot(np.arange(data1000.shape[0]),data1000,label=label)
    plt.plot(np.arange(data200.shape[0]),data200,label=label2)
    print(data1000)
    print(data200)
    plt.xticks(np.arange(data1000.shape[0]),['基隆市','臺北市','新北市','桃園市','新竹市','新竹縣','苗栗縣','臺中市','彰化縣','雲林縣','南投縣','嘉義縣','嘉義市','臺南市','高雄市','屏東縣','宜蘭縣','花蓮縣','臺東縣','澎湖縣','金門縣','連江縣'],fontproperties=font)    #,fontproperties=font
    plt.yticks(np.arange(maxdata+1),timenumber,fontproperties=font)    #fontproperties=font
    #['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']
    plt.legend(loc='upper right',prop=font) #prop=font
    plt.title('各縣市中獎次數',fontproperties=font) #fontproperties=font
    plt.xlabel('縣市',fontproperties=font)#fontproperties=font
    plt.ylabel('次數',fontproperties=font)#fontproperties=font
    plt.savefig("final.png")
    plt.show()
    
    #im=PhotoImage(file="final.png")
    
    canvas =FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().place(x=440,y=40)
    # = Label(root, imag=im)
    #img_label.pack(row=11)
###

### 視窗 ###
if __name__ == '__main__':
    root=Tk()
    root.geometry('1300x500')
    root.title("季陽統一發票統計系統")
    root.configure(background='#FFFFBB')
    
    def fun_shot1(add):
        global shot1
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
    # filemenu.add_command(label="區間模式")
    filemenu.add_command(label="Exit",command=root.quit)
    
    root.config(menu=menu)
    
    root.mainloop()
    root.destroy()

###