import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from analyzeItem import AnalyzeItem

### 折線圖 ###
def line_chart(analyzeItem_list):

    font = FontProperties(fname='./STHeiti Medium.ttc',size=9)

    all_locate_list = [] # e.g. [{"臺北市":5, ...}, {"臺北市":2, ...}]
    all_locate_count_data = []  # e.g. [[5, ...], [2, ...]]
    for _ in analyzeItem_list:
        assert isinstance( _, AnalyzeItem), "需要AnalyzeItem物件才能畫折線圖"
        all_locate_list.append( _.locate())

    # 只留下每個縣市的中獎次數
    for locate in all_locate_list:
        locate_count_data = []
        for _ in locate.count():
            locate_count_data.append(locate.getCount(_))
        all_locate_count_data.append(locate_count_data)

    # 整理 ndarray
    all_data =[] # 每個 AnaylzeItem的各縣市中獎次數(array)
    all_max_data = []   # 每個AnaylzeItem的最高中獎次數(不分縣市)
    for locate_count_data in all_locate_count_data:
        data = np.array(locate_count_data)
        all_data.append(data)
        maxdata = max(data)
        all_max_data.append(maxdata)

    # 從所有AnaylzeItem找出最高的中獎次數，當y軸的最大值
    maxdata=0
    for _ in all_max_data:
        if maxdata < _ :
            maxdata = _
    # y軸
    timenumber=[]
    for i in range(maxdata+1):  
        timenumber.append(str(i))

    all_label =[]
    for _ in analyzeItem_list:  
        label= str( _.prize()) + '萬特別獎中獎曲線'
        all_label.append(label)

    f = plt.figure(figsize=(8,3.5))
    plt.rcParams['axes.facecolor'] = '#FFFFBB'
    plt.tick_params(axis='x', which='major', labelsize=1)
    plt.tight_layout()

    for i in range(len(all_data)):
        plt.plot(np.arange(all_data[i].shape[0]), all_data[i], label=all_label[i])
    plt.xticks(np.arange(all_data[0].shape[0]),['基隆市','臺北市','新北市','桃園市','新竹市','新竹縣','苗栗縣','臺中市','彰化縣','雲林縣','南投縣','嘉義縣','嘉義市','臺南市','高雄市','屏東縣','宜蘭縣','花蓮縣','臺東縣','澎湖縣','金門縣','連江縣'],fontproperties=font)    #,fontproperties=font
    plt.yticks(np.arange(maxdata+1),timenumber,fontproperties=font)    #fontproperties=font
    plt.legend(loc='upper right',prop=font) #prop=font
    plt.title('各縣市中獎次數',fontproperties=font) #fontproperties=font
    plt.xlabel('縣市',fontproperties=font)  #fontproperties=font
    plt.ylabel('次數',fontproperties=font)  #fontproperties=font
    plt.savefig("final.png")
    # plt.show()
    
    #im=PhotoImage(file="final.png")
    
    canvas = FigureCanvasTkAgg(f)
    # canvas.show()
    canvas.get_tk_widget().place(x=470,y=100)
    # = Label(root, imag=im)
    #img_label.pack(row=11)