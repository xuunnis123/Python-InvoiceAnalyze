# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 21:16:30 2018
統計104/01~109/11統一發票特別獎1000萬與特獎200萬中獎(分開計算)在每個縣市出現次數。
0.禁止先下載整理好的統一發票特別獎與特獎資料
1.要使用thread，分別抓取不同時間網頁
2.要使用matplotlib模組顯示相關資訊
3.能夠指定任意104/01~109/11統計時間區間
/店招、地址、類別、金額/
//多少區間中獎機會高//
1.使用tkinter模組(或其他GUI模組)設計GUI，讓使用者可以輕易操作你的程式
2.程式還提供不同的統計(例如依照發票類別，如食品，停車費等)
@author: Ji-Yang Lin
"""
import os 
import time
import concurrent.futures
from tkinter import Tk, Label,Text, Button, Entry, IntVar, END,W,E,N,S,messagebox,simpledialog,filedialog,Menu,Checkbutton,TOP,BOTTOM,LEFT,RIGHT,PhotoImage

# 分出來的部分
from analyzeItem import AnalyzeItem
import view

# shot1:開始區間
# shot2:結束區間
shot1=""
shot2=""
timechoose=['10401','10403','10405','10407','10409','10411','10501','10503','10505','10507','10509','10511','10601','10603','10605','10607','10609','10611','10701','10703','10705','10707','10709','10711','10801','10803','10805','10807','10809','10811','10901','10903','10905','10907','10909','10911']

analyze_1000 = AnalyzeItem(1000)
analyze_200 = AnalyzeItem(200)
analyzeItem_list =[analyze_1000, analyze_200]

def collect_and_devide(shot,start,end):
    analyze_1000.update(shot)
    analyze_200.update(shot)

    # 計算每個縣市的中獎次數
    if start==end:
        analyze_1000.cal_locate_count()
        analyze_200.cal_locate_count()
        # 畫折線圖
        view.line_chart(analyzeItem_list)        
    return analyze_1000.locate().count(), analyze_200.locate().count()
      
def fun_shot1(add):
    global shot1,shot1_label
    if len(add)==2: #月份
        assert len(shot1)==3, "先選年份"
        shot1+=add
    else:
        shot1=add
    shot1_label.config(text = f"開始區間:{shot1}")

def fun_shot2(add):
    global shot2,shot2_label
    if len(add)==2: #月份
        assert len(shot2)==3, "先選年份"
        shot2+=add
    else:
        shot2=add
    shot2_label.config(text = f"結束區間:{shot2}")

def reset(shot1_label, shot2_label):
    global shot1,shot2,analyze_1000,analyze_200,analyzeItem_list
    shot1=""
    shot1_label.config(text = "開始區間:")
    shot2=""
    shot2_label.config(text = "結束區間:")
    T1.delete(0.0,END)
    T2.delete(0.0,END)
    analyze_1000 = AnalyzeItem(1000)
    analyze_200 = AnalyzeItem(200)
    analyzeItem_list =[analyze_1000, analyze_200]


def sure(shot1,shot2):
    global analyze_1000,analyze_200,analyzeItem_list
    analyze_1000 = AnalyzeItem(1000)
    analyze_200 = AnalyzeItem(200)
    analyzeItem_list =[analyze_1000, analyze_200]
    T1.delete(0.0,END)
    T2.delete(0.0,END)
    if shot1 == '':
        shot1 = timechoose[0]
    if shot2 == '':
        shot2 = timechoose[-1]
    try:
        start = timechoose.index(shot1)
        end = timechoose.index(shot2)
    except ValueError:
        assert False, "請選擇正確的時間"
    
    assert start !=-1 and end !=-1 and start<=end, "選擇區間不正確"

    begin=time.time()     
    while start<=end:   
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:   
            executor.map(collect_and_devide(timechoose[start],start,end))
        start+=1
    over=time.time()
    print("time:",over-begin)
    # 項目清單
    finalitemlist1000=list(sorted(analyze_1000.item().items(),key=lambda item:item[1],reverse=True))  
    for i in finalitemlist1000:
        output1="{}:{}\n".format(i[0],i[1])
        T1.insert(END,output1)
    finalitemlist200 = list(sorted(analyze_200.item().items(),key=lambda item:item[1],reverse=True))
    for i in finalitemlist200:
        output2="{}:{}\n".format(i[0],i[1])
        T2.insert(END,output2)  

### 視窗 ###
if __name__ == '__main__':
    root=Tk()
    root.geometry('1300x500')
    root.title("統一發票統計系統")
    root.configure(background='#FFFFBB')
    shot1_label = Label(root,text="開始區間:",bg="#FFFFBB")
    shot1_label.place(x=40,y=40)
    shot2_label = Label(root,text="結束區間:",bg="#FFFFBB")
    shot2_label.place(x=40,y=60)

    start_label=Label(text="選出開始的區間:",bg="#FFFFBB")
    start_label.place(x=40, y= 80)   
    # 開始區間按鈕
    button104=Button(text="104",command=lambda:fun_shot1("104"),bg='#FF0088')
    button104.place(x=40, y= 100)
    button105=Button(text="105",command=lambda:fun_shot1("105"),bg='#FF3333')
    button105.place(x=70, y= 100)
    button106=Button(text="106",command=lambda:fun_shot1("106"),bg='#FF0088')
    button106.place(x=100, y= 100)
    button107=Button(text="107",command=lambda:fun_shot1("107"),bg='#FF3333')
    button107.place(x=130, y= 100)
    button108=Button(text="108",command=lambda:fun_shot1("108"),bg='#FF0088')
    button108.place(x=160, y= 100)
    button109=Button(text="109",command=lambda:fun_shot1("109"),bg='#FF3333')
    button109.place(x=190, y= 100)
    
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

    
    end_label=Label(text="選出結束的區間:",bg="#FFFFBB")
    end_label.place(x=260, y= 80)
    # 結束區間按鈕
    button104=Button(text="104",command=lambda:fun_shot2("104"),bg='#CCCCFF')
    button104.place(x=260, y= 100)
    button105=Button(text="105",command=lambda:fun_shot2("105"),bg='#5555FF')
    button105.place(x=290, y= 100)
    button106=Button(text="106",command=lambda:fun_shot2("106"),bg='#CCCCFF')
    button106.place(x=320, y= 100)
    button107=Button(text="107",command=lambda:fun_shot2("107"),bg='#5555FF')
    button107.place(x=350, y= 100)
    button108=Button(text="108",command=lambda:fun_shot2("108"),bg='#CCCCFF')
    button108.place(x=380, y= 100)
    button109=Button(text="109",command=lambda:fun_shot2("109"),bg='#5555FF')
    button109.place(x=410, y= 100)
    
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
    button_reset=Button(text="重置",command=lambda:reset(shot1_label, shot2_label),width=7,bg="#888800").place(x=320, y= 40)
    button_exit=Button(text="離開",command=root.quit,width=7,bg="#886600").place(x=380, y= 40)

    # 項目清單
    T1=Text(root,height=15,width=20,bg="#FFFFBB")
    T1.place(x=40,y=250)
    Label(root,text="1000萬獎項交易項目：",bg="#FFFFBB").place(x=40,y=220)

    T2=Text(root,height=15,width=20,bg="#FFFFBB")
    T2.place(x=260,y=250)
    Label(root,text="200萬獎項交易項目：",bg="#FFFFBB").place(x=260,y=220)

    root.mainloop()
    root.destroy()