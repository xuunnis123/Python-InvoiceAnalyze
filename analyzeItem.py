from bs4 import BeautifulSoup
import requests

locations = [
    "基隆市", "臺北市", "新北市",
    "桃園市", "新竹市", "新竹縣", 
    "苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣",
    "嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣",
    "宜蘭縣", "花蓮縣", "臺東縣",
    "澎湖縣", "金門縣","連江縣"
]

item_list = []

class Locations:

    def __init__(self, location_list=locations):
        self.__count = {}
        assert location_list!=None, "地區不能是空的"
        assert isinstance(location_list[0], str), "地區清單需要為字串"

        for _ in location_list:
            self.__count[_] = 0

    def count(self):
        return self.__count

    def addCount(self, location):
        location_list = self.getPlaceList()
        assert location in location_list, "沒有此地區"
        self.__count[location] += 1

    def getCount(self, location):
        return self.__count[location]

    def getPlaceList(self):
        return list(self.__count.keys())

class AnalyzeItem:

    def __init__(self, prize=1000):
        self.__prize = prize    # 中獎金額 (e.g. 1000萬 => prize=1000)
        self.__locate = Locations() # 每個地區的中獎次數, type => dict
        self.__alldata = []
        self.__company = []
        self.__address = []
        self.__item = {}  
    
    # get value
    def prize(self):
        return self.__prize

    def alldata(self):
        return self.__alldata
    
    def company(self):
        return self.__company
    
    def address(self):
        return self.__address

    def item(self):
        return self.__item

    def locate(self):
        return self.__locate
    
    # update data
    def update(self, time):
        prize = self.__prize
        # time example: 10705
        url='https://www.etax.nat.gov.tw/etw-main/web/ETW183W3_'+ time +'/'
        html = requests.get(url).content.decode('utf-8')
        sp = BeautifulSoup(html,'html.parser')

        # h_id: headers id
        if int(prize) == 1000:
            table = sp.find('table',{'id':"fbonly"})
            h_id = ''
        elif int(prize) == 200:
            table = sp.find('table',{'id':"fbonly_200"})
            h_id = '2'
        else:
            assert True, "目前只提供200萬、1000萬的獎項分析功能"

        save = table.find_all('tr')
        save_company = table.findAll('td',{'headers':'companyname'+h_id})
        save_address = table.findAll('td',{'headers':'companyAddress'+h_id})
        save_item = table.findAll('td',{'headers':'tranItem'+h_id})

        # 更新到 analyzerItem 
        for row in save_company:
            self.__company.append(row.get_text())

        for row in save_address:
            self.__address.append(row.get_text())
        
        for row in save_item:
            # 去除項目中的單位以及價錢(會在逗號後面)
            # e.g. 菸品2包，計250元
            item = row.get_text()
            item = item[ 0:item.find("，") ]
            for i in range(len(item)):
                if item[i] >= '0' and item[i] <='9':
                    item = item[0:i]
                    break
            if item not in self.__item.keys():
                self.__item[item]=1
            else:
                self.__item[item]+=1

        for idx,row in enumerate(save[1:]):
            self.__alldata.append(row.get_text())

    def cal_locate_count(self):
        locate = self.__locate
        for addr in self.__address:
            for i in locate.getPlaceList():
                # 改制
                if addr.find("桃園縣")!=-1:
                    locate.addCount('桃園市')
                    break
                if addr.find("臺北縣")!=-1:
                    locate.addCount('新北市')   
                    break
                if addr.find("臺中縣")!=-1:
                    locate.addCount('臺中市')
                    break
                if addr.find("臺南縣")!=-1:
                    locate.addCount('臺南市')
                    break
                if addr.find("高雄縣")!=-1:
                    locate.addCount('高雄市')  
                    break
                # 正常
                if addr.find(i) !=-1:
                    locate.addCount(str(i))  
